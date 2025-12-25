import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

        try:
            guild = discord.Object(id=1453325791080222774)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')


    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author}')
    
    async def on_reaction_add(self, reaction, user):
            if user.bot:
                return
            
            guild = reaction.message.guild

            if not guild:
                return
            
            if hasattr(self, "colour_roles_message_id") and reaction.message.id != self.colour_roles_message_id:
                return
            
            emoji = str(reaction.emoji)

            reaction_role_map = {
                '🥇': 'Number 1',
                '🥈': 'Number 2',
                '🥉': 'Number 3'
            }

            if emoji in reaction_role_map:

                role_name = reaction_role_map[emoji]
                role = discord.utils.get(guild.roles, name=role_name)

                if role and user:
                    await user.add_roles(role)
                    print(f"Assigned {role_name} to {user}")
    
    async def on_reaction_remove(self, reaction, user):
                if user.bot:
                    return
                
                guild = reaction.message.guild

                if not guild:
                    return
                
                if hasattr(self, "colour_roles_message_id") and reaction.message.id != self.colour_roles_message_id:
                    return
                
                emoji = str(reaction.emoji)

                reaction_role_map = {
                    '🥇': 'Number 1',
                    '🥈': 'Number 2',
                    '🥉': 'Number 3'
                }

                if emoji in reaction_role_map:

                    role_name = reaction_role_map[emoji]
                    role = discord.utils.get(guild.roles, name=role_name)

                    if role and user:
                        await user.remove_roles(role)
                        print(f"Assigned {role_name} to {user}")

    

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
client = Client(command_prefix="!", intents=intents)


GUILD_ID = discord.Object(id=)

@client.tree.command(name="medalroules", description="Create a message to than lets users to pick a role", guild=GUILD_ID)
async def colour_roles(interaction: discord.Interaction):
    #check admin
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("U must be an admin to run this command", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    
    description = (
        "React to this massage to get your medal role!\n\n"
        "🥇 Number 1\n"
        "🥈 Number 2\n"
        "🥉 Number 3\n"
    )

    embed = discord.Embed(title="Pick ur status!", description=description, color=discord.Color.blurple())
    message = await interaction.channel.send(embed=embed)
    
    emojis = ['🥇', '🥈', '🥉']

    for emoji in emojis:
        await message.add_reaction(emoji)

    client.colour_roles_message_id = message.id

    await interaction.followup.send("Colour role message created!", ephemeral=True)



@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

@client.tree.command(name="printer", description="i will print whatever you give me", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="embed", description="Embed demo!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a title", url="https://github.com/drizzy1772", description="i am the description", color=discord.Color.red())
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzVJkX7cjj9KxqZvESRGM2dW49atnotjLjdQ&s")
    embed.add_field(name="Field 1 title", value="subscribe to the greatest github on the internet", inline=False)
    embed.add_field(name="Field 2 title", value="Lets Gooo", inline=True)
    embed.add_field(name="Field 3 title", value="Suiii", inline=True)
    embed.set_footer(text="Its freezinggg")
    embed.set_author(name=interaction.user.name, url="https://leetcode.com/problem-list/array/", icon_url="https://cdn-icons-png.flaticon.com/128/5968/5968350.png")
    await interaction.response.send_message(embed=embed)

class View(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.red, emoji="😄")
    async def two_button_callback(self, button, interaction):
        await button.response.send_message("You have clicked the button!")
    
    @discord.ui.button(label="2nd Button!", style=discord.ButtonStyle.blurple, emoji="😇")
    async def three_button_callback(self, button, interaction):
        await button.response.send_message("This is the second button")

    @discord.ui.button(label="3rd Button!", style=discord.ButtonStyle.green, emoji="🥰")
    async def button_callback(self, button, interaction):
        await button.response.send_message("This is the third button")

@client.tree.command(name="button", description="Displaying a button", guild=GUILD_ID)
async def myButton(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())


class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Option 1",
                description="This is option",
                emoji="😇"
            ),

            discord.SelectOption(
                label="Option 2",
                description="This is option 2",
                emoji="🥰"
            ),

            discord.SelectOption(
                label="Option 3",
                description="This is option 3",
                emoji="😂"
            )
        ]

        super().__init__(placeholder="Please choose an option:", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Option 1":
            await interaction.response.send_message("Yay youve picked option 1")
        
        elif self.values[0] == "Option 2":
            await interaction.response.send_message("This is now option 2")

        
        elif self.values[0] == "Option 3":
            await interaction.response.send_message("This is the last option")
        

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())

@client.tree.command(name="menu", description="Displaying a drop down menu", guild=GUILD_ID)
async def myMenu(interaction: discord.Interaction):
    await interaction.response.send_message(view=MenuView())



client.run()








