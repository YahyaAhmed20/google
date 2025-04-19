import os
import django
from django.contrib.sites.models import Site

# تحديد إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

# تهيئة Django
django.setup()

# تحقق إذا كان الموقع موجود بالفعل
site, created = Site.objects.get_or_create(domain='127.0.0.1:8000', defaults={'name': 'localhost'})

if not created:
    print(f"الموقع موجود بالفعل: {site.name}")
else:
    print(f"تم إنشاء الموقع الجديد: {site.name}")
