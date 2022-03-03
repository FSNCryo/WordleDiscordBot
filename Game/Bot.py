import discord
from discord.ext import commands
import numpy as np

bot = commands.Bot(command_prefix='!')

letters = {0: ":black_large_square:", 1: ":regional_indicator_a:", 2: ":regional_indicator_b:",
           3: ":regional_indicator_c:", 4: ":regional_indicator_d:", 5: ":regional_indicator_e:",
           6: ":regional_indicator_f:", 7: ":regional_indicator_g:", 8: ":regional_indicator_h:",
           9: ":regional_indicator_i:", 10: ":regional_indicator_j:", 11: ":regional_indicator_k:",
           12: ":regional_indicator_l:", 13: ":regional_indicator_m:", 14: ":regional_indicator_n:",
           15: ":regional_indicator_o:", 16: ":regional_indicator_p:", 17: ":regional_indicator_q:",
           18: ":regional_indicator_r:", 19: ":regional_indicator_s:", 20: ":regional_indicator_t:",
           21: ":regional_indicator_u:", 22: ":regional_indicator_v:", 23: ":regional_indicator_w:",
           24: ":regional_indicator_x:", 25: ":regional_indicator_y:", 26: ":regional_indicator_z:"}

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


async def editMessage():
    global msg
    embedVar = getNormalEmbededData(title="Wordle", description="{}".format(getGameGrid()))
    await msg.edit(embed=embedVar)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="start")
async def hello_world(ctx: commands.Context):
    await sendMessage(ctx)


@bot.command(name="test")
async def hello_world(ctx: commands.Context):
    reset()
    await editMessage()


with open("TOKEN.txt", "r") as f:
    TOKEN = f.readline()
    f.close()

bot.run(TOKEN)

# https://www.wordleunlimited.com/
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
# https://tutorial.vcokltfre.dev/tutorial/04-pong/


# create 'embed' grid like snake
# useful links
# https://github.com/Terra-rian/snakecord/blob/main/index.js
