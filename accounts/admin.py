from django.contrib import admin
from .models import Profile
# Register your models here.

admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone_number', 'has_image')

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