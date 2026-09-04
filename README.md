# Zootopia

Zootopia is a Python project that fetches animal data from the API Ninjas Animals API and generates an HTML website with the results.

## Features

- Fetch animal data from an API
- Search animals by name
- Filter results by skin type
- Generate an HTML website
- Handle searches with no results

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your API key:

```text
API_NINJAS_KEY=your_api_key_here
```

Make sure `.env` is included in `.gitignore`.

## Usage

Run the program:

```bash
python animals_web_generator.py
```

Enter an animal name when prompted.

The program fetches matching animals from the API and generates the file:

```text
animals.html
```

Open `animals.html` in your browser to view the generated website.