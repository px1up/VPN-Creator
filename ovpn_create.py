#!/usr/bin/python3
import os
import time

#путь к RSA
rsa_path = ('/etc/openvpn/rsa')

name = str(input('Введите имя пользователя: '))
os.chdir(rsa_path)
os.system('. ./vars')
#задержка чтобы успели подключится vars
time.sleep(4)
os.system('./build-key-pass ' + name)

#если сертификаты не подписываются автоматически
#os.system('/easyrsa gen-req ' + name)
#подписать сертификат
#os.system('./easyrsa sign-req client ' + name)

#Копирование файлов сертификата в директорию
os.system('cp /etc/openvpn/rsa/keys/' + name + '.crt ' + '/etc/openvpn/rsa/keys/' +  name +'.key '+ '/etc/openvpn/rsa/keys/ca.crt /etc/openvpn/rsa/keys/ta.key /home/tmp')
os.system('chmod -R a+r /home/tmp/')

#Необходимо создать папку /tmp/OVPN_temp
#Чистим временную папку OVPN
os.system('rm -r /tmp/OVPN_temp/*')
#Копируем во временную папку
os.system('cp /home/tmp/' + name + '.crt ' + '/home/tmp/' +  name +'.key '+ '/home/tmp/ca.crt /home/tmp/ta.key /home/tmp/template /tmp/OVPN_temp')

os.chdir('/tmp/OVPN_temp')
os.rename('ta.key','ta')

#Поучаем файл с расширением *.key
for file in os.listdir():
    if file.endswith(".key"):
        key = (os.path.join(file))

#Поучаем файл с расширением *.crt
for file in os.listdir():
    if file.endswith(".crt"):
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
    file.write(config  + "key-direction 1\n")

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
print("Файл успешно создан")

exit()
