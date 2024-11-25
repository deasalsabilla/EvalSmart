from django.contrib import admin
from .models import Bidang, Pegawai
admin.site.site_header = 'EvalSmart'
admin.site.register(Bidang)
admin.site.register(Pegawai)