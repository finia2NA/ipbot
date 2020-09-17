import asyncio
import json
from time import sleep

import discord
import miniupnpc

client = discord.Client()

def getConfig():
  try:
    with open("config.json", 'r') as j:
      return json.load(j)
  except FileNotFoundError:
    FileNotFoundError: "Please provide a config.json"

def getIP():
  u = miniupnpc.UPnP()
  u.discoverdelay = 200
  u.discover()
  u.selectigd()
  return u.externalipaddress()

async def eventloop():
  await client.wait_until_ready()

  # channels = getConfig()["channels"]
  # for identifier in channels:
  #   channel = client.get_channel(identifier)
  #   await channel.send('New IP:')

  # endlosschleife inc (TM)

  lastIP = None
  while(True):
    if getIP() != lastIP:
      lastIP = getIP()

      channels = getConfig()["channels"]

      for identifier in channels:
        channel = client.get_channel(identifier)
        await channel.send('New IP: `' + lastIP + '`')
    print("ip changed to " + lastIP + ",   messages have been sent")
    sleep(120)
  
  

TOKEN = getConfig()["token"]
print("ipbot: starting")

client.loop.create_task(eventloop())

client.run(TOKEN)

