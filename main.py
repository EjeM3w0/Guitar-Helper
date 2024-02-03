import discord
from discord.ext import commands
from model import get_class

guitar_info = {'классическая гитара': 'https://www.youtube.com/watch?v=1lYaVJMRRTE',
               'акустическая гитара': 'https://www.youtube.com/watch?v=1ZZV9bODLEY',
               'электрогитара stratocaster': 'https://www.youtube.com/watch?v=sioBKPlRnhs',
               'электрогитара telecaster': 'https://www.youtube.com/watch?v=VDrrYyRooag',
               'электрогитара explorer': 'https://www.youtube.com/watch?v=m8TyGbWykUI'}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send("Привет! Я - бот GuitarHelper. Я помогаю начинающим гитаристам, незнающим особенности разных гитар. С помощью комманды $howtoplay вы можете разобраться, какая у вас гитара и какие у неё особености")

@bot.command()
async def howtoplay(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            photo_name = attachment.filename
            if photo_name.endswith('.jpg') or photo_name.endswith('.jpeg') or photo_name.endswith('.png'):
                await attachment.save(f'images/{photo_name}')
                wait_message = await ctx.send("секундочку, ваша картинка обрабатывается...")
                class_name,score = get_class(model_path='gtm_model/keras_model.h5', label_path='gtm_model/labels.txt', image_path=f'images/{photo_name}')
                await wait_message.delete()
                await ctx.send(f"На вашем фото с вероятностью {score} [{class_name}]({guitar_info.get(class_name)})")
            else:
                await ctx.send("Простите, но я приинмаю файлы таких расширений как png, jpg и jpeg")
                return
    else:
        await ctx.send("Прошу вас прикрепить фото для распознавания")

bot.run("MTIwMDc3MTUxNzAzNDc5OTE5NA.GrH0rL.ueM-dLxk_lK5BE2RTOC--PeJdmZZc9Toka-PKY")