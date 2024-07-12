import pandas as pd
jobber = pd.read_excel("Z:\Jobber\VGOR_Jobber_JULY_2024_v2.0.xlsx", sheet_name=1, header=0)
add = pd.read_excel("Z:\Jobber\Top_100_Part_and_all_2023-2024_Part(1).xlsx", sheet_name=2, header=0)
add2 = pd.read_excel("Z:\Jobber\Top_100_Part_and_all_2023-2024_Part(1).xlsx", sheet_name=0, header=2)
compiled = pd.read_excel('Z:\Jobber\VGOR_Jobber_JULY_2024_v2.0.xlsx',sheet_name=4, header=2)

# Initialize an empty DataFrame to store the results
matched_rows = pd.DataFrame()

# Convert to string and fill empty cells with '' (empty string)
add['Sub'] = add['Sub'].astype(str).fillna('')
#jobber['Part Number'] = jobber['Part Number'].astype(str).fillna('')

# Iterate over each substring in the 'Sub' column of the 'add' DataFrame
for sub in add['Sub']:
    # Filter rows in the 'jobber' DataFrame where 'Part Number' contains the substring
    matched = jobber[jobber['Part Number'].str.contains(sub, na=False)]
    
    # Append the matched rows to the results DataFrame
    matched_rows = pd.concat([matched_rows, matched])

# Reset the index of the result DataFrame
matched_rows.reset_index(drop=True, inplace=True)

# Filter out rows that contain 'VGRBG' and keep 'VGRB'
filtered_rows = matched_rows[~matched_rows['Part Number'].str.contains("VGRBG", na=False)]

# Print the matched rows
print(filtered_rows.head())

# Save the matched rows to an Excel file
filtered_rows.to_excel('VGRB.xlsx', index=False)

# Convert columns to strings and handle NaN values
add['Sub2'] = add['Sub2'].astype(str).fillna('')
add['Name or Series2'] = add['Name or Series2'].astype(str).fillna('')
jobber['Part Number'] = jobber['Part Number'].astype(str).fillna('')
jobber['Name or Series'] = jobber['Name or Series'].astype(str).fillna('')

# Initialize an empty DataFrame to store the matched rows
matched_rows = pd.DataFrame()

# Iterate over each pair of substrings in the 'Sub2' and 'Name or Series2' columns of the 'add' DataFrame
for sub2, name_or_series2 in zip(add['Sub2'], add['Name or Series2']):
    # Filter rows in the 'jobber' DataFrame where 'Part Number' contains the substring 'sub2' 
    # and 'Name or Series' contains the substring 'name_or_series2'
    matched = jobber[jobber['Part Number'].str.contains(sub2, na=False) & 
                     jobber['Name or Series'].str.contains(name_or_series2, na=False)]
    
    # Append the matched rows to the results DataFrame
    matched_rows = pd.concat([matched_rows, matched])

# Reset the index of the result DataFrame
matched_rows.reset_index(drop=True, inplace=True)

# Print the matched rows
print(matched_rows)

# Save the matched rows to an Excel file
matched_rows.to_excel('matched_rows_dual_criteria.xlsx', index=False)


### Left merging to get the rest of unselected data from jobber
# Drop the column Top 100 bc it is not in both df. Merge the two DataFrames on all columns and use the indicator to mark the presence of rows
#jobber = jobber.drop(columns=['Top 100'])
merged_df = jobber.merge(compiled, on=list(jobber.columns), how='left', indicator=True)

# Filter the rows that are only in the 'jobber' DataFrame
unselected = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge']).reset_index(drop=True)
unselected.drop_duplicates(ignore_index=True)

unselected.to_excel('Notinjobber.xlsx', index=False)
