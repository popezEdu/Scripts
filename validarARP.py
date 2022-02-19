#!/usr/bin/env python

# ---------------------------------------------------------
# validarARP: 2020 Por Eduardo Lopez Zuniga
# Python: 2
#
# Version-Revision: 1.0 (31/08/2020)
# Liberacion del script, reemplaza el anterior script .sh
# 
# Version-Revision: 1.1 (09/10/2020)
# Envia un email indicando que hubo un bloqueo de MAC.
# ---------------------------------------------------------

# Si es que se detecta una entrada no valida en la tabla arp
# Se procede a bloquear el equipo.


# REACHABLE: la entrada ARP es valida y hay conectividad.
# STALE: la entrada ARP es valida pero no hay conectividad.
# FAILED: no hay conectividad y la MAC no ha sido detectada.
# DELAY: a la espera de confirmacion tras el envio de un paquete.


f_arpTemporal = r'/tmp/listaARP.txt'
f_arpValidos = r'/usr/local/sbin/ARPsPermitidos.txt'
f_reglas = r'/etc/shorewall/rules'

arpEncontrados = []
arpValidos = []
arpDenegar = []

redes = { 'lan': '192.168.0.', 'vpn' : '192.168.220.' , 'svr' : '10.1.0.'}

def leerARPsValidos():
    f = open(f_arpValidos, 'r')
    for linea in f:
        if not linea.startswith('\n'):
            corte = linea.split(' ')
            arpValidos.append(corte[0])
    f.close()    

def obtenerListaARP(red):
    import subprocess
    subprocess.call('/sbin/ip neigh show | grep ' + red + ' > ' + f_arpTemporal, shell=True)
    f = open(f_arpTemporal, 'r')
    for linea in f:
        lista = linea.split(' ')
        arpEncontrados.append(lista[4])
    f.close()


def validar(nombreRed):
    
    for valor in arpEncontrados:

        if not valor in arpValidos:

            if len(valor) == 17:
		   
                bandera = False
                texto = 'REJECT ' + nombreRed + ':~' + valor

                f = open(f_reglas,'r')            
			   
                for linea in f:
			   
                    if texto in linea:
                        bandera = True
                        break
                f.close()

                if not bandera:     
                    arpDenegar.append(texto) 
		           

def ajustarReglas():

    from datetime import datetime
    hoy = datetime.now()
    tiempo = hoy.strftime('%Y-%m-%d %H:%M:%S')
    
    texto = '#ARP Restringidos Automaticamente\n'
    contador = 1
    longitud = len(arpDenegar)
    for valor in arpDenegar:
        if longitud == contador:
            texto = texto + valor + ' any #Bloqueo ' + tiempo
        else:
            texto = texto + valor + ' any #Bloqueo ' + tiempo + '\n'
        contador = contador + 1

    f = open(f_reglas,'rt')
    datos = f.read()
    datos = datos.replace('#ARP Restringidos Automaticamente',texto)
    f.close()

    f = open(f_reglas,'wt')
    f.write(datos)
    f.close()

def reiniciarFirewall():
    import subprocess
    subprocess.call('/sbin/shorewall restart', shell=True)

def enviarEmail():
    import smtplib

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    


def limpiar():
    import subprocess
    subprocess.call('rm -rf ' + f_arpTemporal, shell=True)

def main():
    
    leerARPsValidos()

    # Iterar sobre las redes definidas en la variable redes
    for k in redes.keys():
        obtenerListaARP(redes[k])
        validar(k)
        del arpEncontrados[:]
    if len(arpDenegar) > 0:
        ajustarReglas()
        reiniciarFirewall()
    limpiar()
    

if __name__ == '__main__':
    main()
