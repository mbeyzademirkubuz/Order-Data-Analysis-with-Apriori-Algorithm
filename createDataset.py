import json
from datetime import datetime, timedelta
import random

# JSON dosyasını yükleyin
with open('C:/Users/beyza/Downloads/orders.json', 'r', encoding='utf-8') as file:
    siparisler = json.load(file)

# Rastgele tarih oluşturma fonksiyonu
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# Başlangıç ve bitiş tarihlerini tanımlayın
start_date = datetime.strptime('15/04/2024', '%d/%m/%Y')
end_date = datetime.strptime('15/05/2024', '%d/%m/%Y')

# Her siparişe rastgele bir tarih ve quantity değeri ekleyin ve total_price güncelleyin
for siparis in siparisler:
    siparis['date'] = random_date(start_date, end_date).strftime('%d/%m/%Y')
    total_price = 0  # Toplam fiyatı sıfırla
    for urun in siparis['items']:
        urun['quantity'] = random.randint(1, 10)
        total_price += urun['quantity'] * urun['price']  # Her ürünün fiyatını hesapla ve toplam fiyata ekle
    siparis['total_price'] = total_price  # Güncellenmiş toplam fiyatı siparişe ekle

# Güncellenmiş JSON dosyasını kaydedin
with open('Orders.json', 'w', encoding='utf-8') as file:
    json.dump(siparisler, file, ensure_ascii=False, indent=4)

print("Siparişlere tarih, quantity ve güncellenmiş total_price ekleme işlemi tamamlandı.")
