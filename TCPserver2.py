import socket
import threading
import RPi.GPIO as GPIO
import time

execfile("TCPserver_data.py")






def mainLooper(me):
 mlooper = True
 while mlooper:
  print "mainlooper " + str(me.readPR())
  me.auto_switcher()
  time.sleep(10)


def handle_client_connection(client_socket, me):
# try:
 continueloop = True
 while continueloop:
  try:
   request = client_socket.recv(1024)
  except:
   client_socket.send('server killed client')
   print 'client died'
   me.client_socket_list.remove(client_socket)
   client_socket.close()
#  time.sleep(15)
  if request is not None and len(request)>0:
   dataFromClient = request.decode()
   dataFromClient = dataFromClient.strip()
   print dataFromClient
   command = dataFromClient.split(" ")
   print command[0]
   if command[0] == me.unit_name:
    handle_command(client_socket, command, me)
   elif command[0] == "ping":
    client_socket.send("pong")
    print 'pong send'
   elif command[0] == "break":
    continueloop = False
    print "Connection breaked"
    client_socket.close()
   else:
    print 'forwarded: ' + dataFromClient
    if command[0] == him.unit_name:
     him.s.send(dataFromClient)
  else:
   me.client_socket_list.remove(client_socket)
   client_socket.close()
   continueloop = False
   print 'connection terminated'



  
def handle_command(client_socket, command, me):
 try:
  if command[1] == "r1":
   me.relay_switch(int(command[2]),int(command[3]))
   me.send_relay_status(client_socket)
  elif command[1] == "rs":
   me.relays_switch(int(command[2]))
   me.send_relay_status(client_socket)
  elif command[1] == "st":
   me.send_relay_status(client_socket)
  elif command[1] == "rauto":
   me.auto_switch(int(command[2]), int(command[3]))
  else:
   print 'Im stuck'
 except Exception as ex:
  print 'handle command failed: ' + ex.message


def startapp(master):
 global me
 global him
 if master:
  print 'I am the master'
  me = unit_me('Warsztat', '0.0.0.0', 9999)
  print 'me created'
  him = unit('Kury','192.168.1.151',9998)
  print 'him created as well'
 else:
  print 'I am her to server you'
  me = unit_me('Kury', '0.0.0.0', 9998)
  print 'me created'
 me.setPins()
 mainL = threading.Thread(target=mainLooper, args=(me,)).start()
 print 'I am after mainlooper'
 continueloop = True
 while continueloop:
  client_sock, address = me.s.accept()
  me.client_socket_list.insert(0,client_sock)
  print 'STARTAPP(): Accepted connection from {}:{}'.format(address[0], address[1])
  client_handler = threading.Thread(
   target=handle_client_connection,
   args=(client_sock, me,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
   )
  client_handler.start()



#startapp()









def i():
 GPIO.cleanup()
 exit()





#saved
