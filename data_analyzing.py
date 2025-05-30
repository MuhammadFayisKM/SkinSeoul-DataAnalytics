import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("product_dataset.csv")
# print(dataset.head(10)) #test 1

# print(dataset.info())
# after the info() - we confirmed the data is cleanerversion of itself


# finding gross profit margin
# gpm
dataset["Gross Profit"] = (
    (dataset["Price (USD)"] - dataset["Cost Price (USD)"]) / dataset["Price (USD)"]
) * 100

# competitor prices and differences
dataset["Competitor Price Differences"] = (
    dataset["Price (USD)"] - dataset["Competitor Price (USD)"]
)

# sorting by Units Sold
dataset = dataset.sort_values(by="Units Sold", ascending=False)

# print(dataset.head(10)) # test 2


# price recomendaton
def price_recommendation(row):
    if row["Competitor Price Differences"] < 0:
        return "Consider increasing the price"
    elif row["Competitor Price Differences"] > 0:
        return "Consider decreasing the price"
    else:
        return "Price is competitive"


dataset["Price Recommendation"] = dataset.apply(price_recommendation, axis=1)

# print(dataset[["Product Name", "Price Recommendation"]]) #test 3 and recommendation to the product owner!


# finding which stocks are good to promote
def promotion_recommendation(row):
    if row["Units Sold"] > 1000 and row["Gross Profit"] > 35:
        return "High potential for profit with a promotion"
    elif row["Units Sold"] < 500 and row["Gross Profit"] < 10:
        return "Low potential for profit with a promotion"
    else:
        return "Neutral potential for profit with a promotion"


# product priced lower than competitors
lower_priced = dataset[dataset["Competitor Price Differences"] < 0].copy()

lower_priced = dataset[dataset["Competitor Price Differences"] < 0].copy()

# Using existing column
lower_priced["Potential Increase (USD)"] = -lower_priced["Competitor Price Differences"]

# Plot
plt.figure(figsize=(10, 6))
plt.barh(
    lower_priced["Product Name"],
    lower_priced["Potential Increase (USD)"],
    color="skyblue",
)
plt.xlabel("Potential Price Increase (USD)")
plt.title("Products with Potential for Price Increase Compared to Competitors")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("price_increase_potential.png", dpi=300)
# plt.savefig("price_increase_potential.jpg", dpi=300)
plt.show()

# Filter: products with high units sold and strong margins
promo_targets = dataset[
    (dataset["Units Sold"] > 1000) & (dataset["Gross Profit"] > 35)
].copy()

# Estimate growth (e.g., 20% projected increase)
promo_targets["Expected Sales Growth"] = promo_targets["Units Sold"] * 0.2

# Plot
plt.figure(figsize=(10, 6))
plt.barh(
    promo_targets["Product Name"],
    promo_targets["Expected Sales Growth"],
    color="lightgreen",
)
plt.xlabel("Expected Additional Units Sold")
plt.title("Expected Sales Boost from Promotions")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("promotion_sales_growth.png", dpi=300)
# plt.savefig("promotion_sales_growth.jpg", dpi=300)
plt.show()
