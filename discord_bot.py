import discord
from discord.ext import commands

import json
import os
import pandas as pd
import main  # Assuming the existing script is named main.py

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    
@client.slash_command(name="view_setup")
async def setup(ctx):
    with open("./setup.json", "r") as f:
        setup = json.load(f)
        
    make = setup['facebook']['make']
    model = setup['facebook']['model']
    min_price = setup['facebook']['min_price']
    max_price = setup['facebook']['max_price']
    min_year = setup['facebook']['min_year']
    max_mileage = setup['facebook']['max_mileage']

    with open("./setup.json", "w") as f:
        json.dump(setup, f, indent=4)

    await ctx.respond(f"Setup is: Make: {make}, Model: {model}, Minimum price: {min_price}, Maximum price: {max_price}, Minimum year: {min_year}, and Maximum miles: {max_mileage} ")


@client.slash_command(name="setup")
async def setup(ctx, make: discord.Option(str), model: discord.Option(str), min_price: discord.Option(int), max_price: discord.Option(int), min_year: discord.Option(int), max_mileage: discord.Option(int)):
    with open("./setup.json", "r") as f:
        setup = json.load(f)

    setup['facebook']['make'] = make
    setup['facebook']['model'] = model
    setup['facebook']['min_price'] = min_price
    setup['facebook']['max_price'] = max_price
    setup['facebook']['min_year'] = min_year
    setup['facebook']['max_mileage'] = max_mileage

    with open("./setup.json", "w") as f:
        json.dump(setup, f, indent=4)

    await ctx.respond(f"Setup has been updated with make: {make}, model: {model}, minimum price: {min_price}, and maximum price: {max_price}")

@client.slash_command(name="search", description="Search for cars matching your setup")
async def search(ctx):
    await ctx.defer()
    main.main()
    
    # Assuming the last generated CSV is the desired one
    csv_file = sorted([f for f in os.listdir() if f.startswith('sc_') and f.find('desired') and f.endswith('.csv')])[-1]
    df = pd.read_csv(csv_file)
    top_rows = df.head(3)
    
    

    for index, row in top_rows.iterrows():
        year, name, price, mileage, loc, link = row['year'], row['name'], row['price'], row['mileage'], row['location'], row['link']
        # result = f"Year: {year}\nName: {name}\nPrice: {price}\nMileage: {mileage}\nLocation: {loc}\nLink: {link}"
        embed = discord.Embed(
            title="Carketplace",
            description=price,
            color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )
        embed.set_footer(text="2023 Carketplace. All rights reserved.") # footers can have icons too
        embed.set_author(name="Carketplace Bot", icon_url="https://i.postimg.cc/y655rHLF/app-icon.png")
        embed.set_thumbnail(url="https://i.postimg.cc/y655rHLF/app-icon.png")
        # embed.set_image(url="https://example.com/link-to-my-banner.png")
        embed.add_field(name="Year", value=year, inline=True)
        embed.add_field(name="Price", value=price, inline=True)
        embed.add_field(name="Link", value=link, inline=True)
        await ctx.followup.send(name, embed=embed)

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual Discord bot token
client.run(os.getenv('DISCORD_BOT_TOKEN'))


# import json
# import os
# import pandas as pd
# import discord
# from discord import app_commands
# from dotenv import load_dotenv
# import main  # Assuming the existing script is named main.py

# # load env for discord bot token
# load_dotenv()
# # define intents, client and tree
# intents = discord.Intents.default()
# client = discord.Client(intents=intents)
# tree = app_commands.CommandTree(client)

# @client.event
# async def on_ready():
#     await tree.sync(guild=discord.Object(id=os.getenv('DISCORD_GUILD_ID')))
#     # print "ready" in the console when the bot is ready to work
#     print("ready")

# @tree.command(name="modify_setup",
#              description="Create a Facebook Marketplace search with price preferences",
#              options=[
#                  {
#                      "name": "model",
#                      "description": "Search model",
#                      "type": 3,
#                      "required": True
#                  },
#                  {
#                      "name": "min_price",
#                      "description": "Minimum price",
#                      "type": 4,
#                      "required": True
#                  },
#                  {
#                      "name": "max_price",
#                      "description": "Maximum price",
#                      "type": 4,
#                      "required": True
#                  }
#              ])

# async def modify_setup(interaction):
#     with open("./setup.json", "r") as f:
#         setup = json.load(f)

#     # define interaction data
#     model = interaction.data['options'][0]['value']
#     min_price = interaction.data['options'][1]['value']
#     max_price = interaction.data['options'][2]['value']
    
#     setup['facebook']['model'] = model
#     setup['facebook']['min_price'] = min_price
#     setup['facebook']['max_price'] = max_price

#     with open("./setup.json", "w") as f:
#         json.dump(setup, f)

#     await interaction.response.send_message(f"Setup modified: model={model}, min_price={min_price}, max_price={max_price}")

# @tree.command(name="run_scraper",
#             description="Run the scraper and return the top three results")

# async def run_scraper(interaction):
#     main.main()  # Run your existing script
#     # Assuming the last generated CSV is the desired one
#     csv_file = sorted([f for f in os.listdir() if f.startswith('sc_') and f.endswith('.csv')])[-1]
#     df = pd.read_csv(csv_file)
#     top_rows = df.head(3)

#     for index, row in top_rows.iterrows():
#         year, name, price, mileage, loc, link = row['year'], row['name'], row['price'], row['mileage'], row['location'], row['link']
#         result = f"Year: {year}\nName: {name}\nPrice: {price}\nMileage: {mileage}\nLocation: {loc}\nLink: {link}"
#         await interaction.response.send_message(result)

# # Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual Discord bot token
# client.run(os.getenv('DISCORD_BOT_TOKEN'))

