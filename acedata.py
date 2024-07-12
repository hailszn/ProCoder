import pandas as pd
#Import and Define Relevant Data Frames and Columns
jobber = pd.read_excel("Z:\Hao\jobace\VGOR_Jobber_JUNE_2024.xlsx", sheet_name=1, header=2)
jobberdf = jobber[['Part Number','Start year','End Year','Make','Model','Aces Part Type']]
part_numbers = jobberdf['Part Number']
makes = jobberdf['Make']
models = jobberdf['Model']

ymmsr = pd.read_excel("Z:\Hao\jobace\AcePartType.xlsx", sheet_name=1, header=0)
ymmsrVar = ymmsr[ymmsr["Region"] == "United States"][['YearID','Make','Model','SubModel','Region']]

PT = pd.read_excel("Z:\Hao\jobace\AcePartType.xlsx", sheet_name="Part Type", skiprows=[3,3], header=2)
PTdf = PT[['Part Type ID','Part Type Description']]

# List to store the results
results = []

for part_number, make, model in zip(part_numbers, makes, models):
    matches = jobberdf[(jobberdf['Part Number'] == part_number) & 
                       (jobberdf['Make'] == make) & 
                       (jobberdf['Model'] == model)]
    if not matches.empty:
        results.append(matches[['Part Number', 'Start year', 'End Year', 'Make', 'Model', 'Aces Part Type']])
    else:
        # If combination is not found, append a row with NaN values for the rest
        results.append(pd.DataFrame({
            'Part Number': [part_number],
            'Start year': [None],
            'End Year': [None],
            'Make': [make],
            'Model': [model],
            'Aces Part Type': [None]
        }))

# Concatenate all results into a single DataFrame
result_df = pd.concat(results, ignore_index=True)


def expand_year_range(df):
    # List to store the expanded rows
    expanded_rows = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        start_year = row['Start year']
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
    expanded_df = pd.DataFrame(expanded_rows).drop(columns=['Start year', 'End Year'])
    return expanded_df

expanded_result_df = expand_year_range(result_df)

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


# Drop duplicated values from PTdf: Part Type Description then Merge final_result_df with PTdf to add Part Type ID
PTdf_unique = PTdf.drop_duplicates(subset=['Part Type Description', 'Part Type ID'])
final_result_with_part_id = pd.merge(
    final_result_df, PTdf_unique, left_on='Aces Part Type', right_on='Part Type Description', how='left')

# Drop the Part Type Description column as it's redundant
final_result_with_part_id = final_result_with_part_id.drop(columns=['Aces Part Type'])

column_order = ['Part Number','Part Type ID','Part Type Description','Year','Make','Model','SubModel']
final_result_with_part_id = final_result_with_part_id[column_order].reset_index(drop=True)

final_result_with_part_id.to_excel('acestest.xlsx')