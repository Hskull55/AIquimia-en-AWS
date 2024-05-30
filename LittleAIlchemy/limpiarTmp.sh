#!/bin/bash
# Script limpiarTmp.sh que borra el contenido del directorio tmp

# Borrar el contenido del directorio /tmp
rm -rf /tmp/*

# Mostramos un mensaje por si se ejecuta el script manualmente
if [ $? -eq 0 ]; then
    echo "Contenido de /tmp borrado exitosamente"
else
    echo "Error al intentar borrar el contenido de /tmp"
fi
