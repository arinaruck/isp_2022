from email import message
import requests
from bs4 import BeautifulSoup


user = 'james@bond.mi5'
first_name = 'james'

r = requests.get(f"http://localhost:5001/messages?id=100' OR mail='{user}")
soup = BeautifulSoup(r.text, 'html.parser')
messages = soup.find_all('blockquote', {'class': 'blockquote'})
for message in messages:
    print(message.text)