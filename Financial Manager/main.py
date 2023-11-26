""" 
Financial Manager
Modified by: Fatih Raka Ksatria 
"""

from tkinter import *
from tkinter import messagebox
import csv
from tkinter import ttk
from tkinter.ttk import Combobox
from category import category
from functions import *

def input_income_check(*args):
    try:
        income.setIncome(int(VARincome.get()))
    except ValueError:
        if VARincome.get() == "":
            pass
        else:
            messagebox.showwarning('Peringatan!', 'Harap masukkan angka!')
            INPUTincome.delete(len(INPUTincome.get()) - 1)

def check_ratio_limit(*args):
    RATIOtotal = getTOtalRatio(widget_data)
    LABELtotalvalue.config(text=RATIOtotal)
    if RATIOtotal > 100:
        ratio_warning()
    else:
        ratio_normal()

def ratio_warning():
    LABELtotalvalue.config(fg='red')
    LABELtotaltext.config(fg='red')
    LABELpercent.config(fg='red')
    BUTTONnominal_calculation.config(state=DISABLED, text='Cek\ntotal\nrasio!')

def ratio_normal():
    LABELtotalvalue.config(fg='black')
    LABELtotaltext.config(fg='black')
    LABELpercent.config(fg='black')
    BUTTONnominal_calculation.config(state=ACTIVE, text='Hitung!')

def set_to_default_ratio():
    category_object = []
    for gui_data in gui_declaration_data:
        category_object.append(gui_declaration_data[gui_data][0])
    for i, RATIOcategory in enumerate(widget_data):
        RATIOcategory[0].set(category_object[i].getRatio_default())
    LABELtotalvalue.config(text=100, fg='black')
    ratio_normal()

def calculate_nominal():
    try:
        int(VARincome.get())
        RATIOtotal = getTOtalRatio(widget_data)
        if RATIOtotal < 100:
            ratio_under_value = messagebox.askyesno('?', 'Nilai total rasio di bawah 100%, lanjutkan?')
            if ratio_under_value:
                for i, object in enumerate(gui_declaration_data):
                    gui_declaration_data[object][0].setRatio(widget_data[i][0].get())
                    widget_data[i][4].config(text=f"Rp{int(gui_declaration_data[object][0].getNominal(income.getIncome()))}")
                
        else:
            for i, object in enumerate(gui_declaration_data):
                gui_declaration_data[object][0].setRatio(widget_data[i][0].get())
                widget_data[i][4].config(text=f"Rp{int(gui_declaration_data[object][0].getNominal(income.getIncome()))}")
    except ValueError:
        messagebox.showerror('Error!', 'Input pendapatan tidak valid!')

def save_to_csv():
    with open("cicilan.csv", "a", newline='') as cicilan_file:
        fieldnames = ["Nama", "Jumlah", "Status"]
        cicilan_writer = csv.DictWriter(cicilan_file, fieldnames=fieldnames)
        
        # Tulis judul kolom jika file kosong
        if cicilan_file.tell() == 0:
            cicilan_writer.writeheader()

        # Simpan data cicilan
        cicilan_writer.writerow({"Nama": VARnama_cicilan.get(), "Jumlah": VARjumlah_cicilan.get(), "Status": "Belum Lunas"})
    
    messagebox.showinfo('Info', 'Data telah disimpan ke cicilan.csv')
    

def save_to_record_csv():
    try:
        # Dapatkan data dari inputan
        bulan = VARbulan.get()  # Mengambil bulan yang dipilih
        pendapatan = income.getIncome()

        # Data hasil perhitungan sesuai dengan kolom yang sesuai
        hasil_perhitungan = [
            basic_needs.getNominal(pendapatan),
            productivity.getNominal(pendapatan),
            bill.getNominal(pendapatan),
            installment.getNominal(pendapatan),
            insurance.getNominal(pendapatan),
            desire.getNominal(pendapatan),
            emergency.getNominal(pendapatan),
            saving.getNominal(pendapatan),
            investment.getNominal(pendapatan),
            others.getNominal(pendapatan)
        ]

        # Simpan data ke dalam "record.csv"
        with open("record.csv", "a", newline='') as record_file:
            record_writer = csv.writer(record_file)
            if record_file.tell() == 0:
                # Tulis judul kolom jika file kosong
                fieldnames = ["Bulan", "Pendapatan", "Kebutuhan pokok", "Produktivitas", "Tagihan", "Cicilan", "Asuransi", "Keinginan", "Darurat", "Tabungan", "Investasi", "Lain-lain"]
                record_writer.writerow(fieldnames)
            
            # Tulis data ke dalam file
            record_writer.writerow([bulan, pendapatan] + hasil_perhitungan)

        messagebox.showinfo('Info', 'Data telah disimpan ke record.csv')
    except ValueError:
        messagebox.showerror('Error!', 'Terjadi kesalahan saat menyimpan data.')

