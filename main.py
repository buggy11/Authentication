import os
import discord
import json
import socket
import string
from getmac import get_mac_address as gma
from discord.ext import commands
from pymongo import MongoClient

bot = commands.Bot(command_prefix='!')

BOT_TOKEN = ""

cluster = MongoClient("")

db = cluster["Authentication"]

collection = db["SoftwareLicenses"]

key_generate_list = []

@bot.event
async def on_ready():
    print('Online')

@bot.command()
async def generate(ctx, arg1, arg2):
    key_count = int(arg1)
    key_type = arg2
    if key_type == "lifetime":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Lifetime", "Suspended": "No", "User bound to": "null", "Mac Address": "null", "IP Address": "null"}
            collection.insert_one(post)
    if key_type == "renewal":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Renewal", "Suspended": "No", "User bound to": "null", "Mac Address": "null", "IP Address": "null"}
            collection.insert_one(post)
    if key_type == "beta":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Beta", "Suspended": "No", "User bound to": "null", "Mac Address": "null", "IP Address": "null"}
            collection.insert_one(post)
    if key_type == "fnf":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Friends and Family", "Suspended": "No", "User bound to": "null", "Mac Address": "null", "IP Address": "null"}
            collection.insert_one(post)
    if key_type == "staff":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Staff", "Suspended": "No", "User bound to": "null", "Mac Address": "null", "IP Address": "null"}
            collection.insert_one(post)

#working-finished

