from django import forms
from .models import Shortcut

class ShortcutForm(forms.ModelForm):
    class Meta:
        model = Shortcut
        fields = ['name', 'url', 'icon_class']
