# @title Paso 1: Configuración Completa
from google.colab import drive
from pathlib import Path
import os
import requests
import time

# --- Configuración Interactiva ---
version = "1.21.1"       #@param ["1.21.1", "1.20.4", "1.19.4"]
ram = "12G"              #@param ["6G", "8G", "10G", "12G"]
server_type = "paper"    #@param ["paper", "vanilla", "fabric"]
tunnel_type = "ngrok"    #@param ["ngrok", "playit"]

# --- Inicialización ---
print("🛠️ Iniciando configuración del servidor...")
drive.mount('/content/drive', force_remount=True)
server_path = Path("/content/drive/My Drive/Minecraft-Server")
server_path.mkdir(parents=True, exist_ok=True)
os.chdir(server_path)

# --- Instalación de Java ---
java_version = "17" if any(v in version for v in ["1.19", "1.18"]) else "21"
print(f"☕ Instalando Java {java_version}...")
!sudo apt update -qq && sudo apt install -y openjdk-{java_version}-jre-headless

# --- Configuración del Túnel ---
if tunnel_type == "ngrok":
    print("\n🔌 Configurando Ngrok...")
    !curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    !echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    !sudo apt update && sudo apt install -y ngrok

    print("\n🔑 Requerimiento de Token:")
    print("1. Obtén tu token gratis en: https://dashboard.ngrok.com/get-started/your-authtoken")
    ngrok_token = input("2. Ingresa tu token de Ngrok: ").strip()
    !ngrok config add-authtoken $ngrok_token
else:
    print("\n🎮 Configurando Playit.gg...")
    !curl -sSL https://github.com/playit-cloud/playit-agent/releases/latest/download/playit-linux-amd64 -o playit
    !chmod +x playit && sudo mv playit /usr/local/bin/
    (server_path / "playit-config").mkdir(exist_ok=True)
    !ln -sf "$(pwd)/playit-config" "/root/.config/playit"

# --- Descarga del Servidor ---
print(f"\n⬇️ Descargando {server_type} {version}...")
if server_type == "paper":
    api_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}"
    build = requests.get(api_url).json()["builds"][-1]
    !wget -q --show-progress -O server.jar "{api_url}/builds/{build}/downloads/paper-{version}-{build}.jar"
elif server_type == "fabric":
    !wget -q --show-progress -O server.jar "https://meta.fabricmc.net/v2/versions/loader/{version}/latest/server/jar"
else:
    manifest = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    version_data = next(v for v in manifest["versions"] if v["id"] == version)
    jar_url = requests.get(version_data["url"]).json()["downloads"]["server"]["url"]
    !wget -q --show-progress -O server.jar "$jar_url"

# --- Configuración Final ---
!echo "eula=true" > eula.txt
(server_path / "plugins").mkdir(exist_ok=True)

print("\n✅ ¡Configuración completada!")
print(f"""
📋 Resumen:
- Versión: {version}
- RAM: {ram}
- Tipo: {server_type}
- Túnel: {tunnel_type}
- Ruta: {server_path}
""")
print("➡️ Ejecuta el 'Paso 2: Inicio del Servidor' para comenzar")