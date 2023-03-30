import os
import discord
from discord.ext import commands
import random
from server import keep_alive
# from database.player_stats import player_stats

#client = commands.Bot(command_prefix='!')
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)
# Create a dictionary to store player stats
player_stats = {}


class Vampire:
    def __init__(self, name, strength, speed, health, defense):
      #insert here
        self.name = name
        self.strength = strength
        self.speed = speed
        self.health = health
        self.defense = defense

    def attack(self, player_id, target):
      #get function query takes param in to select $(param) from db
        self_id = player_id
        self_stats = player_stats.get(self_id)
        self_name = self_stats['name']
        self_attack = self_stats['strength']
        target_id = target.id
        target_stats = player_stats.get(target_id)
        target_name = target_stats['name']
        target_speed = target_stats['speed']
        target_defense = target_stats['defense']
        damage = (random.randint(self_attack, 100)) - (
            (target_defense) * random.randint(1, 10))
        if (target_speed * random.randint(1, 10) > damage):
            damage = 0
        target_stats['health'] -= damage
        if damage == 0:
            return f"{self_name} attack miss!"
        else:
            return f"{self_name} attacks {target_name} and deals {damage} damage!"

    def is_alive(self, target_id):
        target_stats = player_stats.get(target_id)
        target_health = target_stats['health']
        return target_health > 0

    def exist(self, player_id):

        if player_id in player_stats:
            # Player exists
            return True
        else:
            # Player does not exist
            # Rest of the code for when the player does not exist
            return False


class VampireRPG:
    def __init__(self):
        self.players = {}
        self.vampires = []

    def add_player(self, player):
        self.players[player.id] = {"name": player.name, "vampire": None}

    def remove_player(self, player):
        del self.players[player.id]

    def get_players(self):
        return list(self.players.values())

    def create_vampire(self, name, player_id):
        strength = random.randint(5, 10)
        speed = random.randint(5, 10)
        health = random.randint(50, 100)
        defense = random.randint(5, 10)
        vampire = Vampire(name, strength, speed, health, defense)
        self.vampires.append(vampire)
        player_stats[player_id] = {
            'name': name,
            'health': health,
            'strength': strength,
            'speed': speed,
            'defense': defense
        }
        return vampire

    def assign_vampire(self, player_id):
        if not self.players[player_id]["vampire"]:
            vampire_name = f"{self.players[player_id]['name']}'s vampire"
            vampire = self.create_vampire(vampire_name, player_id)
            self.players[player_id]["vampire"] = vampire
            return f"{self.players[player_id]['name']} is now a Vampire!!"
        else:
            return f"{self.players[player_id]['name']} already is a vampire!"

    def get_vampire(self, player_id):
        return self.players[player_id]["vampire"]

    def start_game(self):
        if len(self.vampires) < 2:
            return "At least two vampires are required to start the game."
        else:
            return "The game has started!"

    def get_vampires(self):
        return self.vampires


# Create the RPG game
game = VampireRPG()


# Define the join command
@client.command()
async def awaken(ctx):
    player = ctx.author
    player_id = ctx.author.id
    vampire_exist = False
    try:
        game.get_vampire(player_id)
        await ctx.send("Vampire is already lurking in the wilderness")
        vampire_exist = True
    except Exception as ex:
        print(ex)

    if not vampire_exist:
        game.add_player(player)
        await ctx.send(f"{player.mention} is officially AWAKEN. BEWARE!!!.")
        message = game.assign_vampire(player_id)
        await ctx.send(message)


# Define the leave command
@client.command()
async def leave(ctx):
    player = ctx.author
    game.remove_player(player)
    await ctx.send(f"{player.mention} has left the game.")


# Define the assign command
# @client.command()
# async def assign(ctx):
#     player_id = ctx.author.id
#     message = game.assign_vampire(player_id)
#     await ctx.send(message)


@client.command()
async def profile(ctx, target: discord.Member = None):
    # player_id = str(type(ctx.author.id))
    #await ctx.send("Player ID: " + player_id + "Target ID: " + target_id)
    vampire_exist = True
    if target == None:
        target = ctx.author
    try:
        game.get_vampire(target.id)
    except Exception:
        await ctx.send("Vampire is not awaken")
        vampire_exist = False

    if vampire_exist:
        target_id = target.id
        target_stats = player_stats.get(target_id)
        if target_stats:
            target_health = target_stats['health']
            target_attack = target_stats['strength']
            target_speed = target_stats['speed']
            target_name = target_stats['name']
        await ctx.send(
            f"{target_name} has {target_health} health, {target_attack} strength & {target_speed} speed"
        )


# Define the attack command
@client.command()
async def attack(ctx, target: discord.Member = None):
    player_id = ctx.author.id
    vampire = game.get_vampire(player_id)
    target_id = target.id
    try:
        if not vampire.exist:
            await ctx.send(f"This user don't have a vampire!")
        elif not vampire.is_alive(target_id):
            target_id = target.id
            target_stats = player_stats.get(target_id)
            target_name = target_stats['name']
            await ctx.send(f"{target_name} is dead!")
        else:
            if vampire.is_alive(player_id):
                message = vampire.attack(player_id, target)
                await ctx.send(message)
            else:
                await ctx.send("You are dead, please heal!")
            # if not target.bot and target.id != ctx.author.id:
            #     await ctx.send(
            #         f"{target.mention} has {target.vampire.health} health remaining."
            #     )
    except Exception as ex:
        print(ex)
        await ctx.send(
            "Vampire is currently hibernating, please wait for the next moon!")


# # Define the start command
# @client.command()
# async def start(ctx):
#     message = game.start_game()
#     await ctx.send(message)

# Run the bot
keep_alive()
client.run(os.environ['Distoken'])


