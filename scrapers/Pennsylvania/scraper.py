import requests
import json


def fetch_data():
    url = "https://www.electionreturns.pa.gov/api/ElectionReturn/GET?methodName=GetSummaryData&electionid=undefined&electiontype=undefined&isactive=1"

    response = requests.get(url)
    return json.loads(json.loads(response.text))


def process_data(data):
    results = {
        "counted": {"republican": 0, "democrat": 0},
        "exit_poll": {"republican": 0, "democrat": 0},
        "reporting": 0,
        "called": False,
    }

    # Extract presidential race data
    presidential_race = data["Election"]["President of the United States"][0][
        "Statewide"
    ]

    # Process votes for each candidate
    for candidate in presidential_race:
        party = candidate["PartyName"].lower()
        votes = int(candidate["Votes"])

        if party == "rep":
            results["counted"]["republican"] = votes
        elif party == "dem":
            results["counted"]["democrat"] = votes

    return results


def main():
    data = fetch_data()
    results = process_data(data)

    # Save to latest.json
    with open("latest.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
