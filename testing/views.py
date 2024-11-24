from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Bidang
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

# mengarahkan ke halaman beranda
# Redirect ke halaman login jika belum login
@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')

# fungsi login
def login(request):
    if request.method == "POST":
        # Ambil data dari form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentikasi pengguna
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login berhasil
            auth_login(request, user)
            return redirect('home')  # Ubah 'home' ke URL utama Anda
        else:
            # Login gagal
            messages.success(request, "Username atau password salah.")
            return redirect('login')

    # Jika request bukan POST, render halaman login
    return render(request, 'login.html')

# fungsi logout
def logout_view(request):
    logout(request)
    messages.success(request, "Anda telah berhasil logout.")
    return redirect('login')

# mengarahkan ke halaman kelola user
def user(request):
    # Ambil data user yang bukan staff dan aktif
    users = User.objects.filter(is_staff=False, is_active=True).order_by('id')
    return render(request, 'user.html', {'users': users})

# fungsi tambah user
def tambah_user(request):
    if request.method == "POST":
        # Ambil data dari form
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validasi input
        if password != password2:
            messages.error(
                request, "Password dan Konfirmasi Password tidak cocok.")
            return redirect('tambah_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('tambah_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah terdaftar.")
            return redirect('tambah_user')

        # Simpan data user ke database
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nama_depan,
            last_name=nama_belakang
        )
        user.save()
        messages.success(request, "User berhasil ditambahkan!")
        return redirect('user')  # Ubah sesuai kebutuhan

    # Jika request bukan POST, kembalikan halaman form
    return render(request, 'tambah_user.html')

# fungsi hapus user
def hapus_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if not user.is_staff:  # Pastikan pengguna yang dihapus bukan staff
            user.delete()
            messages.success(request, "User berhasil dihapus.")
        else:
            messages.error(
                request, "Tidak dapat menghapus user dengan status staff.")
    except User.DoesNotExist:
        messages.error(request, "User tidak ditemukan.")
    return redirect('user')

# mengarahkan ke halaman kelola bidang dan menampilkan data bidang
def bidang(request):
    # Ambil semua data dari model Bidang
    bidangs = Bidang.objects.all()
    # Kirimkan data ke template
    return render(request, 'bidang.html', {'bidangs': bidangs})

# fungsi tambah bidang
def tambah_bidang(request):
    if request.method == "POST":
        # Ambil data dari input form
        nama_bidang = request.POST.get('nama_bidang')
        if nama_bidang:  # Validasi jika nama_bidang tidak kosong
            # Buat objek Bidang dan simpan ke database
            Bidang.objects.create(nama=nama_bidang)
            # Tambahkan pesan sukses
            messages.success(request, "Bidang berhasil ditambahkan!")
            # Redirect ke halaman daftar bidang
            return redirect('bidang')

        else:
            # Tambahkan pesan error jika input kosong
            messages.error(request, "Nama bidang tidak boleh kosong.")
            return redirect('tambah_bidang')

    # Render halaman tambah bidang
    return render(request, 'tambahBidang.html')

# Fungsi Edit Bidang
def edit_bidang(request, id):
    bidang = get_object_or_404(Bidang, id=id)
    if request.method == 'POST':
        bidang.nama = request.POST.get('nama', bidang.nama)
        bidang.save()
        messages.success(request, 'Bidang berhasil diubah!')
        return redirect('bidang')  # Kembali ke halaman tabel
    return render(request, 'edit_bidang.html', {'bidang': bidang})

# Fungsi Hapus Bidang
def delete_bidang(request, id):
    bidang = get_object_or_404(Bidang, id=id)
    if request.method == 'POST':
        bidang.delete()
        messages.success(request, 'Bidang berhasil dihapus!')
        return redirect('bidang')  # Kembali ke halaman tabel

# mengarahkan ke halaman kelola pegawai
def pegawai(request):
    return render(request, 'pegawai.html')

# mengarahkan ke halaman tambah pegawai
def tambah_pegawai(request):
    return render(request, 'tambah_pegawai.html')

# mengarahkan ke halaman kelola kriteria
def kriteria(request):
    return render(request, 'kriteria.html')

# mengarahkan ke halaman tambah kriteria
def tambah_kriteria(request):
    return render(request, 'tambah_kriteria.html')

# mengarahkan ke halaman kelola penilaian
def penilaian(request):
    return render(request, 'penilaian.html')

# mengarahkan ke halaman pegawai terbaik
def pegawai_terbaik(request):
    return render(request, 'pegawai_terbaik.html')
