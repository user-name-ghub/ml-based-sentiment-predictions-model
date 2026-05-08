import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

PRODUCTS = [
    "Wireless Headphones","USB-C Cable","Laptop Stand","Power Bank","Smartphone Case",
    "LED Desk Lamp","Mechanical Keyboard","Webcam","Wireless Mouse","Smart Watch",
    "Electric Toothbrush","Air Purifier","Coffee Maker","Yoga Mat","Water Bottle",
    "Travel Backpack","Earbuds","Tablet Stand","Pen Drive","Smart Bulb",
    "Security Camera","Blender","Beard Trimmer","Running Shoes","Face Wash",
    "Gaming Chair","Monitor","External HDD","Bluetooth Speaker","Air Fryer",
    "Electric Kettle","Rice Cooker","Neck Pillow","Desk Organizer","Screen Guard"
]

# ── Real-world-style sentence pools ──────────────────────────────────────────
# All classes share the SAME nouns/verbs — only key adjectives differ
# 10% label noise is added at the end to cap accuracy at 88-93%

POSITIVE_REVIEWS = [
    "I bought this {p} and I am very happy with the quality. Works great every day.",
    "Received the {p} on time. Excellent build quality and amazing performance overall.",
    "This {p} is fantastic. Great value and I love using it. Highly recommend.",
    "Ordered the {p} last week. Outstanding quality, fast delivery, very satisfied.",
    "The {p} works perfectly. Solid build and superb performance. Will buy again.",
    "Really impressed with this {p}. Excellent quality and brilliant value for money.",
    "Wonderful {p}. Works brilliantly every time. Great packaging and fast shipping.",
    "This {p} exceeded my expectations. Amazing quality and reliable performance.",
    "Very happy with the {p}. Premium feel, great design, excellent performance.",
    "The {p} is outstanding. Works flawlessly and quality is top notch. Love it.",
    "Superb {p}. Delivery was fast and quality is excellent. Highly satisfied.",
    "Brilliant product. The {p} works great and quality is very impressive indeed.",
    "Happy with this {p}. Great quality, reasonable price, very reliable daily use.",
    "Loved the {p}. Excellent performance, great build, fantastic value for money.",
    "The {p} is perfect. Impressed with quality and very happy with this purchase.",
    "Great {p} at a great price. Quality is solid and performance is reliable.",
    "Very satisfied with the {p}. Excellent quality and works as expected perfectly.",
    "This {p} is wonderful. Highly recommend it. Quality is brilliant and love it.",
    "The {p} works amazingly. Excellent quality, superb design, great daily use.",
    "Really love this {p}. Fantastic quality and great performance. Very satisfied.",
    "Brilliant purchase. The {p} has excellent quality and works very reliably.",
    "The {p} is superb. Very happy with the quality and performance every day.",
    "Satisfied with the {p}. Great quality, fast delivery, very good overall.",
    "This {p} is excellent. Works perfectly and quality is impressive. Love it.",
    "Happy customer. The {p} is amazing quality and performs brilliantly daily.",
]

NEGATIVE_REVIEWS = [
    "I bought this {p} and I am very disappointed with the quality. Broke quickly.",
    "Received the {p} damaged. Terrible build quality and awful performance overall.",
    "This {p} is horrible. Bad value and I hate using it. Strongly avoid.",
    "Ordered the {p} last week. Poor quality, slow delivery, very dissatisfied.",
    "The {p} stopped working. Weak build and pathetic performance. Never buying again.",
    "Really disappointed with this {p}. Poor quality and terrible value for money.",
    "Awful {p}. Does not work reliably at all. Bad packaging and slow shipping.",
    "This {p} fell below my expectations. Terrible quality and unreliable performance.",
    "Very unhappy with the {p}. Cheap feel, bad design, awful performance.",
    "The {p} is pathetic. Works inconsistently and quality is very low. Hate it.",
    "Terrible {p}. Delivery was slow and quality is awful. Very dissatisfied.",
    "Horrible product. The {p} does not work and quality is very disappointing.",
    "Unhappy with this {p}. Poor quality, high price, very unreliable daily use.",
    "Hated the {p}. Terrible performance, poor build, awful value for money.",
    "The {p} is defective. Disappointed with quality and very unhappy with purchase.",
    "Bad {p} at a high price. Quality is weak and performance is unreliable.",
    "Very dissatisfied with the {p}. Poor quality and does not work as expected.",
    "This {p} is awful. Would avoid it. Quality is horrible and hate using it.",
    "The {p} broke immediately. Poor quality, terrible design, useless daily use.",
    "Really hate this {p}. Terrible quality and poor performance. Very dissatisfied.",
    "Horrible purchase. The {p} has poor quality and works very unreliably.",
    "The {p} is terrible. Very unhappy with the quality and performance every day.",
    "Dissatisfied with the {p}. Poor quality, slow delivery, very bad overall.",
    "This {p} is awful. Does not work and quality is terrible. Hate it.",
    "Unhappy customer. The {p} is horrible quality and performs terribly daily.",
]

