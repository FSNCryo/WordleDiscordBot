import string

import discord
from discord.ext import commands
import numpy as np
import json

bot = commands.Bot(command_prefix='!')
intents = discord.Intents.default()
intents.dm_reactions = True
intents.reactions = True
bot.command(intents=intents)

import random

global word
global started
global index
letters = {0: ":white_square_button:", 1: "🇦", 2: "🇧", 3: "🇨", 4: "🇩", 5: "🇪", 6: "🇫", 7: "🇬", 8: "🇭",
           9: "🇮", 10: "🇯", 11: "🇰", 12: "🇱", 13: "🇲", 14: "🇳", 15: "🇴", 16: "🇵", 17: "🇶",
           18: "🇷", 19: "🇸", 20: "🇹", 21: "🇺", 22: "🇻", 23: "🇼", 24: "🇽", 25: "🇾", 26: "🇿",
           27: ":black_large_square:", 28: ":green_square:", 29: ":yellow_square:"}

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
global lettersLocationIndex
global lettersDeleted
lettersDeleted = ""
lettersLocationIndex = 0
lettersLocation = {}

Grid = np.array([
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
    [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27]
])


def getWord():
    with open("../Game/words.json", "r") as words_file:
        data = json.loads(words_file.read())

        words = data[0]["5"]
        num = random.randint(0, len(words) - 1)
        word = list(words.keys())[num]
        return word


def reset():
    global Grid, index
    index = 0
    Grid = np.array([
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
        [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27]
    ])

def resetRow(i):
    global Grid
    Grid[i] = [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27]

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
    embedVar.add_field(name="To Start enter a Word or Letter", value="\u200b")
    msg = await message.channel.send(embed=embedVar)


async def updateMessage():
    global msg
    embedVar = getNormalEmbededData(title="Wordle", description="{}".format(getGameGrid()))
    embedVar.add_field(name="Backspace = :arrow_backward:", value="\u200b", inline=True)
    embedVar.add_field(name="Enter Word = :arrow_right:", value="\u200b", inline=True)
    embedVar.add_field(name="Clear Row = :arrows_counterclockwise:", value="\u200b", inline=False)
    embedVar.add_field(name="Line: "+str(index+1), value="\u200b", inline=False)
    await msg.edit(embed=embedVar)

    #  add previously correct letters

    await msg.add_reaction('◀')
    await msg.add_reaction('➡')
    await msg.add_reaction('🔄')


# on reaction remove
@bot.event
async def on_reaction_add(reaction, user):
    # print("reaction added")
    global index, lettersLocationIndex, lettersDeleted
    emoji = reaction.emoji
    channel = reaction.message.channel
    if user == bot.user:
        return

    if emoji == "◀":
        tempList = list(lettersLocation)
        letter = lettersLocation[tempList[-1]]
        letterIndex = letter[0]
        letterNum = letter[1]

        lettersLocation.popitem()
        temp = np.where(Grid[letterIndex] == letterNum)
        squares = temp[0]
        nextSquare = squares[-1]
        Grid[index, nextSquare] = 0

        messages = await channel.history(limit=5).flatten()
        # check if the letter deleted is in messages, if so delete it
        letterChar = alphabet[letterNum-1]
        lettersDeleted = letterChar+lettersDeleted
        for message in messages:
            print("letters: " + lettersDeleted)
            print("message: " + message.content)
            if message.content == lettersDeleted:
                await message.delete()
                lettersDeleted = ""
                break

    if emoji == "🔄":
        messages = await channel.history(limit=5).flatten()
        lettersList = list(lettersLocation)

        guess = ""
        for message in messages:
            letterNum = lettersLocation[lettersList[0]]
            letter = alphabet[letterNum[1] - 1]
            guess += letter
            print(message.content)
            if message.content == guess:
                await message.delete()

            lettersList.pop(0)




        resetRow(index)

    if emoji == "➡":
        if len(Grid) < index + 1:
            return
        if 0 in Grid[index]:
            return

        wordArr = []
        for L in word:
            wordArr.append(L)
        letterIndexArr = []
        for i in wordArr:
            letterIndexArr.append(alphabet.index(i) + 1)
        temp = np.where(Grid[index] != 27)
        squares = temp[0]

        print("squares: ", squares)
        for i in range(5):
            print("i: ", i)
            squareIndex = squares[i]

            letterIndex = letterIndexArr[i]
            squareGrid = Grid[index, squareIndex]
            letter = alphabet[squareGrid - 1]

            if squareGrid == letterIndex:
                Grid[index, squareIndex - 1] = 28
                Grid[index, squareIndex + 1] = 28
                wordArr.pop(0)

            elif letter in wordArr:
                Grid[index, squareIndex - 1] = 29
                Grid[index, squareIndex + 1] = 29
                # NOTE: get the square value add one and get the letter from alphabet index

        # last line
        index += 1
    # 28 = green, 29 = yellow
    # if letter correct letter pos -1 and +1 == green etc
    await msg.remove_reaction(reaction, user)
    await updateMessage()
    return


@bot.event
async def on_ready():
    user = await bot.fetch_user(303249482651402261)
    await user.send("I'm online!")
    await bot.change_presence(activity=discord.Game(name="Wordle"))
    print('We have logged in as {0.user}'.format(bot))
    print("TODO: in on message check if it is the user who started the game")
    print("TODO: game doesn't work in DM (onReactionAdd not running in DM) (check intents)")
    print("TODO: put the wordle game in a separate file, this will allow for multiple games to be played at once")
    print("TODO: add a way to end the game")

@bot.event
async def on_message(message):
    global lettersLocationIndex, index

    if message.author == bot.user:
        return

    if message.content[0] == "!":
        await bot.process_commands(message)
        return

    temp = np.where(Grid[index] == 0)
    squares = temp[0]

    if len(squares) != 0:

        msgArr = []
        for i in message.content.lower():
            msgArr.append(i)

        temp = np.where(Grid[index] == 0)
        squares = temp[0]
        lettersByIndex = list(letters)

        for char in msgArr:
            for letter in letters:
                if len(squares) != 0 and letter != 0 and letter < 27:
                    nextSquare = squares[0]
                    if alphabet[letter - 1] == char:
                        Grid[index, nextSquare] = lettersByIndex[letter]  # add letters to grid
                        lettersLocation[lettersLocationIndex] = (index, Grid[index, nextSquare])  # save letters location (row and the letter)
                        lettersLocationIndex += 1

                        squares = np.delete(squares, 0)
                        continue

    await updateMessage()


@bot.command(name="start")
async def hello_world(ctx: commands.Context):
    global word
    reset()
    word = getWord()
    # await ctx.send("The word is: " + word)
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
