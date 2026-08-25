import json


def load_data(file_path):
    """Load a JSON file."""
    with open(file_path, "r") as file_r:
        return json.load(file_r)


def load_html(file_path):
    """Load an HTML file."""
    with open(file_path, "r") as html_r:
        return html_r.read()


def save_html(file_path: str, file: str):
    """Save content to an HTML file."""
    with open(file_path, "w") as html_w:
        html_w.write(file)


def get_animals_info(animals_data: list[dict]) -> str:
    """Generate the output string for all animals."""
    all_animals_info = ""
    for animal in animals_data:
        animal_infos = get_animal_infos(animal)
        all_animals_info += animal_infos + "\n"

    return all_animals_info


def get_animal_infos(animal: dict) -> str:
    """Generate the output string for one animal."""
    output = "<li class='cards__item'>"
    categories = get_categories()

    for category in categories:
        value = animal
        path = categories[category]
        skip = False

        for step in path:
            try:
                value = value[step]
            except (KeyError, IndexError):
                skip = True
                break

        if skip:
            continue
        output += f"{category.title()}: {value}<br/>\n"
    output += "</li>"
    return output


def get_categories() -> dict[str, list[str | int]]:
    """Return the category lookup table used for printing animal data."""
    return {
        "name": ["name"],
        "diet": ["characteristics", "diet"],
        "location": ["locations", 0],
        "type": ["characteristics", "type"]
    }


def generate_animals_html(animals_info: str):
    """Create an HTML file by inserting the animal data into the template."""
    template = load_html("animals_template.html")
    new_html = template.replace("__REPLACE_ANIMALS_INFO__", animals_info)
    save_html("animals.html", new_html)


def main():
    """Load the animal data and integrate it into HTML."""
    animals_data = load_data("animals_data.json")
    animals_info = get_animals_info(animals_data)
    generate_animals_html(animals_info)


if __name__ == "__main__":
    main()

