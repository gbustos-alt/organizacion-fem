#!/bin/bash

# ==============================================================================
# Script de Despliegue - Organización FEM
# ==============================================================================
# Este script se ejecuta localmente. Se conecta al VPS a través de SSH en el
# puerto 5363, descarga los últimos cambios del repositorio, actualiza
# dependencias, compila estilos CSS y reinicia el servicio systemd.
# ==============================================================================

# Configuración de Servidor
VPS_USER="guillermo25"
VPS_HOST="149.50.134.206"
VPS_PORT="5363"
VPS_PATH="/home/guillermo25/fundacion_fem"

echo "======================================================================"
echo "🚀 Iniciando despliegue de Organización FEM en VPS..."
echo "🔗 Servidor: $VPS_HOST:$VPS_PORT"
echo "======================================================================"
echo ""
echo "🔑 Nota: Se solicitará tu contraseña de SSH para la conexión."
echo "   Sudo en el servidor podría requerir tu contraseña nuevamente."
echo ""

# Comandos remotos a ejecutar secuencialmente tras la sincronización
REMOTE_COMMANDS="
  echo '📂 [2/4] Navegando a $VPS_PATH...' && \
  cd $VPS_PATH && \
  \
  echo '🐍 [3/4] Actualizando dependencias de Python en venv...' && \
  source venv/bin/activate && \
  pip install -r requirements.txt && \
  \
  echo '🎨 [4/4] Instalando dependencias de Node y compilando CSS (Sass)...' && \
  rm -rf node_modules package-lock.json && \
  npm install && \
  npm run build:css && \
  \
  echo '🔄 [5/4] Reiniciando servicio systemd (fundacion_fem)...' && \
  sudo systemctl restart fundacion_fem && \
  \
  echo '✅ ¡Despliegue finalizado con éxito!'
"

echo "📤 [1/4] Sincronizando archivos locales con el VPS (rsync)..."
rsync -avzh --delete \
  --exclude='venv/' \
  --exclude='node_modules/' \
  --exclude='.git/' \
  --exclude='*.db' \
  --exclude='.DS_Store' \
  --exclude='deploy.sh' \
  -e "ssh -p $VPS_PORT" \
  ./ "$VPS_USER@$VPS_HOST:$VPS_PATH/"

if [ $? -ne 0 ]; then
    echo "❌ Error al sincronizar archivos mediante rsync."
    exit 1
fi

echo ""
echo "🔑 Conectando al VPS para compilar y reiniciar la aplicación..."
# Conexión SSH con asignación de terminal virtual (-t) para permitir ingresar contraseñas interactivamente
ssh -p "$VPS_PORT" -t "$VPS_USER@$VPS_HOST" "$REMOTE_COMMANDS"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ¡El despliegue ha terminado correctamente!"
    echo "🌍 Sitio web actualizado en: https://fem.becubical.com"
else
    echo ""
    echo "❌ Ocurrió un error durante el despliegue. Por favor verifica los mensajes anteriores."
fi
