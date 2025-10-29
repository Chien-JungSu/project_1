# fact_fetcher.py

import requests
import json

def fetch_random_fact():
    """
    Connects to the useless-facts API, fetches a random fact, and displays it.
    """
    api_url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    print("🚀 Connecting to the Fact Stream...")

    try:
        # Make the GET request to the API
        response = requests.get(api_url)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # Parse the JSON response into a Python dictionary
        fact_data = response.json()
        
        # Extract the fact text
        fact_text = fact_data.get("text")
        
        if fact_text:
            print("\n✅ Fact Retrieved Successfully!")
            print("---------------------------------")
            print(f"💡 FACT: {fact_text}")
            print("---------------------------------")
        else:
            print("⚠️ Could not find the fact text in the API response.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Could not connect to the API. Please check your internet connection. Details: {e}")
    except json.JSONDecodeError:
        print("❌ Error: Failed to parse the response from the API.")

if __name__ == "__main__":
    fetch_random_fact()