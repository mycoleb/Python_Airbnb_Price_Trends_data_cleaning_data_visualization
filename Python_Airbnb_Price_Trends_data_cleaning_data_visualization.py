#Importing the data
#Cleaning the price column
#Calculating the average price
#Comparing costs to the private rental market
#Cleaning the room_type column
#Determining the timeframe of the data
#Joining the DataFrames
#Analyzing listing prices by NYC borough
#Analyzing price range by borough
#Storing the final result

#Task 1 Import
import numpy as np
import pandas as pd
import datetime as dt

# Load airbnb_price.csv, prices
prices = pd.read_csv("data/airbnb_price.csv")

# Load airbnb_room_type.xlsx, xls
xls = pd.ExcelFile("data/airbnb_room_type.xlsx")

# Parse the first sheet from xls, room_types
room_types = xls.parse(0)

# Load airbnb_last_review.tsv, reviews
reviews = pd.read_csv("data/airbnb_last_review.tsv", sep="\t")

# Task 2. Cleaning the price column

# Remove whitespace and string characters from prices column
prices["price"] = prices["price"].str.replace(" dollars", "")

# Convert prices column to numeric datatype
prices["price"] = pd.to_numeric(prices["price"])

# Task 3. Calculate average prices

# Subset prices for listings costing $0, free_listings
free_listings = prices["price"] == 0

# Update prices by removing all free listings from prices
prices = prices.loc[~free_listings]

# Calculate the average price, avg_price
avg_price = round(prices["price"].mean(), 2)

# Task 4. Compare airbnb costs to the private rental market
# Add a new column to the prices DataFrame, price_per_month
prices["price_per_month"] = prices["price"] * 365 / 12

# Calculate average_price_per_month
average_price_per_month = round(prices["price_per_month"].mean(), 2)
difference = round((average_price_per_month - 3100),2)
# Task 5. Clean the room_type column

# Convert the room_type column to lowercase
room_types["room_type"] = room_types["room_type"].str.lower()

# Update the room_type column to category data type
room_types["room_type"] = room_types["room_type"].astype("category")

# Create the variable room_frequencies
room_frequencies = room_types["room_type"].value_counts()

# Task 6. Determine time frame of Airbnb listings

# Change the data type of the last_review column to datetime
reviews["last_review"] = pd.to_datetime(reviews["last_review"])

# Create first_reviewed that contains the earliest review date
first_reviewed = reviews["last_review"].dt.date.min()

# Create last_reviewed variable that contains the most recent review date
last_reviewed = reviews["last_review"].dt.date.max()

# Task 7 Join dataframes

# Merge prices and room_types to create rooms_and_prices
rooms_and_prices = prices.merge(room_types, how="outer", on="listing_id")

# Merge rooms_and_prices with the reviews DataFrame to create airbnb_merged
airbnb_merged = rooms_and_prices.merge(reviews, how="outer", on="listing_id")

# Drop missing values from airbnb_merged
airbnb_merged.dropna(inplace=True)

#Task 8 analyze NYC prices for each borough

# Extract information from the nbhood_full column and store as a new column, borough
airbnb_merged["borough"] = airbnb_merged["nbhood_full"].str.partition(",")[0]

# Group by borough and calculate summary statistics
boroughs = airbnb_merged.groupby("borough")["price"].agg(["sum", "mean", "median", "count"])

# Round boroughs to 2 decimal places, and sort by mean in descending order
boroughs = boroughs.round(2).sort_values("mean", ascending=False)
# Task 9 Price range of each borough

# Create labels for the price range, label_names
label_names = ["Budget", "Average", "Expensive", "Extravagant"]

# Create the label ranges, ranges
ranges = [0, 70, 170, 350, np.inf]

# Insert new column, price_range, into DataFrame
airbnb_merged["price_range"] = pd.cut(airbnb_merged["price"], bins=ranges, labels=label_names)

# Use prices_by_borough to calculate frequencies
prices_by_borough = airbnb_merged.groupby(["borough", "price_range"])["price_range"].count()

# Task 10 final result

solution = {'avg_price':avg_price,
            'average_price_per_month': average_price_per_month,  
            'difference':difference,
            'first_reviewed': first_reviewed,
            'last_reviewed': last_reviewed,
            'prices_by_borough':prices_by_borough,
           'room_frequencies':room_frequencies }
print(solution)
