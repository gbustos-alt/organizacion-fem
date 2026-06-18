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

# Comandos remotos a ejecutar secuencialmente
REMOTE_COMMANDS="
  echo '📂 [1/5] Navegando a $VPS_PATH...' && \
  cd $VPS_PATH && \
  \
  echo '📥 [2/5] Descargando últimos cambios de GitHub (git pull)...' && \
  git pull origin main && \
  \
  echo '🐍 [3/5] Actualizando dependencias de Python en venv...' && \
  source venv/bin/activate && \
  pip install -r requirements.txt && \
  \
  echo '🎨 [4/5] Instalando dependencias de Node y compilando CSS (Sass)...' && \
  rm -rf node_modules package-lock.json && \
  npm install && \
  npm run build:css && \
  \
  echo '🔄 [5/5] Reiniciando servicio systemd (fundacion_fem)...' && \
  sudo systemctl restart fundacion_fem && \
  \
  echo '✅ ¡Despliegue finalizado con éxito!'
"

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
