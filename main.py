import discord
from discord.ext import commands
from openai import OpenAI

bot = commands.Bot(command_prefix="!")

openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ask(ctx, *, question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    await ctx.send(response.choices[0].message.content)

bot.run("MTQ4MzE1ODcyNDE0MjE3MDE1Mw.GJRX3B.IzgyG29De8CQD44e2xnNBSo851tASMNu1xlrg4")
