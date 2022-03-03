from discord.ext import commands

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="hello")
async def hello_world(ctx: commands.Context):
    await ctx.send("Hello, world!")


bot.run('OTQ4MzMyMjA3NzQ1OTQ1NjUy.Yh6RMQ.XkaWYCV_NuB0iQhSIhCQ_48JxeI')

# https://www.wordleunlimited.com/
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
# https://tutorial.vcokltfre.dev/tutorial/04-pong/


# create 'embed' grid like snake
# useful links
# https://github.com/Terra-rian/snakecord/blob/main/index.js
