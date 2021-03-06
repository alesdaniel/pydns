#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script de actualizacion automatica para Hurricane Electric DNS
# Testeado en Python 3.4 windows, Debian
#BSD
#Copyright (c) 2016, Ales Daniel alesdaniel77@gmail.com
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#* Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#
#* Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
#* Neither the name of pydns nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# 28/03/2016 - Version Inicial - Daniel.
# 07/04/2016 - Agrega log - Daniel.

import sys
import re
import ssl
import logging
import socket
import urllib.request, urllib.parse, urllib.error

pagina = ''
ips = ''

def actualiza_ip():
    global ips
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='py_dns.log',
                        level=logging.ERROR)
    datos = {}
    #Datos de pagina a actualizar IPs
    datos['hostname'] = 'rsync.petro-tandil.com.ar'
    datos['password'] = 'pass'
    datos['myip'] = ips[0]
    pag = urllib.parse.urlencode(datos)
    print(pag)
    url='https://dyn.dns.he.net/nic/update?'
    urlc=url + pag
    context = ssl._create_unverified_context()
    print(urlc)
    try:
        datos = urllib.request.urlopen(urlc, context=context)
    except urllib.error.URLError as e:
        logging.error("actualiza_ip() " + e)
        print(e);
    except socket.error as e:
        logging.error("actualiza_ip() " + e)
        print(e);
    except socket.timeout as e:
        logging.error("actualiza_ip() " + e)
        print(e);
    except UnicodeEncodeError as e:
        logging.error("actualiza_ip() " + e)
        print(e);
    except http.client.BadStatusLine as e:
        logging.error("actualiza_ip() " + e)
        print(e);
    except http.client.IncompleteRead as e:
        logging.error("actualiza_ip() " + e)
        print(e);
    except urllib.error.HTTPError as e:
        logging.error("actualiza_ip() " + e)
        print(e);
    #https: // dyn.dns.he.net / nic / update?hostname = dyn.example.com & password = password & myip = 192.168.0.1

#Compara que la ultima ip sea igual a la ultima grabada
def consulta(ips):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='py_dns.log',
                        level=logging.ERROR)
    try:
        a = open('ip.txt', 'r+')
    except IOError:
        a = open('ip.txt', 'w+')
    str = a.read()
    if str == ips:
        a.closed
        return True
    else:
        a.close()
        a = open('ip.txt', 'w+')
        a.write(ips)
        logging.error("Actualizacion IP: " + ips)
        a.closed
        return False

# Busca dentro del html o texto devuelto la direccion ip
def busca_ip():
    global ips
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='py_dns.log',
                        level=logging.ERROR)
    ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', pagina)
    print(ips[0])
    try:
        socket.inet_aton(ips[0])
    except TypeError:
        print("type")
        logging.error("busca_ip() type " + ips[0])
        exit(1)
    except socket.error:
        print("sock")
        logging.error("busca_ip() sock " + ips[0])
        exit(1)

    if consulta(ips[0]):
        pass
    else:
        actualiza_ip()

def descarga():
    global pagina
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='py_dns.log',
                        level=logging.ERROR)
    try:
        #html = urllib.request.urlopen("http://www.see-my-ip.com/")
        html = urllib.request.urlopen("http://checkip.dyndns.org/")
        pagina = html.read().decode("latin1", 'ignore')
    except urllib.error.URLError as e:
        print(e);
        logging.error("descarga() " + e)
        pagina = ''
    except socket.error as e:
        print(e);
        logging.error("descarga() " + e)
        pagina = ''
    except socket.timeout as e:
        print(e);
        logging.error("descarga() " + e)
        pagina = ''
    except UnicodeEncodeError as e:
        print(e);
        logging.error("descarga() " + e)
        pagina = ''
    except http.client.BadStatusLine as e:
        print(e);
        logging.error("descarga() " + e)
        pagina = ''
    except http.client.IncompleteRead as e:
        print(e);
        logging.error("descarga() " + e)
        pagina = ''
    except urllib.error.HTTPError as e:
        print(e);
        logging.error("descarga() " + e)
        pagina = ''

    if len(pagina) > 0:
        print(pagina)
    else:
        logging.error("descarga() len(pagina) = 0")
        exit(1)


if __name__ == "__main__":
    if sys.version_info < (3, 0, 0):
        sys.stderr.write("You need python 3.0 or later to run this script\n")
        exit(1)

    descarga()
    busca_ip()

