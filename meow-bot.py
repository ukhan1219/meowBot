import random
import discord
import sqlite3
from datetime import datetime, timedelta

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

    if message.content.startswith('!petleaderboard'):
        await pet_leaderboard(message)
    elif message.content.startswith('!pettimer'):
        await pet_timer(message)
    elif message.content.startswith('!pet'):
        await pet_user(message)
    else:
        await check_triggers(message)

# Define the triggers and responses
triggers = ['meow', 'mrow', ':3', 'nya', 'mew', 'maow', 'mow']
responses = [
    # ... your predefined responses
]

async def pet_user(message):
    guild_id = message.guild.id
    user_id = message.author.id
    current_time = datetime.now()
    cursor.execute('SELECT last_pet_time FROM pet_stats WHERE guild_id = ? AND user_id = ?', (guild_id, user_id))
    result = cursor.fetchone()
    last_pet_time = result[0] if result else None

    if last_pet_time:
        last_pet_time = datetime.fromisoformat(last_pet_time)
        time_since_last_pet = (current_time - last_pet_time).total_seconds()
    else:
        time_since_last_pet = float('inf')

    if time_since_last_pet < 1800:
        remaining_time = timedelta(seconds=1800 - time_since_last_pet)
        minutes, seconds = divmod(remaining_time.seconds, 60)
        await message.channel.send(f"You can pet me again in **{minutes}** minutes and **{seconds}** seconds.")
    else:
        new_pet_count = (result[1] + 1) if result else 1
        cursor.execute('INSERT OR REPLACE INTO pet_stats (guild_id, user_id, pet_count, last_pet_time) VALUES (?, ?, ?, ?)', (guild_id, user_id, new_pet_count, current_time.isoformat()))
        db.commit()
        response = random.choice(responses)
        await message.channel.send(f"Thanks for the pet, **{response}**! **{message.author.display_name}** has petted me **{new_pet_count}** times in this server.")

async def pet_timer(message):
    guild_id = message.guild.id
    user_id = message.author.id
    current_time = datetime.now()
    cursor.execute('SELECT last_pet_time FROM pet_stats WHERE guild_id = ? AND user_id = ?', (guild_id, user_id))
    result = cursor.fetchone()
    last_pet_time = result[0] if result else None

    if last_pet_time:
        last_pet_time = datetime.fromisoformat(last_pet_time)
        time_since_last_pet = (current_time - last_pet_time).total_seconds()
    else:
        time_since_last_pet = float('inf')

    if time_since_last_pet < 1800:
        remaining_time = timedelta(seconds=1800 - time_since_last_pet)
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


# import random
# import discord
# from datetime import datetime, timedelta
# from collections import defaultdict

# intents = discord.Intents.default()
# intents.messages = True
# intents.message_content = True

# client = discord.Client(intents=intents)

# # In-memory storage for pet counts and cooldowns, now with server IDs as keys
# last_pet_time = defaultdict(lambda: defaultdict(lambda: datetime.min))
# pet_counts = defaultdict(lambda: defaultdict(int))

# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     # Check for pet leaderboard command
#     if message.content.startswith('!petleaderboard'):
#         await pet_leaderboard(message)

#     # Check for pet timer command
#     elif message.content.startswith('!pettimer'):
#         await pet_timer(message)

#     # Check for pet command
#     elif message.content.startswith('!pet'):
#         await pet_user(message)
    
#     else:
#         for trigger in triggers:
#             if trigger in message.content.lower():
#                 if random.random() < 0.35:
#                     await message.channel.send(random.choice(responses))
#                 break  # Once a trigger matches, break out of the loop

# # Define the triggers and responses
# triggers = ['meow', 'mrow', ':3', 'nya', 'mew', 'maow', 'mow']
# responses = [
#     'Meow', 'Mrow', ':3', 'Nya', 'Mew', 'Maow', 'Mow', 'Meow~', 'Mrow~', 'Nya~', 'Mew~', 'Maow~', 'Mow~',
#     '₍˄·͈༝·͈˄₎◞ ̑̑', '  (=ↀωↀ=) ', '(^･o･^)ﾉ” ', 'ᓚᘏᗢ', 'ฅ^•ﻌ•^ฅ', '≽ܫ≼',
#     '  ₍˄·͈༝·͈˄₍˄·͈༝·͈˄( ͒ ु•·̫• ू ͒)˄·͈༝·͈˄₎˄·͈༝·͈˄₎ ',
#     '(,,,)=(^.^)=(,,,)', '=^..^='
# ]

# async def pet_user(message):
#     guild_id = message.guild.id
#     user_id = message.author.id
#     current_time = datetime.now()
#     user_last_pet_time = last_pet_time[guild_id][user_id]
#     time_since_last_pet = (current_time - user_last_pet_time).total_seconds()

#     if time_since_last_pet < 1800:  # 30 minutes cooldown
#         remaining_time = timedelta(seconds=1800 - time_since_last_pet)
#         minutes, seconds = divmod(remaining_time.seconds, 60)
#         await message.channel.send(f"You can pet me again in **{minutes} minutes** and **{seconds} seconds.**")
#     else:
#         pet_counts[guild_id][user_id] += 1
#         last_pet_time[guild_id][user_id] = current_time
#         response = random.choice(responses)
#         await message.channel.send(f"Thanks for the pet, **{response}**! **{message.author.display_name}** has petted me **{pet_counts[guild_id][user_id]}** times in this server.")

# async def pet_timer(message):
#     guild_id = message.guild.id
#     user_id = message.author.id
#     current_time = datetime.now()
#     user_last_pet_time = last_pet_time[guild_id][user_id]
#     if current_time - user_last_pet_time < timedelta(minutes=30):
#         time_left = timedelta(minutes=30) - (current_time - user_last_pet_time)
#         minutes, seconds = divmod(time_left.seconds, 60)
#         await message.channel.send(f"You can pet me again in **{minutes} minutes** and **{seconds} seconds.**")
#     else:
#         await message.channel.send("**You can pet me now!**")

# async def pet_leaderboard(message):
#     guild_id = message.guild.id
#     guild_pet_counts = pet_counts[guild_id]
#     leaderboard = sorted(guild_pet_counts.items(), key=lambda x: x[1], reverse=True)
#     leaderboard_message = f"🏆 **{message.guild.name} pet leaderboard**\n"
#     for idx, (user_id, count) in enumerate(leaderboard[:15], start=1):  # Get the top 15 petters
#         user = await client.fetch_user(user_id)
#         leaderboard_message += f"{idx}. **{user.display_name}** — {count} pets\n"
#     await message.channel.send(leaderboard_message)

#     # # Check if any trigger word is in the message content
#     # if any(trigger in message.content.lower() for trigger in triggers):
#     #     # 35% chance to respond
#     #     if random.random() < 0.35:
#     #         # Respond with a random choice from the responses list
#     #         await message.channel.send(random.choice(responses))


client.run('MTIyODM3MDUwOTg4MDg4OTM5NQ.GMi-jy.aCfQta_gD4r8mP95-kCRM2P_wmZvy45qegkXQI')
