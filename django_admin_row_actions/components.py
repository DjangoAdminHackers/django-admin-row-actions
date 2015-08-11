import weakref
from django.template.loader import render_to_string


class BaseComponent(object):
    
    template = None
    instances = []

    def __init__(self, **kwargs):
        
        # Add ourselves to the class's list of instances
        # so we can generate a unique id number for the html
        
        self.__class__.instances.append(weakref.proxy(self))
        self.context = kwargs
        self.context['dom_id'] = self.get_unique_id()

    @classmethod
    def get_unique_id(cls):
        return "{}-{}".format(cls.__name__.lower(), len(cls.instances))

    def render(self):
        return render_to_string(
            self.template,
            self.context,
        )

    def __unicode__(self):
        return self.render()


class Dropdown(BaseComponent):

    template = 'django_admin_row_actions/dropdown.html'

    def __init__(self, **kwargs):
        super(Dropdown, self).__init__(**kwargs)
