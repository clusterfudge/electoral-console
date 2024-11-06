import os
import re


def setup_scrapers():
    # List of all US states plus DC in alphabetical order
    states = [
        "Alabama",
        "Alaska",
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
        "Pennsylvania",
        "Puerto Rico",
        "Rhode_Island",
        "South_Carolina",
        "South_Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West_Virginia",
        "Wisconsin",
        "Wyoming",
    ]

    # Base directory for scrapers
    base_dir = "scrapers"

    # Path to Florida template
    florida_template = os.path.join(base_dir, "Florida", "scraper.py")

    # Read Florida template content
    with open(florida_template, "r") as f:
        template_content = f.read()

    # Base race ID for Alabama (first state)
    base_race_id = 52793

    # Process each state
    for i, state in enumerate(states):
        # Skip Florida since it's our template
        if state == "Florida":
            continue

        # Calculate race ID for current state
        race_id = base_race_id + i

        # Create state directory path
        state_dir = os.path.join(base_dir, state)
        state_scraper = os.path.join(state_dir, "scraper.py")

        # Create directory if it doesn't exist
        os.makedirs(state_dir, exist_ok=True)

        # Skip if scraper already exists
        if os.path.exists(state_scraper):
            print(f"Skipping {state} - scraper already exists")
            continue

        # Replace race ID in template content
        # Look for URL pattern and replace the ID
        new_content = re.sub(
            r"(https://embed-api\.ddhq\.io/v2/races/)\d+",
            f"\\g<1>{race_id}",
            template_content,
        )

        # Write new scraper file
        with open(state_scraper, "w") as f:
            f.write(new_content)

        print(f"Created scraper for {state} with race ID {race_id}")


if __name__ == "__main__":
    setup_scrapers()
