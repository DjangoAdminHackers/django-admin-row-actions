Django Admin Row Actions
========================

Inspired (and code based on): https://github.com/crccheck/django-object-actions
jquery-dropdown credits go to Cory LaViska: http://labs.abeautifulsite.net/jquery-dropdown/


1. Until this is submitted to PyPi install using git:

```
pip install git+https://github.com/DjangoAdminHackers/django-admin-row-actions.git
```
    
2. Add to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'django_admin_row_actions',
    ...
]
```
    
3. Add the mixin to your ModelAdmin:

```python
from django_admin_row_actions import AdminRowActionsMixin
...

class ExampleAdmin(AdminRowActionsMixin, admin.ModelAdmin):
...

```
    

4. Define a get_row_actions method on your ModelAdmin

```python
def get_row_actions(self, obj):
    row_actions = [
        {'label': 'Edit', 'url': obj.get_edit_url(), 'enabled': obj.status is not 'cancelled'},
        {'label': 'Download PDF', 'url': obj.get_pdf_url()},
        {'label': 'Convert', 'url': reverse('convert_stuff', args=[obj.id]), tooltip='Convert stuff'},
        {'label': 'Cancel', 'action': 'mark_cancelled'},
    ]
    row_actions += super(ExampleAdmin, self).get_row_actions(obj)
    return row_actions
```

The first three menu items are simple links to a url you provide by whatever means you choose.

The final one defines 'action' instead of 'url'.

This should be the name of a callable on your ModelAdmin or Model class
(similar to https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display )

Also note the use of 'enabled' and 'tooltip' 
    
