import streamlit as st
import heapq
from collections import defaultdict

# =========================
# Kelas Node Huffman
# =========================
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# =========================
# Fungsi Huffman
# =========================
def hitung_frekuensi(teks):
    frekuensi = defaultdict(int)
    for c in teks:
        frekuensi[c] += 1
    return frekuensi

def buat_pohon(frekuensi):
    heap = [Node(c, f) for c, f in frekuensi.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        kiri = heapq.heappop(heap)
        kanan = heapq.heappop(heap)
        gabung = Node(None, kiri.freq + kanan.freq)
        gabung.left = kiri
        gabung.right = kanan
        heapq.heappush(heap, gabung)
    return heap[0]

def buat_kode(node, kode="", tabel={}):
    if node:
        if node.char is not None:
            tabel[node.char] = kode
        buat_kode(node.left, kode + "0", tabel)
        buat_kode(node.right, kode + "1", tabel)
    return tabel

def encoding(teks, kode_huffman):
    return ''.join(kode_huffman[c] for c in teks)

def decoding(encoded, root):
    hasil = ""
    node = root
    for bit in encoded:
        node = node.left if bit == '0' else node.right
        if node.char:
            hasil += node.char
            node = root
    return hasil

# =========================
# Streamlit App
# =========================
st.set_page_config(page_title="Kompresi Huffman Teks Berita", layout="centered")
st.title("🔍 Kompresi Teks Berita dengan Huffman Coding")

uploaded_file = st.file_uploader("📄 Upload File Teks Berita (.txt)", type=["txt"])

if uploaded_file:
    teks = uploaded_file.read().decode("utf-8")
    st.subheader("📜 Isi Teks Asli")
    st.text(teks)

    # Proses kompresi
    freq = hitung_frekuensi(teks)
    root = buat_pohon(freq)
    kode_huffman = buat_kode(root)
    hasil_encoded = encoding(teks, kode_huffman)
    hasil_decoded = decoding(hasil_encoded, root)

    st.subheader("📉 Tabel Kode Huffman")
    st.table([{ "Karakter": repr(k), "Kode": v } for k, v in kode_huffman.items()])

    st.subheader("🧾 Hasil Kompresi (Binary)")
    st.text_area("Output Biner", hasil_encoded, height=200)

    st.subheader("📊 Perbandingan Ukuran")
    before = len(teks) * 8
    after = len(hasil_encoded)
    st.markdown(f"- Ukuran asli: **{before} bit**")
    st.markdown(f"- Ukuran terkompresi: **{after} bit**")
    st.markdown(f"- Efisiensi: **{100 - (after/before)*100:.2f}%** pengurangan")

    st.subheader("✅ Validasi Dekompresi")
    if hasil_decoded == teks:
        st.success("Hasil dekompresi sama persis dengan input asli!")
    else:
        st.error("Dekompresi tidak sama. Ada kesalahan.")

    # =========================
    # Fitur Download
    # =========================
    st.subheader("⬇️ Download File")

    st.download_button(
        label="📥 Download Hasil Kompresi",
        data=hasil_encoded,
        file_name="berita_terkompresi.bin.txt",
        mime="text/plain"
    )

    st.download_button(
        label="📥 Download Hasil Dekompresi",
        data=hasil_decoded,
        file_name="berita_dekompresi.txt",
        mime="text/plain"
    )
