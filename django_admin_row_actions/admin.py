from django import VERSION
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from six import string_types

from .components import Dropdown
from .views import ModelToolsView


def patterns(prefix, *args):
    if VERSION < (1, 9):
        from django.conf.urls import patterns as django_patterns
        return django_patterns(prefix, *args)
    elif prefix != '':
        raise Exception("You need to update your URLConf to be a list of URL "
                        "objects")
    else:
        return list(args)


class AdminRowActionsMixin(object):
    
    """ModelAdmin mixin to add row actions just like adding admin actions"""

    rowactions = []
    _named_row_actions = {}

    @property
    def media(self):
        media = super(AdminRowActionsMixin, self).media
        media.add_js(['js/jquery.dropdown.min.js'])
        media.add_css({'all': ['css/jquery.dropdown.min.css']})
        return media
        
    def get_list_display(self, request):
        list_display = super(AdminRowActionsMixin, self).get_list_display(request)
        if '_row_actions' not in list_display:
            list_display += ('_row_actions',)
        return list_display
    
    def get_actions_list(self, obj, includePk=True):
        
        def to_dict(tool_name):
            return dict(
                name=tool_name,
                label=getattr(tool, 'label', tool_name).replace('_', ' ').title(),
            )
        
        items = []
        
        row_actions = self.get_row_actions(obj)
        url_prefix = '{}/'.format(obj.pk if includePk else '')
        
        for tool in row_actions:
            if isinstance(tool, string_types):  # Just a str naming a callable
                tool_dict = to_dict(tool)
                items.append({
                    'label': tool_dict['label'],
                    'url': '{}rowactions/{}/'.format(url_prefix, tool),
                })
                
            elif isinstance(tool, dict):  # A parameter dict
                tool['enabled'] = tool.get('enabled', True)
                if 'action' in tool:  # If 'action' is specified then use our generic url in preference to 'url' value
                    if isinstance(tool['action'], tuple):
                        self._named_row_actions[tool['action'][0]] = tool['action'][1]
                        tool['url'] = '{}rowactions/{}/'.format(url_prefix, tool['action'][0])
                    else:
                        tool['url'] = '{}rowactions/{}/'.format(url_prefix, tool['action'])
                items.append(tool)
        
        return items
    
    def _row_actions(self, obj):
        
        items = self.get_actions_list(obj)
        if items:
            html = Dropdown(
                label=_("Actions"),
                items=items,
            ).render()

            return html
        return ''
    _row_actions.short_description = ''
    _row_actions.allow_tags = True
    
    def get_tool_urls(self):
        
        """Gets the url patterns that route each tool to a special view"""
        
        my_urls = patterns(
            '',
            url(r'^(?P<pk>\d+)/rowactions/(?P<tool>\w+)/$',
                self.admin_site.admin_view(ModelToolsView.as_view(model=self.model))
            )
        )
        return my_urls
    
    ###################################
    # EXISTING ADMIN METHODS MODIFIED #
    ###################################
    
    def get_urls(self):
        
        """Prepends `get_urls` with our own patterns"""
        
        urls = super(AdminRowActionsMixin, self).get_urls()
        return self.get_tool_urls() + urls
    
    ##################
    # CUSTOM METHODS #
    ##################
    
    def get_row_actions(self, obj):
        return getattr(self, 'rowactions', False) or []
    
    def get_change_actions(self, request, object_id, form_url):
    
        # If we're also using django_object_actions
        # then try to reuse row actions as object actions
    
        change_actions = super(AdminRowActionsMixin, self).get_change_actions(request, object_id, form_url)
        
        # Make this reuse opt-in
        if getattr(self, 'reuse_row_actions_as_object_actions', False):

            obj = self.model.objects.get(pk=object_id)
            row_actions = self.get_actions_list(obj, False) if obj else []
    
            for row_action in row_actions:
                # Object actions only supports strings as action indentifiers
                if isinstance(row_action, string_types):
                    change_actions.append(row_action)
                elif isinstance(row_action, dict):
                    if isinstance(row_action['action'], string_types):
                        change_actions.append(row_action['action'])
                    elif isinstance(row_action['action'], tuple):
                        change_actions.append(str(row_action['action'][1]))
        return change_actions
