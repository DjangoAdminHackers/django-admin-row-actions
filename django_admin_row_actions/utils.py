from functools import wraps
from django.db.models.query import QuerySet


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
