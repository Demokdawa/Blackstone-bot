import sqlite3

db = sqlite3.connect('blackbotdb.sqlite3')
cursor = db.cursor()

cursor.execute('''CREATE TABLE if not exists Users (
IDuser integer PRIMARY KEY AUTOINCREMENT,
DiscordUserId integer,
DiscordUserTag text,
WarnsNumber unsigned tinyint default 0
)''')

db.commit()