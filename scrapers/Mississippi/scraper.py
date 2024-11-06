import requests
import json


def fetch_data():
    url = "https://embed-api.ddhq.io/v2/races/52817"

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://e.ddhq.io",
        "priority": "u=1, i",
        "referer": "https://e.ddhq.io/",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def process_data(data):
    results = {
        "counted": {"republican": 0, "democrat": 0},
        "exit_poll": {"republican": 0, "democrat": 0},
        "reporting": 0,
        "called": False,
    }

    if not data:
        return results

    try:
        # Extract vote counts from the response
        race = data
        candidates = race.get("candidates", [])
        print(f"Title: {race.get('title')}")

        for candidate in candidates:
            party = candidate.get("party_name", "").lower()
            votes = int(candidate.get("votes", 0))

            if party == "republican":
                results["counted"]["republican"] = votes
            elif (
                party == "democratic"
            ):  # Note: API might use 'democratic' instead of 'democrat'
                results["counted"]["democrat"] = votes

        # Get reporting percentage if available
        results["reporting"] = (
            race.get("topline_results", {})
            .get("estimated_votes", {})
            .get("percent", 0.0)
        )
        # Check if race is called
        results["called"] = race.get("called", False)

    except Exception as e:
        print(f"Error processing data: {e}")

    return results


def main():
    data = fetch_data()
    results = process_data(data)

    # Save to latest.json
    try:
        with open("latest.json", "w") as f:
            json.dump(results, f, indent=2)
    except IOError as e:
        print(f"Error saving results: {e}")


if __name__ == "__main__":
    main()