NEUTRAL_REVIEWS = [
    "I bought this {p} and I feel okay about the quality. Works adequately each day.",
    "Received the {p} on time. Average build quality and moderate performance overall.",
    "This {p} is decent. Fair value and I feel neutral about it. Might recommend.",
    "Ordered the {p} last week. Average quality, standard delivery, somewhat satisfied.",
    "The {p} works okay. Average build and moderate performance. Might buy again.",
    "Somewhat impressed with this {p}. Average quality and okay value for money.",
    "Okay {p}. Works adequately most of the time. Standard packaging and shipping.",
    "This {p} met my average expectations. Acceptable quality and okay performance.",
    "Somewhat okay with the {p}. Average feel, basic design, moderate performance.",
    "The {p} is acceptable. Works inconsistently and quality is average. It is okay.",
    "Average {p}. Delivery was okay and quality is acceptable. Somewhat satisfied.",
    "Passable product. The {p} works sometimes and quality is just adequate.",
    "Neutral about this {p}. Average quality, fair price, moderately reliable use.",
    "Mixed feelings about {p}. Moderate performance, average build, okay value.",
    "The {p} is acceptable. Neither impressed nor disappointed with quality.",
    "Okay {p} at an okay price. Quality is average and performance is moderate.",
    "Somewhat satisfied with the {p}. Average quality and works most of the time.",
    "This {p} is okay. Would neither recommend nor avoid. Quality is average.",
    "The {p} works adequately. Average quality, standard design, basic daily use.",
    "Somewhat like this {p}. Acceptable quality and moderate performance overall.",
    "Average purchase. The {p} has okay quality and works somewhat reliably.",
    "The {p} is acceptable. Somewhat okay with the quality and performance daily.",
    "Neutral about the {p}. Average quality, standard delivery, just okay overall.",
    "This {p} is acceptable. Works okay and quality is passable enough. Fine.",
    "Neutral customer. The {p} is average quality and performs acceptably daily.",
]

def inject_mess(text):
    r = random.random()
    if r < 0.13:
        tags = ["<br/>","<p>","</p>","<b>","</b>","<span>","&amp;","&nbsp;","<i>","<div>"]
        pos  = random.randint(0, max(0, len(text)-8))
        text = text[:pos] + random.choice(tags) + " " + text[pos:]
    elif r < 0.21:
        text = "".join(c.upper() if random.random()<0.45 else c for c in text)
    elif r < 0.28:
        text = text.replace(" ", "  ", random.randint(1,3))
    elif r < 0.34:
        text += random.choice([" @@@"," ###"," !!!"," ???"," ---"])
    elif r < 0.38:
        text += f"  (ref #{random.randint(1000,9999)})"
    return text

def random_date():
    s = datetime(2021,1,1); e = datetime(2024,12,31)
    return (s + timedelta(days=random.randint(0,(e-s).days))).strftime("%Y-%m-%d")

rows = []
configs = [("Positive",[4,5],POSITIVE_REVIEWS,21000),
           ("Negative",[1,2],NEGATIVE_REVIEWS,17000),
           ("Neutral", [3],  NEUTRAL_REVIEWS, 13000)]

for sentiment, rating_pool, pool, count in configs:
    for _ in range(count):
        p    = random.choice(PRODUCTS)
        text = random.choice(pool).format(p=p)
        text = inject_mess(text)
        rows.append({
            "review_id":         len(rows)+1,
            "product_name":      None if random.random()<0.04 else random.choice(PRODUCTS),
            "user_review":       None if random.random()<0.06 else text,
            "rating":            random.choice(rating_pool),
            "verified_purchase": None if random.random()<0.05 else random.choice(["Yes","No"]),
            "review_date":       None if random.random()<0.05 else random_date(),
            "price":             None if random.random()<0.07 else round(random.uniform(99,9999),2),
            "helpful_votes":     None if random.random()<0.08 else random.randint(0,200),
        })

random.shuffle(rows)
df = pd.DataFrame(rows)

# ── Add 10% LABEL NOISE by flipping ratings ───────────────────────────────
# This simulates real-world ambiguous/mislabeled reviews
# and naturally limits model accuracy to 87-93% range
noise_idx = np.random.choice(len(df), size=int(0.10*len(df)), replace=False)
noisy_ratings = df["rating"].values.copy()
for i in noise_idx:
    current_rating = noisy_ratings[i]
    if current_rating in [1, 2]:
        noisy_ratings[i] = np.random.choice([3, 4, 5])
    elif current_rating == 3:
        noisy_ratings[i] = np.random.choice([1, 2, 4, 5])
    else:
        noisy_ratings[i] = np.random.choice([1, 2, 3])
df["rating"] = noisy_ratings

# Add ~2% duplicate rows
dupes = df.sample(n=int(0.02*len(df)), random_state=55)
df    = pd.concat([df, dupes], ignore_index=True)
df["review_id"] = range(1, len(df)+1)

df.to_csv("/home/claude/product_reviews_messy.csv", index=False)
print(f"Total rows     : {len(df)}")
print(f"Unique reviews : {df['user_review'].nunique()}")
print(f"Rating dist:\n{df['rating'].value_counts().sort_index()}")
print(f"\nNulls:\n{df.isnull().sum()}")
