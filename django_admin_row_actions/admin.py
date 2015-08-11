from django.conf.urls import patterns
from django.contrib import admin

from .components import Dropdown
from .views import ModelToolsView


class AdminRowActionsMixin(admin.ModelAdmin):
    
    """ModelAdmin mixin to add row actions just like adding admin actions"""

    rowactions = []

    class Media:
        js = ('js/jquery.dropdown.min.js',)
        css = {
            'all': ['css/jquery.dropdown.min.css',],
        }
        
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

        r = self.get_row_actions(obj)
        url_prefix = '{}/'.format(obj.pk if includePk else '')
        
        for tool in r:
            if isinstance(tool, basestring):
                tool_dict = to_dict(tool)
                items.append({
                    'label': tool_dict['label'],
                    'url': '{}rowactions/{}/'.format(url_prefix, tool),
                })
                
            elif isinstance(tool, dict):
                tool['enabled'] = tool.get('enabled', True)
                if 'action' in tool:  # If action is set then use our generic url in preference to 'url' value
                    tool['url'] = '{}rowactions/{}/'.format(url_prefix, tool['action'])
                items.append(tool)
        
        return items

    def _row_actions(self, obj):

        items = self.get_actions_list(obj)
        html = Dropdown(
            label="Actions",
            items=items,
        ).render()

        return html
    _row_actions.short_description = ''
    _row_actions.allow_tags = True

    def get_tool_urls(self):
        
        """Gets the url patterns that route each tool to a special view"""
        
        my_urls = patterns(
            '',
            (r'^(?P<pk>\d+)/rowactions/(?P<tool>\w+)/$',
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
        if getattr(self, 'rowactions', False):
            return []
        else:
            return self.rowactions

    # Default to using row actions for object actions
    # Aside from the 'Edit' action of course

    def get_object_actions(self, request, context, **kwargs):
        obj = context.get('original', None)
        row_actions = self.get_actions_list(obj, False) if obj else []
        return [x for x in row_actions if not(isinstance(x, dict) and x['label'] == 'Edit')]
    
    class Meta:
        css = {
            'all': [
                'css/jquery.dropdown.min.css',
            ],
        }


