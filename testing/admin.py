from django.contrib import admin
from .models import Bidang, Pegawai, Kriteria, Penilaian
admin.site.site_header = 'EvalSmart'
admin.site.register(Bidang)
admin.site.register(Pegawai)
admin.site.register(Kriteria)
admin.site.register(Penilaian)