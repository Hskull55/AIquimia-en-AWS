#!/bin/bash
# Script backup.sh para la instancia EC2 encargada de las copias de seguridad y logs (172.31.0.69)

HOST="database-1.ctgdefdtrckg.us-east-1.rds.amazonaws.com"
USUARIO="admin"
BASE_DATOS="aiquimia"
CONTRASENA="123456Aa"
DIRECTORIO="/dbBackup"
# La zona horaria la tuve que especificar porque la máquina estaba en UTC, aunque ya he cambiado eso, lo dejo por si acaso me hiciera falta en algún momento
FECHA=$(TZ="Europe/Madrid" date +"%Y-%m-%d_%H-%M-%S")
FICHERO_COPIA="$DIRECTORIO/$BASE_DATOS-$FECHA.sql"

# Creamos el directorio donde irán las copias de seguridad (si no existía ya, usando -p, que crea los directorios necesarios si no existen. Si existen no hace nada)
# Lo podríamos hacer con un if, pero así es más sencillo
mkdir -p $DIRECTORIO

# Hacemos la copia de seguridad con el endpoint de la instancia RDS
mysqldump -h $HOST -u $USUARIO -p$CONTRASENA $BASE_DATOS > $FICHERO_COPIA

# Mostramos un mensaje de éxito/error por si el script se ejecuta manualmente en lugar de usando el cron
if [ $? -eq 0 ]; then
    echo "Copia de seguridad creada con éxito en: $DIRECTORIO"
else
    echo "Error al crear la copia de seguridad"
fi
