import os 
import sys
import requests
import re
import json
from collections import OrderedDict


URL_TEMPLATE = 'https://api.ror.org/organizations/{}'

def get_ror_data(key):
    """Get ROR data for a given institution name."""
    response = requests.get(URL_TEMPLATE.format(key))

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        err = f"Error: {response.status_code} - {response.text}"
        print(err)
        fail.append(err)
        return None

def parse_ror_data(ror_data):
    """Parse ROR data and return relevant information."""
    if ror_data:

        return {
            "indentifiers": {
                'institution_name': ror_data['name'],
                'aliases': ror_data.get('aliases', []),
                'acronyms': ror_data.get('acronyms', []),
                'labels': [i['label'] for i in ror_data.get('lables', [])],
                'ror': ror_data['id'].split('/')[-1],
                'url': ror_data.get('links', []),
                'established': ror_data.get('established'),
                'type': ror_data.get('types', [])[0] if ror_data.get('types') else None,
            },
            "location": {
                'lat': ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
                'lon': ror_data['addresses'][0].get('lng') if ror_data.get('addresses') else None,
                # 'latest_address': ror_data['addresses'][0].get('line') if ror_data.get('addresses') else None,
                'city': ror_data['addresses'][0].get('city') if ror_data.get('addresses') else None,
            #     'country': ror_data['country']['country_name'] if ror_data.get('country') else None
                'country': list(ror_data['country'].values())  if ror_data.get('country') else None
            },
            "consortiums":[]
            
        }
    else:
        return None


def get_variables(input_string):

    # Regular expression pattern to match variables denoted between **
    pattern = r"\*\*(.*?)\*\*:\s*\"(.*?)\""
    
    # Extract variables and their contents using regular expression
    variables = dict(re.findall(pattern, input_string))
    
    # Print extracted variables
    print(variables)



def get_issue_fields():
    try:
        # Get the path to the GitHub event payload file
        event_path = os.getenv('GITHUB_EVENT_PATH')

        # Read the contents of the event payload file
        with open(event_path, 'r') as file:
            event_data = json.load(file)
            # Extract the entire .issue object
            issue_fields = event_data.get('issue', {})
            return issue_fields
    except Exception as e:
        print(f"FAILED to read the Issue contents: {e}")
        return None

'''
Simialrity algorithm
'''
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, char1 in enumerate(s1):
        current_row = [i + 1]
        for j, char2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (char1 != char2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def similarity_score(s1, s2):
    max_length = max(len(s1), len(s2))
    if max_length == 0:
        return 1.0
    
    distance = levenshtein_distance(s1, s2)
    similarity = 1.0 - (distance / max_length)
    return similarity





if __name__ == '__main__':
    issue_fileds = get_issue_fields()
    body = issue_fields.body
    varaibles = get_variables(body)
    # {'Issuer': 'dan', 'Name': 'York', 'ROR link': 'https://ror.org/04m01e293'} 'ACRONYM'
    print(variables)

    ror_id = variables['ROR'].split('/')[-1]
    ror_data = get_ror_data(ror_id)
    ror = parse_ror_data(ror_data)

    # checks
    name = ror['indentifiers']['institution_name']
    threshold = 0.6
    if similarity_score(name, variables['Name']) < threshold:
        sys.exit(f"FAILED: The names are not similar enough. please confirm. \n Name provided: {variables['Name']} \n ROR given name: {name}")

    filename = '../../institutions.json'
    if os.path.exists(filename):
        data = json.load(open(filename, 'r'))
    else: 
        data = {}

    acronym = variables['Acronym']
    if acronym in data:
        sys.exit(f'FAILED: {acronym} already exists')

    rors = [i['indentifiers']['ror'] for i in data.values()]
    if ror_id in rors:
        where = list(dict.keys())[rors.index(ror_id)]
        sys.exit(f'FAILED: {ror_id} already exists in the list under key "{where}"')


    # final check that acronym already exists in ROR?

    data[acronym] = ror

    # Sort the dictionary by keys alphabetically and maintain order
    data = OrderedDict(sorted(data.items(), key=lambda item: item[0]))

    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)




    
    
