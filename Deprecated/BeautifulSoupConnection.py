import requests
from bs4 import BeautifulSoup

url = 'https://www.immoweb.be/en/classified/apartment/for-sale/boom/2850/20310616'

session = requests.Session()
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
cookies = {'immoweb_session' : 'eyJpdiI6IjVubHc4Q1R3RlpvRXkwaVVWQkdNZ3c9PSIsInZhbHVlIjoiakZGMjViTnVxTmROYm1GU2ZYUU9XR3NLMjJrTG84cmVkYm1NN2tqSWhCWjFHQjJQNmxHdDBZbnhPS1JsdzBzSmtUdmpWOXhOdllaeTdqRWZhZ0k4cWhwQWw5MGVwZVlZVTlDQ0ZWcHNJR3h6aXZEdFNMZVg3UTVnR0tGWHcyK1UiLCJtYWMiOiIxZDg1ZjRhNTkxODlkM2VhN2Y3MzY2NTdmMDRkYTc5NjAzYzY5YWVkNDAyYTFjMDEzMmQ3ZmI1MGYyYWY4MjBlIn0%3D',
                       'XSRF-TOKEN': 'eyJpdiI6IkxwRzIwZFEzMTg5VzJDYWtvWi8zM3c9PSIsInZhbHVlIjoiNERVU1NhdlEzVzBIbkZ4cmV4Z2JMbHN3NjVrRWZUMzg0OWd1MVd3N1E3ckI5aGhIRVlaa2czWnl4QVdvbjJUSTZxMkhGdlA1ZzA1c0xxU1A0N0hlaS8rZnV4TmxldDVIbHNUZDVNNCtpSS9qb2x3enNodFFITFJGTlZEZVVrN2siLCJtYWMiOiI2MTJmZDcxNzkyM2YwMTM1ZjZkZGRjZTM5YjIzMGFmNTNiNDA1NTAyMmE0OWRhMTBlMzQwMDVjZjY3YmMzNmE3In0%3D',
                       '__cf_bm' : 'MoKFFUtnsCnBMVsc_XiGba.KtzFY_Ta1f6UtGsI_7j4-1731414232-1.0.1.1-0sQuyt.MEHq3govqH2hn5G0QTGypm5VhAs_Bbhx8a1jvPdIz6yUY5HZKXWDlbV8WF2w.FVvnEgBOUdzQ46C3Rw'}
session.cookies.update(cookies)

try_request = session.get(url, headers= headers)
html = try_request.content

soup = BeautifulSoup(try_request.content, 'html')
table_rows = soup.find_all('tr', attrs= {'class': 'classified-table__row'})

'Available as of' in table_rows[0].find_all('th')[0]

table_rows[0].find_all('td')[0]