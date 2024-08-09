import requests
import json
from colorama import init, Fore
import discord
from discord.ext import commands
from discord import app_commands

init(autoreset=True)

TOKEN = "EL TOKEN DE TU BOT"

intents = discord.Intents.default()
intents.message_content = True  

ALLOWED_USER_ID = 1238471224510648412  

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

def realizar_pedido(url, seguidores, service_id, use_alternate_api=False):
    if use_alternate_api:
        api_endpoint = "API DE TU PANEL PRINCIPAL"  
        api_key = "API KEY DE TU PANEL PRINCIPAL"  
    else:
        api_endpoint = "API DE TU PANEL SECUNDARIO (OPCIONAL)" 
        api_key = "API KEY DE TU PANEL SECUNDARIO (OPCIONAL)"  

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "key": api_key,
        "action": "add",
        "service": service_id,
        "link": url,
        "quantity": seguidores
    }

    try:
        response = requests.post(api_endpoint, headers=headers, json=data)
        response.raise_for_status()
        return "success"
    except requests.exceptions.ConnectionError as e:
        return f"Error de conexión: {e}"
    except requests.exceptions.HTTPError as e:
        return f"Error HTTP: {e}"
    except requests.exceptions.RequestException as e:
        return f"Error durante la solicitud HTTP: {e}"

@bot.tree.command(name="realizar_pedido", description="Realiza un pedido de seguidores o likes.")
@app_commands.describe(
    servicio="Elige el servicio",
    url="Introduce el URL de la persona",
    cantidad="Introduce la cantidad de seguidores/likes que quieres comprar"
)
@app_commands.choices(servicio=[
    app_commands.Choice(name="Seguidores Instagram", value="seguidores_instagram"),
    app_commands.Choice(name="Likes Instagram", value="likes_instagram"),
    app_commands.Choice(name="Seguidores TikTok", value="seguidores_tiktok"),
    app_commands.Choice(name="Visitas TikTok", value="visitas_tiktok"),
    app_commands.Choice(name="Likes TikTok", value="likes_tiktok"),
    app_commands.Choice(name="Visitas Instagram", value="visitas_instagram")
])
async def realizar_pedido_command(interaction: discord.Interaction, servicio: app_commands.Choice[str], url: str, cantidad: int):
    if interaction.user.id != ALLOWED_USER_ID:
        await interaction.response.send_message("No tienes permiso para usar este comando.", ephemeral=True)
        return


#AQUI POR ID DE LOS SERVICIOS
    service_ids = {
        "seguidores_instagram": 0000,  
        "likes_instagram": 0000,
        "visitas_instagram": 0000,
        "seguidores_tiktok": 0000,
        "likes_tiktok": 0000,
        "visitas_tiktok": 0000     
    }
    use_alternate_api = servicio.value in ["seguidores_tiktok", "seguidores_instagram", "visitas_tiktok", "likes_tiktok", "visitas_instagram"]
    
    service_id = service_ids.get(servicio.value)
    if not service_id:
        await interaction.response.send_message("Servicio no válido.")
        return
    
    resultado = realizar_pedido(url, cantidad, service_id, use_alternate_api)
    
    if resultado == "success":
        embed = discord.Embed(
            title=f"{servicio.name} - Pedido Realizado",
            description=f"Se han enviado {cantidad} {servicio.name.lower()}.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Servicio", value=servicio.name, inline=True)
        embed.add_field(name="Cantidad", value=str(cantidad), inline=True)
        embed.add_field(name="URL", value=url, inline=False)
        embed.set_footer(text="Bot Created By Kayy")
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(resultado)

@bot.tree.command(name="encontrar", description="Encuentra un perfil de TikTok o Instagram.")
@app_commands.describe(
    plataforma="Elige la plataforma",
    usuario="Introduce el nombre de usuario"
)
@app_commands.choices(plataforma=[
    app_commands.Choice(name="Instagram", value="instagram"),
    app_commands.Choice(name="TikTok", value="tiktok")
])
async def encontrar_command(interaction: discord.Interaction, plataforma: app_commands.Choice[str], usuario: str):
    if plataforma.value == "instagram":
        url = f"https://www.instagram.com/{usuario}/"
    elif plataforma.value == "tiktok":
        url = f"https://www.tiktok.com/@{usuario}"
    else:
        await interaction.response.send_message("Plataforma no válida.")
        return
    
    await interaction.response.send_message(f"{url}")

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

bot.run(TOKEN)