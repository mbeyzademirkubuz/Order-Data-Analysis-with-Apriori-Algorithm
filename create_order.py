import json
import random
import uuid


import json

# Orijinal veriyi düzeltilmiş JSON formatına dönüştürme
data = [
    {
        "id": "1",
        "name": "Pizza Pepperoni",
        "cookTime": "10-20",
        "price": 10,
        "favorite": False,
        "origins": ["italy"],
        "stars": 4.5,
        "imageUrl": "food-1.jpg",
        "tags": ["FastFood", "Pizza", "Lunch"]
    },
    {
        "id": "2",
        "name": "Meatball",
        "price": 20,
        "cookTime": "20-30",
        "favorite": True,
        "origins": ["persia", "middle east", "china"],
        "stars": 5,
        "imageUrl": "food-2.jpg",
        "tags": ["SlowFood", "Lunch"]
    },
    {
        "id": "3",
        "name": "Hamburger",
        "price": 5,
        "cookTime": "10-15",
        "favorite": False,
        "origins": ["germany", "us"],
        "stars": 3.5,
        "imageUrl": "food-3.jpg",
        "tags": ["FastFood", "Hamburger"]
    },
    {
        "id": "4",
        "name": "Fried Potatoes",
        "price": 2,
        "cookTime": "15-20",
        "favorite": True,
        "origins": ["belgium", "france"],
        "stars": 3,
        "imageUrl": "food-4.jpg",
        "tags": ["FastFood", "Fry"]
    },
    {
        "id": "5",
        "name": "Chicken Soup",
        "price": 11,
        "cookTime": "40-50",
        "favorite": False,
        "origins": ["india", "asia"],
        "stars": 3.5,
        "imageUrl": "food-5.jpg",
        "tags": ["SlowFood", "Soup"]
    },
    {
        "id": "6",
        "name": "Vegetables Pizza",
        "price": 9,
        "cookTime": "40-50",
        "favorite": False,
        "origins": ["italy"],
        "stars": 4.0,
        "imageUrl": "food-6.jpg",
        "tags": ["FastFood", "Pizza", "Lunch"]
    },
    {
        "id": "1008",
        "name": "Carbonara",
        "cookTime": "20-30",
        "price": 19.00,
        "favorite": False,
        "origins": ["italy"],
        "stars": 4.2,
        "imageUrl": "food-1008.jpg",
        "tags": ["SlowFood", "Pasta", "Dinner"]
    },
    {
        "id": "1009",
        "name": "Fettuccine Alfredo",
        "cookTime": "20-30",
        "price": 21.00,
        "favorite": True,
        "origins": ["italy"],
        "stars": 4.3,
        "imageUrl": "food-1009.jpg",
        "tags": ["SlowFood", "Pasta", "Dinner"]
    },
    {
        "id": "1010",
        "name": "Chicken Parmesan",
        "cookTime": "25-35",
        "price": 23.00,
        "favorite": True,
        "origins": ["italy"],
        "stars": 4.5,
        "imageUrl": "food-1010.jpg",
        "tags": ["SlowFood", "Chicken", "Dinner"]
    },
    {
        "id": "1011",
        "name": "Caesar Salad",
        "cookTime": "10-15",
        "price": 15.00,
        "favorite": False,
        "origins": ["italy"],
        "stars": 4.0,
        "imageUrl": "food-1011.jpg",
        "tags": ["Appetizer", "Salad", "Lunch"]
    },
    {
        "id": "1012",
        "name": "Cheeseburger",
        "cookTime": "10-15",
        "price": 18.00,
        "favorite": True,
        "origins": ["us"],
        "stars": 4.3,
        "imageUrl": "food-1012.jpg",
        "tags": ["FastFood", "Burger", "Lunch"]
    },
    {
        "id": "1013",
        "name": "Veggie Burger",
        "cookTime": "10-15",
        "price": 17.00,
        "favorite": False,
        "origins": ["us"],
        "stars": 4.1,
        "imageUrl": "food-1013.jpg",
        "tags": ["FastFood", "Burger", "Lunch"]
    },
    {
        "id": "1014",
        "name": "Belgian Waffle",
        "cookTime": "10-20",
        "price": 12.00,
        "favorite": True,
        "origins": ["belgium"],
        "stars": 4.4,
        "imageUrl": "food-1014.jpg",
        "tags": ["Breakfast", "Sweet"]
    },
    {
        "id": "1015",
        "name": "Eggs Benedict",
        "cookTime": "15-25",
        "price": 14.00,
        "favorite": False,
        "origins": ["us"],
        "stars": 4.2,
        "imageUrl": "food-1015.jpg",
        "tags": ["Breakfast", "Eggs"]
    },
    {
        "id": "1016",
        "name": "Chicken Shawarma",
        "cookTime": "20-30",
        "price": 22.00,
        "favorite": True,
        "origins": ["middle east"],
        "stars": 4.5,
        "imageUrl": "food-1016.jpg",
        "tags": ["FastFood", "Wrap", "Lunch"]
    },
    {
        "id": "1017",
        "name": "Falafel Wrap",
        "cookTime": "15-25",
        "price": 19.00,
        "favorite": False,
        "origins": ["middle east"],
        "stars": 4.0,
        "imageUrl": "food-1017.jpg",
        "tags": ["FastFood", "Wrap", "Lunch"]
    },
    {
        "id": "1018",
        "name": "Chocolate Brownie",
        "cookTime": "20-30",
        "price": 8.00,
        "favorite": True,
        "origins": ["us"],
        "stars": 4.7,
        "imageUrl": "food-1018.jpg",
        "tags": ["Dessert", "Chocolate"]
    },
    {
        "id": "1019",
        "name": "Tiramisu",
        "cookTime": "20-30",
        "price": 10.00,
        "favorite": True,
        "origins": ["italy"],
        "stars": 4.8,
        "imageUrl": "food-1019.jpg",
        "tags": ["Dessert", "Sweet"]
    },
    {
        "id": "1020",
        "name": "Iced Caramel Macchiato",
        "cookTime": "5-10",
        "price": 6.00,
        "favorite": False,
        "origins": ["us"],
        "stars": 4.3,
        "imageUrl": "food-1020.jpg",
        "tags": ["ColdDrink", "Coffee"]
    },
    {
        "id": "1021",
        "name": "Iced Lemonade",
        "cookTime": "5-10",
        "price": 5.00,
        "favorite": True,
        "origins": ["us"],
        "stars": 4.1,
        "imageUrl": "food-1021.jpg",
        "tags": ["ColdDrink", "Lemon"]
    },
    {
        "id": "1022",
        "name": "Hot Chocolate",
        "cookTime": "5-10",
        "price": 4.00,
        "favorite": True,
        "origins": ["us"],
        "stars": 4.5,
        "imageUrl": "food-1022.jpg",
        "tags": ["HotDrink", "Chocolate"]
    },
    {
        "id": "1023",
        "name": "Cappuccino",
        "cookTime": "5-10",
        "price": 4.00,
        "favorite": False,
        "origins": ["italy"],
        "stars": 4.3,
        "imageUrl": "food-1023.jpg",
        "tags": ["HotDrink", "Coffee"]
    },
    {
        "id": "1024",
        "name": "Virgin Mojito",
        "cookTime": "5-10",
        "price": 7.00,
        "favorite": False,
        "origins": ["cuba"],
        "stars": 4.2,
        "imageUrl": "food-1024.jpg",
        "tags": ["Cocktail", "NonAlcoholic"]
    },
    {
        "id": "1025",
        "name": "Piña Colada",
        "cookTime": "5-10",
        "price": 8.00,
        "favorite": True,
        "origins": ["puerto rico"],
        "stars": 4.5,
        "imageUrl": "food-1025.jpg",
        "tags": ["Cocktail", "NonAlcoholic"]
    }
]

