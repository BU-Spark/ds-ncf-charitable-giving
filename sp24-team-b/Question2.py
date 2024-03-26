"""
Questions to be answered:
What nonprofits have received grants and where are they based (geo? 
What recipients and Who is giving to nonprofits with recipient subject codes or population served codes corresponding to African and Latin American descent?
"""

import pandas as pd
  
Grants = pd.read_csv('Data\Grants.csv', low_memory=False)

african_descent_code = 'PE030000'
latin_american_descent_code = 'PE050000'

# Nonprofits that have received grants and their locations
nonprofits_received_grants = Grants[['recip_name', 'recip_city', 'recip_state', 'recip_country']].drop_duplicates()

print(nonprofits_received_grants.head(10))

# Recipients serving populations of African and Latin American descent
recipients_serving_specific_populations = Grants[
    (Grants['recip_subject_code'].str.contains(african_descent_code)) | 
    (Grants['recip_population_code'].str.contains(latin_american_descent_code)) |
    (Grants['recip_subject_code'].str.contains(latin_american_descent_code)) | 
    (Grants['recip_population_code'].str.contains(african_descent_code))
][['recip_name', 'recip_city', 'recip_state', 'recip_country', 'gm_name', 'recip_name']].drop_duplicates()

print(recipients_serving_specific_populations.head(10))