# koronebot
discord bot that lets you see the status of UCSD areas
add this bot to your server:
https://discord.com/api/oauth2/authorize?client_id=958851491333013525&permissions=36507290624&scope=bot%20applications.commands

COMMANDS 

/rimac
gives you how busy the RIMAC weight room is 

/maingym
gives you how busy the main gym weight room is

/geisel [floor]

if no floor is specified, the top 3 least busiest floors are displayed
if a floor is specified, the activity level on that floor is displayed

ABOUT THE WAITZ API USED 

https://waitz.io/live/ucsd
requesting from this url returns activity levels of 
all ucsd areas in json format


https://waitz.io/compare/ucsd
requesting from this url returns trend data of the
activity levels in json format
Example: "Peak hours are 1PM, 2PM, 3PM" 