# Veriyi yeni bir JSON dosyasına kaydetme
with open('C:/Users/beyza/Downloads/fixed_foods.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Düzeltilmiş JSON verileri fixed_foods.json dosyasına kaydedildi.")



# Yemek verilerini JSON dosyasından okuma
try:
    with open('C:/Users/beyza/Downloads/fixed_foods.json', 'r') as file:
        foods = json.load(file)
        print("Yemek verileri başarıyla yüklendi.")
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    foods = []

# Verileri kontrol etmek için ilk birkaç öğeyi yazdırma
if foods:
    for food in foods[:5]:
        print(food)
else:
    print("Yemek verileri yüklenemedi.")

# Rastgele siparişler oluşturma fonksiyonu
def create_random_orders(num_orders, foods):
    orders = []
    for _ in range(num_orders):
        order_id = str(uuid.uuid4())
        num_items = random.randint(1, 5)  # Her sipariş 1-5 arasında rastgele ürün içerir
        items = random.sample(foods, num_items)
        order = {
            'order_id': order_id,
            'items': [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'price': item['price']
                }
                for item in items
            ],
            'total_price': sum(item['price'] for item in items)
        }
        orders.append(order)
    return orders

if foods:
    # 1000 sipariş oluştur
    num_orders = 1000
    orders = create_random_orders(num_orders, foods)

    # Oluşturulan siparişleri yeni bir JSON dosyasına kaydetme
    with open('C:/Users/beyza/Downloads/orders.json', 'w') as file:
        json.dump(orders, file, indent=4)

    print("1000 rastgele sipariş oluşturuldu ve orders.json dosyasına kaydedildi.")
else:
    print("Siparişler oluşturulamadı çünkü yemek verileri yüklenemedi.")
