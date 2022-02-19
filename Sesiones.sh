#!/bin/bash

# ---------------------------------------------------------
# UsuariosUltimaSesion.sh © 2018 Por Eduardo López Zúñiga
# Versión-Revisión: 1.1
# Fecha: 17/11/2018
# ---------------------------------------------------------

# Parámetros

flUsuariosTemporal=/tmp/flUsuariosTemporal.txt
flUsuarioTemporal=/tmp/flUsuarioTemporal.txt
flArchivoLog=`date +%F'_'%T`
flArchivoLog=/tmp/Sesiones_$flArchivoLog.txt
numeroBase=500

# Se procede a crear el archivoLog de accesos
if  [ -f $flArchivoLog ]
then
  rm -f $flArchivoLog
fi

echo -e "Creando archivo:\t"$flArchivoLog

/usr/bin/touch $flArchivoLog

if [ -f $flUsuariosTemporal ]
then
  rm -f $flUsuariosTemporal
fi

cut -d ":" -f 1,3 /etc/passwd > $flUsuariosTemporal

# Se procede a listar los usuarios
 
for usuario in `cat $flUsuariosTemporal`
do

  echo $usuario > $flUsuarioTemporal
  usrID=`cut -d ":" -f 2 $flUsuarioTemporal` 
  
  if [ $usrID -ge $numeroBase ]
  then
  
    # Este usuario fue creado y debe ser utilizado
	
    usrNombre=`cut -d ":" -f 1 $flUsuarioTemporal`
    echo "UsrID: "$usrNombre >> $flArchivoLog
	
    lstLog=`lastlog | grep $usrNombre`
    echo -e "\tlastlog: "$lstLog >> $flArchivoLog
	
    lstLog=`last -d -n 1 $usrNombre | head -1`
    echo -e "\tlast: "$lstLog"\n" >> $flArchivoLog
  fi
done

echo "UsrID: root" >> $flArchivoLog

lstLog=`lastlog | grep root`
echo -e "\tlastlog: "$lstLog >> $flArchivoLog

lstLog=`last -d -n 1 root | head -1`
echo -e "\tlast: "$lstLog"\n" >> $flArchivoLog

lstLog=`last root | tail -1`
echo "Archivo: "$lstLog >> $flArchivoLog

# Limpieza de archivos

if [ -f $flUsuariosTemporal ]
then
  rm -f $flUsuariosTemporal
fi

if [ -f $flUsuarioTemporal ]
then
  rm -f $flUsuarioTemporal
fi

echo -e "\nFin del Proceso ..."

exit 0
