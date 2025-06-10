# scripts/config_server.py  (extracto)
from pathlib import Path
import argparse

def init_drive(version, ram, server_type, mount_point):
    drive_path = Path(mount_point) / 'Minecraft-Server'
    world_path = drive_path / 'world'
    plugins_path = drive_path / 'plugins'
    drive_path.mkdir(parents=True, exist_ok=True)
    world_path.mkdir(exist_ok=True)
    plugins_path.mkdir(exist_ok=True)
    # Descarga y configura el jar:
    jar_url = f'https://papermc.io/api/v2/projects/{server_type}/versions/{version}/builds/latest/downloads/{server_type}-{version}.jar'
    # ... código para descargar con requests y guardar en drive_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', required=True)
    parser.add_argument('--ram', default='2G')
    parser.add_argument('--type', choices=['paper','vanilla','fabric'], default='paper')
    parser.add_argument('--mount-point', default='/content/drive/My Drive')
    args = parser.parse_args()
    init_drive(args.version, args.ram, args.type, args.mount_point)