import os 
import sys
import requests

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



body = os.environ.keys()
print(body)
print(sys.argv)

with open('ouput.txt','w') as f:
    f.write(str(body))
    f.write('\n\n')
    f.write(str(sys.argv))
    f.write('\n\n')
    f.write(str(os.env))


try:
  os.mkdir(sys.argv[1])
  os.system(f'touch {sys.argv[1]+"test"}')
  print(sys.argv[1]+'yay')

except Exception as err: 
  print('FAILED',err)


'''
env 
GITHUB_WORKSPACE = directory location
same as 'PWD': '/home/runner/work/GithubActionTest/GithubActionTest'

'GITHUB_TRIGGERING_ACTOR': 'wolfiex',


'GITHUB_REPOSITORY': 'cmip-ipo-internal/GithubActionTest'

'''

