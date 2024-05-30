import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from flask import Flask, request, jsonify
from flask_cors import CORS

# Dosyayı yükleme
with open('C:/Users/beyza/Downloads/Orders.json') as f:
    orders = json.load(f)

# Veriyi DataFrame'e dönüştürme
order_data = []
for order in orders:
    for item in order['items']:
        order_data.append({
            'order_id': order['order_id'],
            'date': order['date'],
            'item_id': item['id'],
            'item_name': item['name'],
            'quantity': item['quantity']
        })

df = pd.DataFrame(order_data)

# Tarih formatını dönüştürme
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Haftalık ve aylık veriler için ek kolonlar
df['week'] = df['date'].dt.isocalendar().week
df['month'] = df['date'].dt.month

# Order ID bazında item listesi oluşturma
basket = df.groupby(['order_id', 'item_name'])['quantity'].sum().unstack().reset_index().fillna(0).set_index('order_id')

# Değerleri boolean türüne dönüştürme
basket_sets = basket.applymap(lambda x: 1 if x > 0 else 0)

# Apriori algoritmasını kullanarak sık örüntüleri bulma
frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True)

# Birliktelik kurallarını çıkarma
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Haftanın ve ayın en çok tercih edilen yemeklerini bulma
def get_top_items_by_week(df):
    top_items_by_week = df.groupby(['week', 'item_name'])['quantity'].sum().reset_index()
    top_items_by_week = top_items_by_week.sort_values(['week', 'quantity'], ascending=[True, False]).groupby('week').head(1)
    return top_items_by_week

def get_top_items_by_month(df):
    top_items_by_month = df.groupby(['month', 'item_name'])['quantity'].sum().reset_index()
    top_items_by_month = top_items_by_month.sort_values(['month', 'quantity'], ascending=[True, False]).groupby('month').head(1)
    return top_items_by_month

# Haftanın en çok tercih edilen yemekleri
weekly_top_items = get_top_items_by_week(df)

# Ayın en çok tercih edilen yemekleri
monthly_top_items = get_top_items_by_month(df)

# Flask API oluşturma
app = Flask(__name__)
CORS(app)

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    item_name = request.args.get('item_name')
    recommendations = rules[rules['antecedents'].apply(lambda x: item_name in str(x))]
    if not recommendations.empty:
        result = recommendations.iloc[0]
        return jsonify({
            'antecedents': list(result['antecedents']),
            'consequents': list(result['consequents']),
            'support': result['support'],
            'confidence': result['confidence'],
            'lift': result['lift']
        })
    else:
        return jsonify({"error": "No recommendations found for the given item."})


@app.route('/weekly_favorites', methods=['GET'])
def get_weekly_favorites():
    top_items_by_week = get_top_items_by_week(df)
    weekly_favorites = top_items_by_week.to_dict(orient='records')
    return jsonify(weekly_favorites)

@app.route('/monthly_favorites', methods=['GET'])
def get_monthly_favorites():
    top_items_by_month = get_top_items_by_month(df)
    monthly_favorites = top_items_by_month.to_dict(orient='records')
    return jsonify(monthly_favorites)

if __name__ == '__main__':
    app.run(debug=True)
