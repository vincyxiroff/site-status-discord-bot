from config import Config
import discord
from discord.ext import commands
from os import name, system
from time import sleep
try:
    from config import data
except Exception as oof:
    ex=input(f"Error in Config File, Please fix then try again. Be sure that all files are in the same directory and that your 'token.txt' file is there as well.\n\nError: {str(oof)}")
    exit(0)
from client_hook import logging
from host_check import host
from create_embed import embed_content
from create_alert import embed_alert
from tkinter import messagebox
import tkinter
root = tkinter.Tk()
root.withdraw()
class global_:
    max_interval = 4096
pragma = True

client=discord.Client()

@client.event
async def on_ready():
    global pragma
    my_client = logging.load(client)
    test = my_client.test_channels()
    if test['result'] == None:
        if pragma == True:
            die = str(
                ">Failed to validate 1 or more channels, see below:"
                f"\n\n>Admin Logging Channel:\n{test['admin']}"
                "\n-------------------------------------------"
                f"\n>Public Checks Channel:\n{test['public']}"
                "\n-------------------------------------------"
                "\n>Please use valid channel Id's an try again."
                "\n\nScript will now close on accept."
                )
            messagebox.showinfo("Error! | Made with ♥️ by vincyilmagnifico#8965", die)
            exit()
    else:
        out = f"""
> Bot Is Live!
> Admin Channel: Ready!
> Public Updates Channel: Ready!
------------------------------------------------------
Bot Name: {data.bot_name}
Currently Probing: {data.my_url}
Max Intervals: {global_.max_interval} Loops
Interval Time: {data.interval_time} Seconds
Max Allocated Uptime:
{str(int(int(global_.max_interval) * int(data.interval_time)))} Seconds or {str(round(int(int(global_.max_interval) * int(data.interval_time)) / 3600))} Hours or {str(round(int(int(global_.max_interval) * int(data.interval_time)) / 86400))} Days

[Guild Info]

Admin Channel:
{test['admin_channel_name']}
Admin Server:
{test['admin_guild_name']}

Public Updates Channel:
{test['public_channel_name']}
Public Updates Server:
{test['public_guild_name']}

[Click Ok To Begin Monitoring {data.my_url}!]
"""
        if pragma == True:
            try:
                messagebox.showinfo("Success! | Uptime Monitor",out)
            except Exception as emoji:
                a = input("\nUsually a confirmation window will popup but unfortuntely theres been an error!"
                          "\nThis is most likely due to an emoji in your channel/guild name that caused the window to crash."
                          "\nYour bot should still work correctly but consider changing this in the future for stability reasons**\n"+out+"\nHit ENTER To Begin!")
                await logging.load(client).admin_channel().send(" ",
                                                                embed=embed_alert(
                                                                    f"Failed To Create Start Window, alternate message sent.\n\nResuming deterministic behavior. Continue.\n\nTraceback:\n{str(emoji)}", 1
                                                                    )
                                                                )            
            if name == 'nt': _ = system('cls')
            else: _ = system('clear')
    try:
        await client.change_presence(
            activity=discord.Activity(
            name=data.my_url.replace("https://", "")
            .replace("http://", "")
            .replace("/", ""),
            type=discord.ActivityType.watching)
            )
    except Exception as e:
        await logging.load(client).admin_channel().send(" ",
                                                        embed=embed_alert(
                                                            f"Fatal Client/Websocket Error!\nTraceback:\n\n{str(e)}\n", 1
                                                            )
                                                        )
    print(f"[Currently Monitoring {data.my_url}]")
    pragma = False
    await logging.load(client).admin_channel().send(" ",
                                                embed=embed_alert(
                                                    f"Welcome To {data.bot_name}!"
                                                    f"\n\nCurrently Monitoring: {data.my_url}",
                                                    0
                                                    )
                                                )
    up = True
    for x in range(0, global_.max_interval):
        try:
            status = host(data.my_url).probe()
            up = True
        except Exception as e:
            up = False
            await logging.load(client).admin_channel().send(" ",
                                                            embed=embed_alert(
                                                                f"A Probe Failed!\nTraceback:\n\n{str(e)}\n`", 1
                                                                )
                                                            )
            
        try:
            channels = logging.load(client)
        except Exception as e:
            await logging.load(client).admin_channel().send(" ",
                                                            embed=embed_alert(
                                                                f"Fatal Client Error, Restarting Hook!\nTraceback:\n\n{str(e)}\n", 1
                                                                )
                                                            )
        
        if data.purge_channel == True:
            try:
                await channels.public_channel().purge(
                    limit=100, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True
                    )
            except Exception as e:
                await logging.load(client).admin_channel().send(" ",
                                                                embed=embed_alert(
                                                                    "Failed To Prune Public Updates Channel, Retrying Status Update!\n\n" + str(e), 1
                                                                    )
                                                                )
                try:
                    
                    await channels.public_channel().send(" ", embed=embed_content(status))
                    if up == True:
                        status = "up"
                    else:
                        status = "down"
                    await logging.load(client).admin_channel().send(" ",
                                                                    embed=embed_alert(
                                                                        f"Update: [RETRYING...] Probe #{str(x + 1)} Sent!\n\nStatus: {status}", 0
                                                                        )
                                                                    )
                except Exception as E:
                    await logging.load(client).admin_channel().send(" ",
                                                embed=embed_alert(
                                                    f"[Probe #{{str(x + 1)}}] [RETRYING...]: Failed To Push Update To Updates Channel, Retrying Status Update!\n\n" + str(e), 1
                                                    )
                                                )
                    
        await channels.public_channel().send(" ", embed=embed_content(status))
        if up == True:
            status = "up"
        else:
            status = "down"
        await logging.load(client).admin_channel().send(" ",
                                                        embed=embed_alert(
                                                            f"Update: Probe #{str(x + 1)} Sent!\n\nStatus: {status}", 0
                                                            )
                                                        )
        sleep(data.interval_time)
            



