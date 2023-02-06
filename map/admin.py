from django.contrib import admin

from map.forms import MapForm
from map.models import Category, Map


class MapAdmin(admin.ModelAdmin):
    form = MapForm

    list_display = (
        "category",
        "name",
        "description",
        "image",
        "thumbnail",
        "pub_date",
        "maker",
    )
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = (
        "last_modified",
        "last_modified_by",
    )
    fieldsets = (
        (None, {"fields": ("name", "category", "image", "description", "pub_date")}),
        (
            "Other Information",
            {
                "fields": ("maker", "last_modified", "last_modified_by", "slug"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        print("hey!!!", type(obj))
        if not obj.maker.id:
            obj.maker = request.user
        obj.last_modified_by = request.user
        obj.save()


admin.site.register(Category)
admin.site.register(Map, MapAdmin)
