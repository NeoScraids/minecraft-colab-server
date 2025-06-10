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

## 🛠️ Opcional: Scripts en Python

Si prefieres no usar el notebook:

```bash
pip install -r requirements.txt
python scripts/config_server.py \  
    --version 1.21.1 --ram 12G --type paper --tunnel ngrok
python scripts/start_server.py --tunnel ngrok
# Para reiniciar:
python scripts/restart_server.py --tunnel ngrok
```

Cada script replica la lógica de su paso correspondiente y puede integrarse en workflows automáticos.

---

## 📂 Persistencia en Google Drive

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