prefix = Config.prefix


client = commands.client(command_prefix=prefix, intents=discord.Intents.all())

client.setup = False
client.role_name = Config.role_name
client.message_id = Config.message_id
client.channel_id = Config.channel_id



@client.command()
async def setup(ctx):
    try:
        message_id = int(client.message_id)
    except ValueError:
        return await ctx.send("Invalid Message ID passed")
    except Exception as e:
        raise e

    try:
        channel_id = int(client.channel_id)
    except ValueError:
        return await ctx.send("Invalid Channel ID passed")
    except Exception as e:
        raise e
    try:
        channel_id = int(client.channel_id)
    except ValueError:
        return await ctx.send("Invalid Channel ID passed")
    except Exception as e:
        raise e
    
    channel = client.get_channel(channel_id)
    
    if channel is None:
        return await ctx.send("Channel Not Found")
    
    message = await channel.fetch_message(message_id)
    
    if message is None:
        return await ctx.send("Message Not Found")
    
    await message.add_reaction("✅")
    await ctx.send("Setup Successful")
    
    client.setup = True

@client.event
async def on_raw_reaction_add(payload):
    if client.setup != True:
        return print(f"Bot is not setuped\nType {prefix}setup to setup the bot")
    
    if payload.message_id == int(client.message_id):
        if str(payload.emoji) == "✅":
            guild = client.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = discord.utils.get(guild.roles, name=client.role_name)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member is None:
                return
            try:
                await member.add_roles(role)
            except Exception as e:
                raise e

@client.event
async def on_raw_reaction_remove(payload):
    if client.setup != True:
        return print(f"Bot is not setuped\nType {prefix}setup to setup the bot")
    
    if payload.message_id == int(client.message_id):
        if str(payload.emoji) == "✅":
            guild = client.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = discord.utils.get(guild.roles, name=client.role_name)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member is None:
                return
            try:
                await member.remove_roles(role)
            except Exception as e:
                raise e









client.run(data.bot_token) 

                
                
                
                
            
