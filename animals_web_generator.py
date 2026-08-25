import json


def load_data(file_path):
    """Load a JSON file."""
    with open(file_path, "r") as file_r:
        return json.load(file_r)


def show_animals(animals_data: list[dict]):
    """Send each animal to the print function."""
    for animal in animals_data:
        print_animal(animal)


def print_animal(animal: dict):
    """Print the available categories for one animal."""
    categories = get_categories()

    for category in categories:
        value = animal
        path = categories[category]
        skip = False

        for step in path:
            try:
                value = value[step]
            except KeyError, IndexError:
                skip = True
                break

        if skip:
            continue
        print(f"{category.title()}: {value}")
    print()


def get_categories() -> dict[str, list[str | int]]:
    """Return the category lookup table used for printing animal data."""
    return {
        "name": ["name"],
        "diet": ["characteristics", "diet"],
        "location": ["locations", 0],
        "type": ["characteristics", "type"]
    }


def main():
    """Load the animal data and display all animals."""
    animals_data = load_data("animals_data.json")
    show_animals(animals_data)


if __name__ == "__main__":
    main()

