from django.contrib import admin

from materials.models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id_material', 'name', 'unit', 'material_type')
    list_filter = ('id_material', 'name', 'unit', 'material_type')
    search_fields = ('id_material', 'name', 'unit', 'material_type',)
