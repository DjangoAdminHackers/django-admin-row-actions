Django Admin Row Actions
========================

Inspired (and code borrowed from): https://github.com/crccheck/django-object-actions



1. Until this is submitted to PyPi install using git:

    pip install git+git@github.com:DjangoAdminHackers/django-admin-row-actions.git
    
2. Add to INSTALLED_APPS:

    INSTALLED_APPS = [
      ...
      'django_admin_row_actions',
      ...
    ]
    
3. Add the mixin to your ModelAdmin:

    class ExampleAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    

4. Define a get_row_actions method on your ModelAdmin
    
    def get_row_actions(self, obj):
        row_actions = [
            {'label': 'Edit', 'url': obj.get_edit_url(), 'enabled': obj.status is not 'cancelled'},
            {'label': 'Download PDF', 'url': obj.get_pdf_url(), },
            {'label': 'Cancel', 'action': 'mark_cancelled'},
        ]
        row_actions += super(ExampleAdmin, self).get_row_actions(obj)
        return row_actions
        
    The first two menu items are simple links to a url you provide. The 3rd one defines 'action' instead of 'url'.
    
    This should be the name of a callable on your ModelAdmin or Model class
    (similar to https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display )
    
