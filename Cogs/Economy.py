import discord
from discord import app_commands
from discord.ext import commands
from Functions.DataFunctions import getCoins, addMoney, removeMoney


def is_owner():
    async def predicate(interaction: discord.Interaction) -> bool:
        return await interaction.client.is_owner(interaction.user)
    return app_commands.check(predicate)
  
class EconomyCommands(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    
  Economy_Group = app_commands.Group(name="economy", description="Economy commands")

  

  @app_commands.command(name="wallet", description="See their coins")
  async def wallet(self, interaction: discord.Interaction, user: discord.User):
    coins = getCoins(user.id)
    await interaction.response.send_message(f"@{user} has {coins}¢ in their wallet! ")


  @app_commands.command(name="daily", description="daily free cash")
  @app_commands.checks.cooldown(rate=1, per=86400.0, key=lambda i: i.user.id)
  async def daily(self, interaction: discord.Interaction):
    status, msg =addMoney(interaction.user.id, 250)
    if status == True:
      await interaction.response.send_message("YOU HAVE SUCCESSFULLY CLAIMED YOUR 250¢ DAILY COINS!")
    else:
      print(msg)


  async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
      hours = int(error.retry_after // 3600)
      minutes = int((error.retry_after % 3600) // 60)
      seconds = int(error.retry_after % 60)
      
      time_string = f"{hours}h {minutes}m {seconds}s"
      
      msg = f"⏳ Slow down big boi! You need to wait **{time_string}** before using this command again."
      
      if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
      else:
        await interaction.response.send_message(msg, ephemeral=True)
    else:
      print(f"An error occurred: {error}")









async def setup(bot: commands.Bot):
  await bot.add_cog(EconomyCommands(bot))