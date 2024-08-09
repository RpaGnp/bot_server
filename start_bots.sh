#!/bin/bash

# Array de nombres
ArrayNames=(
  'Bot_MarcadorCali5'
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
  echo "  $bot_name_lower:" >> docker-compose.override.yml
  echo "    build:" >> docker-compose.override.yml
  echo "      context: ." >> docker-compose.override.yml
  echo "    container_name: $bot_name_lower" >> docker-compose.override.yml
  echo "    volumes:" >> docker-compose.override.yml
  echo "      - ./app:/app" >> docker-compose.override.yml
  echo "    environment:" >> docker-compose.override.yml
  echo "      BOT_NAME: ${bot_name}" >> docker-compose.override.yml
done

# Levantar los servicios de docker-compose con la escala especificada
docker-compose up -d
