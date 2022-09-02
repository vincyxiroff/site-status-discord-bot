class data:
    
    # Time Between Checks
    interval_time = 300

    #Timeout (in seconds) For Site Probing
    probe_timeout = 8

    #Channel ID's To Use
    admin_log_channel_id = 1015229097393279067
    public_update_channel_id = 1015220573833539634

    #Your URL To Check
    my_url = "https://www.dynamiccloud.ml"

    #Your Bots Token - For security reasons, use "token.txt"!!!
    try:
        with open("token.txt", "r") as token:
            your_token = token.read()
        token = your_token
    except:
        wait_to_exit = input("FileError: 'token.txt' was not found or is Invalid! Be sure its in your current directory!")
        exit(0)

    #Bots Name To Display
    bot_name = "DynamicCloud Status by vincyilmagnifico#8964"

    #Thumbnail to display 
    thumbnail_url = "https://host-info.net/img/mag.png"
    
    #Purge Channel on update
    #Either "True" or "False"
    purge_channel = True
    
    #Embed Color
    embed_color = 0xfe0000 # Neon-Red

    #Neon-Colors:
    #https://www.color-hex.com/color-palette/1131
    #red = 0xfe0000
    #yellow = 0xfdfe02
    #green = 0x0bff01
    #blue = 0x011efe
    #purple = 0xfe00f6
        
class Config:
    role_name = "members"
    message_id = "1015229867165503569"
    prefix = "."
    channel_id = "1015229754888167426"
