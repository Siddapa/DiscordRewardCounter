import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
import csv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
client = discord.Client()
bot = commands.Bot(command_prefix="!P")


dump_file = 'point_totals.json' # TODO Change to just JSON file name because won't be in repo
whitelist_file = 'whitelist.csv'


@bot.command(name='award')
async def award(ctx, username, points):
    with open('whitelist.csv', 'r') as f_wlist:
        wlist = csv.reader(f_wlist)
        if ctx.author not in wlist:
            await ctx.send('Not Authorized to Use This Command')

    username = username[3:-2] # Only keeps numbers
    points = int(points)
    try:
        with open(dump_file, 'r') as f_read:
            try:
                data = json.load(f_read)
            except ValueError:
                data = {}
    except FileNotFoundError:
        data = {}
    with open(dump_file, 'w') as f_write:
        try:
            data[username] += points
        except KeyError:
            data[username] = points
        f_write.seek(0)
        json.dump(data, f_write)

    await ctx.send('Previous Points ({}) + New Points ({}) = Total Points ({})'.format(int(data[username]) - points, points, data[username]))


@bot.command('my_points')
async def view_points(ctx, *args):
    with open(dump_file, 'r') as f_read:
        data = json.load(f_read)
        id = str(ctx.author.id)
        await ctx.send('Total Points: {}'.format(data[id]))


bot.run(BOT_TOKEN)