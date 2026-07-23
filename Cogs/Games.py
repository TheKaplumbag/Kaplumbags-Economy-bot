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
  async def gamble(self, interaction: discord.Interaction, bet: app_commands.Range[int,1,9999], guess: app_commands.Range[int, 1, 4] ):
    await interaction.response.defer(thinking=True)
    beforeGambleCoins = getCoins(interaction.user.id)

    if beforeGambleCoins <= 0:
      await interaction.followup.send(f"{interaction.user} you cant play with {beforeGambleCoins}¢ balance!")
      return False
    if beforeGambleCoins < bet:
      await interaction.followup.send(f"YOU DONT HAVE ENOUGH MONEY YOU NEED {beforeGambleCoins-bet} MORE COINS!")
      return False

    status, msg = removeMoney(interaction.user.id, bet)
    reward = bet * 2
    if status == True: 
      randomNum = int(random.randint(1,4))
      if guess == randomNum:
        addMoney(interaction.user.id,reward)
        await interaction.followup.send(f"@{interaction.user} WON {reward}¢! number was: {randomNum} ")
      else:
        await interaction.followup.send(
          
          f"@{interaction.user} lost {bet}¢ 😢 number was: {randomNum}")
    else:
      print(msg)


  
  @Games_Group.command(name="coin-flip", description="flip a coin")
  @app_commands.choices(choice=[
    app_commands.Choice(name="Heads", value="heads"),
    app_commands.Choice(name="Tails", value="tails")
  ])
  async def coinFlip(self, interaction: discord.Interaction, bet: app_commands.Range[int, 1, 9999], choice: app_commands.Choice[str] ):
    await interaction.response.defer(thinking=True)
    beforeGambleCoins = getCoins(interaction.user.id)
    if beforeGambleCoins <= 0:
      await interaction.followup.send(f"You can't gamble with {beforeGambleCoins}¢")
      return False
    if beforeGambleCoins < bet:
      await interaction.followup.send(f"You cant bet more than you have!")
      return False
    removeMoney(interaction.user.id, bet)
    outcome = random.choice(["heads", "tails"])
    if choice.value == outcome:
      reward = bet * 2
      addMoney(interaction.user.id, reward)
      await interaction.followup.send(f"You've won {reward}¢!")
    else:
      await interaction.followup.send(f"You've lost {bet}¢!")

  @Games_Group.command(name="slots", description="Play slot")
  async def slots(self, interaction: discord.Interaction, bet: app_commands.Range[int,1,9999]):
    await interaction.response.defer(thinking=True)
    id = interaction.user.id
    beforeGambleCoins = getCoins(id)
    if beforeGambleCoins <= 0:
      await interaction.followup.send(f"You can't play with {beforeGambleCoins}¢")
      return False
    if beforeGambleCoins < bet:
      await interaction.followup.send(f"You can't bet more than you have!")
      return False

    removeMoney(id, bet)

    emojis = ["7️⃣", "💎", "🪙", "💲", "🍎"]
    reel1 = random.choice(emojis)
    reel2 = random.choice(emojis)
    reel3 = random.choice(emojis)

    result = f"**🎰:** **[{reel1} | {reel2} | {reel3}]** "

    if reel1 == reel2 == reel3:
      reward = bet * 5
      addMoney(id, reward)
      await interaction.followup.send(f"{result}\n\nHold up wait You just hit jackpooot! You've won **{reward}¢**!")
    elif reel1 == reel2 or reel2 == reel3 or reel1 == reel3:
      reward = round(bet * 1.5)
      addMoney(id,reward)
      await interaction.followup.send(f"{result}\n\nYou've hit the small prize! it's: ** {reward}¢**!")
    else:
      await interaction.followup.send(f"You've lost {bet}¢!")

  



async def setup(bot: commands.Bot):
  await bot.add_cog(GameCommands(bot))