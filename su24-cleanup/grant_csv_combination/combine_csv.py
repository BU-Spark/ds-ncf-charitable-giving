import pandas as pd

# List of CSV files to combine
filenames = [
    'Grant_Details_2013_2014.csv',
    'Grant_Details_2015.csv',
    'Grant_Details_2016.csv',
    'Grant_Details_2017_2018.csv',
    'Grant_Details_2019_2023.csv'
]

# Create a list of DataFrames
dfs = [pd.read_csv(filename) for filename in filenames]

# Concatenate all DataFrames into one
combined_csv = pd.concat(dfs, ignore_index=True)

# Save the combined CSV to a file
combined_csv.to_csv('Combined_Grant_Details_2013_2023.csv', index=False)