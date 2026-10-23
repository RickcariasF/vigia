# Imagen base: Linux mínimo con Python 3.12 ya instalado
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor (se crea si no existe)
WORKDIR /app

# Copia SOLO la lista de dependencias primero... (pregunta 1 abajo 👇)
COPY requirements.txt .

# Instala las dependencias dentro de la imagen; --no-cache-dir evita guardar basura y la imagen pesa menos
RUN pip install --no-cache-dir -r requirements.txt

# Ahora sí copia el código y la lista de sitios
COPY check.py sites.txt ./

# Comando que se ejecuta cuando arranca un contenedor de esta imagen
CMD ["python", "check.py"]