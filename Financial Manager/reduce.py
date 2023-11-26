import csv
import tkinter as tk
from tkinter import ttk

# Define entry_nama, label_status, and tree_cicilan as global variables
entry_nama = None
label_status = None
tree_cicilan = None

def baca_csv(nama_file):
    with open(nama_file, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def tulis_csv(nama_file, data):
    with open(nama_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def kurangi_nilai_cicilan(cicilan_data, record_data, nama_cicilan):
    # Mendapatkan nilai cicilan dari baris paling akhir di record.csv
    nilai_cicilan_terakhir = float(record_data[-1]['Cicilan'])

    # Mengurangi nilai pada kolom "jumlah" di cicilan.csv sesuai dengan nilai cicilan terakhir
    for baris in cicilan_data:
        if baris['Nama'] == nama_cicilan:
            baris['Jumlah'] = max(0, float(baris['Jumlah']) - nilai_cicilan_terakhir)
            if baris['Jumlah'] == 0:
                baris['Status'] = 'Lunas'

    return cicilan_data

def hapus_data_cicilan(nama_cicilan):
    global tree_cicilan  # Declare tree_cicilan as a global variable

    cicilan_data = baca_csv(cicilan_file)

    # Cari dan hapus data cicilan sesuai dengan nama_cicilan
    for i, baris in enumerate(cicilan_data):
        if baris['Nama'] == nama_cicilan:
            del cicilan_data[i]
            break

    tulis_csv(cicilan_file, cicilan_data)

    # Hapus semua item dalam Treeview
    for item in tree_cicilan.get_children():
        tree_cicilan.delete(item)

    # Tambahkan kembali data terbaru ke dalam Treeview
    for row in cicilan_data:
        tree_cicilan.insert("", "end", values=list(row.values()))

def update_tabel():
    global entry_nama, label_status, tree_cicilan  # Declare entry_nama, label_status, and tree_cicilan as global variables
    nama_cicilan = entry_nama.get()

    if not nama_cicilan:
        label_status.config(text="Masukkan Nama Cicilan")
        return

    cicilan_data = baca_csv(cicilan_file)
    record_data = baca_csv(record_file)

    cicilan_data_updated = kurangi_nilai_cicilan(cicilan_data, record_data, nama_cicilan)

    tulis_csv(cicilan_file, cicilan_data_updated)
    label_status.config(text=f"Jumlah cicilan berhasil dikurangi. Status diubah menjadi 'Lunas' jika jumlah cicilan mencapai 0.")

    # Hapus semua item dalam Treeview
    for item in tree_cicilan.get_children():
        tree_cicilan.delete(item)

    # Tambahkan kembali data terbaru ke dalam Treeview
    for row in cicilan_data_updated:
        tree_cicilan.insert("", "end", values=list(row.values()))

def tampilkan_tabel():
    global entry_nama, label_status, tree_cicilan  # Declare entry_nama, label_status, and tree_cicilan as global variables

    cicilan_data = baca_csv(cicilan_file)
    record_data = baca_csv(record_file)

    root = tk.Tk()
    root.title("Pengurangan Nilai Cicilan")

    # Tampilkan bagian kolom "Cicilan" dari baris terakhir record.csv di atas input
    label_cicilan = ttk.Label(root, text=f"Alokasi cicilan bulan ini: {record_data[-1]['Cicilan']}")
    label_cicilan.pack(pady=10)

    # Tabel cicilan.csv
    frame_cicilan = ttk.Frame(root)
    frame_cicilan.pack(padx=10, pady=10)

    tree_cicilan = ttk.Treeview(frame_cicilan, columns=list(cicilan_data[0].keys()), show="headings")
    for col in cicilan_data[0].keys():
        tree_cicilan.heading(col, text=col)
    for row in cicilan_data:
        tree_cicilan.insert("", "end", values=list(row.values()))
    tree_cicilan.pack()

    # Label dan Entry untuk input Nama Cicilan
    label_nama = ttk.Label(root, text="Nama Cicilan:")
    label_nama.pack(pady=5)

    entry_nama = ttk.Entry(root)
    entry_nama.pack(pady=5)

    # Tombol untuk mengurangi nilai
    button_kurangi = ttk.Button(root, text="Kurangi Nilai", command=update_tabel)
    button_kurangi.pack(pady=10)

    # Tombol untuk menghapus satu data cicilan
    button_hapus = ttk.Button(root, text="Hapus Data Cicilan", command=lambda: hapus_data_cicilan(entry_nama.get()))
    button_hapus.pack(pady=10)

    # Label status
    label_status = ttk.Label(root, text="")
    label_status.pack(pady=10)

    root.mainloop()

# Ganti nama file sesuai dengan nama file yang Anda miliki
cicilan_file = 'cicilan.csv'
record_file = 'record.csv'

# Panggil fungsi untuk menampilkan tabel
tampilkan_tabel()
