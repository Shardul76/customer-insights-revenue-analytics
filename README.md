# Retail360 AI – Customer Lifecycle & Revenue Intelligence Platform

## Project Overview

Retail360 AI is an end-to-end customer analytics project built using Python, SQL, and Power BI.

The project analyzes customer purchasing behavior, identifies churn patterns, and will develop machine learning models to predict customer churn.

## Current Progress

### Phase 1 – Data Understanding
- Loaded the Sample Superstore dataset
- 9,994 transaction records
- 21 variables
- Checked missing values
- Checked duplicate records
- Reviewed numerical statistics

### Phase 2 – Data Cleaning
- Converted Order Date to datetime
- Converted Ship Date to datetime
- Verified data types
- Confirmed dataset quality

### Phase 3 – Customer Analytics
- Created customer-level dataset
- Identified 793 unique customers
- Calculated customer tenure
- Calculated recency
- Calculated total orders
- Calculated total sales
- Calculated total profit
- Calculated average order value
- Analyzed purchase gaps
- Defined a data-driven churn threshold

## Churn Definition

Customers with more than 266 days since their last purchase are classified as churned.

The 266-day threshold is based on the 75th percentile of observed purchase gaps.

## Current Findings

- 793 unique customers
- 136 customers classified as churned
- 657 customers classified as active
- Churn rate: 17.15%
- Churned customers have fewer orders and lower historical sales than active customers
- Average order value is slightly higher among churned customers
- Customer tenure is lower among churned customers

## Tech Stack

- Python
- Pandas
- NumPy
- SQL
- Power BI
- Git/GitHub

## Upcoming Work

- Logistic Regression
- Random Forest
- Model evaluation
- Customer churn probability
- Customer risk segmentation
- Retention recommendations
- Power BI churn dashboard