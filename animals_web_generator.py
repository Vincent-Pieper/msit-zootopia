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


def serialize_animals(animals_data: list[dict]) -> str:
    """Generate the output string for all animals."""
    all_animals_info = ""
    for animal in animals_data:
        animal_infos = serialize_animal(animal)
        all_animals_info += animal_infos + "\n"

    return all_animals_info


def serialize_animal(animal: dict) -> str:
    """Generate the output string for one animal."""
    output = "<li class='cards__item'>"
    categories = get_categories()
    paragraph_open = False

    for category in categories:
        value = animal
        path = categories[category]

        value, skip = get_value(value, path)
        if skip:
            continue

        category_output, paragraph_open = write_html_body(
            category,
            value,
            paragraph_open
        )
        output += category_output

    if paragraph_open:
        output += "</ul>\n"
        output += "</div>\n"
    output += "</li>\n"
    return output


def get_categories() -> dict[str, list[str | int]]:
    """Return the category lookup table used for printing animal data."""
    return {
        "name": ["name"],
        "diet": ["characteristics", "diet"],
        "predators": ["characteristics", "predators"],
        "location": ["locations", 0],
        "type": ["characteristics", "type"],
        "color": ["characteristics", "color"],
        "skin type": ["characteristics", "skin_type"],
        "top speed": ["characteristics", "top_speed"],
        "lifespan": ["characteristics", "lifespan"],
        "weight": ["characteristics", "weight"],
        "length": ["characteristics", "length"]
    }


def get_value(value, path: list[str | int]) -> tuple[str | None, bool]:
    """Returns the values and handles missing data"""
    skip = False
    for step in path:
        try:
            value = value[step]
        except (KeyError, IndexError):
            skip = True
            value = None
            break
    return value, skip


def write_html_body(category: str, value: str, paragraph_open: bool) -> tuple[str, bool]:
    """Writes the HTML body for an animal"""
    category_output = ""

    if category == "name":
        category_output += f"<div class='card__title'>{value}</div>\n"
    else:
        if not paragraph_open:
            category_output += "<div class='card__text'>\n"
            category_output += "<ul class='card__list'>"
            paragraph_open = True

        category_output += (
            f"<li class='card__list-item'>"
            f"<strong>{category.title()}: </strong> {value}"
            f"</li>\n"
        )
    return category_output, paragraph_open


def generate_animals_html(animals_info: str):
    """Create an HTML file by inserting the animal data into the template."""
    template = load_html("animals_template.html")
    new_html = template.replace("__REPLACE_ANIMALS_INFO__", animals_info)
    save_html("animals.html", new_html)


def main():
    """Load the animal data and integrate it into HTML."""
    animals_data = load_data("animals_data.json")
    animals_info = serialize_animals(animals_data)
    generate_animals_html(animals_info)


if __name__ == "__main__":
    main()

