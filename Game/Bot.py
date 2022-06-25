import json
import re

import discord
import numpy as np

from discord.ext import commands

bot = commands.Bot(command_prefix='!')
intents = discord.Intents.default()
intents.dm_reactions = True
intents.reactions = True
bot.command(intents=intents)

import random

letters = {
    # Blank space
    0: "<:Black_Border:961747628792623114>",
    # Black
    1: "<:Black_A:961692131649540178>",
    2: "<:Black_B:961692141527113758>",
    3: "<:Black_C:961692152373583963>",
    4: "<:Black_D:961692165958946836>",
    5: "<:Black_E:961692178747375626>",
    6: "<:Black_F:961692191200268288>",
    7: "<:Black_G:961692201795067974>",
    8: "<:Black_H:961692212326973440>",
    9: "<:Black_I:961692222288453662>",
    10: "<:Black_J:961692234238025808>",
    11: "<:Black_K:961692247680770118>",
    12: "<:Black_L:961692260867670026>",
    13: "<:Black_M:961692278206922852>",
    14: "<:Black_N:961692292157177917>",
    15: "<:Black_O:961692303955722252>",
    16: "<:Black_P:961692315884355615>",
    17: "<:Black_Q:961692327703875684>",
    18: "<:Black_R:961692340555251743>",
    19: "<:Black_S:961692353314291732>",
    20: "<:Black_T:961692368589946950>",
    21: "<:Black_U:961692378320756778>",
    22: "<:Black_V:961692387539836958>",
    23: "<:Black_W:961692406825254992>",
    24: "<:Black_X:961692417738829845>",
    25: "<:Black_Y:961692426911752212>",
    26: "<:Black_Z:961692442632015934>",
    # Grey
    27: "<:Grey_A:961682049775861821>",
    28: "<:Grey_B:961682062719455272>",
    29: "<:Grey_C:961682074614501416>",
    30: "<:Grey_D:961682084647272538>",
    31: "<:Grey_E:961682095145631835>",
    32: "<:Grey_F:961682106197618758>",
    33: "<:Grey_G:961682118222692382>",
    34: "<:Grey_H:961682128238690315>",
    35: "<:Grey_I:961682139626221618>",
    36: "<:Grey_J:961682151949090876>",
    37: "<:Grey_K:961682163491807253>",
    38: "<:Grey_L:961682174183088148>",
    39: "<:Grey_M:961682189328736366>",
    40: "<:Grey_N:961682203618725908>",
    41: "<:Grey_O:961682216574943292>",
    42: "<:Grey_P:961682226607698000>",
    43: "<:Grey_Q:961682240159481916>",
    44: "<:Grey_R:961682250037088276>",
    45: "<:Grey_S:961682259969191976>",
    46: "<:Grey_T:961682271415443546>",
    47: "<:Grey_U:961682282245132341>",
    48: "<:Grey_V:961682294031155330>",
    49: "<:Grey_W:961682304990859304>",
    50: "<:Grey_X:961682315434663956>",
    51: "<:Grey_Y:961682368148668426>",
    52: "<:Grey_Z:961682382203789412>",
    # Yellow
    53: "<:Yellow_A:961671667887788063>",
    54: "<:Yellow_B:961671713366634556>",
    55: "<:Yellow_C:961671725890830346>",
    56: "<:Yellow_D:961671764633600000>",
    57: "<:Yellow_E:961671779338813460>",
    58: "<:Yellow_F:961671792903204894>",
    59: "<:Yellow_G:961671805624541184>",
    60: "<:Yellow_H:961671934293213195>",
    61: "<:Yellow_I:961671972692058194>",
    62: "<:Yellow_J:961672009522245682>",
    63: "<:Yellow_K:961672023673811004>",
    64: "<:Yellow_L:961672038169317496>",
    65: "<:Yellow_M:961672048701227052>",
    66: "<:Yellow_N:961672060218798090>",
    67: "<:Yellow_O:961672071715356762>",
    68: "<:Yellow_P:961672083883044964>",
    69: "<:Yellow_Q:961672101562044426>",
    70: "<:Yellow_R:961672117508800552>",
    71: "<:Yellow_S:961672131505193041>",
    72: "<:Yellow_T:961672148336902154>",
    73: "<:Yellow_U:961672165734895676>",
    74: "<:Yellow_V:961672179374784542>",
    75: "<:Yellow_W:961672195287953518>",
    76: "<:Yellow_X:961672208269320212>",
    77: "<:Yellow_Y:961672222907445339>",
    78: "<:Yellow_Z:961672235884638279>",
    # Green
    79: "<:Green_A:961674702517071892>",
    80: "<:Green_B:961674714290470994>",
    81: "<:Green_C:961674725602496613>",
    82: "<:Green_D:961674740500672572>",
    83: "<:Green_E:961674761975509014>",
    84: "<:Green_F:961674771559493662>",
    85: "<:Green_G:961674780971528243>",
    86: "<:Green_H:961674789162987561>",
    87: "<:Green_I:961674800315654144>",
    88: "<:Green_J:961674810918830160>",
    89: "<:Green_K:961674821572366338>",
    90: "<:Green_L:961674831508672562>",
    91: "<:Green_M:961674840576782376>",
    92: "<:Green_N:961674852874465280>",
    93: "<:Green_O:961674866011033663>",
    94: "<:Green_P:961674879248257115>",
    95: "<:Green_Q:961674890639998997>",
    96: "<:Green_R:961674902107226233>",
    97: "<:Green_S:961674913121468456>",
    98: "<:Green_T:961674924966162443>",
    99: "<:Green_U:961674935598714910>",
    100: "<:Green_V:961674944939438151>",
    101: "<:Green_W:961674960147988510>",
    102: "<:Green_X:961674973167095818>",
    103: "<:Green_Y:961674985292845096>",
    104: "<:Green_Z:961674995879260331>",
    # Blank Colours
    # 105: "<:Grey:961682393851387954>",
    # 106: "<:Green:961681613085868042>",
    # 107: "<:Yellow:961681400174641242>",

}

