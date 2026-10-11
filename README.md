# Flask URL Shortener

A URL Shortener REST API built using Python, Flask,
and SQLite with SQLAlchemy.

## Features

- Create short URLs
- Retrieve URL details using a short code
- Redirect to the original URL
- Track redirect clicks
- Delete short URLs
- Validate submitted URLs
- Paginate URL listings
- Store URL records in SQLite

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- REST API

## Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Install dependencies:

   pip install -r requirements.txt

4. Run the application:

   python app.py

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/urls` | Create a short URL |
| GET | `/api/urls/<short_code>` | Retrieve URL details |
| DELETE | `/api/urls/<short_code>` | Delete a short URL |

Additional endpoints depend on your implementation.

## Example Request

POST `/api/urls`

Content-Type: application/json

{
  "url": "https://example.com"
}

## Database

URL records are stored in SQLite using SQLAlchemy.

## Future Improvements

- Deploy the API publicly
- Add automated tests
- Add authentication and analytics