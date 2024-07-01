import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Load the CSV data into a DataFrame
df = pd.read_csv('/Users/tamiajibade/Desktop/ncf_eda/ncf_eda_data/eda_grants.csv')

# Clean the 'Grant Total Amount' column: replace 'Not Specified' with NaN, remove commas, and convert to numeric
df['Grant Total Amount'] = df['Grant Total Amount'].replace('Not Specified', pd.NA)
df['Grant Total Amount'] = df['Grant Total Amount'].str.replace(',', '')
df['Grant Total Amount'] = pd.to_numeric(df['Grant Total Amount'], errors='coerce')

# List of Boston neighborhoods
boston_neighborhoods = [
    "Allston", "Back Bay", "Bay Village", "Beacon Hill", "Brighton", "Charlestown", 
    "Chinatown–Leather District", "Dorchester", "Downtown", "East Boston", "Fenway-Kenmore", 
    "Hyde Park", "Jamaica Plain", "Mattapan", "Mission Hill", "North End", "Roslindale", 
    "Roxbury", "South Boston", "South End", "West End", "West Roxbury", "Wharf District"
]

# Map Boston neighborhoods to "Boston"
df['City'] = df['City'].apply(lambda x: 'Boston' if x in boston_neighborhoods else x)

# Define a list of cities to exclude (e.g., out-of-state cities)
exclude_cities = ['Chicago', 'New York City']

# Filter out the entries from the cities to exclude
df_filtered = df[~df['City'].isin(exclude_cities)]

# Group the data by City and Region
city_distribution = df_filtered.groupby('City')['Grant Total Amount'].sum().sort_values(ascending=False).head(10)
region_distribution = df_filtered.groupby('Region')['Grant Total Amount'].sum().sort_values(ascending=False)

# Get the top 5 cities for each region
top_cities_per_region = df_filtered.groupby(['Region', 'City'])['Grant Total Amount'].sum().reset_index()
top_cities_per_region = top_cities_per_region.sort_values(['Region', 'Grant Total Amount'], ascending=[True, False])
top_cities_per_region = top_cities_per_region.groupby('Region').head(5)

# Function to add values on top of bars
def add_values_on_bars(ax):
    for p in ax.patches:
        ax.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 9), textcoords='offset points')

# Plot for grants distribution by City (Top 10)
plt.figure(figsize=(14, 7))
ax1 = city_distribution.plot(kind='bar', color='skyblue')
plt.title('Top 10 Cities by Total Grant Amount (Controlled for Out-of-State Entries)')
plt.xlabel('City')
plt.ylabel('Total Grant Amount')
plt.xticks(rotation=90)
ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:,.0f}'))
add_values_on_bars(ax1)
plt.show()

# Plot for grants distribution by Region
plt.figure(figsize=(14, 7))
ax2 = region_distribution.plot(kind='bar', color='orange')
plt.title('Grants Distribution by Region')
plt.xlabel('Region')
plt.ylabel('Total Grant Amount')
plt.xticks(rotation=90)
ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:,.0f}'))
add_values_on_bars(ax2)
plt.show()

# Plot for top 5 cities in each region
regions = top_cities_per_region['Region'].unique()
for region in regions:
    cities = top_cities_per_region[top_cities_per_region['Region'] == region]
    plt.figure(figsize=(14, 7))
    ax3 = cities.plot(kind='bar', x='City', y='Grant Total Amount', legend=False, color='lightgreen')
    plt.title(f'Top 5 Cities in {region} by Grant Amount')
    plt.xlabel('City')
    plt.ylabel('Total Grant Amount')
    plt.xticks(rotation=90)
    ax3.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    add_values_on_bars(ax3)
    plt.show()
