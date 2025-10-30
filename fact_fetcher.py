import requests
import json
import os

# --- Configuration ---
API_URL = "https://uselessfacts.jsph.pl/random.json?language=en" # Assuming this is your API
FACTS_FILE = "fact_archive.json"

# --- Function 1: Fetching (Your refactored code) ---
def fetch_fact_from_api(api_url: str) -> dict | None:
    """
    Fetches a random fact from the API.
    Returns the fact as a dictionary on success, or None on failure.
    """
    print("\n📡 Fetching a new fact from the API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This handles network errors (4xx/5xx)
        fact_data = response.json()
        
        # 💡 We return the entire dictionary, not just the text. This is better for duplicate checking!
        if "text" in fact_data:
            print(f"✔️ Fact Retrieved: \"{fact_data['text']}\"")
            return fact_data
        else:
            print("⚠️ API response did not contain 'text' field.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching fact from API: {e}")
        return None

# --- Function 2: Loading ---
def load_facts(filename: str) -> list:
    """Loads the list of facts from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # Returns an empty list if the file doesn't exist yet

# --- Function 3: Saving ---
def save_facts(filename: str, facts: list):
    """Saves the list of facts to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(facts, f, indent=4)
    print(f"✅ Successfully saved archive. Total facts: {len(facts)}")

# --- Function 4: Duplicate Checking ---
def is_duplicate(new_fact: dict, existing_facts: list) -> bool:
    """Checks if a new fact dictionary is already in the list of existing facts."""
    return new_fact in existing_facts

# --- Main Program Logic ---
def main():
    """Main function to orchestrate the fact collector."""
    print("🚀 Starting the Digital Fact Collector...")

    # STEP 1: Load existing facts. On the first run, this will be an empty list [].
    fact_archive = load_facts(FACTS_FILE)
    print(f"Found {len(fact_archive)} facts in the local archive.")

    # STEP 2: Fetch a new fact using your refactored function.
    new_fact = fetch_fact_from_api(API_URL)

    # STEP 3: Process the fact ONLY IF the fetch was successful.
    if new_fact:
        # STEP 4: Check for duplicates.
        if not is_duplicate(new_fact, fact_archive):
            print("💡 This is a new fact! Adding to the archive.")
            fact_archive.append(new_fact)
            save_facts(FACTS_FILE, fact_archive)
        else:
            print("⚠️ This fact is already in the archive. Skipping.")
    else:
        print("Could not process fact, as fetching failed.")
    
    print("\n✨ Process complete.")

# --- Script Execution ---
if __name__ == "__main__":
    main()