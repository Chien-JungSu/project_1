# fact_automator.py

import requests
import json
import time
import os

# --- Configuration ---
API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"
JSON_FILE = "facts.json"
FETCH_INTERVAL_SECONDS = 30 # 30 seconds for testing. Change to a larger value (e.g., 3600 for 1 hour) for long-term use.

def load_facts():
    """Loads the list of facts from the JSON file."""
    # 💡 If the file doesn't exist, start with an empty list.
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            # Handle case where the file is empty
            if os.path.getsize(JSON_FILE) == 0:
                return []
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"⚠️ Warning: Could not read or parse {JSON_FILE}. Starting with an empty list.")
        return []

def save_facts(facts):
    """Saves the list of facts to the JSON file."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(facts, f, indent=4)

def fetch_fact():
    """Fetches a single fact from the API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Raises an error for bad responses (4xx or 5xx)
        fact_data = response.json()
        return fact_data['text']
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching fact from API: {e}")
        return None

def is_fact_unique(fact, existing_facts):
    """Checks if a fact is already in the list of existing facts."""
    for existing_fact in existing_facts:
        if existing_fact['text'] == fact:
            return False
    return True

def main():
    """Main function to run the automated fact collection process."""
    print("🚀 Starting the Digital Fact Collector...")
    print(f"Configuration: Fetching a new fact every {FETCH_INTERVAL_SECONDS} seconds.")
    print(f"Data will be stored in: {JSON_FILE}")
    print("Press CTRL+C to stop the script.")

    fact_counter = 0

    while True:
        print("\n----------------------------------------")
        print("⚡ Kicking off a new cycle...")

        # 1. Fetch a new fact
        print("1. Fetching a new fact from the API...")
        new_fact_text = fetch_fact()

        if new_fact_text:
            # 2. Load existing facts
            print("2. Loading existing facts from storage...")
            facts_archive = load_facts()

            # 3. Check for duplicates
            print("3. Checking if the fact is unique...")
            if is_fact_unique(new_fact_text, facts_archive):
                # 4. Add new fact and save
                print("✅ Success! New unique fact found. Adding to archive.")
                fact_counter += 1
                new_fact_entry = {
                    "id": len(facts_archive) + 1,
                    "text": new_fact_text,
                    "source": API_URL
                }
                facts_archive.append(new_fact_entry)
                save_facts(facts_archive)
                print(f"Total unique facts in archive: {len(facts_archive)}")
            else:
                print("💡 Fact already exists in the archive. Skipping.")

        # 5. Wait for the next interval
        print(f"4. Waiting for {FETCH_INTERVAL_SECONDS} seconds before next run...")
        time.sleep(FETCH_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
