from django.contrib import admin
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin


class ModelToolsView(SingleObjectMixin, View):
    
    """A special view that run the tool's callable"""

    def get(self, request, **kwargs):
        
        # SingleObjectMixin's `get_object`. Works because the view
        # is instantiated with `model` and the urlpattern has `pk`.
        
        obj = self.get_object()
        model_admin = admin.site._registry[obj.__class__]
        
        # Look up the action in the following order:
        # 1. in the named_row_actions dict (for lambdas etc)
        # 2. as a method on the model admin
        # 3. as a method on the model
        if kwargs['tool'] in model_admin._named_row_actions:
            action_method = model_admin._named_row_actions[kwargs['tool']]
            ret = action_method(request=request, obj=obj)
        elif getattr(model_admin, kwargs['tool'], False):
            action_method = getattr(model_admin, kwargs['tool'])
            ret = action_method(request=request, obj=obj)  # TODO should the signature actually be (obj, request) for consistancy?
        elif getattr(obj, kwargs['tool'], False):
            action_method = getattr(obj, kwargs['tool'])
            ret = action_method()
        else:
            raise Http404
        
        # If the method returns a response use that,
        # otherwise redirect back to the url we were called from
        if isinstance(ret, HttpResponse):
            response = ret
        else:
            back = request.META['HTTP_REFERER']
            response = HttpResponseRedirect(back)
            
        return response

    # Also allow POST
    post = get

    def message_user(self, request, message):
        # Copied from django.contrib.admin.options
        # Included to mimic admin actions
        messages.info(request, message)
