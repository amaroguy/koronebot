from email.policy import default
import lightbulb
import hikari
import ucsdstatus
import os

DISCORD_BOT_TOKEN = os.environ['KORONE_API_KEY']
bot = lightbulb.BotApp(token=DISCORD_BOT_TOKEN, 
                        default_enabled_guilds=(806678433303363636))

@bot.command
@lightbulb.add_cooldown(15.0, 10, lightbulb.GuildBucket)
@lightbulb.command('rimac', 'gets the availability of RIMAC')
@lightbulb.implements(lightbulb.SlashCommand)
async def rimac(context): 
    await context.respond(ucsdstatus.rimac_status())

@bot.command
@lightbulb.option("floor", "Floor of geisel to check, leave blank for least busiest floors", required=False, type=int)
@lightbulb.add_cooldown(15.0, 10, lightbulb.GuildBucket)
@lightbulb.command('geisel', 'make sure to input floor you want to check, leave blank for least busiest floors')
@lightbulb.implements(lightbulb.SlashCommand)
async def geisel(context): 
    await context.respond(ucsdstatus.geisel_floor_status(floor=context.options.floor) )

@bot.command
@lightbulb.add_cooldown(15.0, 10, lightbulb.GuildBucket)
@lightbulb.command('maingym', 'gets the availability of the Main Gym')
@lightbulb.implements(lightbulb.SlashCommand)
async def main_gym(context): 
    await context.respond(ucsdstatus.main_gym_status())



bot.run()
