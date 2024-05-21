#!/bin/bash
# Script moverLog.sh que envía el log de aiquimia al directorio temporal

# Movemos el log al tmp
mv /home/admin/Little-AIlchemy-en-AWS/LittleAIlchemy/aiquimia.log /tmp

# Mostramos un mensaje por si se ejecuta el script manualmente
if [ $? -eq 0 ]; then
    echo "El log ha sido movido a /tmp."
else
    echo "Error al mover el log"
fi
