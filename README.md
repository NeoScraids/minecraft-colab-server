# Minecraft Server en Google Colab ☁️🎮

Este repositorio te permite **montar y ejecutar un servidor de Minecraft** completamente gratuito usando Google Colab. Gracias al poder de la nube, podrás compartir tu mundo, invitar a amigos y probar mods sin gastar un solo peso.

---

## 📂 Estructura del repositorio

```bash
minecraft-colab-server/
├── MineServer.ipynb        # Notebook con todos los pasos interactivos
├── requirements.txt        # Dependencias necesarias para scripts adicionales
├── scripts/
│   ├── config_server.py    # Configuración automática de Java y servidor
│   ├── start_server.py     # Inicio del servidor y establecimiento de túnel
│   └── restart_server.py   # Reinicio seguro del servidor
└── README.md               # Esta documentación
```

---

## 🚀 ¿Por qué usar Colab?

* **Gratis**: Google Colab ofrece recursos gratuitos con GPU/CPU.
* **Portátil**: ejecuta tu servidor desde cualquier navegador.
* **Persistente**: guarda tu mundo en Google Drive.

---

## 🔧 Pasos Explicados

### 1️⃣ Paso 1: Configuración Completa

En este paso:

1. **Montas** tu Google Drive para persistir datos.
2. **Instalas** Java (versiones 1.19 a 1.21).
3. Descargas el **jar** del servidor (Paper, Vanilla o Fabric).
4. Creas y configuras el **directorio** del servidor en Drive.
5. Aceptas el **EULA** y creas carpeta de `plugins`.

> 💡 Modifica `version`, `ram`, `server_type` y `tunnel_type` en el notebook o en `scripts/config_server.py`.

### 2️⃣ Paso 2: Inicio del Servidor

Aquí:

1. Ejecutas el **jar** con la RAM especificada.
2. Configuras el **túnel** para exponer tu servidor (Ngrok o Playit.gg).
3. Capturas y muestras la **URL** pública para que otros se conecten.
4. Monitorea en tiempo real los **logs** con `tail -F server.log`.

> 📌 Ajusta `tunnel_type` y asegúrate de tener tu token de Ngrok o cuenta Playit.

### 3️⃣ Paso 3: Reinicio Seguro

Para cuando necesites reiniciar:

1. Detenemos el proceso de Java actual.
2. Volvemos a lanzar el servidor con la misma configuración.
3. Reconectamos el túnel y restablecemos los logs.

> 🔄 Útil tras cambios de `plugins` o actualizaciones de jar.

---

## 📓 Uso desde el Notebook

1. Abre `MineServer.ipynb` en Google Colab.
2. Sigue cada celda en orden: Paso 1, Paso 2 y Paso 3.
3. ¡Listo! Comparte la URL y únete al juego.

---

## 🛠️ Detalle de los Scripts en Python

Además de la versión en Notebook, este repositorio incluye tres scripts independientes en `scripts/`, cada uno pensado para un paso clave:

1. **`config_server.py`** — **Configuración inicial (ejecútalo una sola vez)**

   * *Objetivo*: crear la carpeta base en Google Drive para persistencia del mundo y los plugins.
   * *Funcionalidad principal*:

     ```python
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
     ```
   * **Uso típico**:

     ```bash
     python scripts/config_server.py \
       --version 1.21.1 --ram 8G --type paper --mount-point '/content/drive/My Drive'
     ```

2. **`start_server.py`** — **Inicio del servidor (útil cada vez que arrancas Colab)**

   * *Objetivo*: lanzar el servidor con la configuración elegida y exponerlo mediante túnel.
   * *Funciones principales*:

     ```python
     # scripts/start_server.py  (extracto)
     import subprocess, argparse

     def start_server(ram, jar_path, tunnel):
         cmd = ['java', f'-Xmx{ram}', '-jar', jar_path, 'nogui']
         server_proc = subprocess.Popen(cmd)
         if tunnel == 'ngrok':
             subprocess.run(['ngrok', 'tcp', '25565', '--log', 'stdout'])
         else:  # playit
             subprocess.run(['playit', 'serve', '--port', '25565'])
         server_proc.wait()

     if __name__=='__main__':
         parser = argparse.ArgumentParser()
         parser.add_argument('--ram', default='8G')
         parser.add_argument('--tunnel', choices=['ngrok','playit'], default='ngrok')
         args = parser.parse_args()
         start_server(args.ram, '/content/drive/My Drive/Minecraft-Server/paper-1.21.1.jar', args.tunnel)
     ```
   * **Uso típico**:

     ```bash
     python scripts/start_server.py --ram 8G --tunnel playit
     ```

3. **`restart_server.py`** — **Reinicio seguro (tras instalar plugins o mods)**

   * *Objetivo*: detener el servidor en ejecución y reiniciarlo sin perder el mundo ni configuración de túnel.
   * *Extracto de código*:

     ```python
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
     ```
   * **Uso típico**:

     ```bash
     python scripts/restart_server.py --ram 8G --tunnel ngrok
     ```

### 🔄 Flexibilidad y Configuración

* **Versiones de Minecraft**: soporta `1.19.x` hasta `1.21.x`, simplemente ajusta `--version` en `config_server.py`.
* **Tipos de servidor**:

  * `paper`: alto rendimiento y compatibilidad con plugins.
  * `vanilla`: experiencia oficial sin modificaciones.
  * `fabric`: ideal para mods con Fabric Loader.
* **Proveedores de túnel**:

  * **Ngrok**: rápido de configurar con `ngrok authtoken <TU_TOKEN>` y `--tunnel ngrok`.
  * **Playit.gg**: requiere `playit` CLI y una cuenta gratuita para túneles persistentes.

Con esta estructura modular, puedes integrar tus propios scripts, pipelines CI o incluso un bot de Discord que controle el servidor. ¡La nube es tu límite!

## 📂 Persistencia en Google Drive en Google Drive

El mundo se guarda en tu Drive bajo `Minecraft-Server/`:

```bash
/content/drive/My Drive/Minecraft-Server
```

No pierdas tu progreso: ¡los datos sobreviven entre sesiones!

---

## 💬 Contribuciones

* Reporta issues si algo falla.
* Envía pull requests con mejoras (opción de tunnels, mods, backups automáticos).

---

## 🎉 ¡A jugar!

Comparte tu IP con amigos y disfruta de tu servidor **24/7** (o mientras la sesión de Colab esté activa).

---

*Este proyecto es gratuito y aprovecha recursos de Google Colab. Úsalo con responsabilidad.*
