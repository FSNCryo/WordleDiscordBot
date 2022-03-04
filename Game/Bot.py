import discord
from discord.ext import commands
import numpy as np

bot = commands.Bot(command_prefix='!')

global started
global square
square = 0
letters = {0: ":black_large_square:", 1: "🇦", 2: "🇧", 3: "🇨", 4: "🇩", 5: "🇪", 6: "🇫", 7: "🇬", 8: "🇭",
           9: "🇮", 10: "🇯", 11: "🇰", 12: "🇱", 13: "🇲", 14: "🇳", 15: "🇴", 16: "🇵", 17: "🇶",
           18: "🇷", 19: "🇸", 20: "🇹", 21: "🇺", 22: "🇻", 23: "🇼", 24: "🇽", 25: "🇾", 26: "🇿"}

Grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])


def reset():
    global Grid
    Grid = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])


def getGameGrid():
    str = ""

    for row in Grid:
        for square in row:
            letter = letters.get(square)
            str += letter

        str += "\n"

    return str


def getNormalEmbededData(title, description):
    return discord.Embed(title=title, description=description, color=discord.Color.green())


def getErrorEmbededData(title, description):
    return discord.Embed(title=title, description=description, color=discord.Color.red())


async def sendMessage(message):
    global msg
    embedVar = getNormalEmbededData(title="Wordle", description="{}".format(getGameGrid()))
    msg = await message.channel.send(embed=embedVar)
    for letter in letters:
        if letter != 0:
            await msg.add_reaction(letters[letter])


async def updateMessage():
    global msg
    embedVar = getNormalEmbededData(title="Wordle", description="{}".format(getGameGrid()))
    await msg.edit(embed=embedVar)

@bot.event
async def on_reaction_add(reaction, user):
    global square
    letter = reaction.emoji

    if user.bot:
        return

    for row in range(0, len(Grid)):
        if Grid[row, square] == 0:
            Grid[row, square] = list(letters.keys())[list(letters.values()).index(letter)]
            print("row: " + str(Grid[row]))
            print("grid: " + str(len(Grid)))

            print("square: " + str(square))
            await updateMessage()
            square += 1
            return
        square += 1
        if row == Grid[row, -1]:
            return


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="start")
async def hello_world(ctx: commands.Context):
    global started
    started = True
    await sendMessage(ctx)


@bot.command(name="reset")
async def hello(ctx: commands.Context):
    reset()
    await updateMessage()


with open("TOKEN.txt", "r") as f:
    TOKEN = f.readline()
    f.close()

bot.run(TOKEN)

# https://www.wordleunlimited.com/
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
# https://tutorial.vcokltfre.dev/tutorial/04-pong/


# create 'embed' grid like snake
# useful links
# https://faun.pub/creating-discord-game-bot-using-discord-api-and-python-free-hosting-in-cloud-e127206fafb5
# https://github.com/Terra-rian/snakecord/blob/main/index.js
