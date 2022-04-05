import string

import discord
from discord import reaction
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
letters = {
    0: ":white_square_button:",
    1: "🇦",
    2: "🇧",
    3: "🇨",
    4: "🇩",
    5: "🇪",
    6: "🇫",
    7: "🇬",
    8: "🇭",
    9: "🇮",
    10: "🇯",
    11: "🇰",
    12: "🇱",
    13: "🇲",
    14: "🇳",
    15: "🇴",
    16: "🇵",
    17: "🇶",
    18: "🇷",
    19: "🇸",
    20: "🇹",
    21: "🇺",
    22: "🇻",
    23: "🇼",
    24: "🇽",
    25: "🇾",
    26: "🇿",
    27: ":black_large_square:",
    28: ":green_square:",
    29: ":yellow_square:",
    30: ":white_medium_small_square:",
    31: ":white_medium_small_square:"
}

alphabet = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]
global lettersLocationIndex
global lettersDeleted
global players
lettersDeleted = ""
lettersLocationIndex = 0
lettersLocation = {}
players = {}
Grid = np.array([[27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                 [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                 [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                 [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                 [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                 [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27]])


def getWord():
    with open("commonWords.json", "r") as words_file:
        data = json.loads(words_file.read())

        words = data[0]["5"]
        num = random.randint(0, len(words) - 1)
        word = list(words.keys())[num]
        return word


def reset(userid):
    list(players[userid])[0] = np.array([[27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                                         [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                                         [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                                         [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                                         [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27],
                                         [27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27]])
    list(players[userid])[1] = 0




def resetRow(user, i):
    userid = user.author.id
    list(players[userid])[0][i] = [30, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 27, 27, 0, 31]


def getGameGrid(message):
    str = ""
    authid = message.author.id
    grid = players[authid][0]
    for row in grid:
        for square in row:
            letter = letters.get(square)
            str += letter

        str += "\n"

    return str


def getNormalEmbededData(title, description):
    return discord.Embed(title=title,
                         description=description,
                         color=discord.Color.dark_blue())


def getWinEmbededData(title, description):
    return discord.Embed(title=title,
                         description=description,
                         color=discord.Color.green())


def getLoseEmbededData(title, description):
    return discord.Embed(title=title,
                         description=description,
                         color=discord.Color.red())


async def sendMessage(message):
    global msg

    # get avatar url
    avatar_url = message.author.avatar_url
    embedVar = getNormalEmbededData(title="Wordle",
                                    description="{}".format(getGameGrid(message)))
    embedVar.add_field(name="To Start enter a Word or Letter", value="\u200b")

    embedVar.set_footer(text="{}".format(message.author.name), icon_url=avatar_url)
    msg = await message.channel.send(embed=embedVar)


async def win(user):
    global msg, started
    embedVar = getWinEmbededData(title="Wordle",
                                 description="{}".format(getGameGrid(user)))
    embedVar.add_field(name="YOU WIN!", value="\u200b", inline=True)
    embedVar.add_field(name="The Word Was: ||" + word + "||",
                       value="\u200b",
                       inline=True)
    embedVar.add_field(name="Completed in : ", value="\u200b", inline=False)
    embedVar.add_field(name=str(index + 1), value="\u200b", inline=False)
    await msg.edit(embed=embedVar)

    await msg.remove_reaction('◀', bot.user)
    await msg.remove_reaction('🔄', bot.user)
    await msg.remove_reaction('➡', bot.user)
    started = False


async def lose(user):
    global msg, started
    embedVar = getLoseEmbededData(title="Wordle",
                                  description="{}".format(getGameGrid(user)))
    embedVar.add_field(name="YOU LOSE!", value="\u200b", inline=True)
    embedVar.add_field(name="The Word Was: ",
                       value="||" + word + "||",
                       inline=True)
    await msg.edit(embed=embedVar)

    await msg.remove_reaction('◀', bot.user)
    await msg.remove_reaction('🔄', bot.user)
    await msg.remove_reaction('➡', bot.user)
    started = False


async def updateMessage(user):
    global msg, started
    if started:
        embedVar = getNormalEmbededData(title="Wordle",
                                        description="{}".format(getGameGrid(user)))
        embedVar.add_field(name="```Backspace = ◀\n"
                                "Clear : 🔄\n"
                                "Enter : ➡```",
                           value="\u200b",
                           inline=False)

        embedVar.add_field(name="Line: " + str(index + 1),
                           value="\u200b",
                           inline=False)

        embedVar.footer(text=user, icon_url=user.avatar_url)
        await msg.edit(embed=embedVar)

        await msg.add_reaction('◀')
        await msg.add_reaction('🔄')
        await msg.add_reaction('➡')


@bot.event
async def on_reaction_add(reaction, user):
    # print("reaction added")
    global index, lettersLocationIndex, lettersDeleted, lettersLocation
    emoji = reaction.emoji
    channel = reaction.message.channel
    if user == bot.user:
        return
    await msg.remove_reaction(reaction, user)

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
        letterChar = alphabet[letterNum - 1]
        lettersDeleted = letterChar + lettersDeleted
        for message in messages:

            if message.content == lettersDeleted:
                await message.delete()
                lettersDeleted = ""
                break

    if emoji == "🔄":
        messages = await channel.history(limit=5).flatten()
        guess = ""
        lettersList = list(lettersLocation)
        loopNum = len(lettersList)
        contents = [message.content for message in messages]
        for message in messages:
            for i in range(loopNum):
                print(lettersList[0])
                letterNum = lettersLocation[lettersList[0]]
                letter = alphabet[letterNum[1] - 1]
                guess += letter
                print("message content: " + message.content)
                print("guess: " + guess)
                print("lettersList: " + str(lettersList))
                print("\n")
                if message.content == guess:
                    await message.delete()
                    contents.remove(message.content)
                    if len(guess) == len(word):
                        return

                    guess = ""
                    lettersList = list(lettersLocation)
                    # guess += letter

                lettersList.pop(0)

        resetRow(user, index)

    if emoji == "➡":
        if len(Grid) < index + 1:
            return

        if 0 in Grid[index]:
            return

        Grid[index, 0] = 27
        Grid[index, -1] = 27

        wordArr = []
        for L in word:
            wordArr.append(L)
        letterIndexArr = []

        for i in wordArr:
            letterIndexArr.append(alphabet.index(i) + 1)

        temp = np.where(np.logical_and(Grid[index] >= 1, Grid[index] <= 26))
        squares = temp[0]
        for i in range(5):
            squareIndex = squares[i]

            letterIndex = letterIndexArr[i]
            squareGrid = Grid[index, squareIndex]

            if squareGrid == letterIndex:
                Grid[index, squareIndex - 1] = 28
                Grid[index, squareIndex + 1] = 28
                wordArr[wordArr.index(alphabet[letterIndex - 1])] = "*"

        for i in range(5):
            squareIndex = squares[i]

            squareGrid = Grid[index, squareIndex]
            letter = alphabet[squareGrid - 1]

            if letter in wordArr:
                Grid[index, squareIndex - 1] = 29
                Grid[index, squareIndex + 1] = 29

            # NOTE: get the square value add one and get the letter from alphabet index

        guessedWord = ""
        lettersList = list(lettersLocation)

        for L in lettersList:
            guessedWord += alphabet[lettersLocation[L][1] - 1]

        if guessedWord == word:
            print("correct")
            await win(user)
        elif index >= 5:
            await lose(user)

        index += 1
        Grid[index, 0] = 30
        Grid[index, -1] = 31
    # if guess != word and index = len(Grid) - 1: then end game.
    await msg.remove_reaction(reaction, user)
    await updateMessage(user)
    return


@bot.event
async def on_ready():
    user = await bot.fetch_user(303249482651402261)
    await user.send("I'm online!")
    await bot.change_presence(activity=discord.Game(name="Wordle"))
    print('We have logged in as {0.user}'.format(bot))
    print("TODO: in on message check if it is the user who started the game")
    print(
        "TODO: display username and pfp of the user that started each game making it easier to differentiate "
        "between games")
    print(
        "TODO: game doesn't work in DM (onReactionAdd not running in DM) (check intents)"
    )
    print(
        "TODO: put the wordle game in a separate file, this will allow for multiple games to be played at once"
    )
    print("TODO: check if the word entered is a word in words json")
    print("TODO: add date to win and lose messages")
    print("TODO: add daily Wordles")
    print(
        "TODO: delete users guess when on reaction add is reset and when guess is split into multiple messages"
    )
    print(
        "TODO: add dropdown menu because why not... (https://gist.github.com/lykn/a2b68cb790d6dad8ecff75b2aa450f23)"
    )


@bot.event
async def on_message(message):
    global lettersLocationIndex, index, lettersLocation

    if message.author == bot.user:
        return

    if message.content[0] == "!":
        await bot.process_commands(message)
        return
    player = players[message.author.id]
    grid = player[0]
    index = player[1]
    lettersLocation = {}
    temp = np.where(grid[index] == 0)
    squares = temp[0]

    if len(squares) != 0:

        msgArr = []
        for i in message.content.lower():
            msgArr.append(i)

        temp = np.where(grid[index] == 0)
        squares = temp[0]
        lettersByIndex = list(letters)

        for char in msgArr:
            for letter in letters:
                if len(squares) != 0 and letter != 0 and letter < 27:
                    nextSquare = squares[0]
                    if alphabet[letter - 1] == char:
                        grid[index, nextSquare] = lettersByIndex[
                            letter]  # add letters to grid
                        lettersLocation[lettersLocationIndex] = (
                            index, grid[index, nextSquare]
                        )  # save letters location (row and the letter)
                        lettersLocationIndex += 1

                        squares = np.delete(squares, 0)
                        continue

    if index == 0:
        grid[index, 0] = 30
        grid[index, -1] = 31
    await updateMessage(message.author)


@bot.command(name="start")
async def hello_world(ctx: commands.Context):
    global word, started

    word = getWord()
    # await ctx.send("The word is: " + word)
    print("The word is: " + word)
    players[ctx.author.id] = Grid, 0

    reset(ctx.author.id)

    started = True
    await sendMessage(ctx)


@bot.command(name="reset")
async def hello(ctx: commands.Context):
    reset(ctx.author.id)
    await updateMessage(ctx.author)


with open("TOKEN.txt", "r") as f:
    TOKEN = f.readline()
    f.close()

bot.run(TOKEN)
