# Lodgify Assignment – Python Challenge

## Objective

The goal of this challenge is to assess your ability in:

- Python proficiency  
- Logical and analytical thinking  
- Writing clean and maintainable code  
- Data cleaning and transformation
---

## Business Context

**Lodgify** is a SaaS company. Sometimes customers cancel their subscriptions and later return (reactivate).  
In some cases, users cancel their subscription **before the paid period ends**, meaning they remain active for a short time **even without an active subscription**.

---

## Provided Data

Two CSV files are provided:

1. **Subscription History**  
   Snapshots of user subscriptions taken on the **last day of each month**.  
   If a subscription appears as "canceled" on the last day, we assume the user was **canceled for the entire month**.

2. **Booking History**  
   All booking requests, including their statuses (e.g., confirmed, declined, etc.).

---

## Business Analyst Requirements

The goal is to provide a **monthly breakdown** per customer, answering the following:

For **each customer and each month**:

- How many months have passed since their **first subscription month**?
- How many months were they an **active** or **canceled** subscriber?
- How many months have passed since their **last subscription status change**?
- How many **confirmed bookings** did they receive?

### Note on Data Quality

- A customer may have **multiple statuses** in the same month or **missing months** in the timeline.
- In such cases, **use the most recent available status** to fill gaps or resolve duplicates.

---

## Implementation

A Python script processes and merges both datasets, calculates the required metrics, and exports the result as a CSV.
and plot a summary related to the user analysis

**Output File:**
[user_analysis.csv](user_analysis.csv)

**Users Summary Plot:**
![user_analysis.png](user_analysis.png)