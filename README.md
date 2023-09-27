# API-Data-Fetcher-and-Storage

Fetching Users and Posts from an API
Project Name: API-Data-Fetcher-and-Storage
# Description:
This Python script fetches user and posts data from an external API and stores it in a SQLite database. The script uses the requests library for API requests and the sqlite3 library for database operations.

# Features:
Fetches user data and posts data separately.
Handles missing data fields gracefully.
Stores data in a SQLite database for easy retrieval.
How to Use:
Install the required dependencies: pip install requests sqlite3
Clone this repository: git clone <repository-url>
Navigate to the project folder:cd User-Posts-API-Fetcher
Replace YOUR_API_KEY with your actual API key in the api_fetcher.py file.
Login to the https://dummyapi.io/ and create your app_id.
Use your app_id in the APIs below to get data.
Run the Python script:
python api_fetcher.py
# Database Structure:
users table: Stores user data with columns id, name, and email.
posts table: Stores post data with columns id, user_id, title, and body.