alphabet = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]
global lettersLocationIndex
global lettersDeleted
global players
global customPlayers
lettersDeleted = ""
lettersLocationIndex = 0
lettersLocation = {}
players = {}
customPlayers = {}
Grid = np.array([[0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]])


def getWord():
    with open("commonWords.json", "r") as words_file:
        data = json.loads(words_file.read())

        words = data[0]["5"]
        num = random.randint(0, len(words) - 1)
        word = list(words.keys())[num]
        return word


def resetGrid():
    global Grid
    Grid = np.array([[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]])


def reset(userid):
    list(players[userid])[0] = np.array([[0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0]])
    list(players[userid])[1] = 0


def resetRow(userid, i):
    list(players[userid])[0][i] = [0, 0, 0, 0, 0]


def getGameGrid(authid):
    string = ""

    grid = list(players[authid])[0]
    for row in grid:
        for square in row:
            letter = letters.get(square)
            try:
                string += letter
            except TypeError:
                print("Error concatenating the letter: " + str(letter))

        string += "\n"

    return string


def customResetGrid():
    global Grid
    Grid = np.array([[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]])


def customReset(userid):
    list(players[userid])[0] = np.array([[0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0]])
    list(players[userid])[1] = 0


def customResetRow(userid, i):
    list(players[userid])[0][i] = [0, 0, 0, 0, 0]


def customGetGameGrid(authid):
    string = ""

    grid = list(players[authid])[0]
    for row in grid:
        for square in row:
            letter = letters.get(square)
            try:
                string += letter
            except TypeError:
                print("Error concatenating the letter: " + str(letter))

        string += "\n"

    return string


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
    word = getWord()
    print(message.author.name + "'s word is: " + word)
    players[message.author.id] = Grid, 0, 0, True, word
    avatar_url = message.author.avatar_url
    authid = message.author.id
    embedVar = getNormalEmbededData(title="Wordle",
                                    description="{}".format(getGameGrid(authid)))
    embedVar.add_field(name="To Start enter a Word or Letter", value="\u200b")

    embedVar.set_footer(text="{}".format(message.author.name + "#" + message.author.discriminator), icon_url=avatar_url)
    msg = await message.channel.send(embed=embedVar)

    players[message.author.id] = players[message.author.id][0], 0, msg.id, players[message.author.id][3], \
                                 players[message.author.id][4]

    reset(message.author.id)


