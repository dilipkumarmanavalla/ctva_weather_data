import requests

# Check health of the Service
response = requests.get('http://localhost:5000/health/')
print(response.json())


# Load Data
response = requests.get('http://localhost:5000/load/')
print(response.json())




station_id = 'USC00112193'
date = '19850101'
year = '2001'


# Get Weather Data
response = requests.get('http://localhost:5000/api/weather', params={'station_id': station_id, 'date': date})
print(response.json())

response = requests.get('http://localhost:5000/api/weather', params={'station_id': station_id, 'date': date, 'page': 1, 'per_page': 10})
print(response.json())



# Get Weather Stats Data
response = requests.get('http://localhost:5000/api/weather/stats', params={'station_id': station_id, 'year': year})
print(response.json())

response = requests.get('http://localhost:5000/api/weather/stats', params={'station_id': station_id, 'year': year, 'page': 1, 'per_page': 10})
print(response.json())

