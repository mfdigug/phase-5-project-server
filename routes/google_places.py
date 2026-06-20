import os
import requests
import uuid
from flask import jsonify, make_response, request, session, redirect, url_for
from flask_restful import Resource
from app import db
from sqlalchemy.exc import IntegrityError
from models import Restaurant, UserRestaurant

API_KEY = os.getenv("GOOGLE_API_KEY")
BASE_URL = "https://places.googleapis.com/v1"

def infer_cuisines_from_types(types): 
    cuisine_map = {
        "chinese_restaurant": "Chinese",
        "italian_restaurant": "Italian",
        "korean_restaurant": "Korean",
        "japanese_restaurant": "Japanese",
        "thai_restaurant": "Thai",
        "indian_restaurant": "Indian",
        "mexican_restaurant": "Mexican",
        "vietnamese_restaurant": "Vietnamese",
        "greek_restaurant": "Greek",

        "lebanese_restaurant": "Lebanese",
        "turkish_restaurant": "Turkish",
        "middle_eastern_restaurant": "Middle Eastern",

        "pakistani_restaurant": "Pakistani",
        "afghani_restaurant": "Afghani",

        "french_restaurant": "French",
        "spanish_restaurant": "Spanish",

        "american_restaurant": "American",
        "brazilian_restaurant": "Brazilian",

        "malaysian_restaurant": "Malaysian",
        "indonesian_restaurant": "Indonesian",

        "seafood_restaurant": "Seafood",
        "vegetarian_restaurant": "Vegetarian",
        "vegan_restaurant": "Vegan",

        "mediterranean_restaurant": "Mediterranean",
        "asian_restaurant": "Asian",
        "barbecue_restaurant": "Barbecue",
        "brunch_restaurant": "Brunch",
        "breakfast_restaurant": "Breakfast",
        "cafe": "Cafe",
        "coffee_shop": "Cafe",
        "sushi_restaurant": "Japanese",
        "steak_house": "Steakhouse",
        "hamburger_restaurant": "Burgers",
        "pizza_restaurant": "Pizza",
        "fast_food_restaurant": "Fast Food",
        "meal_takeaway": "Takeaway",
        "bakery": "Bakery",
        "dessert_shop": "Dessert",
        "ice_cream_shop": "Dessert",
        "bar": "Bar",
        "pub": "Pub",
        "wine_bar": "Wine Bar",
    }

    cuisines = []

    for place_type in types:
        cuisine = cuisine_map.get(place_type)

        if cuisine and cuisine not in cuisines:
            cuisines.append(cuisine)

        if len(cuisines) == 3:
            break

    return cuisines or ["Restaurant"]


class Autocomplete(Resource):
    def get(self):
        user_input = request.args.get("input")
        lat = request.args.get("lat")
        lng = request.args.get("lng")

        if not user_input or user_input.strip() == "":
            return {"error": "input required"}, 400
        
        session_token = request.args.get("sessionToken")

        if not session_token:
            session_token = str(uuid.uuid4())
        
        url = f"{BASE_URL}/places:autocomplete"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": (
                "suggestions.placePrediction.placeId,"
                "suggestions.placePrediction.text,"
                "suggestions.placePrediction.structuredFormat,"
                "suggestions.placePrediction.types"
            )
        }

        body = {
            "input": user_input,
            "sessionToken": session_token
        }

        if lat and lng:
            body["locationBias"] = {
                "circle": {
                    "center": {
                        "latitude": float(lat),
                        "longitude": float(lng)
                    },
                    "radius": 10000
                }
            }
        
        body["languageCode"] = "en"
        body["regionCode"] = "AU"
        
        autocomplete_type = request.args.get("type", "restaurant")

        if autocomplete_type == "location":
            body["includedPrimaryTypes"] = ["locality", "sublocality", "administrative_area_level_2"]
        else:
            body["includedPrimaryTypes"] = ["restaurant", "cafe", "bakery", "meal_takeaway"]
        
        res = requests.post(url, json=body, headers=headers)

        if res.status_code != 200:
            print("GOOGLE AUTOCOMPLETE ERROR:", res.text)
            return {"error": "Google API failed"}, 500

        data = res.json()

        if "error" in data:
            return {"error": data["error"]}, 500

        suggestions = data.get("suggestions", [])

        results = [
            {
                "place_id": s["placePrediction"]["placeId"],
                "description": s["placePrediction"]["text"]["text"],
            }
            for s in suggestions
        ]

        return {"results": results}, 200




class PlaceDetails(Resource):
    def get(self, place_id):
        url = f"{BASE_URL}/places/{place_id}"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": (
                "id,"
                "displayName,"
                "formattedAddress,"
                "rating,"
                "priceLevel,"
                "types,"
                "location,"
                "photos.name,"
                "websiteUri,"
                "googleMapsUri"
            )
        }

        res = requests.get(url, headers=headers)
        data = res.json()
        print("PLACE TYPES:", data.get("types"))

        

        photos = data.get("photos") or []
        photos = photos[:5]

        return {
            "id": data.get("id"),
            "name": data.get("displayName", {}).get("text"),
            "address": data.get("formattedAddress"),
            "rating": data.get("rating"),
            "priceLevel": data.get("priceLevel"),
            "types": data.get("types", []),
            "cuisineTags": infer_cuisines_from_types(data.get("types", [])),
            "photos": photos,
            "website": data.get("websiteUri"),
            "mapsLink": data.get("googleMapsUri"),
            "location": data.get("location")
        }, 200



class Photo(Resource):
    def get(self, photo_name):
        
        try:
            url = f"{BASE_URL}/{photo_name}/media"

            print("PHOTO URL:", url)

            params = {
                "maxWidthPx": 400,
                "key": API_KEY
            }

            res = requests.get(url, params=params, stream=True)

            response = make_response(res.content)
            response.headers.set("Content-Type", res.headers.get("Content-Type", "image/jpeg"))

            return response
        
        except Exception as e:
            print("PHOTO ERROR:", str(e))
            return {"error": str(e)}, 500




class Places(Resource):
    def get(self):
        location = request.args.get("location")
        # keyword = request.args.get("keyword", "")

        if not location or location.strip() == "":
            return {"error": "location is required (lat,lng)"}, 400
        
        try:
            lat, lng = map(float, location.split(","))
        except ValueError:
            return {"error": "location must be in format lat,lng"}, 400
        
        url = f"{BASE_URL}/places:searchNearby"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "places.name,places.displayName,places.rating,places.formattedAddress"
        }

        body = {
            "maxResultCount": 10,
            "includedTypes": ["restaurant"],
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lng
                    },
                    "radius": 1500
                }
            }
        }

        response = requests.post(url, json=body, headers=headers)
        data = response.json()
        
        if "error" in data:
            print("GOOGLE ERROR:", data["error"])
            return {"error": data["error"]}, 500
        
        print("NEARBY RESPONSE:", data)

        places = data.get("places", [])

        results = [
            {
                "place_id": p["name"],
                "name": p["displayName"]["text"],
                "rating": p.get("rating"),
                "address": p.get("formattedAddress")
            }
            for p in places
        ]

        return {"results": results}, 200
    
