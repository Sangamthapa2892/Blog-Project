from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Comment, Blog, Contact
from django.utils.html import format_html

# Register your models here.

admin.site.register(Comment)
admin.site.register(Contact)
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'created_at', 'image_tag')  # adjust fields as needed
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "No Image"

    image_tag.short_description = 'Preview'

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'profile_image_tag')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'address', 'profile_image', 'bio')}),  # only model fields here
    )

    readonly_fields = ('profile_image_tag',)  # show image preview

    def profile_image_tag(self, obj):
        return format_html(
            '<img src="{}" width="100" height="auto" style="border-radius:5px;" />',
            obj.get_profile_image_url()
        )
admin.site.register(CustomUser, CustomUserAdmin)