@bot.command()
async def bind(ctx, arg):
    key = arg
    check_database = collection.find( { "Key": key, "Bound": 'False' } ).count() > 0
    check_database_user = collection.find( {"User bound to": ctx.author.id}).count() > 0
    
    if check_database == True:
        if check_database_user == True:
            embed=discord.Embed(title="Cobra AIO", description="You already have a key bound.")
            embed.set_footer(text="Cobra AIO Authentication")
            await ctx.send(embed=embed)
            return
        embed=discord.Embed(title="Cobra AIO", description="Successfully bound. Welcome to Cobra AIO.")
        embed.set_footer(text="Cobra AIO Authentication")
        collection.update_one({"Key": key}, { "$set": {"Bound": "True"}} )
        collection.update_one({"Key": key}, { "$set": {"User bound to": ctx.author.id}})
        await ctx.send(embed=embed)
    
    elif check_database == False:
        embed=discord.Embed(title="Cobra AIO", description="That key either does not exist or is already bound.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
    else:
        await ctx.send('Error, contact an admin.')
#working-finished

@bot.command()
async def unbind(ctx, arg):
    key = arg
    check_database_user = collection.find( {"User bound to": ctx.author.id}).count() > 0
    check_database = collection.find( { "Key": key, "Bound": 'True' } ).count() > 0
    if check_database_user == False:
        embed=discord.Embed(title="Cobra AIO", description="You don't have a key bound.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
    if check_database == True:
        try:
            collection.update_one({"Key": key}, { "$set": {"Bound": "False"}})
            collection.update_one({"Key": key}, { "$set": {"User bound to": "null"}})
            collection.update_one({"Key": key}, { "$set": {"Active": "False"}})
            collection.update_one({"Key": key}, { "$set": {"Mac Address": "null"}})
            collection.update_one({"Key": key}, { "$set": {"IP Address": "null"}})
            embed=discord.Embed(title="Cobra AIO", description="Successfully unbound. We hope you enjoyed your time here being apart of Cobra.")
            embed.set_footer(text="Cobra AIO Authentication")
            await ctx.send(embed=embed)
        except:
            await ctx.send('Error contact an admin for further help.')
#working-finished

@bot.command()
async def deactivate(ctx):
    query = {"User bound to": ctx.author.id}
    query_results = collection.find_one(query)
    if query_results == None:
        embed=discord.Embed(title="Cobra AIO", description="You don't have a key bound.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
        return
    try:
        collection.update_one({"User bound to": ctx.author.id}, { "$set": {"Active": "False"}})
        embed=discord.Embed(title="Cobra AIO", description="Succesfully reset key.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
    except:
        await ctx.send("Error deactivating, contact an admin.")
#working-finished
@bot.command()
async def key_information(ctx):
    query = {"User bound to": ctx.author.id}
    query_results = collection.find_one(query)
    if query_results == None:
        embed=discord.Embed(title="Cobra AIO", description="You don't have a key bound.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
        return

    embed=discord.Embed(title="Key Information")
    embed.add_field(name="Key", value=query_results["Key"], inline=True)
    embed.add_field(name="Key Type", value=query_results["Key-type"], inline=True)
    embed.set_footer(text="Cobra AIO Authentication")
    await ctx.send(embed=embed)
#working-finished

@bot.command()
async def key_types(ctx):
    lifetime_count = collection.find( { "Key-Type": "Lifetime" } ).count()
    renewal_count = collection.find( { "Key-Type": "Renewal" } ).count()
    beta_count = collection.find( { "Key-Type": "Beta" } ).count()
    staff_count = collection.find( { "Key-Type": "Staff" } ).count()
    suspended_count = collection.find( {"Suspended": "Yes"} ).count()
    friends_and_family_count = collection.find( { "Key-Type": "Friends and Family" } ).count()
    embed=discord.Embed(title="Key Types")
    embed.add_field(name="Renewal", value=renewal_count, inline=True)
    embed.add_field(name="Lifetime", value=lifetime_count, inline=True)
    embed.add_field(name="Beta", value=beta_count, inline=True)
    embed.add_field(name="Friends and Family", value=friends_and_family_count, inline=True)
    embed.add_field(name="Staff", value=staff_count, inline=True)
    embed.add_field(name="Suspended", value=suspended_count, inline=True)
    embed.set_footer(text="Cobra AIO Authentication")
    await ctx.send(embed=embed)



@bot.command()
async def search_key(ctx, arg):
    key = arg
    query = {"Key": key}
    query_results = collection.find_one(query)
    if query_results == None:
        embed=discord.Embed(title="Cobra AIO", description="That license key doesn't exist.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
        return
    embed=discord.Embed(title="Cobra AIO")
    embed.add_field(name="Bound", value= query_results["Bound"], inline=True)
    embed.add_field(name="Active", value= query_results["Active"], inline=True)
    embed.add_field(name="Key-Type", value= query_results["Key-Type"], inline=True)
    embed.add_field(name="User Bound To", value= query_results["User bound to"], inline=True)
    embed.add_field(name="Suspended", value=query_results["Suspended"], inline=True)
    embed.set_footer(text="Cobra AIO Authentication")
    await ctx.send(embed=embed)
#working-finished

@bot.command()
async def search_user(ctx, arg):
    user = arg
    query = {"User bound to": int(user)}
    query_results = collection.find_one(query)
    if query_results == None:
        embed=discord.Embed(title="Cobra AIO", description="That user does not have a license key.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
        return
    embed=discord.Embed(title="Cobra AIO")
    embed.add_field(name="Key", value= query_results["Key"], inline=True)
    embed.add_field(name="Bound", value= query_results["Bound"], inline=True)
    embed.add_field(name="Active", value= query_results["Active"], inline=True)
    embed.add_field(name="Key-Type", value= query_results["Key-Type"], inline=True)
    embed.add_field(name="Suspended", value=query_results["Suspended"], inline=True)
    embed.set_footer(text="Cobra AIO Authentication")
    await ctx.send(embed=embed)
#working-finished
    



@bot.command()
async def terminate(ctx, arg):
    key = arg
    query = {"Key": key}
    query_results = collection.find_one(query)
    if query_results == None:
        embed=discord.Embed(title="Cobra AIO", description="That license key doesn't exist.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
        return
    try:
        collection.delete_one(query)
        embed=discord.Embed(title="Cobra AIO", description="Succesfully deleted key.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
    except:
        "Error deleting key."
#working-finished

@bot.command()
async def suspend(ctx, arg):
    key = arg
    query = {"Key": key}
    query_results = collection.find_one(query)

    if query_results == None:
        embed=discord.Embed(title="Cobra AIO", description="That license key doesn't exist.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
        return
    collection.update_one({"Key": key}, { "$set": {"Suspended": "Yes"}})
    collection.update_one({"Key": key}, { "$set": {"Mac Address": "null"}})
    collection.update_one({"Key": key}, { "$set": {"IP Address": "null"}})
    embed=discord.Embed(title="Cobra AIO", description="Succesfully suspended key.")
    embed.set_footer(text="Cobra AIO Authentication")
    await ctx.send(embed=embed)
#working-finished

@bot.command()
async def unsuspend(ctx, arg):
    key = arg
    query = {"Key": key}
    query_results = collection.find_one(query)
    if query_results == None:
        embed=discord.Embed(title="Cobra AIO", description="That license key doesn't exist.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
        return
    collection.update_one({"Key": key}, { "$set": {"Suspended": "No"}})
    embed=discord.Embed(title="Cobra AIO", description="Succesfully unsuspended key.")
    embed.set_footer(text="Cobra AIO Authentication")
    await ctx.send(embed=embed)
#working-finished


@bot.command()
async def key_list(ctx):
    key_list = []
    keys = collection.distinct("Key")
    for i in keys:
        key_list.append(i)
    formatted_list = "\n".join(i for i in key_list)
    await ctx.send(formatted_list)


#working-needs-improvements
    
    
        



bot.run('Nzg5OTg2NzA4OTM0NDkyMTkw.X96CdA.VGvvIDUofs9g7bqIqEHzR5o9Shs')
