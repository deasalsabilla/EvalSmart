from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Bidang, Pegawai, Kriteria
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

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

# mengarahkan ke halaman dan menampilkan data kelola pegawai
def pegawai(request):
    pegawais = Pegawai.objects.all()
    return render(request, 'pegawai.html', {'pegawais' : pegawais})

# fungsi tambah pegawai
def tambah_pegawai(request):
    if request.method == "POST":
        nomor_induk = request.POST.get('nomor_induk')
        nama_pegawai = request.POST.get('nama_pegawai')
        alamat = request.POST.get('alamat')
        no_hp = request.POST.get('no_hp')
        bidang_id = request.POST.get('pilih_bidang')  # ID bidang dari dropdown

        # Validasi dan penyimpanan data
        try:
            bidang = Bidang.objects.get(id=bidang_id)  # Cari bidang berdasarkan ID
            Pegawai.objects.create(
                nomor_induk=nomor_induk,
                nama=nama_pegawai,
                alamat=alamat,
                no_telp=no_hp,
                bidang=bidang
            )
            messages.success(request, "Pegawai berhasil ditambahkan.")
            return redirect('pegawai')  # Redirect ke halaman tambah pegawai
        except Bidang.DoesNotExist:
            messages.error(request, "Bidang tidak ditemukan.")
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")

    # Ambil data bidang untuk ditampilkan di dropdown
    bidang_list = Bidang.objects.all()
    return render(request, 'tambah_pegawai.html', {'bidang_list': bidang_list})

# FUNGSI EDIT PEGAWAI
def edit_pegawai(request, pegawai_id):
    pegawai = get_object_or_404(Pegawai, id=pegawai_id)  # Ambil data pegawai berdasarkan ID
    bidang_list = Bidang.objects.all()  # Ambil semua bidang untuk dropdown

    if request.method == "POST":
        # Ambil data dari form
        pegawai.nomor_induk = request.POST.get('nomor_induk')
        pegawai.nama = request.POST.get('nama_pegawai')
        pegawai.alamat = request.POST.get('alamat')
        pegawai.no_telp = request.POST.get('no_hp')

        bidang_id = request.POST.get('pilih_bidang')
        try:
            pegawai.bidang = Bidang.objects.get(id=bidang_id)  # Update bidang berdasarkan ID yang dipilih
            pegawai.save()  # Simpan perubahan ke database
            messages.success(request, "Data pegawai berhasil diperbarui.")
            return redirect('pegawai')  # Redirect ke halaman daftar pegawai (atau lainnya)
        except Bidang.DoesNotExist:
            messages.error(request, "Bidang tidak ditemukan.")
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")

    return render(request, 'edit_pegawai.html', {'pegawai': pegawai, 'bidang_list': bidang_list})

# Fungsi Hapus Pegawai
def delete_pegawai(request, id):
    pegawai = get_object_or_404(Pegawai, id=id)
    if request.method == 'POST':
        pegawai.delete()
        messages.success(request, 'Pegawai berhasil dihapus!')
        return redirect('pegawai')  # Kembali ke halaman tabel

# mengarahkan ke halaman kelola kriteria
def kriteria(request):
    kriterias = Kriteria.objects.all()
    return render(request, 'kriteria.html', {'kriterias' : kriterias})

# fungsi tambah kriteria
def tambah_kriteria(request):
    if request.method == "POST":
        # Ambil data dari input form
        nama_kriteria = request.POST.get('nama_kriteria')
        if nama_kriteria:  # Validasi jika nama_bidang tidak kosong
            # Buat objek Bidang dan simpan ke database
            Kriteria.objects.create(nama=nama_kriteria)
            # Tambahkan pesan sukses
            messages.success(request, "Kriteria berhasil ditambahkan!")
            # Redirect ke halaman daftar bidang
            return redirect('kriteria')

        else:
            # Tambahkan pesan error jika input kosong
            messages.error(request, "Nama kriteria tidak boleh kosong.")
            return redirect('tambah_kriteria')

    return render(request, 'tambah_kriteria.html')

# Fungsi Edit Kriteria
def edit_kriteria(request, id):
    kriteria = get_object_or_404(Kriteria, id=id)
    if request.method == 'POST':
        kriteria.nama = request.POST.get('nama', kriteria.nama)
        kriteria.save()
        messages.success(request, 'Kriteria berhasil diubah!')
        return redirect('kriteria')  # Kembali ke halaman tabel
    return render(request, 'edit_kriteria.html', {'kriteria': kriteria})

# Fungsi Hapus Kriteria
def delete_kriteria(request, id):
    kriteria = get_object_or_404(Kriteria, id=id)
    if request.method == 'POST':
        kriteria.delete()
        messages.success(request, 'Kriteria berhasil dihapus!')
        return redirect('kriteria')  # Kembali ke halaman tabel
    
# fungsi input bobot
def input_bobot(request):
    if request.method == "POST":
        try:
            bobot_baru = float(request.POST.get('bobot', 0))  # Ambil input bobot dari form
            total_bobot_sekarang = Kriteria.objects.aggregate(total=Sum('bobot'))['total'] or 0

            # Hitung total bobot jika bobot baru ditambahkan
            total_bobot_setelah_input = total_bobot_sekarang + bobot_baru

            if total_bobot_setelah_input > 100:
                # Jika total bobot melebihi 100, tampilkan pesan error
                messages.error(
                    request, 
                    f"Bobot yang Anda masukkan melebihi batas. Maksimal yang bisa ditambahkan adalah {100 - total_bobot_sekarang:.2f}%."
                )
            else:
                # Simpan bobot baru
                kriteria = Kriteria.objects.latest('id')  # Ambil kriteria terakhir yang dibuat
                kriteria.bobot = bobot_baru
                kriteria.save()

                messages.success(request, "Bobot berhasil ditambahkan.")
                return redirect('kriteria')  # Ganti dengan URL yang sesuai
        except ValueError:
            messages.error(request, "Bobot harus berupa angka yang valid.")
    
    # Data untuk ditampilkan di template
    total_bobot_sekarang = Kriteria.objects.aggregate(total=Sum('bobot'))['total'] or 0
    context = {
        'total_bobot_sekarang': total_bobot_sekarang,
        'bobot_maksimal': 100 - total_bobot_sekarang,
    }
    return render(request, 'bobot_kriteria.html', context)

# mengarahkan ke halaman kelola penilaian
def penilaian(request):
    return render(request, 'penilaian.html')

# mengarahkan ke halaman pegawai terbaik
def pegawai_terbaik(request):
    return render(request, 'pegawai_terbaik.html')

# mengarahkan ke halaman riwayat
def riwayat(request):
    return render(request, 'riwayat.html')