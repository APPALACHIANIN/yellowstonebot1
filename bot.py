import discord
from discord.ext import commands 
import os
import datetime
from discord.utils import get
import youtube_dl


PREFIX = '$'

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event

async def on_ready():
	print( 'Бот подключился к серверу' )

	await client.change_presence( status = discord.Status.online, activity = discord.Game( 'Вулканчик Пиндосии' ) )

# Work with errors
@client.event
async def on_command_error( ctx, error ):
	pass 

# Auto-role
@client.event

async def on_member_join( member ):
	channel = client.get_channel( 757431308799574066 )

	role = discord.utils.get( member.guild.roles, id = 756884707831971852 )

	await member.add_roles( role )
	await channel.send( embed = discord.Embed( description = f'Пользователь ``{ member.name }``, присоединился к серверу YELLOWSTONE', 
						color = 0x3c7c5c ) )

# Clear message
@client.command ( pass_context = True )
@commands.has_permissions( administrator = True )

async def clear( ctx, amount : int):
	await ctx.channel.purge( limit = amount )

# Kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True)

async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )
	await ctx.send( f'Пользователь { member.mention } был дисквалифицирован с сервера' )

# Ban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
	emb = discord.Embed( title = 'Блокировка участника', colour = discord.Color.red() )
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )

	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = 'Бан' , value = 'Пользователь заблокирован : {}'.format( member.mention ) )
	emb.set_footer( text = 'Был забанен администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	await ctx.send( embed = emb )

# Unban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )
		await ctx.send( f'Пользователь { user.mention } был разбанен' )

		return

# Command help
@client.command( pass_context = True )
@commands.has_permissions( administrator = True ) 

async def help( ctx ):
	emb = discord.Embed( title = 'Навигация по командам сервера', colour = discord.Color.orange() )

	emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистка чата на n-количество сообщений' )
	emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Дисквалификация участника с сервера' )
	emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Ограничение участнику доступа к серверу' )
	emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Возобновление участнику доступа к серверу' )
	emb.add_field( name = '{}time'.format( PREFIX ), value = 'Время по Иркутску' )
	emb.add_field( name = '{}mute'.format( PREFIX ), value = 'Отключение функции чата у участника( Только администратором )' )


	await ctx.send( embed = emb )

# Time
@client.command()
@commands.has_permissions( administrator = True )

async def time( ctx ):
	emb = discord.Embed( title = 'Ваше время', description = 'Здесь вы сможете узнать время по городу' , colour = discord.Color.green(), url = 'https://www.timeserver.ru/cities/kz/taldykorgan' )

	emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
	emb.set_footer( text = 'Иди своей дорогой, сталкер' , icon_url = ctx.author.avatar_url )
	emb.set_image( url = 'http://pics.wikireality.ru/upload/e/ed/Villi-vonka-nastalo-vremya.jpeg' )
	emb.set_thumbnail( url = 'https://soundtimes.ru/images/simfjniya/610.jpg' )

	now_date = datetime.datetime.now()

	emb.add_field( name = 'Время', value = 'То самое время : {}'.format( now_date ) )

	await ctx.send( embed = emb )

# Mute
@client.command()
@commands.has_permissions( administrator = True )

async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'MUTE' )

	await member.add_roles( mute_role )
	await ctx.send( f'У { member.mention }, ограничение чата за нарушение прав!' )

# Private messages
# Приветствие
@client.command()
async def send_hello( ctx ):
	await ctx.author.send( 'Привет, мудила...' )
# Прощание
@client.command()
async def send_goodbye( ctx ):
	await ctx.author.send( 'Прощай, мудила...' )
# Как дела
@client.command()
async def send_how_are_you( ctx ):
	await ctx.author.send( 'Иди нахуй, у меня все херово. Сегодня мне кастрировали список моих команд((' )
# Для участника
@client.command()
async def send_m( ctx, member: discord.Member ):
	await member.send( f'Привет, { member.name}, передаю важное сообщение от имени { ctx.author.name } - "Ты - ПИДР"' )

# Voice Chat
@client.command()
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()

# Music 
@client.command()
async def play(ctx, url : str):
	song_there = os.path.isfile('song.mp3')

	try:
		if song_there:
			os.remove('song.mp3')
			print('[log] Предыдущая композиция удалена из списка воспроизведения')
	except PermissionError:
		print('[log] Не удалось воспроизвести композицию')

	await ctx.send('Пожалуйста подождите...')

	voice = get(client.voice_clients, guild = ctx.guild)

	ydl_opts = {
		'format' : 'bestaudio/best',
		'postprocessors' : [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec' : 'mp3',
			'preferredquality' : '192'
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print('[log] Загружаю музыкальную композицию...')
		ydl.download([url])

	for file in os.listdir('./'):
		if file.endswith('.mp3'):
			name = file
			print('[log] Переименовываю файл: {file}')
			os.rename(file, 'song.mp3')

	voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, композиция закончила свое проигрывание'))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	song_name = name.rsplit('-', 2)
	await ctx.send(f'Проигрывается композиция: {song_name[0]}')


@client.command()
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.connect()
		await ctx.send(f'Бот YELLOWSTONE отключился от канала: {channel}')


# Error
@clear.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ ctx.author.name }, обязательно укажите аргумент для команды!' )

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'{ ctx.author.name }, у ваша роли недостаточно прав!' )
	
# Get token
token = os.environ.get('BOT_TOKEN')

client.run(str(token))