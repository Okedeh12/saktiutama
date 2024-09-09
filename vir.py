import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import time
from io import StringIO


# Path to data files
STOK_BARANG_FILE = "stok_barang.csv"
PENJUALAN_FILE = "penjualan.csv"
SUPPLIER_FILE = "supplier.csv"

# CSS styles for a professional look
st.markdown("""
    <style>
    .header {
        text-align: center;
        padding: 20px;
        background-color: #f0f4f8;
        border-bottom: 1px solid #ddd;
    }
    .header h1 {
        font-family: 'Arial', sans-serif;
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #f7f9fc;
        padding-top: 20px;
    }
    .sidebar .sidebar-content h2 {
        font-family: 'Arial', sans-serif;
        color: #333;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .radio {
        margin-top: 10px;
    }
    .main-content {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .stDataFrame {
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Display the header
st.markdown('<div class="header"><h1>TOKO SAKTI UTAMA</h1></div>', unsafe_allow_html=True)


# Load data from CSV files
def load_data():
    if os.path.exists(STOK_BARANG_FILE):
        st.session_state.stok_barang = pd.read_csv(STOK_BARANG_FILE, parse_dates=["Waktu Input"])
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Waktu Input"
        ])

    if os.path.exists(PENJUALAN_FILE):
        st.session_state.penjualan = pd.read_csv(PENJUALAN_FILE, parse_dates=["Waktu"])
    else:
        st.session_state.penjualan = pd.DataFrame(columns=[
            "ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", "Jumlah", "Total Harga", "Keuntungan", "Waktu"
        ])

    if os.path.exists(SUPPLIER_FILE):
        st.session_state.supplier = pd.read_csv(SUPPLIER_FILE, parse_dates=["Waktu"])
    else:
        st.session_state.supplier = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"
        ])

# Save data to CSV files
def save_data():
    st.session_state.stok_barang.to_csv(STOK_BARANG_FILE, index=False)
    st.session_state.penjualan.to_csv(PENJUALAN_FILE, index=False)
    st.session_state.supplier.to_csv(SUPPLIER_FILE, index=False)

# Initialize data
if 'stok_barang' not in st.session_state:
    load_data()

# Sidebar menu
menu = st.sidebar.radio("Pilih Menu", ["Stock Barang", "Penjualan", "Supplier", "Owner"])

# Main content area
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Fungsi untuk halaman Stock Barang
def halaman_stock_barang():
    st.header("Stock Barang")
    
    # Dummy function to save data; replace with your actual save_data implementation
    def save_data():
        # Your logic to save data, e.g., to a database or file
        pass
    
    # Form input barang baru dan edit barang
    st.subheader("Tambah/Edit Barang")
    
    # Pilih barang yang akan diedit atau pilih "Tambah Baru"
    selected_action = st.selectbox("Pilih Aksi", ["Tambah Barang", "Edit Barang"])
    
    if selected_action == "Edit Barang":
        # Pilih ID Barang untuk Diedit
        selected_id = st.selectbox("Pilih ID Barang untuk Diedit", st.session_state.stok_barang["ID"].tolist() + ["Tambah Baru"])
    
        if selected_id != "Tambah Baru":
            barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_id]
            default_values = {
                "Nama Barang": barang_dipilih["Nama Barang"].values[0],
                "Merk": barang_dipilih["Merk"].values[0],
                "Ukuran/Kemasan": barang_dipilih["Ukuran/Kemasan"].values[0],
                "Stok": barang_dipilih["Stok"].values[0],
                "Warna/Base": barang_dipilih["Warna/Base"].values[0] if "Warna/Base" in barang_dipilih.columns else ""
            }
        else:
            default_values = {
                "Nama Barang": "",
                "Merk": "",
                "Ukuran/Kemasan": "",
                "Stok": 0,
                "Warna/Base": ""
            }
    
    else:
        # Untuk tambah barang baru, set default values kosong
        selected_id = "Tambah Baru"
        default_values = {
            "Nama Barang": "",
            "Merk": "",
            "Ukuran/Kemasan": "",
            "Stok": 0,
            "Warna/Base": ""
        }
    
    with st.form("input_barang"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        stok = st.number_input("Stok Barang", min_value=0, value=int(default_values["Stok"]))
        warna_base = st.text_input("Warna/Base", value=default_values["Warna/Base"], placeholder="Opsional")
        submit = st.form_submit_button("Simpan Barang")
    
        if submit:
            # Check if an existing item matches the input values
            match_conditions = (
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Merk"] == merk) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran)
            )
            if "Warna/Base" in st.session_state.stok_barang.columns:
                match_conditions &= (st.session_state.stok_barang["Warna/Base"] == warna_base)
            
            match = st.session_state.stok_barang[match_conditions]
    
            if not match.empty:
                # Update the stock of the existing item
                existing_id = match["ID"].values[0]
                updated_stok = match["Stok"].values[0] + stok
                st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == existing_id, "Stok"] = updated_stok
                st.success(f"Stok barang ID {existing_id} berhasil diperbarui!")
            else:
                # Add new item
                new_id = st.session_state.stok_barang["ID"].max() + 1 if not st.session_state.stok_barang.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Stok": [stok],
                    "Warna/Base": [warna_base],
                    "Waktu Input": [datetime.now()]
                })
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)
                st.success("Barang berhasil ditambahkan!")
    
            save_data()  # Save data after adding or updating item
    
    # Tabel stok barang
    st.subheader("Daftar Stok Barang")
    df_stok_barang = st.session_state.stok_barang.copy()
    
    # Hapus kolom Harga dari tampilan
    if "Harga" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Harga"])
    
    # Pencarian nama barang atau merk
    search_text = st.text_input("Cari Nama Barang atau Merk")
    if search_text:
        df_stok_barang = df_stok_barang[
            (df_stok_barang["Nama Barang"].str.contains(search_text, case=False, na=False)) |
            (df_stok_barang["Merk"].str.contains(search_text, case=False, na=False))
        ]
    
    st.dataframe(df_stok_barang)

    
# Fungsi untuk halaman Penjualan
def halaman_penjualan():
    st.header("Penjualan")

    # Form untuk tambah/edit penjualan
    st.subheader("Tambah/Edit Penjualan")

    # Pilih ID Penjualan untuk diedit
    if not st.session_state.penjualan.empty:
        id_penjualan = st.selectbox("Pilih ID Penjualan untuk Diedit", st.session_state.penjualan["ID"].tolist() + ["Tambah Baru"])

        if id_penjualan != "Tambah Baru":
            penjualan_edit = st.session_state.penjualan[st.session_state.penjualan["ID"] == id_penjualan].iloc[0]
            default_values = {
                "Nama Pelanggan": penjualan_edit["Nama Pelanggan"],
                "Nomor Telepon": penjualan_edit["Nomor Telepon"],
                "Alamat": penjualan_edit["Alamat"],
                "Nama Barang": penjualan_edit["Nama Barang"],
                "Ukuran/Kemasan": penjualan_edit["Ukuran/Kemasan"],
                "Merk": penjualan_edit["Merk"],
                "Kode Warna": penjualan_edit["Kode Warna"] if "Kode Warna" in penjualan_edit.index else "",
                "Jumlah": penjualan_edit["Jumlah"]
            }
        else:
            default_values = {
                "Nama Pelanggan": "",
                "Nomor Telepon": "",
                "Alamat": "",
                "Nama Barang": st.session_state.stok_barang["Nama Barang"].tolist()[0] if not st.session_state.stok_barang.empty else "",
                "Ukuran/Kemasan": st.session_state.stok_barang["Ukuran/Kemasan"].tolist()[0] if not st.session_state.stok_barang.empty else "",
                "Merk": st.session_state.stok_barang["Merk"].tolist()[0] if not st.session_state.stok_barang.empty else "",
                "Kode Warna": "",
                "Jumlah": 1
            }
    else:
        id_penjualan = "Tambah Baru"
        default_values = {
            "Nama Pelanggan": "",
            "Nomor Telepon": "",
            "Alamat": "",
            "Nama Barang": st.session_state.stok_barang["Nama Barang"].tolist()[0] if not st.session_state.stok_barang.empty else "",
            "Ukuran/Kemasan": st.session_state.stok_barang["Ukuran/Kemasan"].tolist()[0] if not st.session_state.stok_barang.empty else "",
            "Merk": st.session_state.stok_barang["Merk"].tolist()[0] if not st.session_state.stok_barang.empty else "",
            "Kode Warna": "",
            "Jumlah": 1
        }

    with st.form("input_penjualan"):
        nama_pelanggan = st.text_input("Nama Pelanggan", value=default_values["Nama Pelanggan"])
        nomor_telpon = st.text_input("Nomor Telepon", value=default_values["Nomor Telepon"])
        alamat = st.text_area("Alamat", value=default_values["Alamat"])
        nama_barang = st.selectbox("Pilih Barang", st.session_state.stok_barang["Nama Barang"], index=st.session_state.stok_barang["Nama Barang"].tolist().index(default_values["Nama Barang"]))
        ukuran = st.selectbox("Ukuran/Kemasan", st.session_state.stok_barang["Ukuran/Kemasan"], index=st.session_state.stok_barang["Ukuran/Kemasan"].tolist().index(default_values["Ukuran/Kemasan"]))
        merk = st.selectbox("Merk", st.session_state.stok_barang["Merk"], index=st.session_state.stok_barang["Merk"].tolist().index(default_values["Merk"]))
        kode_warna = st.text_input("Kode Warna", value=default_values["Kode Warna"], placeholder="Opsional")
        jumlah = st.number_input("Jumlah Orderan", min_value=1, value=int(default_values["Jumlah"]))
        submit = st.form_submit_button("Simpan Penjualan")

        if submit:
            # Mengambil data harga dan persentase keuntungan berdasarkan kombinasi
            stok_barang_filter = st.session_state.stok_barang[
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran) &
                (st.session_state.stok_barang["Merk"] == merk)
            ]
            
            if not stok_barang_filter.empty:
                harga_barang = stok_barang_filter["Harga"].values[0]
                persentase_keuntungan = stok_barang_filter["Persentase Keuntungan"].values[0]
                total_harga = harga_barang * jumlah
                keuntungan = total_harga * (persentase_keuntungan / 100)
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Mendapatkan waktu saat ini
                
                new_penjualan = pd.DataFrame({
                    "ID": [st.session_state.penjualan["ID"].max() + 1 if not st.session_state.penjualan.empty else 1],
                    "Nama Pelanggan": [nama_pelanggan],
                    "Nomor Telepon": [nomor_telpon],
                    "Alamat": [alamat],
                    "Nama Barang": [nama_barang],
                    "Ukuran/Kemasan": [ukuran],
                    "Merk": [merk],
                    "Kode Warna": [kode_warna if "Kode Warna" in st.session_state.stok_barang.columns else ""],
                    "Jumlah": [jumlah],
                    "Total Harga": [total_harga],
                    "Keuntungan": [keuntungan],
                    "Waktu": [waktu]
                })
                
                if id_penjualan == "Tambah Baru":
                    st.session_state.penjualan = pd.concat([st.session_state.penjualan, new_penjualan], ignore_index=True)
                else:
                    st.session_state.penjualan.loc[st.session_state.penjualan["ID"] == id_penjualan, 
                        ["Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", "Kode Warna", "Jumlah", "Total Harga", "Keuntungan", "Waktu"]] = \
                        [nama_pelanggan, nomor_telpon, alamat, nama_barang, ukuran, merk, kode_warna, jumlah, total_harga, keuntungan, waktu]
                
                # Update stok barang
                st.session_state.stok_barang.loc[
                    (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                    (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran) &
                    (st.session_state.stok_barang["Merk"] == merk),
                    "Stok"
                ] -= jumlah
                
                st.success(f"Penjualan untuk {nama_pelanggan} berhasil disimpan!")
                save_data()  # Save data after adding or updating sale
            else:
                st.error("Kombinasi Nama Barang, Ukuran/Kemasan, dan Merk tidak ditemukan di stok.")

    # Tabel stok barang terupdate
    st.subheader("Stok Barang Terupdate")
    df_stok_barang = st.session_state.stok_barang.copy()
    if "Persentase Keuntungan" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Persentase Keuntungan"])  # Menghapus kolom Persentase Keuntungan jika ada
    st.dataframe(df_stok_barang, use_container_width=True, hide_index=False)

    # Tabel penjualan
    st.subheader("Data Penjualan")
    if not st.session_state.penjualan.empty:
        st.session_state.penjualan["Nomor Telepon"] = st.session_state.penjualan["Nomor Telepon"].astype(str)
        st.dataframe(st.session_state.penjualan, use_container_width=True, hide_index=False)

    # Tombol pencarian stok barang
    search_barang = st.text_input("Cari Barang")
    if search_barang:
        hasil_pencarian = st.session_state.stok_barang[st.session_state.stok_barang["Nama Barang"].str.contains(search_barang, case=False)]
        st.write("Hasil Pencarian:")
        if "Persentase Keuntungan" in hasil_pencarian.columns:
            hasil_pencarian = hasil_pencarian.drop(columns=["Persentase Keuntungan"])  # Menghapus kolom Persentase Keuntungan jika ada
        st.dataframe(hasil_pencarian, use_container_width=True, hide_index=False)

    # Pencarian nama pelanggan atau nomor telepon
    search_pelanggan = st.text_input("Cari Nama Pelanggan atau Nomor Telepon")
    if search_pelanggan:
        hasil_pencarian_pelanggan = st.session_state.penjualan[
            (st.session_state.penjualan["Nama Pelanggan"].str.contains(search_pelanggan, case=False)) |
            (st.session_state.penjualan["Nomor Telepon"].str.contains(search_pelanggan, case=False))
        ]
        st.write("Hasil Pencarian:")
        st.dataframe(hasil_pencarian_pelanggan, use_container_width=True, hide_index=False)

    # Dropdown untuk memilih ID penjualan
    if not st.session_state.penjualan.empty:
        id_pilihan = st.selectbox("Pilih ID Penjualan untuk Detail", st.session_state.penjualan["ID"].tolist())
        if id_pilihan:
            penjualan_detail = st.session_state.penjualan[st.session_state.penjualan["ID"] == id_pilihan]
            st.write("Detail Penjualan:")
            st.dataframe(penjualan_detail, use_container_width=True, hide_index=False)

    # Dropdown untuk memilih ID penjualan untuk Download Struk
    if not st.session_state.penjualan.empty:
        id_penjualan = st.selectbox("Pilih ID Penjualan untuk Download Struk", st.session_state.penjualan["ID"].unique())
        
        if st.button("Download Struk Penjualan"):
            selected_sale = st.session_state.penjualan[st.session_state.penjualan["ID"] == id_penjualan].iloc[0]
            struk = StringIO()
            struk.write("=== STRUK PENJUALAN SAKTI UTAMA ===\n")
            struk.write(f"Nama Pelanggan: {selected_sale['Nama Pelanggan']}\n")
            struk.write(f"Nomor Telepon: {selected_sale['Nomor Telepon']}\n")
            struk.write(f"Alamat: {selected_sale['Alamat']}\n")
            struk.write(f"Nama Barang: {selected_sale['Nama Barang']}\n")
            struk.write(f"Ukuran/Kemasan: {selected_sale['Ukuran/Kemasan']}\n")
            struk.write(f"Merk: {selected_sale['Merk']}\n")
            if "Kode Warna" in selected_sale.index:
                struk.write(f"Kode Warna: {selected_sale['Kode Warna']}\n")
            struk.write(f"Jumlah: {selected_sale['Jumlah']}\n")
            struk.write(f"Total Harga: {selected_sale['Total Harga']}\n")
            struk.write(f"Waktu: {selected_sale['Waktu']}\n")
            struk.write("============ TERIMA KASIH ============\n")

            # Menyediakan file untuk di-download
            struk_file = 'struk_pembelian.txt'
            with open(struk_file, 'w') as f:
                f.write(struk.getvalue())
            
            with open(struk_file, 'r') as f:
                st.download_button(label="Download Struk Penjualan", data=f, file_name=struk_file, mime="text/plain")

# Fungsi untuk halaman Supplier
def halaman_supplier():
    st.header("Data Supplier")

    # Memilih ID Supplier untuk diedit atau menambah baru
    supplier_ids = st.session_state.supplier["ID"].tolist()
    supplier_ids.insert(0, "Tambah Baru")  # Opsi untuk menambah data baru
    selected_supplier_id = st.selectbox("Pilih ID Supplier untuk Diedit atau Tambah Baru", supplier_ids)

    # Jika 'Tambah Baru' dipilih, buat default nilai kosong
    if selected_supplier_id == "Tambah Baru":
        selected_supplier = None
        default_values = {
            "Nama Barang": "",
            "Merk": "",
            "Ukuran/Kemasan": "",
            "Jumlah Barang": 0,
            "Nama Supplier": "",
            "Tagihan": 0,
            "Jatuh Tempo": datetime.today()
        }
    else:
        # Ambil data dari supplier berdasarkan ID yang dipilih
        selected_supplier = st.session_state.supplier[st.session_state.supplier["ID"] == selected_supplier_id].iloc[0]
        default_values = {
            "Nama Barang": selected_supplier["Nama Barang"],
            "Merk": selected_supplier["Merk"],
            "Ukuran/Kemasan": selected_supplier["Ukuran/Kemasan"],
            "Jumlah Barang": selected_supplier["Jumlah Barang"],
            "Nama Supplier": selected_supplier["Nama Supplier"],
            "Tagihan": selected_supplier["Tagihan"],
            "Jatuh Tempo": selected_supplier["Jatuh Tempo"]
        }

    # Form input data supplier baru atau edit data supplier
    with st.form("supplier_form"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        jumlah_barang = st.number_input("Jumlah Barang", min_value=0, value=int(default_values["Jumlah Barang"]))
        nama_supplier = st.text_input("Nama Supplier", value=default_values["Nama Supplier"])
        tagihan = st.number_input("Tagihan", min_value=0, value=int(default_values["Tagihan"]))
        jatuh_tempo = st.date_input("Tanggal Jatuh Tempo", value=default_values["Jatuh Tempo"])
        submit = st.form_submit_button("Simpan Data Supplier")
        
        if submit:
            if selected_supplier is None:
                # Tambah data baru
                new_id = st.session_state.supplier["ID"].max() + 1 if not st.session_state.supplier.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Jumlah Barang": [jumlah_barang],
                    "Nama Supplier": [nama_supplier],
                    "Tagihan": [tagihan],
                    "Waktu": [datetime.now()],
                    "Jatuh Tempo": [jatuh_tempo]
                })
                st.session_state.supplier = pd.concat([st.session_state.supplier, new_data], ignore_index=True)
                st.success("Data supplier baru berhasil ditambahkan!")
            else:
                # Update data supplier
                st.session_state.supplier.loc[st.session_state.supplier["ID"] == selected_supplier_id, 
                    ["Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Jatuh Tempo"]] = \
                    [nama_barang, merk, ukuran, jumlah_barang, nama_supplier, tagihan, jatuh_tempo]
                st.success(f"Data supplier ID {selected_supplier_id} berhasil diupdate!")
            
            save_data()  # Simpan data setelah menambah atau mengedit supplier

    # Pencarian berdasarkan Nama Barang atau Merk
    search_input = st.text_input("Cari Nama Barang atau Merk")
    
    if search_input:
        filtered_supplier = st.session_state.supplier[
            (st.session_state.supplier["Nama Barang"].str.contains(search_input, case=False)) |
            (st.session_state.supplier["Merk"].str.contains(search_input, case=False))
        ]
        st.write("Hasil Pencarian:")
        st.dataframe(filtered_supplier)
    else:
        # Tabel data supplier tanpa filter
        st.subheader("Daftar Data Supplier")
        st.dataframe(st.session_state.supplier)



# Fungsi untuk menyimpan semua data ke file Excel
def save_to_excel():
    with pd.ExcelWriter('data_laporan.xlsx', engine='openpyxl') as writer:
        # Simpan stok barang
        st.session_state.stok_barang.to_excel(writer, sheet_name='Stok Barang', index=False)
        
        # Simpan penjualan
        st.session_state.penjualan.to_excel(writer, sheet_name='Penjualan', index=False)
        
        # Simpan supplier
        st.session_state.supplier.to_excel(writer, sheet_name='Supplier', index=False)
        
        # Simpan pengeluaran
        st.session_state.pengeluaran.to_excel(writer, sheet_name='Pengeluaran', index=False)
        
        # Simpan piutang konsumen
        if "piutang_konsumen" in st.session_state:
            st.session_state.piutang_konsumen.to_excel(writer, sheet_name='Piutang Konsumen', index=False)

        # Simpan histori analisis keuangan
        if "historis_analisis_keuangan" in st.session_state:
            st.session_state.historis_analisis_keuangan.to_excel(writer, sheet_name='Histori Analisis Keuangan', index=False)
        
        # Simpan keuntungan bersih
        total_penjualan = st.session_state.penjualan["Total Harga"].sum()
        total_pengeluaran = st.session_state.pengeluaran["Jumlah Pengeluaran"].sum()
        total_keuntungan_bersih = total_penjualan - total_pengeluaran
        df_keuntungan_bersih = pd.DataFrame({
            "Total Penjualan": [total_penjualan],
            "Total Pengeluaran": [total_pengeluaran],
            "Keuntungan Bersih": [total_keuntungan_bersih]
        })
        df_keuntungan_bersih.to_excel(writer, sheet_name='Keuntungan Bersih', index=False)

# Fungsi untuk menyimpan semua data ke file Excel
def save_to_excel():
    with pd.ExcelWriter('data_laporan.xlsx', engine='openpyxl') as writer:
        # Simpan stok barang
        st.session_state.stok_barang.to_excel(writer, sheet_name='Stok Barang', index=False)
        
        # Simpan penjualan
        st.session_state.penjualan.to_excel(writer, sheet_name='Penjualan', index=False)
        
        # Simpan supplier
        st.session_state.supplier.to_excel(writer, sheet_name='Supplier', index=False)
        
        # Simpan pengeluaran
        st.session_state.pengeluaran.to_excel(writer, sheet_name='Pengeluaran', index=False)
        
        # Simpan piutang konsumen
        if "piutang_konsumen" in st.session_state:
            st.session_state.piutang_konsumen.to_excel(writer, sheet_name='Piutang Konsumen', index=False)

        # Simpan histori analisis keuangan
        if "historis_analisis_keuangan" in st.session_state:
            st.session_state.historis_analisis_keuangan.to_excel(writer, sheet_name='Histori Analisis Keuangan', index=False)
        
        # Simpan keuntungan bersih
        total_penjualan = st.session_state.penjualan["Total Harga"].sum()
        total_pengeluaran = st.session_state.pengeluaran["Jumlah Pengeluaran"].sum()
        total_keuntungan_bersih = total_penjualan - total_pengeluaran
        df_keuntungan_bersih = pd.DataFrame({
            "Total Penjualan": [total_penjualan],
            "Total Pengeluaran": [total_pengeluaran],
            "Keuntungan Bersih": [total_keuntungan_bersih]
        })
        df_keuntungan_bersih.to_excel(writer, sheet_name='Keuntungan Bersih', index=False)

# Fungsi untuk halaman Owner dengan pengaman password
def halaman_owner():
    st.header("Halaman Owner - Analisa Keuangan")

    # Login form
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Masukkan Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit and password == "Jayaselalu123":  # Ganti dengan password yang Anda inginkan
                st.session_state.authenticated = True
                st.success("Login berhasil!")
            elif submit:
                st.error("Password salah!")
        return

    # Inisialisasi pengeluaran jika belum ada
    if 'pengeluaran' not in st.session_state:
        st.session_state.pengeluaran = pd.DataFrame(columns=["Jenis Pengeluaran", "Jumlah Pengeluaran", "Keterangan", "Waktu"])

    # Form input barang baru dan edit barang
    st.subheader("Tambah/Edit Barang")
    
    # Tambahkan opsi untuk "Tambah Baru" di selectbox
    barang_ids = st.session_state.stok_barang["ID"].tolist()
    barang_ids.insert(0, "Tambah Baru")  # Opsi untuk menambah barang baru
    selected_row = st.selectbox("Pilih ID Barang untuk Diedit atau Tambah Baru", barang_ids)
    
    # Periksa apakah kolom "Warna/Base" ada di stok barang
    has_warna_base = "Warna/Base" in st.session_state.stok_barang.columns
    
    if selected_row == "Tambah Baru":
        barang_dipilih = None
        default_values = {
            "Nama Barang": "",
            "Merk": "",
            "Ukuran/Kemasan": "",
            "Harga": 0,
            "Stok": 0,
            "Persentase Keuntungan": 0,
            "Warna/Base": "" if has_warna_base else None  # Default value for Warna/Base
        }
    else:
        barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_row]
        default_values = {
            "Nama Barang": barang_dipilih["Nama Barang"].values[0],
            "Merk": barang_dipilih["Merk"].values[0],
            "Ukuran/Kemasan": barang_dipilih["Ukuran/Kemasan"].values[0],
            "Harga": barang_dipilih["Harga"].values[0] if pd.notna(barang_dipilih["Harga"].values[0]) else 0,
            "Stok": barang_dipilih["Stok"].values[0] if pd.notna(barang_dipilih["Stok"].values[0]) else 0,
            "Persentase Keuntungan": barang_dipilih["Persentase Keuntungan"].values[0] if pd.notna(barang_dipilih["Persentase Keuntungan"].values[0]) else 0,
            "Warna/Base": barang_dipilih["Warna/Base"].values[0] if has_warna_base and pd.notna(barang_dipilih["Warna/Base"].values[0]) else ""
        }
    
    with st.form("edit_barang"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        
        harga_beli = st.number_input("Harga Beli", min_value=0, value=int(default_values["Harga"]))  # Harga beli barang
        stok = st.number_input("Stok Barang", min_value=0, value=int(default_values["Stok"]))
        persentase_keuntungan = st.number_input("Persentase Keuntungan (%)", min_value=0, max_value=100, value=int(default_values["Persentase Keuntungan"]))
        
        # Hitung harga jual dan nominal keuntungan
        harga_jual = harga_beli + (harga_beli * (persentase_keuntungan / 100))
        nominal_keuntungan = harga_jual - harga_beli
        
        st.write(f"**Harga Jual**: Rp {harga_jual:,.0f}")  # Tampilkan harga jual
        st.write(f"**Nominal Keuntungan**: Rp {nominal_keuntungan:,.0f}")  # Tampilkan nominal keuntungan
        
        # Jika kolom Warna/Base ada, tambahkan input untuk Warna/Base
        if has_warna_base:
            warna_base = st.text_input("Warna/Base (Opsional)", value=default_values["Warna/Base"])
        else:
            warna_base = None
    
        submit = st.form_submit_button("Simpan Barang")
    
        if submit:
            # Cek apakah ada barang dengan atribut yang sama
            match = st.session_state.stok_barang[
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Merk"] == merk) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran) &
                (st.session_state.stok_barang["Warna/Base"] == warna_base if has_warna_base else True)
            ]
    
            if not match.empty:
                # Update stok barang yang ada
                existing_id = match["ID"].values[0]
                existing_stok = match["Stok"].values[0]
                updated_stok = existing_stok + stok
                
                st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == existing_id, ["Stok"]] = updated_stok
                st.success(f"Stok barang ID {existing_id} berhasil diperbarui!")
            else:
                # Tambah barang baru
                new_id = st.session_state.stok_barang["ID"].max() + 1 if not st.session_state.stok_barang.empty else 1
                new_data = {
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Harga": [harga_beli],  # Harga beli barang
                    "Harga Jual": [harga_jual],  # Harga jual hasil dari kalkulasi
                    "Stok": [stok],
                    "Persentase Keuntungan": [persentase_keuntungan],
                }
    
                if has_warna_base:
                    new_data["Warna/Base"] = [warna_base]
    
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, pd.DataFrame(new_data)], ignore_index=True)
                st.success("Barang baru berhasil ditambahkan!")
    
            save_data()  # Simpan data setelah menambah atau mengedit barang
    
    # Tabel stok barang
    st.subheader("Daftar Stok Barang")
    df_stok_barang = st.session_state.stok_barang.copy()
    
    # Hapus kolom Harga dari tampilan jika ada
    if "Harga" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Harga"])
    
    st.dataframe(df_stok_barang)
    
    # Tombol untuk hapus barang (jika ID bukan 'Tambah Baru')
    if selected_row != "Tambah Baru" and st.button("Hapus Barang"):
        st.session_state.stok_barang = st.session_state.stok_barang[st.session_state.stok_barang["ID"] != selected_row]
        st.success(f"Barang ID {selected_row} berhasil dihapus!")
        save_data()  # Simpan data setelah menghapus barang
    
    # Laporan penjualan
    st.subheader("Laporan Penjualan")
    st.dataframe(st.session_state.penjualan)
    
    # Analisa keuangan dengan grafik pemasaran
    st.subheader("Analisa Keuangan")
    
    # Perhitungan total penjualan
    total_penjualan = st.session_state.penjualan["Total Harga"].sum()
    st.write(f"Total Penjualan: Rp {total_penjualan}")
    
    # Perhitungan tagihan supplier bulanan
    current_month = datetime.now().strftime("%Y-%m")
    st.session_state.supplier['Waktu'] = pd.to_datetime(st.session_state.supplier['Waktu'])
    monthly_supplier_bills = st.session_state.supplier[st.session_state.supplier["Waktu"].dt.strftime("%Y-%m") == current_month]["Tagihan"].sum()
    st.write(f"Total Tagihan Supplier Bulan Ini: Rp {monthly_supplier_bills}")
    
    # Menghitung total penjualan
    total_penjualan = st.session_state.penjualan["Total Harga"].sum()

    # Menghitung total tagihan supplier
    if not st.session_state.supplier.empty:
        monthly_supplier_bills = st.session_state.supplier["Tagihan"].sum()
    else:
        monthly_supplier_bills = 0

    # Menghitung selisih antara total penjualan dan tagihan supplier
    selisih = total_penjualan - monthly_supplier_bills

    # Menampilkan hasil perbandingan
    st.write(f"Total Penjualan: Rp {total_penjualan:,.0f}")
    st.write(f"Total Tagihan Supplier: Rp {monthly_supplier_bills:,.0f}")
    st.write(f"Selisih antara Total Penjualan dan Tagihan Supplier: Rp {selisih:,.0f}")

    # Membuat DataFrame untuk analisis keuangan
    analisis_keuangan_df = pd.DataFrame({
        "Tanggal": [datetime.now().strftime("%Y-%m-%d")],
        "Total Penjualan": [total_penjualan],
        "Total Tagihan Supplier": [monthly_supplier_bills],
        "Selisih": [selisih]
    })

    # Menampilkan tabel analisis keuangan
    st.subheader("Tabel Analisis Keuangan")
    st.dataframe(analisis_keuangan_df)

    # Menyimpan histori analisis keuangan ke file CSV
    if "historis_analisis_keuangan" not in st.session_state:
        st.session_state.historis_analisis_keuangan = pd.DataFrame(columns=["Tanggal", "Total Penjualan", "Total Tagihan Supplier", "Selisih"])

    st.session_state.historis_analisis_keuangan = pd.concat([st.session_state.historis_analisis_keuangan, analisis_keuangan_df], ignore_index=True)

    # Menampilkan tabel data supplier dengan pencarian
    st.subheader("Data Supplier")
    
    search_input = st.text_input("Cari Nama Barang atau Merk")
    
    if search_input:
        filtered_supplier = st.session_state.supplier[
            (st.session_state.supplier["Nama Barang"].str.contains(search_input, case=False)) |
            (st.session_state.supplier["Merk"].str.contains(search_input, case=False))
        ]
        st.write("Hasil Pencarian:")
        st.dataframe(filtered_supplier)
    else:
        st.dataframe(st.session_state.supplier)

        # Inisialisasi piutang konsumen jika belum ada
    if 'piutang_konsumen' not in st.session_state:
        st.session_state.piutang_konsumen = pd.DataFrame(columns=[
            "Nama Konsumen", "Alamat", "Nomor Telepon", "Nama Barang", "Merk", 
            "Kode Warna", "Ukuran/Kemasan", "Jumlah", "Total Tagihan", 
            "Cicilan Tagihan", "Sisa Tagihan", "Janji Bayar"
        ])

    # Form Piutang Konsumen
    st.subheader("Form Piutang Konsumen")

    with st.form("form_piutang"):
        nama_konsumen = st.text_input("Nama Konsumen")
        alamat = st.text_input("Alamat")
        nomor_telepon = st.text_input("Nomor Telepon")
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        kode_warna = st.text_input("Kode Warna (opsional)")
        ukuran = st.text_input("Ukuran/Kemasan")
        jumlah = st.number_input("Jumlah", min_value=1)
        total_tagihan = st.number_input("Total Tagihan", min_value=0)
        cicilan_tagihan = st.number_input("Cicilan Tagihan (opsional)", min_value=0, value=0)
        janji_bayar = st.date_input("Janji Bayar")

        # Menghitung Sisa Tagihan
        sisa_tagihan = total_tagihan - cicilan_tagihan

        # Tombol submit untuk menambahkan atau mengedit data piutang
        submit_piutang = st.form_submit_button("Tambah/Edit Piutang")

        if submit_piutang:
            new_piutang = {
                "Nama Konsumen": nama_konsumen,
                "Alamat": alamat,
                "Nomor Telepon": nomor_telepon,
                "Nama Barang": nama_barang,
                "Merk": merk,
                "Kode Warna": kode_warna if kode_warna else "",
                "Ukuran/Kemasan": ukuran,
                "Jumlah": jumlah,
                "Total Tagihan": total_tagihan,
                "Cicilan Tagihan": cicilan_tagihan if cicilan_tagihan else 0,
                "Sisa Tagihan": sisa_tagihan,
                "Janji Bayar": janji_bayar
            }

            # Tambah data piutang ke session state
            st.session_state.piutang_konsumen = st.session_state.piutang_konsumen.append(new_piutang, ignore_index=True)
            st.success("Piutang konsumen berhasil ditambahkan!")
            save_data()  # Panggil fungsi untuk menyimpan data

    # Tabel Piutang Konsumen
    st.subheader("Tabel Piutang Konsumen")

    # Tampilkan tabel piutang dengan fitur edit dan hapus
    if not st.session_state.piutang_konsumen.empty:
        st.dataframe(st.session_state.piutang_konsumen)

        # Pilih piutang yang akan diedit
        selected_row = st.selectbox("Pilih Nama Konsumen untuk Diedit", st.session_state.piutang_konsumen["Nama Konsumen"])

        piutang_dipilih = st.session_state.piutang_konsumen[st.session_state.piutang_konsumen["Nama Konsumen"] == selected_row]

        # Form untuk edit piutang konsumen
        with st.form("edit_piutang"):
            nama_konsumen_edit = st.text_input("Nama Konsumen", value=piutang_dipilih["Nama Konsumen"].values[0])
            alamat_edit = st.text_input("Alamat", value=piutang_dipilih["Alamat"].values[0])
            nomor_telepon_edit = st.text_input("Nomor Telepon", value=piutang_dipilih["Nomor Telepon"].values[0])
            nama_barang_edit = st.text_input("Nama Barang", value=piutang_dipilih["Nama Barang"].values[0])
            merk_edit = st.text_input("Merk", value=piutang_dipilih["Merk"].values[0])
            kode_warna_edit = st.text_input("Kode Warna (opsional)", value=piutang_dipilih["Kode Warna"].values[0])
            ukuran_edit = st.text_input("Ukuran/Kemasan", value=piutang_dipilih["Ukuran/Kemasan"].values[0])
            jumlah_edit = st.number_input("Jumlah", min_value=1, value=int(piutang_dipilih["Jumlah"].values[0]))
            total_tagihan_edit = st.number_input("Total Tagihan", min_value=0, value=int(piutang_dipilih["Total Tagihan"].values[0]))
            cicilan_tagihan_edit = st.number_input("Cicilan Tagihan (opsional)", min_value=0, value=int(piutang_dipilih["Cicilan Tagihan"].values[0]))
            janji_bayar_edit = st.date_input("Janji Bayar", value=pd.to_datetime(piutang_dipilih["Janji Bayar"].values[0]))

            sisa_tagihan_edit = total_tagihan_edit - cicilan_tagihan_edit

            submit_edit_piutang = st.form_submit_button("Update Piutang")

            if submit_edit_piutang:
                st.session_state.piutang_konsumen.loc[st.session_state.piutang_konsumen["Nama Konsumen"] == selected_row, [
                    "Nama Konsumen", "Alamat", "Nomor Telepon", "Nama Barang", "Merk", 
                    "Kode Warna", "Ukuran/Kemasan", "Jumlah", "Total Tagihan", 
                    "Cicilan Tagihan", "Sisa Tagihan", "Janji Bayar"
                ]] = [nama_konsumen_edit, alamat_edit, nomor_telepon_edit, nama_barang_edit, merk_edit, 
                      kode_warna_edit, ukuran_edit, jumlah_edit, total_tagihan_edit, cicilan_tagihan_edit, 
                      sisa_tagihan_edit, janji_bayar_edit]
                st.success("Piutang konsumen berhasil diupdate!")
                save_data()  # Simpan perubahan data

        # Tombol hapus piutang
        if st.button("Hapus Piutang"):
            st.session_state.piutang_konsumen = st.session_state.piutang_konsumen[st.session_state.piutang_konsumen["Nama Konsumen"] != selected_row]
            st.success("Piutang konsumen berhasil dihapus!")
            save_data()  # Simpan setelah hapus
    else:
        st.write("Tidak ada data piutang konsumen.")

    # Menampilkan histori analisis keuangan
    st.subheader("Histori Analisis Keuangan")
    st.dataframe(st.session_state.historis_analisis_keuangan)

    # Tombol untuk mendownload histori analisis keuangan
    if st.button("Download Histori Analisis Keuangan (CSV)"):
        csv = st.session_state.historis_analisis_keuangan.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="histori_analisis_keuangan.csv", mime="text/csv")

    
    # Grafik keuntungan penjualan per barang
    if not st.session_state.penjualan.empty and "Keuntungan" in st.session_state.penjualan.columns:
        st.subheader("Grafik Pemasaran")

        # Grouping the data by "Nama Barang" and summing up the "Keuntungan"
        keuntungan_per_barang = st.session_state.penjualan.groupby("Nama Barang")["Keuntungan"].sum()

        # Plotting the bar chart
        plt.figure(figsize=(10, 6))
        keuntungan_per_barang.sort_values(ascending=False).plot(kind="bar", color="skyblue")
        
        # Adding titles and labels
        plt.title("Keuntungan per Barang", fontsize=14)
        plt.xlabel("Nama Barang", fontsize=12)
        plt.ylabel("Total Keuntungan (Rp)", fontsize=12)
        plt.xticks(rotation=45, ha="right", fontsize=10)

        # Display the plot in Streamlit
        st.pyplot(plt)

    else:
        st.write("Data penjualan kosong atau kolom 'Keuntungan' tidak ditemukan.")
    
    # Simulasi data untuk pengeluaran
    if 'pengeluaran' not in st.session_state:
        st.session_state.pengeluaran = pd.DataFrame(columns=[
            "Jenis Pengeluaran", "Jumlah Pengeluaran", "Keterangan", "Waktu"
        ])

    if 'historis_pengeluaran' not in st.session_state:
        st.session_state.historis_pengeluaran = pd.DataFrame(columns=[
            "Jenis Pengeluaran", "Jumlah Pengeluaran", "Keterangan", "Waktu"
        ])

    # Menampilkan tabel pengeluaran
    st.dataframe(st.session_state.pengeluaran)

    # Form untuk menambah pengeluaran
    with st.form("tambah_pengeluaran"):
        st.write("Tambah Pengeluaran Baru")
        jenis_pengeluaran = st.selectbox("Jenis Pengeluaran", ["Biaya Gaji", "Biaya Operasional", "Biaya Lainnya"])
        jumlah_pengeluaran = st.number_input("Jumlah Pengeluaran (Rp)", min_value=0)
        keterangan_pengeluaran = st.text_input("Keterangan Pengeluaran")
        submit_pengeluaran = st.form_submit_button("Tambah Pengeluaran")

        if submit_pengeluaran:
            new_data = pd.DataFrame({
                "Jenis Pengeluaran": [jenis_pengeluaran],
                "Jumlah Pengeluaran": [jumlah_pengeluaran],
                "Keterangan": [keterangan_pengeluaran],
                "Waktu": [datetime.now()]
            })
            st.session_state.pengeluaran = pd.concat([st.session_state.pengeluaran, new_data], ignore_index=True)
            st.success("Pengeluaran berhasil ditambahkan!")
            save_data()  # Simpan data setelah penambahan pengeluaran

    # Menyaring data pengeluaran berdasarkan bulan yang sama
    current_month = datetime.now().strftime('%Y-%m')
    st.session_state.pengeluaran['Bulan'] = st.session_state.pengeluaran['Waktu'].dt.strftime('%Y-%m')
    historis_bulan_ini = st.session_state.pengeluaran[st.session_state.pengeluaran['Bulan'] == current_month]

    # Tabel historis pengeluaran
    st.subheader("Historis Pengeluaran Bulan Ini")
    st.dataframe(historis_bulan_ini[['Jenis Pengeluaran', 'Jumlah Pengeluaran', 'Keterangan', 'Waktu']])

    # Tabel historis pengeluaran keseluruhan
    st.subheader("Historis Pengeluaran Keseluruhan")
    st.dataframe(st.session_state.pengeluaran[['Jenis Pengeluaran', 'Jumlah Pengeluaran', 'Keterangan', 'Waktu']])

    # Analisa Keuangan - Total Keuntungan Bersih
    st.subheader("Analisa Keuangan - Total Keuntungan Bersih")

    # Perhitungan total pengeluaran
    total_pengeluaran = st.session_state.pengeluaran["Jumlah Pengeluaran"].sum()
    st.write(f"Total Pengeluaran: Rp {total_pengeluaran}")

    # Perhitungan total keuntungan dari penjualan
    total_keuntungan = st.session_state.penjualan["Keuntungan"].sum()
    st.write(f"Total Keuntungan Penjualan: Rp {total_keuntungan}")

    # Tabel analisis keuntungan per barang
    st.subheader("Analisis Keuntungan Per Barang")
    if not st.session_state.penjualan.empty:
        analisis_keuntungan = st.session_state.penjualan.groupby(
            ["Nama Barang", "Ukuran/Kemasan", "Merk", "Waktu"]
        ).agg({
            "Keuntungan": "sum",
            "Jumlah": "sum"
        }).reset_index()
        st.dataframe(analisis_keuntungan)

    # Perhitungan total keuntungan bersih
    total_keuntungan_bersih = total_keuntungan - total_pengeluaran
    st.write(f"Total Keuntungan Bersih: Rp {total_keuntungan_bersih:,.0f}")

    # Tambah data historis keuntungan bersih
    new_historis = pd.DataFrame({
        "Waktu": [datetime.now()],
        "Keuntungan Bersih": [total_keuntungan_bersih]
    })
    
    # Cek apakah data historis sudah ada
    if 'historis_keuntungan_bersih' not in st.session_state:
        st.session_state.historis_keuntungan_bersih = pd.DataFrame(columns=["Waktu", "Keuntungan Bersih"])

    # Menambahkan data historis
    st.session_state.historis_keuntungan_bersih = pd.concat([st.session_state.historis_keuntungan_bersih, new_historis], ignore_index=True)
    
    # Menyaring data historis berdasarkan bulan yang sama
    current_month = datetime.now().strftime('%Y-%m')
    st.session_state.historis_keuntungan_bersih['Bulan'] = st.session_state.historis_keuntungan_bersih['Waktu'].dt.strftime('%Y-%m')
    
    # Mengelompokkan berdasarkan bulan dan mendapatkan total keuntungan bersih
    historis_bulan_ini = st.session_state.historis_keuntungan_bersih[st.session_state.historis_keuntungan_bersih['Bulan'] == current_month]
    
    if not historis_bulan_ini.empty:
        # Mengelompokkan berdasarkan bulan dan menghitung total keuntungan bersih
        total_keuntungan_bersih_bulan_ini = historis_bulan_ini['Keuntungan Bersih'].sum()
        
        # Mengambil data tanggal terbaru di bulan yang sama
        data_bulan_ini = {
            "Waktu": [historis_bulan_ini['Waktu'].max()],
            "Keuntungan Bersih": [total_keuntungan_bersih_bulan_ini]
        }
        historis_bulan_ini = pd.DataFrame(data_bulan_ini)
    else:
        # Menampilkan tabel kosong jika tidak ada data untuk bulan ini
        historis_bulan_ini = pd.DataFrame(columns=["Waktu", "Keuntungan Bersih"])
    
    # Tabel historis keuntungan bersih
    st.subheader("Historis Keuntungan Bersih")
    st.dataframe(historis_bulan_ini[['Waktu', 'Keuntungan Bersih']])
    
    # Tabel ringkasan keuangan
    st.subheader("Ringkasan Keuangan")
    data_ringkasan = pd.DataFrame({
        "Keterangan": ["Total Penjualan", "Total Pengeluaran", "Total Keuntungan Bersih"],
        "Jumlah (Rp)": [
            f"Rp {total_keuntungan:,.0f}",
            f"Rp {total_pengeluaran:,.0f}",
            f"Rp {total_keuntungan_bersih:,.0f}"
        ]
    })
    st.table(data_ringkasan)
    
    # Tombol untuk mendownload semua data ke file Excel
    if st.button("Download Semua Data (Excel)"):
        save_to_excel()
        with open("data_laporan.xlsx", "rb") as file:
            st.download_button(
                label="Download Excel",
                data=file,
                file_name="data_laporan.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            
# Menampilkan halaman berdasarkan menu yang dipilih
if menu == "Stock Barang":
    halaman_stock_barang()
elif menu == "Penjualan":
    halaman_penjualan()
elif menu == "Supplier":
    halaman_supplier()
elif menu == "Owner":
    halaman_owner()

st.markdown('</div>', unsafe_allow_html=True)

# Save data when the app is closed or the menu is changed
save_data()
