import random
import datetime
from PIL import Image, ImageDraw, ImageFont
from faker import Faker
import os

# Inisialisasi Faker untuk menghasilkan data palsu
fake = Faker('id_ID')

# Fungsi untuk menghasilkan nama toko acak
def generate_store_name():
    # Menggunakan kombinasi kata untuk menghasilkan nama toko acak
    adjectives = ["Mega", "Sumber", "Bintang", "Berkah", "Dharma", "Taman", "Sejahtera", "Murah", "Bersama", "ASC", "Sultan", "Zamza", "Airdrop Sultan"]
    nouns = ["Mart", "Toserba", "Supermarket", "Belanja", "Food", "Sumber", "Toko", "Sayur", "Susu"]
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

# Daftar produk acak dengan harga
products = [
    {"name": "Beras 5kg", "price_range": (70000, 80000)},
    {"name": "Minyak Goreng 2L", "price_range": (25000, 30000)},
    {"name": "Gula Pasir 1kg", "price_range": (12000, 15000)},
    {"name": "Telur Ayam 1kg", "price_range": (25000, 30000)},
    {"name": "Indomie Goreng", "price_range": (2000, 3000)},
    {"name": "Tepung Terigu 1kg", "price_range": (10000, 15000)},
    {"name": "Kopi Sachet", "price_range": (1000, 2000)},
    {"name": "Teh Botol Sosro", "price_range": (4000, 6000)},
    {"name": "Sabun Mandi 100gr", "price_range": (2500, 3500)},
    {"name": "Susu UHT 1L", "price_range": (12000, 18000)},
    {"name": "Pasta Gigi 150gr", "price_range": (15000, 20000)},
    {"name": "Rokok Marlboro", "price_range": (25000, 35000)},
    {"name": "Sampo Sachet", "price_range": (800, 1500)},
    {"name": "Kecap Manis 500ml", "price_range": (15000, 20000)},
    {"name": "Sarden Kaleng", "price_range": (12000, 18000)},
    {"name": "Mie Sedap", "price_range": (2000, 3000)},
    {"name": "Coca Cola 330ml", "price_range": (7000, 9000)},
    {"name": "Obat Flu", "price_range": (10000, 20000)},
    {"name": "Biskuit", "price_range": (5000, 10000)},
    {"name": "Permen", "price_range": (2000, 5000)}
]

# Fungsi untuk memilih harga acak berdasarkan rentang harga
def get_random_price(price_range):
    return random.randint(price_range[0], price_range[1])

