from functools import wraps
from .components import Dropdown

from django.conf.urls import patterns
from django.contrib import admin
from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin


class AdminRowActionsMixin(admin.ModelAdmin):
    
    """ModelAdmin mixin to add row actions just like adding admin actions"""

    rowactions = []

    def get_list_display(self, request):
        list_display = super(DjangoRowActions, self).get_list_display(request)
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
            btn_type="btn-link",
            btn_size="btn-sm",
            label="Actions",
            btn_dropdown_position="dropdown-menu-right",
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
        
        urls = super(DjangoRowActions, self).get_urls()
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
        js = ('js/jquery.dropdown.js',)
        css = {
            'all': [
                'css/jquery.dropdown.min.css',
            ],
        }


class ModelToolsView(SingleObjectMixin, View):
    
    """A special view that run the tool's callable"""

    def get(self, request, **kwargs):
        
        # SingleOjectMixin's `get_object`. Works because the view
        # is instantiated with `model` and the urlpattern has `pk`.
        
        obj = self.get_object()
        try:
            model_admin = admin.site._registry[obj.__class__]
            ret = getattr(model_admin, kwargs['tool'])(request, obj)
        except KeyError:
            raise Http404
        if isinstance(ret, HttpResponse):
            return ret
        back = request.path.rsplit('/', 3)[0] + '/'
        return HttpResponseRedirect(back)

    # Allow POST
    post = get

    def message_user(self, request, message):
        # Copied from django.contrib.admin.options
        # Included to mimic admin actions
        messages.info(request, message)


class QuerySetIsh(QuerySet):
    
    """Takes an instance and mimics it coming from a QuerySet"""
    
    def __init__(self, instance=None, *args, **kwargs):
        try:
            model = instance._meta.model
        except AttributeError:
            # Django 1.5 does this instead, getting the model may be overkill
            # we may be able to throw away all this logic
            model = instance._meta.concrete_model
        self._doa_instance = instance
        super(QuerySetIsh, self).__init__(model, *args, **kwargs)
        self._result_cache = [instance]

    def _clone(self, *args, **kwargs):
        # don't clone me, bro
        return self

    def get(self, *args, **kwargs):
        # Starting in Django 1.7, `QuerySet.get` started slicing to `MAX_GET_RESULTS`,
        # so to avoid messing with `__getslice__`, override `.get`.
        return self._doa_instance


def takes_instance_or_queryset(func):
    
    """Decorator that makes standard actions compatible"""
    
    @wraps(func)
    def decorated_function(self, request, queryset):
        # Function follows the prototype documented at:
        # https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/#writing-action-functions
        if not isinstance(queryset, QuerySet):
            queryset = QuerySetIsh(queryset)
        return func(self, request, queryset)
    return decorated_function
