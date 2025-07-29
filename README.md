# MAVKA 🌱
Mavka is a Python script that collects and saves articles from multiple (two for now) sources into a Notion database.

## Features
- Parses articles from different sources (currently: [Re/visions](https://revisionsjournal.com/), [Kontur](https://kontur.media/))
- Checks for duplicates in Notion before adding new entries
- Adds new articles to Notion via API
- Configured to run daily using GitHub Actions
- Allows selecting specific sources to fetch articles from via command-line arguments

## How to Use
Create a Notion database and obtain your ```NOTION_TOKEN``` and ```NOTION_DATABASE_ID```.

1. Set environment variables (e.g., in a .env file):
```
NOTION_TOKEN=your_token_here
NOTION_DATABASE_ID=your_database_id_here
```

2. Install dependencies:
```
uv pip install --system --project . --requirements requirements.txt
```

3. Run the script to fetch articles from all sources:
```
python main.py
```

Or fetch articles from a specific source:
```
python main.py --source kontur
```

## License
[MIT](https://choosealicense.com/licenses/mit/) — feel free to use, modify, and share!

## Authors
Made with 💟 by [@ni4yja.bsky.social](https://bsky.app/profile/did:plc:vhmeqpag4d3ubflbsrgck4nb)
