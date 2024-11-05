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

    response = requests.get(url, headers=headers)
    return response.json()


def process_data(data):
    # Initialize results in the required format
    results = {
        "counted": {"republican": 0, "democrat": 0},
        "exit_poll": {"republican": 0, "democrat": 0},
        "reporting": 0,
        "called": False,
    }

    # Extract the voting data
    for candidate in data["candidates"]:
        if candidate["party_name"] == "Republican":
            results["counted"]["republican"] = candidate["votes"]
        elif candidate["party_name"] == "Democratic":
            results["counted"]["democrat"] = candidate["votes"]

    # Get reporting percentage
    if data["topline_results"]["precincts"]["total"] > 0:
        results["reporting"] = data["topline_results"]["precincts"]["percent"]

    # Get called status
    results["called"] = data["called"]

    return results


def main():
    data = fetch_data()
    results = process_data(data)

    # Save to latest.json
    with open("latest.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
