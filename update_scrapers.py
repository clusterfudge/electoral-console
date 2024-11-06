import os

states = [
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "District_of_Columbia",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New_Hampshire",
    "New_Jersey",
    "New_Mexico",
    "New_York",
    "North_Carolina",
    "North_Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Puerto Rico",
    "Rhode_Island",
    "South_Carolina",
    "South_Dakota",
    "Tennessee",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West_Virginia",
    "Wisconsin",
    "Wyoming",
]

for state in states:
    scraper_path = f"scrapers/{state}/scraper.py"
    if os.path.exists(scraper_path):
        with open(scraper_path, "r") as f:
            content = f.read()

        if "ddhq.io" in content:
            # Add debug print statement
            new_content = content.replace(
                '        candidates = race.get("candidates", [])',
                '        print(f"Title: {race.get(\'title\')}")\n        candidates = race.get("candidates", [])',
            )

            with open(scraper_path, "w") as f:
                f.write(new_content)
            print(f"Updated {state}")
