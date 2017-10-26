Django Admin Row Actions
========================

Allows you to easily define a drop-down 'actions' menu that is appended as the final column in your model's changelist and perform actions on that row.

Menu items can call urls or methods, can be disabled, have tooltips, etc.

I've extracted this from code written for http://hireablehq.com/. The admin there has Bootstrap available but I've modified this version to use a standalone jQuery dropdown.


Installation
============

1. Install from PyPI:

    ```bash
    pip install django-admin-row-actions
    ```

    or install using pip and git:

    ```bash
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

4. Define a `get_row_actions` method on your ModelAdmin

    ```python
    def get_row_actions(self, obj):
        row_actions = [
            {
                'label': 'Edit',
                'url': obj.get_edit_url(),
                'enabled': obj.status is not 'cancelled',
            }, {
                'label': 'Download PDF',
                'url': obj.get_pdf_url(),
            }, {
                'label': 'Convert',
                'url': reverse('convert_stuff', args=[obj.id]),
                'tooltip': 'Convert stuff',
            }, {
                'divided': True,
                'label': 'Cancel',
                'action': 'mark_cancelled',
            },
        ]
        row_actions += super(ExampleAdmin, self).get_row_actions(obj)
        return row_actions
    ```

The first three menu items are simple links to a url you provide by whatever means you choose.

The final one defines 'action' instead of 'url'. This should be the name of a callable on your `ModelAdmin` or `Model` class (similar to [ModelAdmin.list_display](https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)).

You can add mouseover tooltips to each individual actions with the 'tooltip' dictionary key, and enable/disable individual actions for each individual object with the 'enabled'.

Special option 'divided' can be passed to any item to display horizontal rule above it.


Credits
=======

Inspired (and code based on): [django-object-actions](https://github.com/crccheck/django-object-actions)

Includes parts of [jquery-dropdown](http://labs.abeautifulsite.net/jquery-dropdown/); credits go to Cory LaViska.
