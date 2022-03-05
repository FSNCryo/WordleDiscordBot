import string

import discord
from discord.ext import commands
import numpy as np

bot = commands.Bot(command_prefix='!')

global started
global index
index = 0
letters = {0: ":black_large_square:", 1: "🇦", 2: "🇧", 3: "🇨", 4: "🇩", 5: "🇪", 6: "🇫", 7: "🇬", 8: "🇭",
           9: "🇮", 10: "🇯", 11: "🇰", 12: "🇱", 13: "🇲", 14: "🇳", 15: "🇴", 16: "🇵", 17: "🇶",
           18: "🇷", 19: "🇸", 20: "🇹", 21: "🇺", 22: "🇻", 23: "🇼", 24: "🇽", 25: "🇾", 26: "🇿",
           27: ":black_large_square:"}

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

Grid = np.array([
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27]
])


def reset():
    global Grid
    Grid = np.array([
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27]
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


async def updateMessage():
    global msg
    embedVar = getNormalEmbededData(title="Wordle", description="{}".format(getGameGrid()))
    await msg.edit(embed=embedVar)


# on reaction remove
@bot.event
async def on_reaction_add(reaction, user):
    await updateMessage()
    return


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    global index

    if message.author == bot.user:
        return

    temp = np.where(Grid[index] == 0)
    squares = temp[0]
    # when you click enter it does index += 1 to change row (until then stops you from entering values)
    if message.content[0] == "!":  # put all code in if statement don't do index += 1
        await bot.process_commands(message)
        return

    if len(squares) != 0:

        msgArr = []
        for i in message.content:
            msgArr.append(i)

        temp = np.where(Grid[index] == 0)
        squares = temp[0]
        lettersByIndex = list(letters)

        for char in msgArr:
            for letter in letters:
                if len(squares) != 0 and letter != 0 and letter != 27:
                    nextSquare = squares[0]
                    if alphabet[letter - 1] == char:
                        Grid[index, nextSquare] = lettersByIndex[letter]
                        await updateMessage()
                        squares = np.delete(squares, 0)
                        continue

        index += 1


@bot.command(name="start")
async def hello_world(ctx: commands.Context):
    reset()
    global started
    started = True
    await sendMessage(ctx)


@bot.command(name="reset")
async def hello(ctx: commands.Context):
    reset()
    await updateMessage()


with open("../TOKEN/TOKEN.env", "r") as f:
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