def display_records():
    try:
        with open("record.csv", newline='') as record_file:
            record_data = list(csv.reader(record_file))
            if record_data:
                # Create a new window to display the records
                records_window = Toplevel(root)
                records_window.title("Record Data")

                # Create a treeview widget to display the records
                tree = ttk.Treeview(records_window, columns=("Bulan", "Pendapatan", "Kebutuhan pokok", "Produktivitas", "Tagihan", "Cicilan", "Asuransi", "Keinginan", "Darurat", "Tabungan", "Investasi", "Lain-lain"), show="headings")

                # Create a horizontal scrollbar
                horizontal_scrollbar = ttk.Scrollbar(records_window, orient="horizontal", command=tree.xview)
                horizontal_scrollbar.pack(side="bottom", fill="x")
                tree.configure(xscrollcommand=horizontal_scrollbar.set)

                # Define column headings
                headings = [
                    ("Bulan", 50),
                    ("Pendapatan", 100),
                    ("Kebutuhan pokok", 100),
                    ("Produktivitas", 100),
                    ("Tagihan", 100),
                    ("Cicilan", 100),
                    ("Asuransi", 100),
                    ("Keinginan", 100),
                    ("Darurat", 100),
                    ("Tabungan", 100),
                    ("Investasi", 100),
                    ("Lain-lain", 100)
                ]

                for i, (heading, minwidth) in enumerate(headings):
                    tree.heading(f"#{i+1}", text=heading)
                    tree.column(f"#{i+1}", minwidth=minwidth, width=minwidth)

                for record in record_data[1:]:
                    tree.insert("", "end", values=record)

                tree.pack(fill="both", expand=True)

            else:
                tk.messagebox.showinfo("Info", "Tidak ada data di record.csv")
    
    except FileNotFoundError:
        tk.messagebox.showinfo("Info", "File record.csv tidak ditemukan")

def reduce_cicilan():
    # Menggunakan modul subprocess untuk menjalankan program reduce.py
    import subprocess
    subprocess.run(["python", "reduce.py"])
        
## Instansiasi
# income
income = category()
# Wajib dipenuhi 60%
basic_needs = category(25.0)
productivity = category(10.0)
bill = category(9.0)
installment = category(15.0)
insurance = category(1.0)
# Keinginan 20%
desire = category(20.0)
# Tabungan & dana darurat 15%
emergency = category(7.5)
saving = category(6.5)
# Investasi 5%
investment = category(5.0)
others = category(1.0)

## GUI
# main window
root = Tk()
root.title("Financial Manager")
root.resizable(0, 0)

# Frame
FRAMEheader = Frame(root, borderwidth=2, relief=GROOVE, width=270, height=140)
FRAMEheader.grid_propagate(0)
gridding(FRAMEheader, 0, 0)
FRAMEcaltulation = Frame(root, borderwidth=2, relief=GROOVE, width=70, height=70)
FRAMEcaltulation.grid_propagate(0)
gridding(FRAMEcaltulation, 0, 1)
FRAMEratio = Frame(root, borderwidth=2, relief=GROOVE, width=340, height=265)
FRAMEratio.grid_propagate(0)
gridding(FRAMEratio, 1, 0, None, 2, N)
FRAMEfooter = Frame(root, borderwidth=2, relief=GROOVE, width=340, height=60)
FRAMEfooter.grid_propagate(0)
gridding(FRAMEfooter, 2, 0, None, 2)

# TITLE
Title = Label(FRAMEheader, text='Financial Manager', font=('Arial Bold', 16))
gridding(Title, 0, 0, 1, 4, N)

# Income input
VARincome = StringVar()
VARincome.trace(W, input_income_check)
LABELincome = Label(FRAMEheader, text='Pendapatan : Rp')
gridding(LABELincome, 1, 0)
TOOLTIPincome = Balloon(FRAMEheader)
TOOLTIPincome.bind_widget(LABELincome, balloonmsg='Pendapatan perbulan setelah dipotong pajak.')
INPUTincome = Entry(FRAMEheader, textvariable=VARincome, width=25)
gridding(INPUTincome, 1, 1, None, 3)

# Nama Cicilan
LABELnama_cicilan = Label(FRAMEheader, text='Nama Cicilan:')
gridding(LABELnama_cicilan, 2, 0)
VARnama_cicilan = StringVar()
INPUTnama_cicilan = Entry(FRAMEheader, textvariable=VARnama_cicilan, width=25)
gridding(INPUTnama_cicilan, 2, 1)

# Jumlah Cicilan
LABELjumlah_cicilan = Label(FRAMEheader, text='Jumlah Cicilan (Rp):')
gridding(LABELjumlah_cicilan, 3, 0)
VARjumlah_cicilan = StringVar()
INPUTjumlah_cicilan = Entry(FRAMEheader, textvariable=VARjumlah_cicilan, width=25)
gridding(INPUTjumlah_cicilan, 3, 1)

# Tambahkan Combobox untuk memasukkan bulan
LABELbulan = Label(FRAMEheader, text='Bulan:')
gridding(LABELbulan, 4, 0)
bulan_list = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]
VARbulan = StringVar()
INPUTbulan = Combobox(FRAMEheader, textvariable=VARbulan, values=bulan_list, width=22)
gridding(INPUTbulan, 4, 1)
# Alokasi Pengeluaran title
LABELalocation = Label(FRAMEratio, text='Alokasi Pengeluaran', font=('Arial bold',))
gridding(LABELalocation, 0, 0, None, 5, N)

