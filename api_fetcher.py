import requests
import sqlite3

# Step 1: Create a new SQLite database and 'users' and 'posts' tables
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS posts')

# Create 'users' table with a TEXT primary key named 'id'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')

# Create 'posts' table with an INTEGER PRIMARY KEY
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        title TEXT,
        body TEXT
    )
''')

conn.commit()

# Step 2: Fetch Users Data from API and Store in the 'users' Table
api_url = "https://dummyapi.io/data/v1/user"
headers = {
    "app-id": "65141c8dbac0bd26cb4cabf6",  # Replace with your actual App ID
}

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    users_data = response.json()
    
    conn.execute("BEGIN")  # Start a transaction
    
    for user in users_data["data"]:
        user_id = user["id"]
        name = user["firstName"] + " " + user["lastName"]
        email = user.get("email")
        
        # Use INSERT OR IGNORE to avoid violating UNIQUE constraint
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)", (user_id, name, email))

    conn.commit()  # Commit the transaction
    print("Users data has been fetched and stored.")
else:
    print("Failed to fetch users data from the API.")

# Step 3: Fetch Users List from the 'users' Table
cursor.execute("SELECT id FROM users")
user_ids = cursor.fetchall()

# Step 4: Fetch Corresponding Posts Data from API and Store in the 'posts' Table
for user_id in user_ids:
    user_id = user_id[0]  # Extract the user_id from the tuple
    
    # Construct the API URL for posts
    posts_api_url = f"https://dummyapi.io/data/v1/user/{user_id}/post"
    
    response = requests.get(posts_api_url, headers=headers)
    
    if response.status_code == 200:
        posts_data = response.json()
        
        conn.execute("BEGIN")  # Start a transaction
        
        for post in posts_data["data"]:
            post_id = str(post["id"])  # Ensure post_id is treated as a string
            title = post.get("title", None)
            body = post.get("text", None)
            
            cursor.execute("INSERT OR IGNORE INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)", (post_id, user_id, title, body))
        
        conn.commit()  # Commit the transaction
        print(f"Posts data for user {user_id} has been fetched and stored.")
    else:
        print(f"Failed to fetch posts data for user {user_id} from the API.")

# Step 5: Close the database connection
conn.close()
