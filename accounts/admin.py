from django.contrib import admin
from .models import Profile
# Register your models here.

admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone_number', 'has_image')

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'

    def save_model(self, request, obj, form, change):
        if change and 'image' in form.changed_data and not obj.image:
            # If the image was removed, delete the file from storage
            try:
                old_instance = Profile.objects.get(pk=obj.pk)
                if old_instance.image:
                    old_instance.image.delete(save=False)
            except Profile.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)
        
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'signup_method', 'is_staff', 'date_joined')

    def signup_method(self, obj):
        if SocialAccount.objects.filter(user=obj).exists():
            return "Google"
        return "Manual"
    signup_method.short_description = "Signup Method"

# إلغاء التسجيل الافتراضي وتسجيل الجديد
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)