import random
import os
import discord
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


DISCORD_API_KEY = os.getenv('DISCORD_API_KEY')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
db = sqlite3.connect('pet_stats.db')
cursor = db.cursor()

# Create the table for pet statistics if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS pet_stats (
    guild_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    pet_count INTEGER NOT NULL DEFAULT 0,
    last_pet_time TIMESTAMP,
    PRIMARY KEY (guild_id, user_id)
)
''')
db.commit()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    command = message.content.lower()
    if command.startswith('!petleaderboard'):
        await pet_leaderboard(message)
    elif command.startswith('!pettimer'):
        await pet_timer(message)
    elif command.startswith('!pet'):
        await pet_user(message)
    else:
        await check_triggers(message)

# Define the triggers and responses
triggers = ['meow', 'mrow', ':3', 'nya', 'mew', 'maow', 'mow']
responses = [
    'Meow', 'Mrow', ':3', 'Nya', 'Mew', 'Maow', 'Mow', 'Meow~', 'Mrow~', 'Nya~', 'Mew~', 'Maow~', 'Mow~',
    '₍˄·͈༝·͈˄₎◞ ̑̑', '  (=ↀωↀ=) ', '(^･o･^)ﾉ” ', 'ᓚᘏᗢ', 'ฅ^•ﻌ•^ฅ', '≽ܫ≼',
    '  ₍˄·͈༝·͈˄₍˄·͈༝·͈˄( ͒ ु•·̫• ू ͒)˄·͈༝·͈˄₎˄·͈༝·͈˄₎ ',
    '(,,,)=(^.^)=(,,,)', '=^..^='
]

async def pet_user(message):
    guild_id = message.guild.id
    user_id = message.author.id
    current_time = datetime.now()
    cursor.execute('SELECT pet_count, last_pet_time FROM pet_stats WHERE guild_id = ? AND user_id = ?', (guild_id, user_id))
    result = cursor.fetchone()
    last_pet_time = datetime.fromisoformat(result[1]) if result else None
    pet_count = result[0] if result else 0

    if last_pet_time and (current_time - last_pet_time).total_seconds() < 1800:
        remaining_time = timedelta(seconds=1800 - (current_time - last_pet_time).total_seconds())
        minutes, seconds = divmod(remaining_time.seconds, 60)
        await message.channel.send(f"You can pet me again in **{minutes}** minutes and **{seconds}** seconds.")
    else:
        # Determine random pets based on specified probabilities
        random_number = random.random()
        if random_number < 0.50:
            additional_pets = random.randint(1, 50)
        elif random_number < 0.75:
            additional_pets = random.randint(51, 75)
        elif random_number < 0.90:
            additional_pets = random.randint(76, 90)
        else:
            additional_pets = random.randint(91, 100)

        new_pet_count = pet_count + additional_pets
        cursor.execute('INSERT OR REPLACE INTO pet_stats (guild_id, user_id, pet_count, last_pet_time) VALUES (?, ?, ?, ?)',
                       (guild_id, user_id, new_pet_count, current_time.isoformat()))
        db.commit()
        response = random.choice(responses)
        # Update the message to include the number of additional pets
        await message.channel.send(f"Thanks for the pet, **{response}**! **{message.author.display_name}** has petted me **{new_pet_count}** times in this server, adding **{additional_pets}** pets this time.")

async def pet_timer(message):
    guild_id = message.guild.id
    user_id = message.author.id
    current_time = datetime.now()
    cursor.execute('SELECT last_pet_time FROM pet_stats WHERE guild_id = ? AND user_id = ?', (guild_id, user_id))
    result = cursor.fetchone()
    last_pet_time = datetime.fromisoformat(result[0]) if result else None

    if last_pet_time and (current_time - last_pet_time).total_seconds() < 1800:
        remaining_time = timedelta(seconds=1800 - (current_time - last_pet_time).total_seconds())
        minutes, seconds = divmod(remaining_time.seconds, 60)
        await message.channel.send(f"You can pet me again in **{minutes}** minutes and **{seconds}** seconds.")
    else:
        await message.channel.send("**You can pet me now!**")

async def pet_leaderboard(message):
    guild_id = message.guild.id
    cursor.execute('SELECT user_id, pet_count FROM pet_stats WHERE guild_id = ? ORDER BY pet_count DESC LIMIT 15', (guild_id,))
    leaderboard = cursor.fetchall()
    leaderboard_message = f"🏆 **{message.guild.name} pet leaderboard**\n"
    for idx, (user_id, count) in enumerate(leaderboard, start=1):
        user = await client.fetch_user(user_id)
        leaderboard_message += f"**#{idx}. {user.display_name}** — **{count}** pets\n"
    await message.channel.send(leaderboard_message)

async def check_triggers(message):
    for trigger in triggers:
        if trigger in message.content.lower():
            if random.random() < 0.35:
                await message.channel.send(random.choice(responses))
            break


client.run(DISCORD_API_KEY)