"""
generate_dataset.py
--------------------
Generates a realistic e-commerce product review dataset (mimicking Flipkart/Amazon
style reviews) to be used as a stand-in dataset for the pipeline. Structure and
columns match exactly what scraper.py (real scraper) would produce, so this CSV
can be seamlessly replaced by actual scraped data without changing downstream code.

Columns: product_name, rating, review_text, sentiment
"""

import pandas as pd
import random

random.seed(42)

products = ["Wireless Bluetooth Earbuds", "Smartphone X200", "Running Shoes Pro",
            "Stainless Steel Water Bottle", "Cotton Bedsheet Set", "Laptop Backpack",
            "Smartwatch Fit 3", "Kitchen Mixer Grinder"]

positive_templates = [
    "Absolutely loved this product, {aspect} is amazing and works perfectly.",
    "Great {aspect}, exceeded my expectations. Highly recommend to everyone.",
    "The {aspect} is excellent for the price. Very happy with this purchase.",
    "Superb build quality and the {aspect} works flawlessly. Five stars!",
    "I am extremely satisfied, the {aspect} is top notch and delivery was fast.",
    "Best purchase this year, {aspect} is outstanding and value for money.",
    "Works like a charm, {aspect} is impressive and battery backup is great.",
    "Really good product, {aspect} is smooth and packaging was excellent.",
    "Awesome quality, {aspect} is comfortable and durable, will buy again.",
    "Nice product overall, the {aspect} feels premium and looks stylish.",
    "Fantastic experience, {aspect} performs better than expected, love it.",
    "Perfect fit and finish, the {aspect} is reliable and easy to use.",
    "Happy with the purchase, {aspect} is efficient and setup was simple.",
    "Wonderful product, {aspect} is sturdy and customer service was helpful.",
    "Excellent value, {aspect} works great and arrived earlier than expected."
]

negative_templates = [
    "Very disappointed, the {aspect} stopped working within a week.",
    "Poor quality product, {aspect} is faulty and packaging was damaged.",
    "Waste of money, {aspect} does not work as advertised at all.",
    "Terrible experience, {aspect} broke on the first day of use.",
    "Not satisfied with the {aspect}, it feels cheap and flimsy.",
    "The {aspect} is defective, requested a replacement but no response.",
    "Bad build quality, {aspect} stopped functioning after two days.",
    "Extremely unhappy, {aspect} is nothing like the product description.",
    "Regret buying this, the {aspect} is uncomfortable and low quality.",
    "Disappointing purchase, {aspect} makes a strange noise and lags often.",
    "Product arrived damaged, {aspect} was broken inside the box.",
    "Not worth the price, {aspect} feels flimsy and unreliable.",
    "Horrible experience, {aspect} failed within a few hours of use.",
    "Would not recommend, the {aspect} is slow and battery drains fast.",
    "Complete letdown, {aspect} does not match the online pictures at all."
]

aspects_pos = ["sound quality", "battery life", "build quality", "design", "comfort",
               "performance", "delivery", "packaging", "screen quality", "grip",
               "material", "connectivity", "warranty support", "finish", "durability"]

aspects_neg = ["sound quality", "battery life", "build quality", "stitching", "comfort",
               "performance", "delivery", "packaging", "screen quality", "grip",
               "material", "connectivity", "customer support", "finish", "durability"]

extra_positive = [
    "Superb product, totally worth every penny spent.",
    "Five stars, this is exactly what I was looking for.",
    "Great gift item, my family loved it a lot.",
    "Highly durable and easy to carry around daily.",
    "The color and texture are exactly as shown online.",
    "Genuinely impressed by the overall quality and speed of delivery.",
    "Compact, lightweight, and very easy to operate.",
    "This exceeded my expectations, works perfectly since day one.",
    "Value for money product, works smoothly without any issues.",
    "Simple to set up, and the instructions were very clear."
]

extra_negative = [
    "One star only because zero is not an option.",
    "Never buying from this brand again, total disappointment.",
    "The product smells odd and quality feels substandard.",
    "Customer care did not respond to my complaint at all.",
    "Size does not match the description, very misleading.",
    "It stopped charging after just three uses, very frustrating.",
    "The color faded after a single wash, poor material.",
    "Delivery took forever and the box was completely crushed.",
    "Instructions were unclear and the app kept crashing.",
    "This is a cheap knockoff, nothing like the original brand."
]

rows = []

for i in range(65):
    product = random.choice(products)
    template = random.choice(positive_templates)
    aspect = random.choice(aspects_pos)
    text = template.format(aspect=aspect)
    rating = random.choice([4, 5, 5, 4])
    rows.append((product, rating, text, "positive"))

for t in extra_positive:
    rows.append((random.choice(products), random.choice([4, 5]), t, "positive"))

for i in range(65):
    product = random.choice(products)
    template = random.choice(negative_templates)
    aspect = random.choice(aspects_neg)
    text = template.format(aspect=aspect)
    rating = random.choice([1, 2, 1, 2])
    rows.append((product, rating, text, "negative"))

for t in extra_negative:
    rows.append((random.choice(products), random.choice([1, 2]), t, "negative"))

random.shuffle(rows)

df = pd.DataFrame(rows, columns=["product_name", "rating", "review_text", "sentiment"])
df.drop_duplicates(subset="review_text", inplace=True)
df.reset_index(drop=True, inplace=True)

df.to_csv("/home/claude/project/data/reviews.csv", index=False)
print("Dataset shape:", df.shape)
print(df['sentiment'].value_counts())
