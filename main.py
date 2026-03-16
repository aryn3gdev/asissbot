import os
import discord
from discord.ext import commands
from openai import OpenAI

# Load environment variables
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Set up intents (use default intents or customize)
intents = discord.Intents.default()
intents.message_content = True  # Required if your bot reads message content

# Initialize bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ask(ctx, *, question):
    """Responds to user queries using OpenAI."""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}]
    )
    await ctx.send(response.choices[0].message.content)

bot.run(DISCORD_TOKEN)
