import discord
from discord import app_commands
from discord.ext import commands
from Functions.DataFunctions import getCoins, addMoney, removeMoney


def is_owner():
    async def predicate(interaction: discord.Interaction) -> bool:
        return await interaction.client.is_owner(interaction.user)
    return app_commands.check(predicate)


class OwnerCommands(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    
  Owner_Group = app_commands.Group(name="owner", description="Owner only")



  @Owner_Group.command(name="take-money", description="takes money no matter what")
  @is_owner()
  async def takeMoney(self, interaction: discord.Interaction, who: discord.User, amount: app_commands.Range[int, 1, 9999]):
    status, msg = removeMoney(who.id, amount)
    if status == True:
      await interaction.response.send_message(f"{amount}¢ money has been taken from @{who}")
    else:
      print(msg)

  async def takeMoney_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
      await interaction.response.send_message("❌ Only the bot owner can use this command!", ephemeral=True)


  
  @Owner_Group.command(name="give-money", description="gives money no matter what")
  @is_owner()
  async def giveMoney(self, interaction: discord.Interaction, who: discord.User, amount: app_commands.Range[int, 1, 9999]):
    status, msg = addMoney(who.id, amount)
    if status == True:
      await interaction.response.send_message(f"{amount}¢ money has been given to @{who}")
    else:
      print(msg)

  async def giveMoney_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
      await interaction.response.send_message("❌ Only the bot owner can use this command!", ephemeral=True)
      


  





async def setup(bot: commands.Bot):
  await bot.add_cog(OwnerCommands(bot))