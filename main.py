import pandas as pd
import numpy as np

# -----------------------------------
# 1. Load Dataset
# -----------------------------------

df = pd.read_csv(
    "Data/archive (1)/Sample - Superstore.csv",
    encoding="latin1"
)

# -----------------------------------
# 2. Convert Dates
# -----------------------------------

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# -----------------------------------
# 3. Create Customer-Level Dataset
# -----------------------------------

customer_df = df.groupby(
    ["Customer ID", "Customer Name", "Segment"]
).agg(
    First_Purchase=("Order Date", "min"),
    Last_Purchase=("Order Date", "max"),
    Total_Orders=("Order ID", "nunique"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Number_of_Products=("Product ID", "nunique")
).reset_index()

# -----------------------------------
# 4. Average Order Value
# -----------------------------------

customer_df["Average_Order_Value"] = (
    customer_df["Total_Sales"] /
    customer_df["Total_Orders"]
)

# -----------------------------------
# 5. Customer Tenure
# -----------------------------------

customer_df["Customer_Tenure_Days"] = (
    customer_df["Last_Purchase"] -
    customer_df["First_Purchase"]
).dt.days

# -----------------------------------
# 6. Recency
# -----------------------------------

analysis_date = df["Order Date"].max()

customer_df["Recency_Days"] = (
    analysis_date -
    customer_df["Last_Purchase"]
).dt.days

# -----------------------------------
# 7. Purchase Frequency
# -----------------------------------

customer_df["Purchase_Frequency"] = (
    customer_df["Total_Orders"] /
    (customer_df["Customer_Tenure_Days"] / 30 + 1)
)

# -----------------------------------
# 8. Display Results
# -----------------------------------

print("\nCustomer-Level Dataset:")
print(customer_df.head())

print("\nCustomer Dataset Shape:")
print(customer_df.shape)

print("\nNumber of Unique Customers:")
print(customer_df["Customer ID"].nunique())

print("\nCustomer Dataset Columns:")
print(customer_df.columns.tolist())

print("\nCustomer Summary:")
print(customer_df.describe())

# -----------------------------------
# 9. Calculate Purchase Gaps
# -----------------------------------

order_dates = (
    df[["Customer ID", "Order Date"]]
    .drop_duplicates()
    .sort_values(["Customer ID", "Order Date"])
)

order_dates["Purchase_Gap_Days"] = (
    order_dates
    .groupby("Customer ID")["Order Date"]
    .diff()
    .dt.days
)

# Remove first purchase of each customer
purchase_gaps = order_dates["Purchase_Gap_Days"].dropna()

# -----------------------------------
# 10. Purchase Gap Statistics
# -----------------------------------

print("\nPurchase Gap Statistics:")
print(purchase_gaps.describe())

print("\nPurchase Gap Percentiles:")
print(purchase_gaps.quantile([0.25, 0.50, 0.75, 0.90, 0.95]))

# -----------------------------------
# 11. Define Customer Churn
# -----------------------------------

CHURN_THRESHOLD = 266

customer_df["Churn"] = (
    customer_df["Recency_Days"] > CHURN_THRESHOLD
).astype(int)

# -----------------------------------
# 12. Churn Summary
# -----------------------------------

print("\nChurn Distribution:")
print(customer_df["Churn"].value_counts())

print("\nChurn Percentage:")
print(
    customer_df["Churn"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# -----------------------------------
# 13. Compare Active vs Churned
# -----------------------------------

comparison = customer_df.groupby("Churn")[
    [
        "Total_Orders",
        "Total_Sales",
        "Total_Profit",
        "Total_Quantity",
        "Number_of_Products",
        "Average_Order_Value",
        "Customer_Tenure_Days",
        "Purchase_Frequency",
        "Recency_Days"
    ]
].mean()

print("\nActive vs Churned Customers:")
print(comparison.round(2))

# -----------------------------------
# 14. Churn by Segment
# -----------------------------------

segment_churn = pd.crosstab(
    customer_df["Segment"],
    customer_df["Churn"],
    normalize="index"
) * 100

print("\nChurn Rate by Segment (%):")
print(segment_churn.round(2))

# -----------------------------------
# 15. Churn by Segment - Customer Count
# -----------------------------------

segment_count = pd.crosstab(
    customer_df["Segment"],
    customer_df["Churn"]
)

print("\nCustomer Count by Segment:")
print(segment_count)


# -----------------------------------
# 16. Average Purchase Gap per Customer
# -----------------------------------

customer_gap = (
    order_dates
    .groupby("Customer ID")["Purchase_Gap_Days"]
    .mean()
    .reset_index()
)

customer_gap.columns = [
    "Customer ID",
    "Average_Purchase_Gap_Days"
]

# Merge with customer dataset
customer_df = customer_df.merge(
    customer_gap,
    on="Customer ID",
    how="left"
)

# -----------------------------------
# 17. Fill customers with only one order
# -----------------------------------

customer_df["Average_Purchase_Gap_Days"] = (
    customer_df["Average_Purchase_Gap_Days"]
    .fillna(0)
)

print("\nAverage Purchase Gap:")
print(
    customer_df
    .groupby("Churn")["Average_Purchase_Gap_Days"]
    .mean()
    .round(2)
)