async def customSendMessage(message, user, word):
    print(message.author.name + "'s word is: " + word)
    customPlayers[message.author.id] = Grid, 0, 0, True, word
    avatar_url = message.author.avatar_url
    authid = message.author.id
    embedVar = getNormalEmbededData(title="Wordle",
                                    description="{}".format(getGameGrid(authid)))
    embedVar.add_field(name="To Start enter a Word or Letter", value="\u200b")

    embedVar.add_field(name=f"{user} Has Sent You a Wordle!", value="\u200b")

    embedVar.set_footer(text="{}".format(message.author.name + "#" + message.author.discriminator), icon_url=avatar_url)
    msg = await message.channel.send(embed=embedVar)
    # send the message to the user who sent the message as well
    # do this to update message as well
    customPlayers[message.author.id] = customPlayers[message.author.id][0], 0, msg.id, customPlayers[message.author.id][
        3], customPlayers[message.author.id][4]

    reset(message.author.id)  # customReset?


async def customWin(channelid, userId):
    embedVar = getWinEmbededData(title="Wordle",
                                 description="{}".format(getGameGrid(userId)))
    embedVar.add_field(name="YOU WIN!", value="\u200b", inline=True)
    embedVar.add_field(name="The Word Was: ||" + players[userId][4] + "||",
                       value="\u200b",
                       inline=True)

    embedVar.add_field(name="Completed in : " + str(list(players[userId])[1] + 1), value="\u200b", inline=False)

    message = await bot.get_channel(channelid).fetch_message(players[userId][2])

    await message.edit(embed=embedVar)

    await message.remove_reaction('◀', bot.user)
    await message.remove_reaction('🔄', bot.user)
    await message.remove_reaction('➡', bot.user)

    customPlayers[userId] = Grid, 0, None, False
    del players[userId]


async def customLose(channelid, userId):
    embedVar = getLoseEmbededData(title="Wordle",
                                  description="{}".format(getGameGrid(userId)))
    embedVar.add_field(name="YOU LOSE!", value="\u200b", inline=True)

    embedVar.add_field(name="The Word Was: ||" + players[userId][4] + "||",
                       value="\u200b",
                       inline=True)

    message = await bot.get_channel(channelid).fetch_message(players[userId][2])

    await message.edit(embed=embedVar)

    await message.remove_reaction('◀', bot.user)
    await message.remove_reaction('🔄', bot.user)
    await message.remove_reaction('➡', bot.user)

    customPlayers[userId] = Grid, 0, None, False
    del players[userId]


async def win(channelid, userId):
    embedVar = getWinEmbededData(title="Wordle",
                                 description="{}".format(getGameGrid(userId)))
    embedVar.add_field(name="YOU WIN!", value="\u200b", inline=True)
    embedVar.add_field(name="The Word Was: ||" + players[userId][4] + "||",
                       value="\u200b",
                       inline=True)

    embedVar.add_field(name="Completed in : " + str(list(players[userId])[1] + 1), value="\u200b", inline=False)

    message = await bot.get_channel(channelid).fetch_message(players[userId][2])

    await message.edit(embed=embedVar)

    await message.remove_reaction('◀', bot.user)
    await message.remove_reaction('🔄', bot.user)
    await message.remove_reaction('➡', bot.user)

    players[userId] = Grid, 0, None, False
    del players[userId]


async def lose(channelid, userId):
    embedVar = getLoseEmbededData(title="Wordle",
                                  description="{}".format(getGameGrid(userId)))
    embedVar.add_field(name="YOU LOSE!", value="\u200b", inline=True)

    embedVar.add_field(name="The Word Was: ||" + players[userId][4] + "||",
                       value="\u200b",
                       inline=True)

    message = await bot.get_channel(channelid).fetch_message(players[userId][2])

    await message.edit(embed=embedVar)

    await message.remove_reaction('◀', bot.user)
    await message.remove_reaction('🔄', bot.user)
    await message.remove_reaction('➡', bot.user)

    players[userId] = Grid, 0, None, False
    del players[userId]


