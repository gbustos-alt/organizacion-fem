#!/bin/bash
# Script de Despliegue Automatizado - Testing

# 1. Comprobar si hay cambios sin confirmar y guardarlos en stash
CHANGES_STASHED=false
if ! git diff-index --quiet HEAD --; then
    echo "📦 Guardando tus cambios locales en progreso en el stash..."
    git stash -u
    CHANGES_STASHED=true
fi

# 2. Descargar lo último de GitHub (Gabi u otros)
echo "🔄 Sincronizando con los cambios de GitHub..."
git fetch origin
git pull --rebase origin develop

if [ $? -ne 0 ]; then
    echo "❌ Error al sincronizar. Hay conflictos complejos en las ramas remota y local."
    echo "Resuelve los conflictos en Git y vuelve a correr el script."
    exit 1
fi

# 3. Devolver los cambios del stash (si los había)
if [ "$CHANGES_STASHED" = true ]; then
    echo "📥 Restaurando tus cambios locales en progreso..."
    git stash pop
    if [ $? -ne 0 ]; then
        echo "⚠️  Conflicto al restaurar tus cambios. Resuélvelos manualmente y haz commit."
        exit 1
    fi
fi

# 4. Confirmar y subir cambios
echo "💬 ¿Quieres confirmar tus cambios actuales y subirlos a GitHub? (s/n)"
read -r CONFIRM
if [ "$CONFIRM" = "s" ]; then
    echo "Escribe el mensaje de commit:"
    read -r COMMIT_MSG
    git add .
    git commit -m "$COMMIT_MSG"
    git push origin develop
fi

# 5. Desplegar en el VPS (usando SSH sin contraseña)
echo "🚀 Desplegando en el VPS de testing..."
ssh -p 5363 gianluca@149.50.134.206 "
    cd /home/guillermo25/testing_fem && \
    git fetch origin && \
    git reset --hard origin/develop && \
    npm install && \
    npm run build:css
"
echo "✅ ¡Despliegue finalizado con éxito!"
