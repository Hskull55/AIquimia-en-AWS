#!/bin/bash
# Script copiarLog.sh que copia los logs del servidor principal a la EC2 de backup

# Miramos la hora para que los logs no se sobrescriban
hora=$(TZ="Europe/Madrid" date +"%Y-%m-%d_%H-%M-%S")

# Copiamos el log a la instancia EC2 de backup
scp -i /home/admin/Little-AIlchemy-en-AWS/LittleAIlchemy/ssh/labsuser.pem /tmp/aiquimia.log admin@172.31.0.69:/home/admin/logs/aiquimia-$hora.log

# Mostramos un mensaje por si se ejecuta el script manualmente
if [ $? -eq 0 ]; then
  echo "Archivo copiado exitosamente"
else
  echo "Error al copiar el archivo"
fi
