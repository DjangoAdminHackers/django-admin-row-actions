from django.contrib import admin
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin


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
