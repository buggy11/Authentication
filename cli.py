import os
import discord
import socket
import requests
import warnings
from getmac import get_mac_address as gma
from pymongo import MongoClient

warnings.simplefilter("ignore")

cluster = MongoClient("")

db = cluster["Authentication"]

collection = db["SoftwareLicenses"]

computer_address = gma()

hostname = socket.gethostname()
IP_address = socket.gethostbyname(hostname)

check_database_for_id = collection.find( { "Mac Address": computer_address, "IP Address": IP_address } ).count() > 0
def set_up():
    if check_database_for_id == True:
        print('Validated.')
    elif check_database_for_id == False:
        print('Welcome to Cobra AIO. Please enter your license key.')
        key = input()
        check_database_for_key_status = collection.find( { "Key": key, "Suspended": 'Yes' } ).count() > 0
        check_database_for_key = collection.find( { "Key": key}).count() > 0
        check_database_active_status = collection.find( { "Key": key, "Active": "False"} ).count() > 0
        if check_database_for_key_status == False:
            if check_database_for_key == True:
                if check_database_active_status == True:
                    collection.update_one({"Key": key}, { "$set": {"Active": "True"}})
                    collection.update_one({"Key": key}, { "$set": {"Mac Address": computer_address}})
                    collection.update_one({"Key": key}, { "$set": {"IP Address": IP_address}})
                    print('Welcome, validated.')
                elif check_database_active_status == False:
                    print('That key is active on another device.')
            

            elif check_database_for_key == False:
                print('Invalid key.')
            return
        if check_database_for_key_status == True:
            print('That key is currently suspended. Contact an admin if you believe this is a mistake.')
            return
set_up()
        

