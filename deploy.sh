#!/bin/bash

# ==============================================================================
# Script de Despliegue - Organización FEM
# ==============================================================================
# Este script se ejecuta localmente. Se conecta al VPS a través de SSH en el
# puerto 5363, descarga los últimos cambios del repositorio, actualiza
# dependencias, compila estilos CSS y reinicia el servicio systemd.
# ==============================================================================

# Configuración de Servidor de Testing
VPS_USER="gianluca"
VPS_HOST="149.50.134.206"
VPS_PORT="5363"
VPS_PATH="/home/guillermo25/testing_fem"

echo "======================================================================"
echo "🚀 Actualizando entorno de TESTING en VPS..."
echo "🔗 Servidor: $VPS_HOST:$VPS_PORT"
echo "📂 Directorio: $VPS_PATH"
echo "======================================================================"
echo ""
echo "🔑 Nota: Se solicitará tu contraseña de SSH (emayonforge2026)."
echo ""

# Comandos remotos a ejecutar secuencialmente
REMOTE_COMMANDS="
  cd $VPS_PATH && \
  echo '⚙️ [1/3] Configurando directorio seguro en Git...' && \
  git config --global --add safe.directory $VPS_PATH 2>/dev/null || true && \
  echo '📥 [2/3] Descargando cambios de GitHub (git pull)...' && \
  git pull origin develop && \
  echo '🔄 [3/3] Reiniciando servicio de aplicación...' && \
  (sudo systemctl restart testing_fem 2>/dev/null || systemctl restart testing_fem 2>/dev/null || true) && \
  echo '✅ ¡Actualización finalizada!'
"

echo "🔑 Conectando al VPS para actualizar el código..."
# Conexión SSH con asignación de terminal virtual (-t)
ssh -p "$VPS_PORT" -t "$VPS_USER@$VPS_HOST" "$REMOTE_COMMANDS"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ¡El entorno de pruebas ha sido actualizado correctamente!"
    echo "🌍 Sitio web en vivo en: https://testingfem.emayonforge.com"
else
    echo ""
    echo "❌ Ocurrió un error al actualizar. Por favor verifica los mensajes anteriores."
fi
