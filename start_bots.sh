#!/bin/bash

# Array de nombres de los bots
ArrayNames=(
    'Bot_GestorCali1'
    'Bot_GestorCali2'
    'Bot_GestorCali3'
    'Bot_GestorCali4'
    'Bot_GestorCali5'
    'Bot_MarcadorCali'
    'Bot_MarcadorCali1'
    'Bot_MarcadorCali2'
    'Bot_MarcadorCali3'
    'Bot_MarcadorCali4'
    'Bot_MarcadorCali5'
    'Bot_Gestor1'
    'Bot_Gestor2'
    'Bot_Gestor3'
    'Bot_Gestor4'
    'Bot_Gestor5'
    'Bot_GestorBuc1'
    'Bot_GestorBuc2'
    'Bot_GestorBuc3'
    'Bot_GestorBuc4'
    'Bot_GestorBuc5'
    'Bot_GestorBuc6'
    'Bot_Marcador1'
    'Bot_Marcador2'
    'Bot_Marcador3'
    'Bot_Marcador4'
    'Bot_Server'
)

# Si existe un archivo docker-compose.override.yml, detener y eliminar los contenedores especificados en él
if [ -f docker-compose.override.yml ]; then
    # Obtener los nombres de contenedores especificados en el archivo
    override_containers=($(grep -oP '(?<=container_name: )\S+' docker-compose.override.yml))

    # Detener y eliminar solo los contenedores especificados en el archivo
    for container_name in "${override_containers[@]}"; do
        if docker ps -q -f name="^${container_name}$" > /dev/null; then
            # Intentar detener  eliminar el contenedor, ignorar errores si no existe
            docker stop "$container_name" 2>/dev/null || true
            docker rm -v "$container_name" 2>/dev/null || true
        fi
    done
    # Eliminar volúmenes no persistentes
    docker-compose down --volumes
fi

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
    echo "      - /home/Bot_Server/DBGestionBot/:/DBGestionBot" >> docker-compose.override.yml
    echo "    environment:" >> docker-compose.override.yml
    echo "      - BOT_NAME=${bot_name}" >> docker-compose.override.yml
    echo "      - CHROME_PORT=${chrome_port}" >> docker-compose.override.yml
    echo "      - CHROME_HOST=${bot_name_lower}_chrome" >> docker-compose.override.yml

    # Configuración del navegador Selenium para el bot
    echo "  ${bot_name_lower}_chrome:" >> docker-compose.override.yml
    echo "    image: selenium/standalone-chrome" >> docker-compose.override.yml
    echo "    container_name: ${bot_name_lower}_chrome" >> docker-compose.override.yml
    echo "    ports:" >> docker-compose.override.yml
    echo "      - \"$chrome_port:4444\"" >> docker-compose.override.yml
    echo "      - \"$((7900 + i)):7900\"" >> docker-compose.override.yml
    echo "      - \"$((9222 + i)):9222\"" >> docker-compose.override.yml
    echo "    environment:" >> docker-compose.override.yml
    echo "      - SE_VNC_NO_PASSWORD=1" >> docker-compose.override.yml
    echo "      - WAIT_TIMEOUT=0" >> docker-compose.override.yml
    echo "      - NOVNC_ENABLE_CLIPBOARD=true" >> docker-compose.override.yml
    echo "      - VNC_CLIPBOARD_LIMIT=10485760" >> docker-compose.override.yml
    echo "    restart: always" >> docker-compose.override.yml
done

# Levantar los servicios de docker-compose con la escala especificada
docker-compose up -d
