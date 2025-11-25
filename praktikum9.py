import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

#  KONEKSI DATABASE
conn = sqlite3.connect("nilai_siswa.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
    )
""")
conn.commit()

#  FUNGSI LOGIKA PREDIKSI
def prediksi_fakultas(bio, fis, ing):
    if bio > fis and bio > ing:
        return "Kedokteran"
    elif fis > bio and fis > ing:
        return "Teknik"
    elif ing > bio and ing > fis:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

#  FUNGSI SUBMIT DATA
def submit_data():
    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fisika.get())
    ing = int(entry_inggris.get())

    prediksi = prediksi_fakultas(bio, fis, ing)

    cur.execute("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)",
                (nama, bio, fis, ing, prediksi))
    conn.commit()

    messagebox.showinfo("Sukses", "Data berhasil disimpan!")
    load_data()

#  FUNGSI UPDATE DATA
def update_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Perhatian", "Pilih data yang mau diupdate!")
        return

    item = tree.item(selected)
    data_id = item["values"][0]

    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fisika.get())
    ing = int(entry_inggris.get())

    prediksi = prediksi_fakultas(bio, fis, ing)

    cur.execute("""
        UPDATE nilai_siswa SET
            nama_siswa = ?, 
            biologi = ?, 
            fisika = ?, 
            inggris = ?, 
            prediksi_fakultas = ?
        WHERE id = ?
    """, (nama, bio, fis, ing, prediksi, data_id))

    conn.commit()
    messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
    load_data()

#  FUNGSI DELETE DATA
def delete_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Perhatian", "Pilih data dulu!")
        return

    item = tree.item(selected)
    data_id = item["values"][0]

    cur.execute("DELETE FROM nilai_siswa WHERE id = ?", (data_id,))
    conn.commit()

    messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    load_data()

#  LOAD DATA KE TREEVIEW
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    cur.execute("SELECT * FROM nilai_siswa")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

#  GUI TKINTER
root = tk.Tk()
root.title("Prediksi Prodi Mahasiswa")
root.geometry("700x500")

# LABEL DAN ENTRY
tk.Label(root, text="Nama Siswa").grid(row=0, column=0)
tk.Label(root, text="Nilai Biologi").grid(row=1, column=0)
tk.Label(root, text="Nilai Fisika").grid(row=2, column=0)
tk.Label(root, text="Nilai Inggris").grid(row=3, column=0)

entry_nama = tk.Entry(root)
entry_bio = tk.Entry(root)
entry_fisika = tk.Entry(root)
entry_inggris = tk.Entry(root)

entry_nama.grid(row=0, column=1)
entry_bio.grid(row=1, column=1)
entry_fisika.grid(row=2, column=1)
entry_inggris.grid(row=3, column=1)

# BUTTON CRUD
btn_submit = tk.Button(root, text="Submit", command=submit_data, bg="green", fg="white")
btn_update = tk.Button(root, text="Update", command=update_data, bg="blue", fg="white")
btn_delete = tk.Button(root, text="Delete", command=delete_data, bg="red", fg="white")

btn_submit.grid(row=4, column=0, pady=10)
btn_update.grid(row=4, column=1, pady=10)
btn_delete.grid(row=4, column=2, pady=10)

# TABEL TREEVIEW
columns = ("ID", "Nama", "Biologi", "Fisika", "Inggris", "Prediksi")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.grid(row=5, column=0, columnspan=3, pady=20)

load_data()

root.mainloop()
