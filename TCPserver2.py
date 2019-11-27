import socket
import threading
import RPi.GPIO as GPIO
import time

execfile("TCPserver_data.py")


def mainLooper(me):
 mlooper = True
 while mlooper:
  me.auto_switcher()
  time.sleep(10)




def startapp(master):
 global me
 global him
 him = []
 if master:
  print str('{:.5f} '.format(time.time())) +  'I am the master'
  me = unit_me('Warsztat', '0.0.0.0', 9999)
  print str('{:.5f} '.format(time.time())) +  'me created'
  him.insert(0, unit('Kury','192.168.1.151',9998))
  print str('{:.5f} '.format(time.time())) +  'him created as well'
 else:
  print str('{:.5f} '.format(time.time())) +  'I am her to server you'
  me = unit_me('Kury', '0.0.0.0', 9998)
  him.insert(0, unit('Warsztat','192.168.1.150',9999))
  print str('{:.5f} '.format(time.time())) +  'me created'
# me.setPins()
# mainL = threading.Thread(target=mainLooper, args=(me,)).start()
 continueloop = True
 while continueloop:
  client_sock, address = me.s.accept()
  me.client_socket_list.insert(0,client_sock)
  print str('{:.5f} '.format(time.time())) +  'STARTAPP(): Accepted connection from {}:{}'.format(address[0], address[1])
  client_handler = threading.Thread(
   target=me.handle_client_connection,
   args=(client_sock, )  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
   )
  client_handler.start()








def i():
 GPIO.cleanup()
 exit()




