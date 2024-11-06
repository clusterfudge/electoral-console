import os


def update_scraper(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # Define the pattern to match and its replacement
    old_pattern = """    race = data
        candidates = race.get("candidates", [])"""
    new_pattern = """    race = data
        candidates = race.get("candidates", [])
    print(f"Title: {race.get('title')}")"""

    if old_pattern in content and new_pattern not in content:
        # Only replace if the old pattern exists and new pattern doesn't
        new_content = content.replace(old_pattern, new_pattern)
        with open(file_path, "w") as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    else:
        print(f"No update needed for {file_path}")


def main():
    scrapers_dir = "scrapers"
    for state in os.listdir(scrapers_dir):
        scraper_path = os.path.join(scrapers_dir, state, "scraper.py")
        if os.path.exists(scraper_path):
            update_scraper(scraper_path)


if __name__ == "__main__":
    main()
