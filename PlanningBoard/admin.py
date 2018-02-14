from django.contrib import admin

# Register your models here.

from .models import (
    Planning,
    Tag_Region,
    Tag_Subregion,
    Tag_Project,
    Tag_Language,
    )

admin.site.register(Planning)
admin.site.register(Tag_Subregion)
admin.site.register(Tag_Project)
admin.site.register(Tag_Language)
admin.site.register(Tag_Region)