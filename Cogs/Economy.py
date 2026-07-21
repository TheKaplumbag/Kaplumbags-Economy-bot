import discord
from discord import app_commands
from discord.ext import commands
from Functions.DataFunctions import getCoins

class EconomyCommands(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name="wallet", description="See their coins")
  async def wallet(self, interaction: discord.Interaction, user: discord.User):
    coins = getCoins(user.id)
    await interaction.response.send_message(f"{user} has {coins}¢ in their wallet! ")




async def setup(bot: commands.Bot):
  await bot.add_cog(EconomyCommands(bot))