# Fungsi untuk generate struk belanja acak dan simpan sebagai gambar
def generate_receipt_image(receipt_number=1, folder_name='struk'):
    # Membuat folder jika belum ada
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for n in range(1, receipt_number + 1):
        # Pilih toko acak
        store_name = generate_store_name()
        store_address = fake.address().replace("\n", ", ")
        store_phone = fake.phone_number()

        # Tanggal dan waktu pembelian
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Jumlah item belanjaan
        item_count = random.randint(5, 15)  # antara 5 hingga 15 item

        # Pilih item secara acak (boleh ada duplikasi untuk merepresentasikan beberapa jenis barang)
        purchased_items = [random.choice(products) for _ in range(item_count)]

        # Hitung jumlah setiap item yang dibeli
        cart = {}
        for item in purchased_items:
            if item['name'] in cart:
                cart[item['name']]['quantity'] += 1
            else:
                cart[item['name']] = {
                    'price': get_random_price(item['price_range']),
                    'quantity': 1
                }

        # Hitung subtotal
        subtotal = sum(details['price'] * details['quantity'] for details in cart.values())

        # Terapkan diskon acak (jika ada)
        discount = random.choice([0, 0.05, 0.1, 0.15])  # Diskon 0%, 5%, 10%, atau 15%
        discount_amount = subtotal * discount
        total = subtotal - discount_amount

        # Menghitung jumlah baris yang diperlukan
        base_height = 150  # Tinggi dasar untuk header, footer, dan elemen lainnya
        per_item_height = 20  # Tinggi per item
        extra_height = 100  # Buffer tambahan
        img_height = base_height + len(cart) * per_item_height + extra_height

        # Membuat gambar struk dengan lebar lebih kecil
        img_width = 300  # Lebar lebih ramping
        img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
        d = ImageDraw.Draw(img)

        # Font
        try:
            # Coba menggunakan font yang lebih baik jika tersedia
            font_path = "raial.ttf"  # Ganti dengan path font yang sesuai jika diperlukan
            header_font = ImageFont.truetype(font_path, 18)
            regular_font = ImageFont.truetype(font_path, 12)
            bold_font = ImageFont.truetype(font_path, 14)
        except IOError:
            # Gunakan font default jika tidak menemukan font yang ditentukan
            header_font = ImageFont.load_default()
            regular_font = ImageFont.load_default()
            bold_font = ImageFont.load_default()

        # Header struk (Toko)
        y_position = 10
        # Menghitung bounding box teks untuk menentukan lebar teks
        bbox = d.textbbox((0, 0), store_name, font=bold_font)
        text_width = bbox[2] - bbox[0]
        d.text(((img_width - text_width) // 2, y_position), store_name, font=bold_font, fill=(0, 0, 0))
        y_position += 25
        
        # Alamat dan telepon
        for line in [store_address, f"Telp: {store_phone}"]:
            # Membungkus teks jika terlalu panjang
            wrapped_lines = wrap_text(line, regular_font, img_width - 20)
            for wrapped_line in wrapped_lines:
                d.text((10, y_position), wrapped_line, font=regular_font, fill=(0, 0, 0))
                y_position += 15

        # Tanggal dan Waktu
        d.text((10, y_position), f"Date/Time: {date_time}", font=regular_font, fill=(0, 0, 0))
        y_position += 20

        # Garis pembatas
        d.line([(10, y_position), (img_width - 10, y_position)], fill=(0, 0, 0), width=1)
        y_position += 10

        # Header tabel item
        d.text((10, y_position), "Item", font=bold_font, fill=(0, 0, 0))
        d.text((180, y_position), "Qty", font=bold_font, fill=(0, 0, 0))
        d.text((220, y_position), "Price", font=bold_font, fill=(0, 0, 0))
        y_position += 15

        # Garis pembatas
        d.line([(10, y_position), (img_width - 10, y_position)], fill=(0, 0, 0), width=1)
        y_position += 10

        # Daftar item belanja
        for item_name, details in cart.items():
            # Pastikan nama item tidak terlalu panjang
            display_name = (item_name[:15] + '..') if len(item_name) > 15 else item_name
            d.text((10, y_position), display_name, font=regular_font, fill=(0, 0, 0))  # Item
            d.text((180, y_position), str(details['quantity']), font=regular_font, fill=(0, 0, 0))  # Quantity
            d.text((220, y_position), f"Rp{details['price']:,}", font=regular_font, fill=(0, 0, 0))  # Price
            y_position += 20

        # Garis pembatas
        d.line([(10, y_position), (img_width - 10, y_position)], fill=(0, 0, 0), width=1)
        y_position += 10

        # Subtotal
        d.text((180, y_position), "Subtotal:", font=bold_font, fill=(0, 0, 0))
        d.text((230, y_position), f"Rp{subtotal:,.0f}", font=bold_font, fill=(0, 0, 0))
        y_position += 15

        # Diskon
        if discount > 0:
            d.text((180, y_position), "Diskon:", font=bold_font, fill=(0, 0, 0))
            d.text((230, y_position), f"Rp{discount_amount:,.0f}", font=bold_font, fill=(255, 0, 0))  # Diskon dalam warna merah
            y_position += 15

        # Total
        d.text((180, y_position), "Total:", font=bold_font, fill=(0, 0, 0))
        d.text((230, y_position), f"Rp{total:,.0f}", font=bold_font, fill=(0, 0, 0))
        y_position += 20

        # Ucapan Terima Kasih
        thank_you_message = "Channel : https://t.me/airdropasc"
        bbox = d.textbbox((0, 0), thank_you_message, font=bold_font)
        text_width = bbox[2] - bbox[0]
        d.text(((img_width - text_width) // 2, y_position), thank_you_message, font=bold_font, fill=(0, 0, 0))
        y_position += 40  # Menambah jarak setelah ucapan terima kasih

        # Simpan gambar struk belanja ke folder yang ditentukan
        img.save(os.path.join(folder_name, f"bb_ASC_{n}.png"))
        print(f"Struk belanja {n} telah dihasilkan sebagai '{folder_name}/bb_ASC_{n}.png'.")

# Fungsi untuk membungkus teks jika terlalu panjang
def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        # Coba tambahkan kata ke baris saat ini
        test_line = f"{current_line} {word}".strip()
        if font.getbbox(test_line)[2] <= max_width:
            current_line = test_line
        else:
            # Jika panjangnya melebihi batas, simpan baris saat ini dan mulai baris baru
            lines.append(current_line)
            current_line = word
    # Tambahkan baris terakhir yang tersisa
    lines.append(current_line)
    return lines

# Fungsi utama
def main():
    try:
        jumlah_struk = int(input("Masukkan jumlah struk yang ingin dibuat: "))
        generate_receipt_image(jumlah_struk)
    except ValueError:
        print("Tolong masukkan angka yang valid.")

if __name__ == "__main__":
    main()
