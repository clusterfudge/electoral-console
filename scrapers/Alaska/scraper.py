import requests
import json
import pandas as pd
import io
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_data():
    url = "https://www.elections.alaska.gov/results/24GENR/ENRbyPrecinct.csv"

    headers = {
        "Referer": "https://www.elections.alaska.gov/election-results/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    response = requests.get(url, headers=headers, verify=False)

    # Read CSV directly from response content
    df = pd.read_csv(io.StringIO(response.text))

    return df


def process_data(df):
    # Find presidential race data
    pres_data = df[df["Contest_title"].str.contains("President", na=False, case=False)]

    # Initialize results in the required format
    results = {
        "counted": {"republican": 0, "democrat": 0},
        "exit_poll": {"republican": 0, "democrat": 0},
        "reporting": 0,
        "called": False,
    }

    # Process votes for each candidate
    for _, row in pres_data.iterrows():
        # Get total votes for each candidate
        if "Trump" in row["candidate_name"]:
            results["counted"]["republican"] += row["total_votes"]
        elif "Harris" in row["candidate_name"]:  # Biden's replacement for 2024
            results["counted"]["democrat"] += row["total_votes"]

    # Convert vote counts to integers
    results["counted"]["republican"] = int(results["counted"]["republican"])
    results["counted"]["democrat"] = int(results["counted"]["democrat"])

    return results


def main():
    df = fetch_data()
    results = process_data(df)

    # Save to latest.json
    with open("latest.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
