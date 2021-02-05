from discord.ext import commands
import random
import requests
import pprint
from datetime import datetime
import os
import re

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

#mute une personne
@bot.command()
async def mute(ctx, user_id):
    id_member = int(user_id[3:len(user_id)-1])
    if ctx.author.guild_permissions.mute_members:
            user = ctx.guild.get_member(id_member)
            await user.edit(mute=True)

#unmute
@bot.command()
async def unmute(ctx, user_id):
    id_member = int(user_id[3:len(user_id)-1])
    if ctx.author.guild_permissions.mute_members:
        user = ctx.guild.get_member(id_member)
        await user.edit(mute=False)

#Mute everyone on the bot channel
@bot.command()
async def muteAll(ctx, *args):
    if ctx.author.guild_permissions.mute_members:
        # member_tab = []
        # for user_id in args:
        #     id_member = int(user_id[3:len(user_id) - 1])
        #     member = ctx.guild.get_member(id_member)
        #     member_tab.append(member)
        # member_tab.append(ctx.author)

        #Supprimer dans la liste le membre ayant le meme id que dans arg
        print(member_tab, 'member_tab')
        members_current_channel = ctx.author.voice.channel.members
        for member in members_current_channel:
            await member.edit(mute=True)
        print(members_current_channel, 'member_channel')
    else:
        #Ejecter du salon vocal
        await ctx.author.edit(voice_channel=None)


#Unmute everyone on the channel
@bot.command()
async def unmuteAll(ctx, *args):
    if ctx.author.guild_permissions.mute_members:
        # #Membre a ne pas mute
        # member_tab = []
        # for user_id in args:
        #     id_member = int(user_id[3:len(user_id) - 1])
        #     member = ctx.guild.get_member(id_member)
        #     member_tab.append(member)

        members_current_channel = ctx.author.voice.channel.members
        # ajoute l'utilisateur dans les membres a mute
        # members_current_channel.append(ctx.author)
        for member in members_current_channel:
            await member.edit(mute=False)
    else:
        await ctx.author.edit(voice_channel=None)

#-----------------------------------------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------------------------------------------
#Affiche la documentation
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
            "-------------------------------------------\n" \
            "#mute #unmute <@username>\n" \
            " .mute une personne e.g #mute @Frayk (meme fonctionnement pour #unmute)\n" \
            "-------------------------------------------\n" \
            "#muteAll #unmuteAll e.g #muteAll <optional: @username>\n" \
            " .attention ces commandes ne sont pas autorisees aux personnes n'ayant pas les permissions\n" \
            " .mute toutes les personnes du salon sauf l'appelant\n" \
            " e.g #muteAll @Frayk @Skulld\n" \
            "  .mute tout le monde sauf l'appelant, frayk et skulld\n" \
            "-------------------------------------------\n" \
            "#help\n" \
            " .afficher la documentation\n```"

    await ctx.send(infos)

bot.run(os.environ['TOKEN'])