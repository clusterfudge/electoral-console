import requests
import json


def fetch_data():
    url = "https://embed-api.ddhq.io/v2/races/52815"

    headers = {
        "sec-ch-ua-platform": "macOS",
        "Referer": "https://e.ddhq.io/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None


def process_data(data):
    if data is None:
        return None

    try:
        # Initialize results in the required format
        results = {
            "counted": {"republican": 0, "democrat": 0},
            "exit_poll": {"republican": 0, "democrat": 0},
            "reporting": 0,
            "called": False,
        }

        # Extract the voting data
        candidates = data.get("candidates", [])
        for candidate in candidates:
            party = candidate.get("party_name", "").lower()
            votes = int(candidate.get("votes", 0))

            if party == "republican":
                results["counted"]["republican"] = votes
            elif party == "democratic":
                results["counted"]["democrat"] = votes

        # Get reporting percentage
        topline = data.get("topline_results", {})
        precincts = topline.get("precincts", {})
        total_precincts = precincts.get("total", 0)

        if total_precincts > 0:
            results["reporting"] = precincts.get("percent", 0)

        # Get called status
        results["called"] = data.get("called", False)

        return results

    except Exception as e:
        print(f"Error processing data: {e}")
        return None


def main():
    data = fetch_data()
    results = process_data(data)

    if results is not None:
        try:
            # Save to latest.json
            with open("latest.json", "w") as f:
                json.dump(results, f, indent=2)
        except IOError as e:
            print(f"Error saving results: {e}")


if __name__ == "__main__":
    main()
