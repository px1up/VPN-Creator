#!/usr/bin/python3
import os
import time
import random
import subprocess

name = str(input('Введите имя пользователя: '))

chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
number = int(1)
length = int(8)
for n in range(number):
    password =''
    for i in range(length):
        password += random.choice(chars)

Fout = open ( "/home/OVPN/pass.txt","w" )
Fout.write(password)
os.system('mv /home/OVPN/pass.txt '+ '/home/OVPN/' + name +'-pass.txt')


print('\n' ,'\033[1;31;40m При создании сертификата введите сгенерированный пароль для пользователя:\n ', '\033[1;33;40m', password, '\033[0;37;40m')


subprocess.check_call(['./easyrsa', 'build-client-full', name], cwd='/usr/share/easy-rsa/3')

#Копирование файлов сертификата в директорию
os.system('cp /usr/share/easy-rsa/3/pki/issued/' + name + '.crt ' + '/usr/share/easy-rsa/3/pki/private/' +  name +'.key '+ '/etc/openvpn/keys/ca.crt /etc/openvpn/keys/ta.key /tmp/keys')
os.system('chmod -R a+r /tmp/keys')

#Необходимо создать папку /tmp/OVPN_temp
#Чистим временную папку OVPN
os.system('rm -r /tmp/OVPN_temp/*')
#Копируем во временную папку
os.system('cp /tmp/keys/' + name + '.crt ' + '/tmp/keys/' +  name +'.key '+ '/tmp/keys/ca.crt /tmp/keys/ta.key /tmp/keys/template /tmp/OVPN_temp')

os.chdir('/tmp/OVPN_temp')
os.rename('ta.key','ta')

#Поучаем файл с расширением *.key
for file in os.listdir():
    if file.endswith(name + ".key"):
        key = (os.path.join(file))

#Поучаем файл с расширением *.crt
for file in os.listdir():
    if file.endswith(name + ".crt"):
        crt = (os.path.join(file))

for file in os.listdir():
    if file.endswith("ta"):

        ta = (os.path.join(file))
#Обрезаем файл crt
fileName=crt
with open(fileName,'r+') as f:
  contents=f.read()
  contents=contents[contents.find("-----BEGIN"):]
  f.seek(0)
  f.write(contents)
  f.truncate()

#обрезаем ключи
  fileName=key
with open(fileName,'r+') as f:
  contents=f.read()
  contents=contents[contents.find("-----BEGIN"):]
  f.seek(0)
  f.write(contents)
  f.truncate()
#обрезаем ta
  fileName=ta
with open(fileName,'r+') as f:
  contents=f.read()
  contents=contents[contents.find("-----BEGIN"):]
  f.seek(0)
  f.write(contents)
  f.truncate()

#Открываем файл конфига *.ovpn
with open("template") as file:
    config = file.read()

#Открываем файл ca
with open("ca.crt") as file:
    ca = file.read()

#Открываем файл ta
with open("ta") as file:
    ta = file.read()

#Открываем файл *.crt
with open(crt) as file:
    user_crt = file.read()

#Открываем файл конфига *key
with open(key) as file:
     user_key = file.read()

#Создаем файл *.ovpn на основе config.ovpn
with open("client.ovpn", "w") as file:
    #file.write(config + "\n" + "key-direction 1\n")
    file.write(config  + "\nkey-direction 1\n")

#Записываем ca
with open("client.ovpn", "a") as file:
    file.write("<ca>\n" + ca + "</ca>")

#Записываем user_crt
with open("client.ovpn", "a") as file:
    file.write("\n<cert>\n" + user_crt + "</cert>\n")

#Записываем user_key
with open("client.ovpn", "a") as file:
    file.write("<key>\n" + user_key + "</key>\n")

#Записываем ta
with open("client.ovpn", "a") as file:
    file.write("<tls-auth>\n" + ta + "</tls-auth>")

os.rename('ta','ta.key')
os.rename('client.ovpn', name + ".ovpn")

os.system('cp /tmp/OVPN_temp/' + name + '.ovpn' + ' /home/OVPN/')
os.system('chmod 777 -R /home/OVPN/')
print("Файл успешно создан")

exit()