async def updateMessage(channel_id, user_id, user_name, user_avatar):
    if user_id not in players:
        return

    if list(players[user_id])[3]:
        embedVar = getNormalEmbededData(title="Wordle",
                                        description="{}".format(getGameGrid(user_id)))

        embedVar.add_field(name="Line: " + str(list(players[user_id])[1] + 1),
                           value="\u200b",
                           inline=False)

        embedVar.set_footer(text="{}".format(user_name), icon_url=user_avatar)

        message = await bot.get_channel(channel_id).fetch_message(players[user_id][2])
        await message.edit(embed=embedVar)
        # check if channel is not a dm
        if message.channel.type != discord.ChannelType.private:
            await message.add_reaction('◀')
            await message.add_reaction('🔄')
            await message.add_reaction('➡')

        if message.channel.type == discord.ChannelType.private:
            embedVar.add_field(name="**Clear line:** /", value="\u200b")
            embedVar.add_field(name="**Backspace:** -", value="\u200b")
            embedVar.add_field(name="**Enter Word:** .", value="\u200b")

@bot.event
async def on_reaction_add(reaction, user):
    global lettersLocationIndex, lettersDeleted, lettersLocation

    if user == bot.user:
        return

    emoji = reaction.emoji

    channel = reaction.message.channel

    msg = players[user.id][2]

    index = list(players[user.id])[1]

    word = players[user.id][4]

    await reaction.remove(user)

    if emoji == "◀":
        await backspace(user.id, channel)

    if emoji == "🔄":
        await clear(user.id, channel)

    if emoji == "➡":
        await nextLine(user.id, channel.id)

    await updateMessage(channel.id, user.id, user.display_name + "#" + user.discriminator, user.avatar_url)
    return


async def nextLine(userId, channelId):
    word = players[userId][4]
    index = players[userId][1]

    if len(players[userId][0]) < index + 1:
        return

    if 0 in players[userId][0][index]:
        return

    guessedWord = ""
    lettersList = list(lettersLocation)

    for L in lettersList:
        guessedWord += alphabet[lettersLocation[L][1] - 1]

    with open("commonWords.json", "r") as words_file:
        data = json.loads(words_file.read())

        words = data[0]["5"].keys()
        if guessedWord not in words:
            channel = bot.get_channel(channelId)

            guessedWord = re.sub(r'[^a-zA-Z]', '', guessedWord)
            await channel.send(
                f"<@{userId}> The word ` {guessedWord} ` is not in the list of common words. Please try again.")
            await clear(userId, channel)
            return

    wordArr = []
    for L in word:
        wordArr.append(L)
    letterIndexArr = []

    for i in wordArr:
        letterIndexArr.append(alphabet.index(i) + 1)

    for i in range(5):
        letterIndex = letterIndexArr[i]
        squareGrid = players[userId][0][index, i]

        if squareGrid == letterIndex:
            players[userId][0][index, i] += 78  # Green

            wordArr[i] = "*"

    for i in range(5):
        letter = alphabet[players[userId][0][index, i] - 1]

        if letter == "*":
            continue

        if letter in wordArr:
            players[userId][0][index, i] += 52  # Yellow

            for L in wordArr:
                if L == letter:
                    wordArr[wordArr.index(L)] = "*"

    for i in range(5):
        if players[userId][0][index, i] <= 26:
            players[userId][0][index, i] += 26  # Grey

    if guessedWord == word:
        await win(channelId, userId)
        return
    elif index >= 5:
        await lose(channelId, userId)
        return

    index += 1
    players[userId] = (
        players[userId][0], players[userId][1] + 1, players[userId][2], players[userId][3], players[userId][4])


