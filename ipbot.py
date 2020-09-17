import asyncio
import json
from asyncio import sleep
import os

import discord
import miniupnpc

client = discord.Client()

def storeLastIP(lastip):
  with open(".lastip", "w") as f:
    f.write(lastip)
    f.close()

def getLastIP():
  with open(".lastip", "r") as f:
    re = f.read()
    f.close
  return re


def getConfig():
  try:
    with open("config.json", 'r') as j:
      return json.load(j)
  except FileNotFoundError:
    FileNotFoundError: "Please provide a config.json"

def ipChanged():
  try:
    u = miniupnpc.UPnP()
    u.discoverdelay = 200
    u.discover()
    u.selectigd() 
    currentip = u.externalipaddress()
    # print("lastIP:", getLastIP(), "currentIP:", currentip)
    if getLastIP() != currentip:
      return (True, currentip)
    else:
      return (False, currentip)
  except Exception:
    print("ip lookup was unsuccessfull.")
    return (False, getLastIP())

  

async def eventloop():
  await client.wait_until_ready()

  # endlosschleife inc (TM)
  while(True):
    ipResult = ipChanged()

    if ipResult[0]:
      storeLastIP(ipResult[1])

      channels = getConfig()["channels"]

      for identifier in channels:
        channel = client.get_channel(identifier)
        await channel.send('New IP: `' + ipResult[1] + '`')

      print("ip changed to " + ipResult[1] + ",   messages have been sent")

    else:
      print("ip has not changed, is", ipResult[1])

    await sleep(120)
  
  

TOKEN = getConfig()["token"]
print("ipbot: starting")

# create .lastip if not exists
if not os.path.exists(".lastip"):
  with open(".lastip", "w+") as f:
    f.close()

client.loop.create_task(eventloop())

client.run(TOKEN)

