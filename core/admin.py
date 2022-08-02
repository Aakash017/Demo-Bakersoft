from django.contrib import admin

# Register your models here.
from core.models import User, Project, TimeTracking


class UserAdmin(admin.ModelAdmin):
    list_display = ("email",)
    readonly_fields = ("email", "password")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TimeTracking)
