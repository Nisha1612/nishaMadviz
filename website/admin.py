from django.contrib import admin
from .models import Profile, AIUseCase

# Register the Profile model with the default admin options
admin.site.register(Profile)

class AIUseCaseAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('category', 'example_name', 'user','link', 'created_at', 'updated_at')

    # Ensure only superusers can add, change, delete, or view entries
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

# Register the AIUseCase model with the custom admin options
admin.site.register(AIUseCase, AIUseCaseAdmin)