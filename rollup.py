import requests
import pandas as pd
import sys


def get_bom():
    # Get response from api
    response = requests.get('https://interviewbom.herokuapp.com/bom/', headers={'accept': 'application/json'})

    # Convert response to json
    response_json = response.json()

    # Put the data in a list of dictionaries to make it ready for manipulation
    data = []
    for element in response_json['data']:
        data_dict = {'id': element['id'], 'parent_part_id': element['parent_part_id'], 'part_id': element['part_id'],
                     'quantity': element['quantity']}
        data.append(data_dict)
    return data


# Convert the data from response to DataFrame
df = pd.DataFrame(data=get_bom())

# Replace NaN values with 'Unknown'
fillNa_df = df.fillna('Unknown')

# Group the data in a new df to show results of
df_final = fillNa_df.groupby(['parent_part_id'], as_index=False).agg(quantity=('quantity', 'sum'))


# Convert the DataFrame into Excel
try:
    # Check if argument ends with exel format extension
    if sys.argv[1].endswith('.xlsx'):
        # Save excel file
        df_final.to_excel(sys.argv[1], index=False)
    # Set excel file extension
    else:
        # Save excel file
        df_final.to_excel(sys.argv[1] + '.xlsx', index=False)
# Handle error when no argument is provided
except Exception as e:
    print("Enter a valid name variable for the output.")
    print(e)
