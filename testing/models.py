from django.db import models
# from django.contrib.auth.models import User

class Bidang(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)

    def __str__(self):  # Nama method harus __str__ (dua garis bawah di kiri dan kanan)
        return self.nama
    
    class Meta:
        verbose_name_plural = "Bidang"
        ordering = ['id']

class Pegawai(models.Model):
    id = models.AutoField(primary_key=True)  # ID otomatis
    nomor_induk = models.CharField(max_length=20, unique=True)  # Nomor induk pegawai
    nama = models.CharField(max_length=100)  # Nama pegawai
    alamat = models.TextField()  # Alamat pegawai
    no_telp = models.CharField(max_length=15)  # Nomor telepon pegawai
    bidang = models.ForeignKey(Bidang, on_delete=models.CASCADE)  # Relasi ke tabel Bidang

    def __str__(self):
        return f"{self.nama} - {self.nomor_induk}"
    
    class Meta:
        verbose_name_plural = "Pegawai"
        ordering = ['nama']