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
   client_socket.close()
  dataFromClient = request.decode()
  dataFromClient = dataFromClient.strip()
  print dataFromClient
  command = dataFromClient.split(" ")
  if command[0] == me.unit_name:
   handle_command(client_socket, command, me)
  elif command[0] == "ping":
   client_socket.send("pong")
  elif command[0] == "break":
   continueloop = False
   print "Connection breaked"
   client_socket.close()
  else:
   print 'forwarded: ' + dataFromClient


  
def handle_command(client_socket, command, me):
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
 

def startapp():
 me = unit_me('Warsztat', '0.0.0.0', 9999)
 him = unit('Kury','192.168.1.151',9999)
 #server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 #server.bind((bind_ip, bind_port))
 #server.listen(15)  # max backlog of connections
 #print 'Listening on {}:{}'.format(bind_ip, bind_port)
 me.setPins()
 threading.Thread(target=mainLooper, args=(me,)).start()
 him.keep_alive()
 continueloop = True
 while continueloop:
  client_sock, address = me.s.accept()
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






