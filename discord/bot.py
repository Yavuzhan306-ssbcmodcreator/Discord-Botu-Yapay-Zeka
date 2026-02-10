import discord
from discord.ext import commands
import os
from model import get_class

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def check(ctx):
  # Eğer mesajda görsel (attachment) varsa
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename  # Dosya adını al
            # Dosyayı bulunduğun klasöre indir
                        # Kullanıcıya dosyanın kaydedildiğini bildir
            await attachment.save(f"./{file_name}")

            await ctx.send(f"Saved the image to ./{file_name}")
            
            #buraya tahmin yapacak kodun yazılması lazım
            prediction = get_class(model_path = "keras_model.h5",
                                labels_path = "labels.txt",
                                image_path = f"./{file_name}")
            
            class_name , confidince = prediction  #confidince 0.80'e eşit yada daha düşükse "Bunu bilmiyorum"
            #Eğer yüksekse  await ctx.send (f"Tahmin Yapıldı Tahmininiz {prediction}")
            if (confidince <= 0.80):
                await ctx.send (f"Bunu Bilmiyorum {confidince}")
            else:
                await ctx.send (f"Tahmin Yapıldı Tahmininiz {prediction}")

    else:
        # Eğer görsel yoksa kullanıcıyı bilgilendir
        await ctx.send("You forgot to upload the image :(")
    

bot.run("secret token")
