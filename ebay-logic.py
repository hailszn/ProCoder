import pandas as pd
jobber = pd.read_excel('Z:\Jobber\VGOR_Jobber_JULY_2024_v2.0.xlsx', sheet_name=0, header=2)
jobberdf = jobber[['Part Number','Make','Model','Start Year','End Year','Submodel']]

ymmsr = pd.read_excel("Z:\Hao\jobace\AcePartType.xlsx", sheet_name=1, header=0)
ymmsrVar = ymmsr[ymmsr["Region"] == "United States"][['YearID','Make','Model','SubModel','Region']]

part_numbers = jobberdf['Part Number']
makes = jobberdf['Make']
models = jobberdf['Model']

# List to store the results
results = []

for part_number, make, model in zip(part_numbers, makes, models):
    matches = jobberdf[(jobberdf['Part Number'] == part_number) & 
                       (jobberdf['Make'] == make) & 
                       (jobberdf['Model'] == model)]
    if not matches.empty:
        results.append(matches[['Part Number', 'Start Year', 'End Year', 'Make', 'Model']])
    else:
        # If combination is not found, append a row with NaN values for the rest
        results.append(pd.DataFrame({
            'Part Number': [part_number],
            'Start Year': [None],
            'End Year': [None],
            'Make': [make],
            'Model': [model]
        }))

# Concatenate all results into a single DataFrame
result_df = pd.concat(results, ignore_index=True)
print(result_df)

def expand_year_range(df):
    # List to store the expanded rows
    expanded_rows = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        start_year = row['Start Year']
        end_year = row['End Year']

        # If start year and end year are not NaN
        if pd.notna(start_year) and pd.notna(end_year):
            # Iterate over each year in the range (inclusive)
            for year in range(int(start_year), int(end_year) + 1):
                # Create a new row with the current year and other column values
                new_row = row.copy()
                new_row['Year'] = year
                expanded_rows.append(new_row)
        else:
            # If start year or end year is NaN, append the row without expanding
            expanded_rows.append(row)

    # Create a new DataFrame from the expanded rows
    expanded_df = pd.DataFrame(expanded_rows).drop(columns=['Start Year', 'End Year'])
    return expanded_df

expanded_result_df = expand_year_range(result_df)
print(expanded_result_df)

# Function to match and expand with submodels
def match_and_expand_submodels(df1, df2):
    # Convert 'Make' columns to lowercase to handle case insensitivity
    df1['Make'] = df1['Make'].str.lower()
    df2['Make'] = df2['Make'].str.lower()
    
    merged_df = pd.merge(df1, df2, left_on=['Year', 'Make', 'Model'], right_on=['YearID', 'Make', 'Model'])
    final_df = merged_df.drop(columns=['YearID'])
        
    # Capitalize the first letter of 'Make' column
    final_df['Make'] = final_df['Make'].str.capitalize()
    
    return final_df

# Match and expand with submodels
final_result_df = match_and_expand_submodels(expanded_result_df, ymmsrVar)
final_unique = final_result_df.drop_duplicates().reset_index(drop=True).drop(columns='Region')
final_unique.rename(columns={'Part Number':'sku','Make':'make','Model':'model','Year':'year','SubModel':'submodel'},inplace=True)
final_unique['year'] = final_unique['year'].astype(int)

final_unique['part'] = ''
final_unique['item_id'] = ''
final_unique['brand_code'] = ''
final_unique['partterminologyname'] = ''
final_unique['notes'] = ''
final_unique['qty'] = ''
final_unique['mfrlabel'] = ''
final_unique['position'] = ''
final_unique['aspiration'] = ''
final_unique['bedlength'] = ''
final_unique['bedtype'] = ''
final_unique['block'] = ''
final_unique['bodynumdoors'] = ''
final_unique['bodytype'] = ''
final_unique['brakeabs'] = ''
final_unique['brakesystem'] = ''
final_unique['cc'] = ''
final_unique['cid'] = ''
final_unique['cylinderheadtype'] = ''
final_unique['cylinders'] = ''
final_unique['drivetype'] = ''
final_unique['enginedesignation'] = ''
final_unique['enginemfr'] = ''
final_unique['engineversion'] = ''
final_unique['enginevin'] = ''
final_unique['frontbraketype'] = ''
final_unique['frontspringtype'] = ''
final_unique['fueldeliverysubtype'] = ''
final_unique['fueldeliverytype'] = ''
final_unique['fuelsystemcontroltype'] = ''
final_unique['fuelsystemdesign'] = ''
final_unique['fueltype'] = ''
final_unique['ignitionsystemtype'] = ''
final_unique['liters'] = ''
final_unique['mfrbodycode'] = ''
final_unique['rearbraketype'] = ''
final_unique['rearspringtype'] = ''
final_unique['region'] = ''
final_unique['steeringsystem'] = ''
final_unique['steeringtype'] = ''
final_unique['transmissioncontroltype'] = ''
final_unique['transmissionmfr'] = ''
final_unique['transmissionmfrcode'] = ''
final_unique['transmissionnumspeeds'] = ''
final_unique['transmissiontype'] = ''
final_unique['valvesperengine'] = ''
final_unique['wheelbase'] = ''
column_order = ['sku','part','item_id','brand_code','make','model','year','partterminologyname','notes','qty','mfrlabel','position','aspiration','bedlength','bedtype','block','bodynumdoors','bodytype','brakeabs','brakesystem','cc','cid','cylinderheadtype','cylinders','drivetype','enginedesignation','enginemfr','engineversion','enginevin','frontbraketype','frontspringtype','fueldeliverysubtype','fueldeliverytype','fuelsystemcontroltype','fuelsystemdesign','fueltype','ignitionsystemtype','liters','mfrbodycode','rearbraketype','rearspringtype','region','steeringsystem','steeringtype','submodel','transmissioncontroltype','transmissionmfr','transmissionmfrcode','transmissionnumspeeds','transmissiontype','valvesperengine','wheelbase']
final_unique = final_unique[column_order].reset_index(drop=True)

print(final_unique)
final_unique.to_csv('ebay-logic.csv', index=False)