import os
import gradio as gr


def hitung_penjualan(nama_barang, jumlah_barang, barang_terjual, harga_beli, harga_jual):
    """Menghitung omzet, sisa stok, laba sederhana, dan modal tertahan."""

    # Validasi input angka
    jumlah_barang = 0 if jumlah_barang is None else jumlah_barang
    barang_terjual = 0 if barang_terjual is None else barang_terjual
    harga_beli = 0 if harga_beli is None else harga_beli
    harga_jual = 0 if harga_jual is None else harga_jual

    if jumlah_barang < 0 or barang_terjual < 0 or harga_beli < 0 or harga_jual < 0:
        return "⚠️ Error: Angka tidak boleh negatif.", "-", "-", "-"

    if barang_terjual > jumlah_barang:
        return "⚠️ Error: Terjual melebihi stok!", "-", "-", "-"

    sisa_barang = jumlah_barang - barang_terjual
    omset = barang_terjual * harga_jual
    modal_terjual = barang_terjual * harga_beli
    laba_bersih = omset - modal_terjual
    modal_tertahan = sisa_barang * harga_beli

    # Format angka sebagai rupiah tanpa angka desimal
    str_omset = f"Rp {omset:,.0f}".replace(",", ".")
    str_sisa = f"{sisa_barang:,.0f} Unit".replace(",", ".")
    str_laba = f"Rp {laba_bersih:,.0f}".replace(",", ".")
    str_modal = f"Rp {modal_tertahan:,.0f}".replace(",", ".")

    return str_omset, str_sisa, str_laba, str_modal


# Lokasi logo mengikuti folder tempat app.py berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")

with gr.Blocks(theme=gr.themes.Soft(), title="Sistem Penjualan UMKM") as app:

    # Bagian logo dan judul
    with gr.Row():
        if os.path.exists(LOGO_PATH):
            gr.Image(
                value=LOGO_PATH,
                show_label=False,
                container=False,
                width=120,
                height=120,
                interactive=False,
            )
        with gr.Column():
            gr.Markdown("# 📊 Kalkulator Penjualan UMKM")
            gr.Markdown(
                "Kelola penjualan, hitung omzet, dan pantau untung rugi dengan mudah."
            )

    gr.Markdown("---")

    # Bagian input dan output
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📝 Input Data Barang")
            in_nama = gr.Textbox(
                label="Nama Barang",
                placeholder="Contoh: Keripik Pisang",
            )
            in_stok = gr.Number(label="Jumlah Barang (Stok Awal)", value=0)
            in_terjual = gr.Number(label="Barang Terjual", value=0)

            with gr.Row():
                in_hbeli = gr.Number(label="Harga Modal per Unit (Rp)", value=0)
                in_hjual = gr.Number(label="Harga Jual per Unit (Rp)", value=0)

            btn_hitung = gr.Button("🚀 Hitung Penjualan", variant="primary")

        with gr.Column():
            gr.Markdown("### 📈 Laporan Keuangan")
            out_omset = gr.Textbox(label="Total Omzet", interactive=False)
            out_sisa = gr.Textbox(label="Sisa Stok", interactive=False)
            out_laba = gr.Textbox(label="Laba Bersih", interactive=False)
            out_modal = gr.Textbox(
                label="Modal Tertahan (Nilai Modal Stok Tersisa)",
                interactive=False,
            )

    btn_hitung.click(
        fn=hitung_penjualan,
        inputs=[in_nama, in_stok, in_terjual, in_hbeli, in_hjual],
        outputs=[out_omset, out_sisa, out_laba, out_modal],
    )


if __name__ == "__main__":
    # Render menyediakan PORT melalui environment variable.
    port = int(os.environ.get("PORT", 7860))
    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        show_error=True,
        favicon_path=LOGO_PATH if os.path.exists(LOGO_PATH) else None,
    )