async def backspace(userId, channel):
    global lettersLocationIndex, lettersDeleted, lettersLocation

    index = players[userId][1]

    tempList = list(lettersLocation)
    letter = lettersLocation[tempList[-1]]
    letterIndex = letter[0]
    letterNum = letter[1]

    lettersLocation.popitem()
    temp = np.where(list(players[userId])[0][letterIndex] == letterNum)
    squares = temp[0]
    nextSquare = squares[-1]
    list(players[userId])[0][index, nextSquare] = 0

    messages = [message for message in await channel.history(limit=50).flatten() if message.author.id == userId]
    messages = messages[:10]  # only look at the first 10 messages
    # check if the letter deleted is in messages, if so delete it
    letterChar = alphabet[letterNum - 1]
    lettersDeleted = letterChar + lettersDeleted
    for message in messages:
        if message.content == lettersDeleted:
            await message.delete()
            lettersDeleted = ""
            break


async def clear(userId, channel):
    word = players[userId][4]
    index = players[userId][1]

    global lettersLocationIndex, lettersDeleted, lettersLocation
    messages = [message for message in await channel.history(limit=50).flatten() if message.author.id == userId]
    resetRow(userId, index)

    guess = ""
    lettersList = list(lettersLocation)
    loopNum = len(lettersList)

    for message in messages:
        for i in range(loopNum):
            letterNum = lettersLocation[lettersList[i]]
            letter = alphabet[letterNum[1] - 1]
            guess += letter
            if message.content == guess:
                await message.delete()
                print("deleted")
                if len(guess) == len(word):
                    break

                guess = ""
                lettersList = list(lettersLocation)


@bot.event
async def on_ready():
    user = await bot.fetch_user(303249482651402261)
    await user.send("I'm online!")
    await bot.change_presence(activity=discord.Game(name="Wordle"))
    print('We have logged in as {0.user}'.format(bot))
    print("TODO: in on message check if it is the user who started the game")
    print(
        "TODO: display username and pfp of the user that started each game making it easier to differentiate between games")
    print("TODO: game doesn't work in DM (onReactionAdd not running in DM) (check intents)")
    print("TODO: put the wordle game in a separate file, this will allow for multiple games to be played at once")
    print("TODO: check if the word entered is a word in words json")
    print("TODO: add date to win and lose messages")
    print("TODO: add daily Wordles")
    print("TODO: delete users guess when on reaction add is reset and when guess is split into multiple messages")
    print("TODO: add dropdown menu because why not... (https://gist.github.com/lykn/a2b68cb790d6dad8ecff75b2aa450f23)")
    print("TODO: ability to create and send wordles to friends DMs")


@bot.event
async def on_message(message):
    global lettersLocationIndex, lettersLocation

    if message.author == bot.user:
        return

    if message.content[0] == "!":
        await bot.process_commands(message)
        return

    if message.author.id not in players:
        print("user " + str(message.author.id) + " has not started a game")
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

    if message.content[-1] == ".":
        await nextLine(message.author.id, message.channel.id)

    if "-" in message.content:
        await backspace(message.author.id, message.channel)

    if "/" in message.content:
        await clear(message.author.id, message.channel)

    await updateMessage(message.channel.id, message.author.id,
                        message.author.display_name + "#" + message.author.discriminator, message.author.avatar_url)


@bot.command(name="start")
async def StartGame(ctx: commands.Context):
    try:
        if players[ctx.author.id] in players:
            del players[ctx.author.id]

    except:
        pass
    resetGrid()
    await sendMessage(ctx)


@bot.command(aliases=["words", "wordlist", "list"])
async def Profile(ctx: commands.Context):
    with open("commonWords.json", "r") as words_file:
        data = json.loads(words_file.read())

        wordsDict = data[0]["5"].keys()

        words = "```"
        for word in wordsDict:
            words += word + ", "
        words += "```"

    await ctx.send(words)


@bot.command(name="reset")
async def hello(ctx: commands.Context):
    reset(ctx.author.id)
    await updateMessage(ctx.channel.id, ctx.author.id, ctx.author.display_name + "#" + ctx.author.discriminator,
                        ctx.author.avatar_url)


with open("TOKEN.txt", "r") as f:
    TOKEN = f.readline()
    f.close()

bot.run(TOKEN)
