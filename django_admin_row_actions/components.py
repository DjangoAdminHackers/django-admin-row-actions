import weakref
from django.template.loader import render_to_string


class BaseComponent:

    template = None
    instances = []

    def __init__(self, **kwargs):
        self.__class__.instances.append(weakref.proxy(self))
        self.request = kwargs.pop('request')
        self.context = kwargs
        self.context['dom_id'] = self.get_unique_id()

    @classmethod
    def get_unique_id(cls):
        return f"{cls.__name__.lower()}-{len(cls.instances)}"

    def render(self):
        return render_to_string(
            self.template,
            self.context,
            request=self.request
        )

    def __str__(self):
        return self.render()


class Dropdown(BaseComponent):
    template = 'django_admin_row_actions/dropdown.html'
