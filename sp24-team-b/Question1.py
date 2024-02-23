import pandas as pd
  
base_bundle = pd.read_csv('sp24-team-b\Base_bundle.csv', low_memory=False)


# Step 1: Filter organizations with recipient subject codes for people of African and Latin American descent
filtered_nonProfit = base_bundle[base_bundle['pcs_population'].str.contains('PE030000|PE050000', na=False)]
print(filtered_nonProfit.head(10))


# Step 2: Calculate total contributions and revenue
# total_contributions = filtered_nonProfit['CONTRIB_ALL'].sum()

# prin"Filtered_non profit" + t(filtered_nonProfit['total_revenue'])
 
total_revenue = filtered_nonProfit['total_revenue'].sum()

# Display the results
# print("Total Contributions of nonprofit organizations for African and Latin American descent:", total_contributions)
print("Total Revenue of nonprofit organizations for African and Latin American descent:", total_revenue)