# GUI declaration data
gui_declaration_data = {
    'basic_needs': [basic_needs, 'Kebutuhan pokok : '],
    'productivity': [productivity, 'Produktivitas : '],
    'bill': [bill, 'Tagihan : '],
    'installment': [installment, 'Cicilan : '],
    'insurance': [insurance, 'Asuransi : '],
    'desire': [desire, 'Keinginan : '],
    'emergency': [emergency, 'Darurat : '],
    'saving': [saving, 'Tabungan : '],
    'investment': [investment, 'Investasi : '],
    'others': [others, 'Lain-lain : ']
}

# GUI declaration
for ratio_category in gui_declaration_data:
    globals()[f"RATIO{ratio_category}"] = DoubleVar(value=gui_declaration_data[ratio_category][0].getRatio())
    globals()[f"LABEL{ratio_category}"] = Label(FRAMEratio, text=gui_declaration_data[ratio_category][1])
    globals()[f"INPUT{ratio_category}"] = Entry(FRAMEratio, width=5)
    globals()[f"SCALE{ratio_category}"] = Scale(FRAMEratio, from_=0, to=75, orient=HORIZONTAL, width=8, bd=1, resolution=0.5, sliderlength=15, showvalue=0)
    globals()[f"LABELNOMINAL{ratio_category}"] = Label(FRAMEratio, text=f'Rp0', width=10, anchor=W)

# Widget data
widget_data = [
    [RATIObasic_needs, LABELbasic_needs, INPUTbasic_needs, SCALEbasic_needs, LABELNOMINALbasic_needs],
    [RATIOproductivity, LABELproductivity, INPUTproductivity, SCALEproductivity, LABELNOMINALproductivity],
    [RATIObill, LABELbill, INPUTbill, SCALEbill, LABELNOMINALbill],
    [RATIOinstallment, LABELinstallment, INPUTinstallment, SCALEinstallment, LABELNOMINALinstallment],
    [RATIOinsurance, LABELinsurance, INPUTinsurance, SCALEinsurance, LABELNOMINALinsurance],
    [RATIOdesire, LABELdesire, INPUTdesire, SCALEdesire, LABELNOMINALdesire],
    [RATIOemergency, LABELemergency, INPUTemergency, SCALEemergency, LABELNOMINALemergency],
    [RATIOsaving, LABELsaving, INPUTsaving, SCALEsaving, LABELNOMINALsaving],
    [RATIOinvestment, LABELinvestment, INPUTinvestment, SCALEinvestment, LABELNOMINALinvestment],
    [RATIOothers, LABELothers, INPUTothers, SCALEothers, LABELNOMINALothers]
]

# Ratio input placement
row = 1
for widget_list in widget_data:
    widget_list[2].config(textvariable=widget_list[0])
    widget_list[3].config(variable=widget_list[0])
    widget_list[0].trace(W, check_ratio_limit)
    gridding(widget_list[1], row, 0)
    gridding(widget_list[2], row, 1)
    LABELpercent = Label(FRAMEratio, text='%')
    gridding(LABELpercent, row, 2)
    gridding(widget_list[3], row, 3)
    gridding(widget_list[4], row, 4)
    row += 1

# RATIO total placement
LABELtotaltext = Label(FRAMEratio, text='TOTAL RASIO : ')
gridding(LABELtotaltext, 11, 0)
LABELtotalvalue = Label(FRAMEratio, text=100)
gridding(LABELtotalvalue, 11, 1)
LABELpercent = Label(FRAMEratio, text='%')
gridding(LABELpercent, row, 2)

# Default Ratio button
RATIOdefault = Button(FRAMEratio, text='Ikuti rekomendasi', command=set_to_default_ratio, width=13, relief=GROOVE)
gridding(RATIOdefault, 11, 3, None, 4)



# Nominal calculation button
BUTTONnominal_calculation = Button(FRAMEcaltulation, text='Hitung!', command=calculate_nominal, height=4, width=8, relief=RAISED)
gridding(BUTTONnominal_calculation, 0, 0)

# Tombol Simpan
BUTTON_save_to_record_csv = Button(FRAMEfooter, text='Simpan ke Catatan', command=save_to_record_csv, width=18, relief=GROOVE)
gridding(BUTTON_save_to_record_csv, 0, 0)

# Tombol Simpan
BUTTON_save_to_csv = Button(FRAMEfooter, text='Simpan Cicilan', command=save_to_csv, width=18, relief=GROOVE)
gridding(BUTTON_save_to_csv, 0, 1)

# Tombol Kurangi Cicilan

display_records_button = Button(FRAMEfooter, text="Tampilkan Catatan", command=display_records, width=18, relief=GROOVE)
gridding(display_records_button, 1, 0)

BUTTON_reduce_cicilan = Button(FRAMEfooter, text='Kurangi Cicilan', command=reduce_cicilan, width=18, relief=GROOVE)
gridding(BUTTON_reduce_cicilan, 1, 1)





root.mainloop()