"""
URL configuration for testing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("bidang/", views.bidang, name="bidang"),
    path("bidang/tambah-bidang/", views.tambah_bidang, name="tambahBidang"),
    path('bidang/edit-bidang/<int:id>/', views.edit_bidang, name='edit_bidang'),
    path('bidang/hapus-bidang/<int:id>/', views.delete_bidang, name='delete_bidang'),
    path("user/", views.user, name="user"),
    path("user/tambah-user/", views.tambah_user, name="tambah_user"),
    path('user/hapus-user/<int:user_id>/', views.hapus_user, name='hapus_user'),
    path("pegawai/", views.pegawai, name="pegawai"),
    path("pegawai/tambah-pegawai/", views.tambah_pegawai, name="tambah_pegawai"),
    path("kriteria/", views.kriteria, name="kriteria"),
    path("kriteria/tambah-kriteria/", views.tambah_kriteria, name="tambah_kriteria"),
    path("penilaian/", views.penilaian, name="penilaian"),
    path("penilaian/pegawai-terbaik/", views.pegawai_terbaik, name="pegawai_terbaik"),
    path("riwayat/", views.riwayat, name="riwayat"),
]