import os
from discord.ext import commands
from openai import OpenAI

print("DISCORD_TOKEN is set to:", os.environ.get("DISCORD_TOKEN"))
print("OPENAI_API_KEY is set to:", os.environ.get("OPENAI_API_KEY"))

# Make sure these environment variables exist in Railway
# OPENAI_API_KEY  -> your OpenAI key
# DISCORD_TOKEN   -> your Discord bot token
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# Initialize OpenAI client (reads OPENAI_API_KEY automatically)
openai_client = OpenAI()

# Initialize Discord bot
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ask(ctx, *, question):
    """Responds to user queries using OpenAI."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        await ctx.send(response.choices[0].message.content)
    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run(DISCORD_TOKEN)
