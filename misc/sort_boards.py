import json
import re
import sys

json_input = "boards_output.json"
json_input_links = "boards_links.json"
json_output = "boards_data.json"

ignore_strings = ["nflpa", "sakar"]


def extract(json_input_links):
    with open(json_input_links, "r") as f:
        link_data = json.load(f)

    link_names = [
        re.sub(
            r"\bhoverboard\b",
            "default",
            item.get("name", "")
            .replace("Wrapped", "xmas2022")
            .replace("8th Birthday", "birthday")
            .replace("Color Shift", "colourshift")
            .replace(" ", "")
            .replace("-", "")
            .replace("&", "")
            .replace("Jr.", "")
            .lower(),
        )
        for item in link_data
    ]

    year = 2021
    for i in range(2, len(link_names) + 1):
        exponent = i + 7
        birthday = f"{exponent}thbirthday"
        link_names = [name.replace(birthday, f"birthday{year}") for name in link_names]
        year += 1

    return link_names


def sort_json(json_input, link_names, json_output):
    with open(json_input, "r") as f:
        data = json.load(f)

    ordered_data = []
    count = 1
    skipped_names = []

    for name in link_names:
        found = False
        for item in data:
            if "id" in item:
                item_id = item["id"].lower()
                for ignore in ignore_strings:
                    item_id = item_id.replace(ignore, "").lower().replace(" ", "")
                if item_id == name:
                    item_with_number = {
                        "number": count,
                        "id": item["id"],
                        "upgrades": item.get("upgrades", ""),
                    }
                    count += 1
                    ordered_data.append(item_with_number)
                    found = True
                    break

        if not found:
            skipped_names.append(name)

    with open(json_output, "w") as f:
        json.dump(ordered_data, f, indent=2)

    return skipped_names


link_names = extract(json_input_links)
skipped_names = sort_json(json_input, link_names, json_output)

if skipped_names:
    print("Skipped Names:")
    for name in skipped_names:
        print(name)
    sys.exit("Error: Items in skipped list.")
