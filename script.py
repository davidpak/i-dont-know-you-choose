from flask import Flask, request, jsonify, render_template
import os
import requests
import random

app = Flask(__name__)

# Get the API key from the environment variable
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if API_KEY is None:
    print("Please set the GOOGLE_PLACES_API_KEY environment variable.")
    exit(1)


# Function to find a random restaurant
def find_random_restaurant(lat, lng):
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': 24140,  # 15 miles in meters
        'type': 'restaurant',
        'key': API_KEY,
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    if 'results' in data:
        restaurants = data['results']
        if restaurants:
            random_restaurant = random.choice(restaurants)
            return random_restaurant['name']
    return None


@app.route('/find-restaurant', methods=['GET'])
def get_random_restaurant():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))

        restaurant_name = find_random_restaurant(lat, lng)

        if restaurant_name:
            return jsonify({"restaurantName": restaurant_name})
        else:
            return jsonify({"error": "No restaurants found nearby."})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
