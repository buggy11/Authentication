import os
import discord
import json
import socket
import random
import string
from getmac import get_mac_address as gma
from discord.ext import commands
from pymongo import MongoClient

bot = commands.Bot(command_prefix='!')

cluster = MongoClient("")
#left blank because of security

db = cluster["Authentication"]

collection = db["testing2"]

key_generate_list = []

@bot.event
async def on_ready():
    print('Online')

@bot.command()
@commands.has_role(803449976600264724)
async def generate(ctx, arg1, arg2):
    key_count = int(arg1)
    key_type = arg2
    if key_type == "lifetime":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Lifetime", "Suspended": "False", "User bound to": "null", "Mac Address": "null", "IP Address": "null", "Claimed": "Null(generated)"}
            collection.insert_one(post)
    if key_type == "renewal":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Renewal", "Suspended": "False", "User bound to": "null", "Mac Address": "null", "IP Address": "null", "Claimed": "Null(generated)"}
            collection.insert_one(post)
    if key_type == "beta":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Beta", "Suspended": "False", "User bound to": "null", "Mac Address": "null", "IP Address": "null", "Claimed": "Null(generated)"}
            collection.insert_one(post)
    if key_type == "fnf":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Friends and Family", "Suspended": "False", "User bound to": "null", "Mac Address": "null", "IP Address": "null", "Claimed": "Null(generated)"}
            collection.insert_one(post)
    if key_type == "staff":
        for i in range(key_count):
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            await ctx.send(key)
            post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": "Staff", "Suspended": "False", "User bound to": "null", "Mac Address": "null", "IP Address": "null", "Claimed": "Null(generated)"}
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
        
        collection.update_one({"Key": key}, { "$set": {"Bound": "True"}} )
        collection.update_one({"Key": key}, { "$set": {"User bound to": ctx.author.id}})
        key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        collection.update_one({"User bound to": ctx.author.id}, { "$set": {"Key": key}})
        
        embed=discord.Embed(title="Cobra AIO", description="Successfully bound. Welcome to Cobra AIO.")
        embed.set_footer(text="Cobra AIO Authentication")
        embed.add_field(name="Important", value='To ensure safety, your key has automatically been reset. Please use the !key_information command to access the new one.')
        await ctx.send(embed=embed)
    
    elif check_database == False:
        embed=discord.Embed(title="Cobra AIO", description="That key either does not exist or is already bound.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
    else:
        await ctx.send('Error, contact an admin.')
#working-finished

@bot.command()
async def unbind(ctx):
    check_database_user = collection.find( {"User bound to": ctx.author.id}).count() > 0
    check_database = collection.find( { "User bound to": ctx.author.id, "Bound": 'True' } ).count() > 0
    if check_database_user == False:
        embed=discord.Embed(title="Cobra AIO", description="You don't have a key bound.")
        embed.set_footer(text="Cobra AIO Authentication")
        await ctx.send(embed=embed)
    if check_database == True:
        try:
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            
            collection.update_one({"User bound to": ctx.author.id}, { "$set": {"Key": key}})
            collection.update_one({"Key": key}, { "$set": {"Bound": "False"}})
            collection.update_one({"Key": key}, { "$set": {"User bound to": "null"}})
            collection.update_one({"Key": key}, { "$set": {"Active": "False"}})
            collection.update_one({"Key": key}, { "$set": {"Mac Address": "null"}})
            collection.update_one({"Key": key}, { "$set": {"IP Address": "null"}})
            
            embed=discord.Embed(title="Cobra AIO", description="Successfully unbound. We hope you enjoyed your time here being apart of Cobra.")
            embed.add_field(name="Important", value=f'Your key is {key}. This will change on the next binding to ensure safety.')
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
    embed.add_field(name="Key Type", value=query_results["Key-Type"], inline=True)
    embed.set_footer(text="Cobra AIO Authentication")
    await ctx.send(embed=embed)
#working-finished


@bot.command()
async def reset_key(ctx):
    query = {"User bound to": ctx.author.id}
    query_results = collection.find_one(query)
    if query_results == None:
        return

    key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    collection.update_one({"User bound to": ctx.author.id}, { "$set": {"Key": key}})
    await ctx.send('Reset key.')



@bot.command()
@commands.has_role(775496025505792020)
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
@commands.has_role(775496025505792020)
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
@commands.has_role(775496025505792020)
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
@commands.has_role(803449976600264724)
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
@commands.has_role(775496025505792020)
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
@commands.has_role(775496025505792020)
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
@commands.has_role(775496025505792020)
async def key_list(ctx):
    key_list = []
    keys = collection.distinct("Key")
    for i in keys:
        key_list.append(i)
    formatted_list = "\n".join(i for i in key_list)
    await ctx.send(formatted_list)


#working-needs-improvements

@bot.command()
@commands.has_role(775496025505792020)
async def generate_release(ctx, arg, arg2):
    number = int(arg)
    release_type = arg2
    for i in range(number):
        key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        post = {"Key": key, "Bound": "False", "Active": "False", "Key-Type": release_type, "Suspended": "False", "User bound to": "null", "Mac Address": "null", "IP Address": "null", "Claimed": "False(release)"}
        collection.insert_one(post)
#working-finished

@bot.command()
async def claim(ctx):
    query = {"Claimed": "False(release)"}
    query_results = collection.find_one(query)
    check_database_user = collection.find( {"User bound to": ctx.author.id}).count() > 0
    if check_database_user == True:
            embed=discord.Embed(title="Cobra AIO", description="You already have a key bound.")
            embed.set_footer(text="Cobra AIO Authentication")
            await ctx.send(embed=embed)
            return
    if query_results == None:
        await ctx.send('No release currently or OOS.')
    else:
        key = query_results["Key"]
        embed=discord.Embed(title="Cobra AIO", description="Successfully generated and bound. Welcome to Cobra AIO.")
        embed.add_field(name="Key",value=key, inline=True)
        embed.set_footer(text="Cobra AIO Authentication")
        collection.update_one({"Key": key}, { "$set": {"Bound": "True"}} )
        collection.update_one({"Key": key}, { "$set": {"User bound to": ctx.author.id}})
        collection.update_one({"Key": key }, { "$set": {"Claimed": "True(release)"}})
        await ctx.send(embed=embed)
#working-finished

        



bot.run('')
#left blank because of security
