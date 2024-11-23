from django.db import models
# from django.contrib.auth.models import User

class Bidang(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    # user = models.ForeignKey(
    #     User, 
    #     on_delete=models.CASCADE, 
    #     related_name='bidangs',
    #     default=1  # Ubah sesuai dengan ID user default di database Anda
    # )

    def __str__(self):  # Nama method harus __str__ (dua garis bawah di kiri dan kanan)
        return self.nama
    
    class Meta:
        verbose_name_plural = "Bidang"
        ordering = ['id']
