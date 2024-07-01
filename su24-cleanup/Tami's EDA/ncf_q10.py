import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a DataFrame
file_path = '/Users/tamiajibade/Desktop/ncf_eda/ncf_eda_data/eda_grants.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Function to count support strategies
def count_support_strategies(df, column_name):
    strategies_count = {}
    for strategies in df[column_name].fillna('Not Specified'):
        for strategy in strategies.split(';'):
            strategy = strategy.strip()
            if strategy in strategies_count:
                strategies_count[strategy] += 1
            else:
                strategies_count[strategy] = 1
    return strategies_count

# Function to list all unique support strategies
def list_support_strategies(df, column_name):
    unique_strategies = set()
    for strategies in df[column_name].fillna('Not Specified'):
        for strategy in strategies.split(';'):
            unique_strategies.add(strategy.strip())
    return list(unique_strategies)

# Classify strategies into restrictive and non-restrictive
restrictive_strategies = {'Equipment', 'Annual campaigns', 'Land acquisitions', 'Recordings', 'Fiscal sponsorships', 
                          'Data and measurement systems', 'Institutional evaluations', 'Marketing', 'Program expansion',
                          'Board development', 'System and operational improvements', 'Fellowships', 'Capital campaigns',
                          'Volunteer development', 'Program evaluations', 'Research', 'Regulation and administration',
                          'Litigation', 'Conferences and exhibits', 'Research and evaluation', 'Collections acquisitions',
                          'Seed money', 'Building acquisitions', 'Presentations and productions', 'Exchange programs',
                          'Camperships', 'Professorships', 'Financial services', 'Product development', 
                          'Commissioning new works', 'Residencies', 'Capital and infrastructure', 'Translation', 
                          'Grassroots organizing', 'Commodity provision', 'Technical assistance', 'Information and Referral',
                          'Collections management and preservation', 'Exhibitions', 'Product and service development', 
                          'Ethics and accountability', 'Awards, prizes and competitions', 'Emergency funds', 
                          'Curriculum development', 'Information technology', 'Capacity-building and technical assistance',
                          'Conference attendance', 'Work-study grants', 'Debt reduction', 'Building and renovations',
                          'Earned income', 'Policy, advocacy and systems reform', 'Online engagement', 'Endowments', 
                          'Program support', 'Program creation', 'Nonprofit collaborations', 'Systems reform', 
                          'Audience development', 'Scholarships', 'Pilot programs', 'Financial sustainability',
                          'Management and leadership development', 'Fundraising', 'Convening', 'Faculty and staff development',
                          'Product and service delivery', 'Sponsorships', 'Travel awards', 'Grantee relations', 
                          'Performances', 'Publications', 'Online media', 'Program replication', 'Student aid', 
                          'Leadership and professional development'}

non_restrictive_strategies = {'General support', 'Continuing support'}

# Calculate the distribution of support strategies
support_strategy_distribution = count_support_strategies(df, 'Grant Support Strategy')

# Classify the support strategies into restrictive, non-restrictive, and not specified
restrictive_count = sum([count for strategy, count in support_strategy_distribution.items() if strategy in restrictive_strategies])
non_restrictive_count = sum([count for strategy, count in support_strategy_distribution.items() if strategy in non_restrictive_strategies])
not_specified_count = support_strategy_distribution.get('Not Specified', 0)

# Plotting the pie chart
labels = ['Restrictive', 'Non-Restrictive', 'Not Specified']
sizes = [restrictive_count, non_restrictive_count, not_specified_count]
colors = ['#ff9999','#66b3ff', '#99ff99']
explode = (0.1, 0, 0)  # explode the first slice (Restrictive)

plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Distribution of Restrictive, Non-Restrictive, and Not Specified Support Strategies')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the plot
plt.show()

# List all unique support strategies
all_support_strategies = list_support_strategies(df, 'Grant Support Strategy')
print("All Support Strategies:")
print(all_support_strategies)
