import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules
from mpl_toolkits.mplot3d import Axes3D


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

# Daha düzenli bir formatta çıktıyı yazdırma
pd.set_option('display.max_columns', None)  # Tüm sütunları göster

# Kuralların çıktısını düzenli bir formatta yazdırma
for index, row in rules.iterrows():
    antecedents = ', '.join(list(row['antecedents']))
    consequents = ', '.join(list(row['consequents']))
    print(f"Antecedents: {antecedents}")
    print(f"Consequents: {consequents}")
    print(f"Antecedent Support: {row['antecedent support']}")
    print(f"Consequent Support: {row['consequent support']}")
    print(f"Support: {row['support']}")
    print(f"Confidence: {row['confidence']}")
    print(f"Lift: {row['lift']}")
    print(f"Leverage: {row['leverage']}")
    print(f"Conviction: {row['conviction']}")
    print(f"Zhang's Metric: {row['zhangs_metric']}")
    print("\n" + "-" * 50 + "\n")


# Eğer belirli bir ürün için önerileri görmek isterseniz, aşağıdaki şekilde kullanabilirsiniz
def get_recommendations(item_name):
    recommendations = rules[rules['antecedents'].apply(lambda x: item_name in str(x))]
    for index, row in recommendations.iterrows():
        antecedents = ', '.join(list(row['antecedents']))
        consequents = ', '.join(list(row['consequents']))
        print(f"Antecedents: {antecedents}")
        print(f"Consequents: {consequents}")
        print(f"Antecedent Support: {row['antecedent support']}")
        print(f"Consequent Support: {row['consequent support']}")
        print(f"Support: {row['support']}")
        print(f"Confidence: {row['confidence']}")
        print(f"Lift: {row['lift']}")
        print(f"Leverage: {row['leverage']}")
        print(f"Conviction: {row['conviction']}")
        print(f"Zhang's Metric: {row['zhangs_metric']}")
        print("\n" + "-" * 50 + "\n")


# Örnek: Chicken Parmesan için öneriler
get_recommendations('Chicken Parmesan')

# Her yemeğin hangi yemekle en sık birlikte tercih edildiğini bulma
most_frequent_pairs = {}
for item in df['item_name'].unique():
    item_rules = rules[rules['antecedents'].apply(lambda x: item in str(x))]
    if not item_rules.empty:
        most_frequent_rule = item_rules.loc[item_rules['support'].idxmax()]
        antecedents = ', '.join(list(most_frequent_rule['antecedents']))
        consequents = ', '.join(list(most_frequent_rule['consequents']))
        most_frequent_pairs[item] = {
            'antecedents': antecedents,
            'consequents': consequents,
            'support': most_frequent_rule['support'],
            'confidence': most_frequent_rule['confidence'],
            'lift': most_frequent_rule['lift']
        }

# Her yemeğin en sık birlikte tercih edildiği yemeklerin çıktısı
for item, details in most_frequent_pairs.items():
    print(f"Item: {item}")
    print(f"Most Frequent Pair: {details['antecedents']} -> {details['consequents']}")
    print(f"Support: {details['support']}")
    print(f"Confidence: {details['confidence']}")
    print(f"Lift: {details['lift']}")
    print("\n" + "-" * 50 + "\n")

# Haftanın ve ayın en çok tercih edilen yemeklerini bulma
def get_top_items_by_week(df):
    top_items_by_week = df.groupby(['week', 'item_name'])['quantity'].sum().reset_index()
    top_items_by_week = top_items_by_week.sort_values(['week', 'quantity'], ascending=[True, False]).groupby(
        'week').head(1)
    return top_items_by_week


def get_top_items_by_month(df):
    top_items_by_month = df.groupby(['month', 'item_name'])['quantity'].sum().reset_index()
    top_items_by_month = top_items_by_month.sort_values(['month', 'quantity'], ascending=[True, False]).groupby(
        'month').head(1)
    return top_items_by_month


# Haftanın en çok tercih edilen yemekleri
print("Haftanın en çok tercih edilen yemekleri:")
print(get_top_items_by_week(df))

# Ayın en çok tercih edilen yemekleri
print("Ayın en çok tercih edilen yemekleri:")
print(get_top_items_by_month(df))


# Grafikler
def plot_item_frequency(df):
    item_counts = df['item_name'].value_counts().reset_index()
    item_counts.columns = ['item_name', 'count']
    plt.figure(figsize=(12, 8))
    sns.barplot(x='count', y='item_name', data=item_counts, palette='viridis', hue=None, legend=False)
    plt.title('Sipariş Sıklığı (Item Frequency)')
    plt.xlabel('Frekans')
    plt.ylabel('Yemekler')
    plt.show()


