import discord
from discord import app_commands
from discord.ext import commands
from Functions.DataFunctions import getCoins, addMoney, removeMoney
import random

class GameCommands(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  Games_Group = app_commands.Group(name="games", description="Games")
  
  @Games_Group.command(name="guess-number", description="Gamble!!!")
  async def gamble(self, interaction: discord.Interaction, bet: int, guess: int ):
    interaction.response.defer(thinking=True)
    beforeGambleCoins = getCoins(interaction.user.id)

    if beforeGambleCoins < bet:
      await interaction.response.send_message(f"YOU DONT HAVE ENOUGH MONEY YOU NEED {bet - beforeGambleCoins} more coins!")

    status : bool, msg = removeMoney(interaction.user.id, bet)
    reward = bet * 2
    if status == True: 
      randomNum = int(random.random(1,10))
      if guess == randomNum:
        addMoney(interaction.user.id,reward)
        await interaction.response.send_message(f"{interaction.user} WON {reward}¢!")
      else:
        await interaction.response.send_message(f"{interaction.user} lost {bet}¢ 😢")
    else:
      print(msg)
      
    



async def setup(bot: commands.Bot):
  await bot.add_cog(GameCommands(bot))