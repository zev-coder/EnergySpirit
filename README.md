# EnergySpirit

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

EnergySpirit adalah project backend untuk brand fiktif bertema energy drink, mirip konsep brand seperti Red Bull dan Monster, tetapi fokusnya bukan hanya minuman. EnergySpirit juga dirancang sebagai brand merchandise seperti apparel, aksesoris, dan produk lifestyle.

Project ini dibuat untuk tujuan belajar saja, terutama untuk latihan membangun backend API menggunakan Python dan FastAPI. Project ini akan terus berkembang seiring proses belajar dan penambahan fitur baru.

## Status Project

Backend masih dalam tahap pengembangan. Frontend akan dibuat setelah backend selesai 100%.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- FastAPI Users
- Uvicorn
- React + Vite untuk frontend nanti
- Tailwind CSS untuk styling frontend nanti

## Fitur Yang Sudah Ada

- Setup aplikasi FastAPI
- Koneksi database dengan SQLAlchemy async
- Auto create table saat database belum ada
- Authentication menggunakan FastAPI Users
- Register user
- Login menggunakan JWT
- Verify account
- Reset password
- Endpoint user management
- Role user

## Fitur Yang Akan Dibuat

- CRUD product merchandise EnergySpirit
- Kategori produk
- Detail produk
- Cart / keranjang belanja
- Cart item dengan quantity
- Status cart atau order
- Role admin dan user
- Admin dashboard untuk mengelola produk
- Sistem checkout sederhana untuk simulasi
- Dokumentasi API yang lebih lengkap
- Frontend dengan React, Vite, dan Tailwind CSS

## Rencana Frontend

Frontend belum dibuat untuk saat ini. Setelah backend selesai, frontend akan dibangun menggunakan React + Vite dan Tailwind CSS.

Rencana tampilan frontend:

- Landing page brand EnergySpirit
- Halaman katalog merchandise
- Halaman detail produk
- Cart page
- Login dan register page
- Dashboard admin sederhana

## Cara Menjalankan Project

Clone repository:

```bash
git clone https://github.com/username/EnergySpirit.git
cd EnergySpirit
```

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan server:

```bash
python main.py
```

API akan berjalan di:

```text
http://localhost:8000
```

Dokumentasi API FastAPI:

```text
http://localhost:8000/docs
```

## Catatan

Project ini dibuat hanya untuk pembelajaran dan portfolio pribadi. EnergySpirit bukan brand asli dan tidak digunakan untuk kebutuhan komersial.
