#!/usr/bin/env python3
from pathlib import Path


def read_template():
    template_path = Path("scrapers/Alabama/scraper.py")
    with open(template_path) as f:
        return f.read()


def get_multiline_input():
    print("Enter your curl command or URL (press Ctrl+D on a new line when done):")
    print("For a single URL, just enter it and press Ctrl+D")
    print("Begin input:")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    return "\n".join(lines)


def main():
    # Get state name
    state_name = input("Enter the state name: ").strip()

    # Get example request using multi-line input
    print("\nExample request:")
    example_request = get_multiline_input()

    # Read template
    read_template()

    # Generate prompt
    prompt = f"""Please write a Python scraper for {state_name}'s election results using this example request:

{example_request}

Pattern this scraper after the one at scrapers/Alabama/scraper.py

Key requirements:
1. The scraper should save results in a 'latest.json' file
2. The results should be in this format:
{{
    "counted": {{"republican": X, "democrat": Y}},
    "exit_poll": {{"republican": 0, "democrat": 0}},
    "reporting": 0,
    "called": false
}}
3. Use appropriate error handling
4. Follow the same structure as the template but modify the fetch_data() and process_data() functions as needed
"""

    print("\n=== Generated Prompt ===\n")
    print(prompt)

    # Optionally save to file
    save = input("\nWould you like to save this prompt to a file? (y/n): ").lower()
    if save == "y":
        filename = f"{state_name.lower()}_scraper_prompt.txt"
        with open(filename, "w") as f:
            f.write(prompt)
        print(f"Prompt saved to {filename}")


if __name__ == "__main__":
    main()