def plot_support_distribution(frequent_itemsets):
    plt.figure(figsize=(10, 6))
    plt.hist(frequent_itemsets['support'], bins=50, color='blue', alpha=0.7)
    plt.title('Sık Örüntülerin Destek Dağılımı (Support Distribution of Frequent Itemsets)')
    plt.xlabel('Support')
    plt.ylabel('Frequency')
    plt.show()


def plot_confidence_distribution(rules):
    plt.figure(figsize=(10, 6))
    plt.hist(rules['confidence'], bins=50, color='green', alpha=0.7)
    plt.title('Birliktelik Kurallarının Güven Dağılımı (Confidence Distribution of Association Rules)')
    plt.xlabel('Confidence')
    plt.ylabel('Frequency')
    plt.show()


def plot_lift_distribution(rules):
    plt.figure(figsize=(10, 6))
    plt.hist(rules['lift'], bins=50, color='red', alpha=0.7)
    plt.title('Birliktelik Kurallarının Kaldırma Dağılımı (Lift Distribution of Association Rules)')
    plt.xlabel('Lift')
    plt.ylabel('Frequency')
    plt.show()


def plot_support_vs_confidence(rules):
    plt.figure(figsize=(10, 6))
    plt.scatter(rules['support'], rules['confidence'], alpha=0.7, marker='o')
    plt.title('Destek vs. Güven (Support vs. Confidence)')
    plt.xlabel('Support')
    plt.ylabel('Confidence')
    plt.show()


def plot_support_vs_lift(rules):
    plt.figure(figsize=(10, 6))
    plt.scatter(rules['support'], rules['lift'], alpha=0.7, marker='o')
    plt.title('Destek vs. Kaldırma (Support vs. Lift)')
    plt.xlabel('Support')
    plt.ylabel('Lİft')
    plt.show()


def plot_support_confidence_lift(rules):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(rules['support'], rules['confidence'], rules['lift'], c='b', marker='o')
    ax.set_xlabel('Support')
    ax.set_ylabel('Confidence')
    ax.set_zlabel('Lift')
    plt.title('Destek vs Güven vs Kaldırma (Support vs Confidence vs Lift)')
    plt.show()


def plot_itemsets_size_distribution(frequent_itemsets):
    itemset_sizes = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    itemset_sizes = itemset_sizes.reset_index()
    itemset_sizes.columns = ['index', 'size']
    plt.figure(figsize=(12, 8))
    sns.countplot(data=itemset_sizes, x='size', palette='viridis', hue=None, legend=False)
    plt.title('Sık Örüntülerin Boyut Dağılımı (Frequent Itemsets Size Distribution)')
    plt.xlabel('Öğe Sayısı')
    plt.ylabel('Frekans')
    plt.show()


def plot_item_cooccurrence_heatmap(basket_sets):
    cooccurrence_matrix = basket_sets.T.dot(basket_sets)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cooccurrence_matrix, cmap='viridis')
    plt.title('Yemek Birlikte Görülme Isı Haritası (Heatmap of Item Co-occurrences)')
    plt.xlabel('Yemekler')
    plt.ylabel('Yemekler')
    plt.show()


# Güncellenmiş Top 10 Kuralları Gösteren Grafik (Scatter Plot)
def plot_top_rules_combined(rules, n=10):
    top_lift = rules.nlargest(n, 'lift')
    top_confidence = rules.nlargest(n, 'confidence')

    fig, ax = plt.subplots(figsize=(12, 8))

    # Top lift scatter plot
    ax.scatter(top_lift.index, top_lift['lift'], color='g', alpha=0.7, label='Lift')

    # Top confidence scatter plot
    ax.scatter(top_confidence.index, top_confidence['confidence'], color='b', alpha=0.7, label='Confidence')

    ax.set_xlabel('Kural İndeksi')
    ax.set_ylabel('Metrik Değeri')
    plt.title(f'En İyi {n} Kural - Kaldırma ve Güven')
    plt.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    plt.show()


# Grafiklerin çizimi
plot_item_frequency(df)
plot_support_distribution(frequent_itemsets)
plot_confidence_distribution(rules)
plot_lift_distribution(rules)
plot_support_vs_confidence(rules)
plot_support_vs_lift(rules)
plot_support_confidence_lift(rules)
plot_itemsets_size_distribution(frequent_itemsets)
plot_item_cooccurrence_heatmap(basket_sets)
plot_top_rules_combined(rules, n=10)