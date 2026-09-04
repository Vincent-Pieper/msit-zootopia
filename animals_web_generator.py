import requests
from dotenv import load_dotenv
import os


load_dotenv()


def fetch_animals(user_animal: str) -> list[dict]:
    """Fetch animal data from the API."""
    url = "https://api.api-ninjas.com/v1/animals"
    params = get_params(user_animal)
    headers = get_headers()
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def get_params(user_animal: str) -> dict[str, str]:
    """Return the API query parameters."""
    params = {
        "name": user_animal
    }
    return params


def get_headers() -> dict[str, str | None]:
    """Return the API request headers."""
    api_key = os.getenv("API_NINJAS_KEY")
    headers = {
        "X-Api-Key": api_key
    }
    return headers


def load_html(file_path):
    """Load an HTML file."""
    with open(file_path, "r", encoding="utf-8") as html_r:
        return html_r.read()


def save_html(file_path: str, file: str):
    """Save content to an HTML file."""
    with open(file_path, "w", encoding="utf-8") as html_w:
        html_w.write(file)


def get_user_animal() -> str:
    """Gets the users choosen animal"""
    while True:
        user_animal = input("Enter a name of an animal: ").strip()

        if user_animal:
            return user_animal

        print("Please enter an animal name.")


def get_skin_types(animals_data: list[dict]) -> list[str]:
    """Return all available skin types."""
    skin_types = set()

    for animal in animals_data:
        skin_type, skip = get_value(
            animal,
            ["characteristics", "skin_type"]
        )

        if not skip:
            skin_types.add(skin_type)

    return sorted(skin_types)


def choose_skin_type(skin_types: list[str]) -> str | None:
    """Let the user choose an available skin type."""
    print("Available skin types:")

    for index, skin_type in enumerate(skin_types, start=1):
        print(f"{index}. {skin_type}")

    all_option = len(skin_types) + 1
    print(f"{all_option}. All skin types")

    user_input = input("Choose a skin type: ")
    choice = validate_skin_type_choice(user_input, all_option)

    if choice == all_option:
        return None

    return skin_types[choice - 1]


def validate_skin_type_choice(
        user_input: str,
        max_choice: int
) -> int:
    """Validate the user's skin type choice."""
    while True:
        try:
            choice = int(user_input)
        except ValueError:
            user_input = input("Please enter a number: ")
            continue

        if 1 <= choice <= max_choice:
            return choice

        user_input = input(
            f"Please enter a number between 1 and {max_choice}: "
        )


def filter_animals_by_skin_type(
        animals_data: list[dict],
        selected_skin_type: str
) -> list[dict]:
    """Return animals matching the selected skin type."""
    filtered_animals = []

    for animal in animals_data:
        skin_type, skip = get_value(
            animal,
            ["characteristics", "skin_type"]
        )

        if not skip and skin_type == selected_skin_type:
            filtered_animals.append(animal)

    return filtered_animals


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


def get_value(
        value,
        path: list[str | int]
) -> tuple[str | None, bool]:
    """Return a value and handle missing data."""
    skip = False
    for step in path:
        try:
            value = value[step]
        except (KeyError, IndexError):
            skip = True
            value = None
            break
    return value, skip


def write_html_body(
        category: str,
        value: str,
        paragraph_open: bool
) -> tuple[str, bool]:
    """Write the HTML body for an animal."""
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
    print("Website was successfully generated to the file animals.html.")


def main():
    """Load, filter and integrate the animal data into HTML."""
    user_animal = get_user_animal()
    animals_data = fetch_animals(user_animal)

    skin_types = get_skin_types(animals_data)
    selected_skin_type = choose_skin_type(skin_types)

    if selected_skin_type is None:
        filtered_animals = animals_data
    else:
        filtered_animals = filter_animals_by_skin_type(
            animals_data,
            selected_skin_type
        )

    animals_info = serialize_animals(filtered_animals)
    generate_animals_html(animals_info)


if __name__ == "__main__":
    main()