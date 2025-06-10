# scripts/restart_server.py  (extracto)
import subprocess, argparse, psutil

def restart(jar_path, ram, tunnel):
    # Encontrar proceso Java y matarlo:
    for proc in psutil.process_iter(['name','pid']):
        if proc.info['name']=='java': proc.kill()
    # Iniciar de nuevo con start_server.py
    subprocess.run(['python','start_server.py','--ram',ram,'--tunnel',tunnel])

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ram', default='8G')
    parser.add_argument('--tunnel', choices=['ngrok','playit'], default='ngrok')
    args = parser.parse_args()
    restart('/content/drive/My Drive/Minecraft-Server/paper-1.21.1.jar', args.ram, args.tunnel)