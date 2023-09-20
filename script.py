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


# ... (previous code)

# Function to fetch more details about a restaurant
def get_restaurant_details(place_id):
    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,photos',
        'key': API_KEY,
    }

    response = requests.get(details_url, params=params)
    details_data = response.json()
    if 'result' in details_data:
        restaurant_details = details_data['result']
        photo_reference = None

        # Get the first photo reference (if available)
        if 'photos' in restaurant_details and len(restaurant_details['photos']) > 0:
            photo_reference = restaurant_details['photos'][0]['photo_reference']

        return {
            'name': restaurant_details.get('name', ''),
            'address': restaurant_details.get('formatted_address', ''),
            'photoReference': photo_reference,
        }
    return None


@app.route('/find-restaurant', methods=['GET'])
def get_random_restaurant():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))

        restaurant_name = find_random_restaurant(lat, lng)

        if restaurant_name:
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
                for restaurant in restaurants:
                    if restaurant['name'] == restaurant_name:
                        place_id = restaurant['place_id']
                        restaurant_details = get_restaurant_details(place_id)
                        if restaurant_details:
                            return jsonify({"restaurant": restaurant_details})
                        else:
                            return jsonify({"error": "Restaurant details not found."})
                return jsonify({"error": "Restaurant not found in results."})
            else:
                return jsonify({"error": "No restaurants found nearby."})
        else:
            return jsonify({"error": "No restaurants found nearby."})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/get-api-key', methods=['GET'])
def get_api_key():
    return jsonify({"apiKey": API_KEY})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
