# # custom_auth/admin.py
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
# from .models import UserProfile

# # Inline admin for UserProfile
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'Profile'

# # Extend User admin
# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     inlines = (UserProfileInline,)
#     list_display = BaseUserAdmin.list_display + ('get_role', 'get_phone')
#     list_filter = BaseUserAdmin.list_filter + ('userprofile__role',)
    
#     def get_role(self, obj):
#         try:
#             return obj.userprofile.role
#         except UserProfile.DoesNotExist:
#             return 'No Profile'
#     get_role.short_description = 'Role'
    
#     def get_phone(self, obj):
#         try:
#             return obj.userprofile.phone
#         except UserProfile.DoesNotExist:
#             return ''
#     get_phone.short_description = 'Phone'

# # Register your models here.


# custom_auth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Inline admin for UserProfile to show profile data on the User page
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    
# Extend User admin to include UserProfile details
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = BaseUserAdmin.list_display + ('get_role', 'get_phone')
    list_filter = BaseUserAdmin.list_filter + ('userprofile__role',)
    
    def get_role(self, obj):
        try:
            return obj.userprofile.role
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'
    
    def get_phone(self, obj):
        try:
            return obj.userprofile.phone
        except UserProfile.DoesNotExist:
            return ''
    get_phone.short_description = 'Phone'

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the User model with your custom UserAdmin
admin.site.register(User, UserAdmin)

# Register your UserProfile model for separate access in the admin panel if needed
# admin.site.register(UserProfile)