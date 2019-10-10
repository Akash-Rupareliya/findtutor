from django.contrib import admin
from django.contrib.auth.models import User
from .models import City,MasterUsers
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from import_export import resources

class CityResource(resources.ModelResource):

    class Meta:
        model = City
@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    pass

class MasterResource(resources.ModelResource):

    class Meta:
        model = MasterUsers
@admin.register(MasterUsers)
class MasterAdmin(ImportExportModelAdmin):
    pass