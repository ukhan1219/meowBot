# meowBot
meowBot is a Discord bot designed to bring a bit of fun and interaction to any server. Hosted on Google Cloud Platform and using SQLite for database management, this bot simulates a virtual cat that responds to various triggers and allows users to interact with it through a petting feature.

## Project Overview
meowBot offers a range of functionalities:

-  **Cat Trigger Responses**: Responds with randomly generated cat-related messages when triggered by certain keywords.
-  **Pet Tracker**: Users can "pet" the virtual cat every 30 minutes, receiving a random number between 1 and 100 with different rarities based on the interval. The bot tracks the number of pets for each user and prevents exploitation by enforcing a cooldown period.
-  **Leaderboard**: Displays a leaderboard of users with the highest pet counts.
-  **Pet Timer**: Notifies users of when they can pet the virtual cat again.
### Key Features
-  **Random Responses**: The bot generates random responses to cat-related triggers like "meow," "mrow," and ":3".
-  **Petting Mechanism**: Each pet command returns a randomly generated number of additional pets, tracked per user.
-  **Leaderboard**: Shows the top users with the most pet counts in the server.
-  **Cooldown Timer**: Prevents users from spamming the pet command by enforcing a 30-minute cooldown.
### How It Works
1.  Setup: The bot connects to a SQLite database to manage pet statistics. It creates a table to store user data, including pet counts and the last petting time.
2.  Message Handling: Responds to various commands:
    -  !pet: Allows users to pet the virtual cat and updates their pet count.
    -  !petleaderboard: Displays a leaderboard of the top users with the most pets.
    -  !pettimer: Informs users when they can pet the cat again.
3.  Trigger Responses: Sends a random cat-related response when specific triggers are detected in the message content.
### Code Explanation
-  **Database Management**: Uses SQLite to store and retrieve pet statistics. The pet_stats table holds data on pet counts and last petting times.
-  **Bot Events**: The bot listens for messages and handles commands to interact with the virtual cat.
-  **Randomness**: Uses the random module to generate responses and determine the number of pets added.
### Getting Started
To use meowBot:

1.  Clone this repository.
2.  Set up a Google Cloud Platform project and configure your environment to run the bot.
3.  Install required Python libraries:
-      pip install discord sqlite3 python-dotenv
4.  Create a .env file in the root directory and add your Discord API key:
-      DISCORD_API_KEY=your_discord_api_key_here
5.  Run the bot:
-      python meow_bot.py
### Prerequisites
-  Python 3.x
-  Discord API account and token
-  Google Cloud Platform account for hosting
## Contributing
Contributions to improve meowBot are welcome! Feel free to open an issue or submit a pull request with suggestions or bug fixes.
