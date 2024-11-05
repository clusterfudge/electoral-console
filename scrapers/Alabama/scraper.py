import requests
import json
import pandas as pd
from datetime import datetime
import os


def fetch_data():
    url = "https://www2.alabamavotes.gov/electionNight/statewideResultsByContest.aspx?ecode=1001225"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www2.alabamavotes.gov",
        "referer": "https://www2.alabamavotes.gov/electionNight/statewideResultsByContest.aspx?ecode=1001225",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    data = {
        "__EVENTTARGET": "hlnkExportData",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "/wEPDwUJODM2OTE1OTcwDxYEHgxlbGVjdGlvbkNvZGUFBzEwMDEyMjUeDF9DdXJyZW50UGFnZQIBFgICAQ9kFgoCAQ9kFgQCAQ8WAh4EaHJlZgUsc3RhdGV3aWRlUmVzdWx0c0J5Q29udGVzdC5hc3B4P2Vjb2RlPTEwMDEyMjVkAgMPFgIfAgUfY2hvb3NlQ291bnR5LmFzcHg/ZWNvZGU9MTAwMTIyNWQCAw8WAh4HVmlzaWJsZWcWAgIBDxYCHwIFLHN0YXRld2lkZVJlc3VsdHNCeUNvbnRlc3QuYXNweD9lY29kZT0xMDAxMjI1ZAIFD2QWAgIDDxYCHwIFLHN0YXRld2lkZVJlc3VsdHNCeUNvbnRlc3QuYXNweD9lY29kZT0xMDAxMjI1ZAIHDxYCHwNoFgICAw8PFgIeBFRleHQFCTMsODY4LDA0M2RkAgkPFgIfA2gWAgIHDzwrAAkAZGSMJBYYxFx7IlWKZCATBONaXm9jiD2SkWgjGu9hpvLJGg==",
        "__VIEWSTATEGENERATOR": "4D03577B",
        "__EVENTVALIDATION": "/wEdAAIa3qmKgfW0/1E8ZPVvJt1xBioLFgMe96DTOceWyPgpdQ+G3HCnAgeRUd4YnChwpMZQje6kFpkXr1a6ffRBJu8g",
    }

    response = requests.post(url, headers=headers, data=data)

    # Save the Excel file temporarily
    with open("temp.xlsx", "wb") as f:
        f.write(response.content)

    # Read the Excel file
    df = pd.read_excel("temp.xlsx")

    # Clean up
    os.remove("temp.xlsx")

    return df


def process_data(df):
    # Find the presidential race data
    pres_data = df[df["Contest Title"].str.contains("President", na=False, case=False)]

    # Group by candidate to get total votes
    candidate_totals = (
        pres_data.groupby(["Candidate Name", "Party Code"])["Votes"].sum().reset_index()
    )
    total_votes = candidate_totals["Votes"].sum()

    # Initialize the results structure
    results = {
        "state": "Alabama",
        "type": "presidential",
        "timestamp": datetime.utcnow().isoformat(),
        "candidates": [],
    }

    # Process each candidate
    for _, row in candidate_totals.iterrows():
        votes = int(row["Votes"])
        candidate = {
            "name": row["Candidate Name"],
            "party": row["Party Code"],
            "votes": votes,
            "percent": votes / total_votes if total_votes > 0 else 0,
        }
        results["candidates"].append(candidate)

    return results


def main():
    df = fetch_data()
    results = process_data(df)

    # Save to latest.json
    with open("latest.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
