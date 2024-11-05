import requests
import json


def fetch_data():
    url = "https://www.electionreturns.pa.gov/api/ElectionReturn/GET?methodName=GetSummaryData&electionid=undefined&electiontype=undefined&isactive=1"

    try:
        response = requests.get(url)
        response.raise_for_status()

        try:
            # The API returns double-encoded JSON
            data = json.loads(json.loads(response.text))
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return None

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def process_data(data):
    if data is None:
        return None

    try:
        results = {
            "counted": {"republican": 0, "democrat": 0},
            "exit_poll": {"republican": 0, "democrat": 0},
            "reporting": 0,
            "called": False,
        }

        # Extract presidential race data
        election_data = data.get("Election", {})
        presidential_data = election_data.get("President of the United States", [])

        if not presidential_data:
            print("No presidential race data found")
            return None

        statewide_data = presidential_data[0].get("Statewide", [])

        # Process votes for each candidate
        for candidate in statewide_data:
            party = candidate.get("PartyName", "").lower()
            try:
                votes = int(candidate.get("Votes", 0))
            except (ValueError, TypeError):
                votes = 0

            if party == "rep":
                results["counted"]["republican"] = votes
            elif party == "dem":
                results["counted"]["democrat"] = votes

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
