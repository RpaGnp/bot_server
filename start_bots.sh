#!/bin/bash

# Array de nombres de los bots
ArrayNames=(
  'Bot_Gestor1'
  'Bot_Gestor2'
  'Bot_Gestor3'
  'Bot_Gestor4'
  'Bot_Gestor5'
  'Bot_Marcador2'
  'Bot_Marcador3'
)

# Detener y eliminar contenedores que no están en el archivo docker-compose.override.yml
running_containers=$(docker ps -q)
for container_id in $running_containers; do
  container_name=$(docker inspect --format '{{.Name}}' $container_id | sed 's/\///')
  if [[ ! " ${ArrayNames[@]} " =~ " ${container_name^} " ]]; then
    echo "Stopping and removing container $container_name"
    docker stop $container_id
    docker rm $container_id
  fi
done

# Crear un archivo docker-compose.override.yml con los nombres del array
echo "version: '3.8'" > docker-compose.override.yml
echo "" >> docker-compose.override.yml
echo "services:" >> docker-compose.override.yml

for i in "${!ArrayNames[@]}"; do
  bot_name="${ArrayNames[$i]}"
  bot_name_lower=$(echo "$bot_name" | tr '[:upper:]' '[:lower:]')

  # Puerto WebDriver único para el navegador asociado al bot
  chrome_port=$((4445 + i))

  # Configuración del bot
  echo "  $bot_name_lower:" >> docker-compose.override.yml
  echo "    build:" >> docker-compose.override.yml
  echo "      context: ." >> docker-compose.override.yml
  echo "    container_name: $bot_name_lower" >> docker-compose.override.yml
  echo "    volumes:" >> docker-compose.override.yml
  echo "      - ./app:/app" >> docker-compose.override.yml
  echo "    environment:" >> docker-compose.override.yml
  echo "      - BOT_NAME=${bot_name}" >> docker-compose.override.yml
  echo "      - CHROME_PORT=${chrome_port}" >> docker-compose.override.yml  # Pasar el puerto del navegador
  echo "      - CHROME_HOST=${bot_name_lower}_chrome" >> docker-compose.override.yml  # Pasar el nombre del host del navegador

  # Configuración del navegador Selenium para el bot
  echo "  ${bot_name_lower}_chrome:" >> docker-compose.override.yml
  echo "    image: selenium/standalone-chrome" >> docker-compose.override.yml
  echo "    container_name: ${bot_name_lower}_chrome" >> docker-compose.override.yml
  echo "    ports:" >> docker-compose.override.yml
  echo "      - \"$chrome_port:4444\"" >> docker-compose.override.yml  # Exponer puerto WebDriver único
  echo "      - \"$((7900 + i)):7900\"" >> docker-compose.override.yml  # Exponer puerto noNvc único
  echo "      - \"$((9222 + i)):9222\"" >> docker-compose.override.yml  # Exponer puerto DevTools único
  echo "    environment:" >> docker-compose.override.yml
  echo "      - SE_VNC_NO_PASSWORD=1" >> docker-compose.override.yml  # Sin contraseña para VNC
  echo "    restart: always" >> docker-compose.override.yml
done

# Levantar los servicios de docker-compose con la escala especificada
docker-compose up -d
