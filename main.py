from discord.ext import commands
import random
import requests
import pprint
from datetime import datetime
import os

pp = pprint.PrettyPrinter()
bot = commands.Bot(command_prefix='#', help_command=None)
api_key = os.environ['API_KEY']


#Nombre aleatoire entre 1 et 100
@bot.command()
async def rand(ctx):
    await ctx.send(f'```css\n{ctx.author} rolls {random.randint(1, 100)} (1-100)\n```')

#Affiche un message inspirant aleatoire via api request
@bot.command()
async def quote(ctx):
    response = requests.get(url="https://zenquotes.io/api/random")
    quote_dict = response.json()[0]
    await ctx.send(f'```fix\nBy {quote_dict["a"]}\n = {quote_dict["q"]}\n``` ')

#Meteo Actuelle
@bot.command()
async def meteo(ctx, city):
        response = requests.get(url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=fr&units=metric")
        meteo = response.json()
        pp.pprint(meteo)

        lever = meteo['sys']['sunrise'] + meteo['timezone']
        coucher = meteo['sys']['sunset'] + meteo['timezone']
        date_lever = datetime.utcfromtimestamp(lever).strftime('%H:%M')
        date_coucher = datetime.utcfromtimestamp(coucher).strftime('%H:%M')
        main = meteo['main']

        infos= f"```fix\nActuellement sur  {meteo['name']} \n" \
               f"{datetime.now().strftime('%d-%m-%Y')} à {datetime.now().strftime('%H:%M:%S')}              =\n" \
               f"---------------------------------------------------\n" \
               f"Ressenti = {main['feels_like']}°C - Temp = {main['temp']}°C\n" \
               f"Temp_Max = {main['temp_max']}°C - Temp_Min = {main['temp_min']}°C\n" \
               f"Description = {meteo['weather'][0]['description'].capitalize()}\n" \
               f"----------------------------------------------------\n"\
               f"Humidite = {main['humidity']}% - Pression = {main['pressure']}hPa\n" \
               f"Vent = {meteo['wind']['deg']}° - Vitesse = {meteo['wind']['speed']}m/s\n" \
               f"Nuage = {meteo['clouds']['all']}%\n" \
               f"Lever du soleil = {date_lever} - Coucher du soleil = {date_coucher}\n```"

        await ctx.send(infos)

@bot.command()
async def help(ctx):
    infos = "```Documentation Frayk BoT\n\n" \
            "#rand\n" \
            " .renvoyer un nombre aleatoire entre 1 et 100\n"\
            "-------------------------------------------\n" \
            "#quote\n" \
            " .afficher une citation inspirante en anglais\n" \
            "-------------------------------------------\n" \
            "#meteo <nom de la ville>\n" \
            " .fournir une météo détaillée e.g. #meteo paris\n" \
            "-------------------------------------------\n" \
            "#join #quit\n" \
            " .connecter le bot au salon vocal / deconnecter le bot du salon vocal\n" \
            "-------------------------------------------\n"\
            "#help\n" \
            " .afficher la documentation\n```"

    await ctx.send(infos)

#Connect/Disconnect
# Rejoindre un salon vocal
@bot.command()
async def join(ctx):
    if ctx.voice_client and ctx.voice_client.is_connected():
        channel = ctx.author.voice.channel
        await ctx.voice_client.move_to(channel)
    else:
        channel = ctx.author.voice.channel
        await channel.connect()

#Deconnecte le bot du salon
@bot.command()
async def quit(ctx):
    await ctx.voice_client.disconnect()


bot.run(os.environ['TOKEN'])