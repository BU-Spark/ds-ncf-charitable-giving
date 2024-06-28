import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the directory and the CSV file

file_path = '/Users/tamiajibade/Desktop/ncf_eda/ncf_eda_data/eda_grants.csv'

# Check if the file exists
if not os.path.isfile(file_path):
    print(f"File not found: {file_path}")
else:
    print(f"File found: {file_path}")

    # List of Boston neighborhoods to be kept separate
    boston_neighborhoods = [
        "Allston", "Back Bay", "Bay Village", "Beacon Hill", "Brighton", "Charlestown", 
        "Chinatown–Leather District", "Dorchester", "Downtown", "East Boston", 
        "Fenway-Kenmore", "Hyde Park", "Jamaica Plain", "Mattapan", "Mission Hill", 
        "North End", "Roslindale", "Roxbury", "South Boston", "South End", 
        "West End", "West Roxbury", "Wharf District"
    ]

    # Load the CSV data into a DataFrame
    df = pd.read_csv(file_path)

    # Exclude Chicago and New York City
    df = df[(df['City'] != 'Chicago') & (df['City'] != 'New York City')]

    # Clean the 'Grant Total Amount' column: replace 'Not Specified' with NaN, remove commas, and convert to numeric
    df['Grant Total Amount'] = df['Grant Total Amount'].replace('Not Specified', pd.NA)
    df['Grant Total Amount'] = df['Grant Total Amount'].str.replace(',', '')
    df['Grant Total Amount'] = pd.to_numeric(df['Grant Total Amount'], errors='coerce')

    # Ensure 'Grant Fiscal Year' is treated as numeric
    df['Grant Fiscal Year'] = pd.to_numeric(df['Grant Fiscal Year'], errors='coerce')

    # Aggregate the data, ensuring Boston neighborhoods are separate
    df['Region'] = df.apply(lambda x: 'Boston Neighborhoods' if x['City'] in boston_neighborhoods else x['Region'], axis=1)

    # Group the data by Grant Fiscal Year, Region, and City, and sum the grant amounts
    grouped_df = df.groupby(['Grant Fiscal Year', 'Region', 'City'])['Grant Total Amount'].sum().reset_index()

    # Save the table to CSV and Excel files
    grouped_df.to_csv('/Users/tamiajibade/Desktop/ncf_eda/grants_by_city_region.csv', index=False)
    grouped_df.to_excel('/Users/tamiajibade/Desktop/ncf_eda/grants_by_city_region.xlsx', index=False)

    # Filter data for the years 2019-2021 for plotting
    df_filtered = df[df['Grant Fiscal Year'].isin([2019, 2020, 2021])]

    # Create a pivot table for plotting the line graph
    pivot_table = df_filtered.pivot_table(index='Grant Fiscal Year', columns=['Region', 'City'], values='Grant Total Amount', aggfunc='sum')

    # Plot 1: Total grant amounts by region over the 2019-2021 timeline
    plt.figure(figsize=(10, 6))
    region_totals = df_filtered.groupby(['Grant Fiscal Year', 'Region'])['Grant Total Amount'].sum().unstack()
    region_totals.plot(kind='line', marker='o')
    plt.title('Total Grant Amounts by Region (2019-2021)')
    plt.xlabel('Year')
    plt.ylabel('Total Grant Amount ($)')
    plt.legend(title='Region')
    plt.grid(True)
    plt.show()

    # Get the top 5 cities of 2019 for each region
    top_cities_2019 = df[df['Grant Fiscal Year'] == 2019].groupby(['Region', 'City'])['Grant Total Amount'].sum().reset_index()
    top_cities_2019 = top_cities_2019.groupby('Region').apply(lambda x: x.nlargest(5, 'Grant Total Amount')).reset_index(drop=True)

    # Plot 2-4: Top 5 cities of 2019 for each region and how they changed over the 2019-2021 timeline
    for region in top_cities_2019['Region'].unique():
        cities = top_cities_2019[top_cities_2019['Region'] == region]['City']
        plt.figure(figsize=(10, 6))
        for city in cities:
            city_data = pivot_table[region][city]
            city_data.plot(kind='line', marker='o', label=city)
        plt.title(f'Top 5 Cities in {region} (2019-2021)')
        plt.xlabel('Year')
        plt.ylabel('Total Grant Amount ($)')
        plt.legend(title='City')
        plt.grid(True)
        plt.show()

    # Display the first few rows of the full grouped table to verify
    print("Grants by City and Region (All Years)")
    print(grouped_df.head(10))
