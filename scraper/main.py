from math import dist
import urllib.parse
from bs4 import BeautifulSoup
import requests

user_type = 'personal'


base_url = 'https://divar.ir/s/tehran/real-estate/'

districts = [173, 979]
# convert district to string
districts_str = ','.join(map(str, districts))
districts_encoded = urllib.parse.quote(districts_str)

final_url = f'{base_url}/?districts={districts_encoded}&user_type={user_type}'

# get the final_url with beautifulsoup



def get_html(url):
    response = requests.get(url)
    return response

print(get_html(final_url))

# pip install beautifulsoup4 
