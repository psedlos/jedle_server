


#function to set all switches at once
def relays_switchsadsadsad(val):
 nval = val%2
 val = val // 2
 vr[0] = (bool(nval)) #
 GPIO.output(17,bool(nval))
 nval = val%2
 val = val // 2
 vr[1] = (bool(nval)) #
 GPIO.output(27,bool(nval))
 nval = val%2
 val = val // 2
 vr[2] = (bool(nval)) #
 GPIO.output(22,bool(nval))
 nval = val%2
 val = val // 2
 vr[3] = (bool(nval)) #
 GPIO.output(5,bool(nval))
 nval = val%2
 val = val // 2
 vr[4] = (bool(nval)) #
 GPIO.output(6,bool(nval))
 nval = val%2
 val = val // 2
 vr[5] = (bool(nval)) #
 GPIO.output(13,bool(nval))
 nval = val%2
 val = val // 2
 vr[6] = (bool(nval)) # 
 GPIO.output(19,bool(nval))
 nval = val%2
 val = val // 2
 vr[7] = (bool(nval)) # 
 GPIO.output(26,bool(nval))

#function to set only one switch at once
def relay_switch(num, nval):
 if num == 0:
  vr[0] = bool(nval) #
  GPIO.output(17,bool(nval))
 elif num == 1:
  vr[1] = bool(nval) #
  GPIO.output(27,bool(nval))
 elif num == 2:
  vr[2] = bool(nval) #
  GPIO.output(22,bool(nval))
 elif num == 3:
  vr[3] = bool(nval) #
  GPIO.output(5,bool(nval))
 elif num == 4:
  vr[4] = bool(nval) #
  GPIO.output(6,bool(nval))
 elif num == 5:
  vr[5] = bool(nval) #
  GPIO.output(13,bool(nval))
 elif num == 6:
  vr[6] = bool(nval) #
  GPIO.output(19,bool(nval))
 elif num == 7:
  vr[7] = bool(nval) #
  GPIO.output(26,bool(nval))
 else :
  print(num + " is out of range") #
  GPIO.output(17,bool(nval))


def printPR(pin):
 loops = 0
 GPIO.setup(pin, GPIO.IN)
 old_val = GPIO.input(pin)
 while (loops < 1000):
  reading = 0
  current_val = GPIO.input(pin)
  while (old_val == current_val):
   reading += 1
   current_val = GPIO.input(pin)
  print loops, current_val, reading
  old_val = current_val 
  loops += 1

def printreadPR(pin):
 loops = 0
 while (loops <100):
  print loops, readPR(pin)
  loops +=1
  
def readPR(Rpin):
 reading=0
 GPIO.setup(Rpin, GPIO.OUT)
 GPIO.output(Rpin, GPIO.LOW)
 time.sleep(0.1)
 GPIO.setup(Rpin, GPIO.IN)
 while (GPIO.input(Rpin) == GPIO.LOW) or reading<20000:
  reading += 1
 return reading  
 
 
 
def setPins4Relay():
 GPIO.setmode(GPIO.BCM)
 for i in relay_pins:
  GPIO.setup(i, GPIO.OUT)
 relays_switch2(0)

def relays_switch(val):
 key = 0
 for i in relay_pins:
  nval = val%2
  val = val // 2
  vr[key] = (bool(nval))
  GPIO.output(i, bool(nval))
  key = key +1
  
def relay_switch2(num, nval, force = False):
 if not vrauto[num] or force :
  vr[num]=bool(nval)
  GPIO.output(relay_pins[num],bool(nval))


def auto_switch(num, nval):
 vrauto[num]=bool(nval)
  








class unit_OLD:
 def __init__(self, unit_name, unit_ip, unit_port):
  self.unit_name = unit_name
  self.unit_ip = unit_ip
  self.unit_port = unit_port
  self.buffor_size = 1024
#  self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  self.connected = False
  self.try_to_connect_again = True
  while self.try_to_connect_again:
   try:
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((self.unit_ip, self.unit_port))
    self.s.send("ping")
    print 'ping sent'
    self.data = self.s.recv(self.buffor_size)
    print 'recieved ' + self.data
    if self.data == "pong":
     print 'pong and proceeded'
     self.connected = True
     keep_alive_thread = threading.Thread(target=self.keep_alive, args=()).start()
     self.try_to_connect_again = False
   except Exception as ex:
    print 'exception has been raised and him.s.closed() ::' + ex.message
    self.s.close()
    time.sleep(15)
 def keep_alive(self):
  print 'keep_alive started'
  while self.connected:
   try:
    self.s.send('ping')
    print 'keep_alive ping sent'
   except Exception as ex:
    self.s.close()
    print 'keep_alive 1st try: ' + ex.message
    #continueloop = False
   try:
    self.data = self.s.recv(self.buffor_size)
    print 'keep_alive received: ' + self.data
   except Exception as ex:
    print 'keep_alive 1st try: ' + ex.message
    self.s.close()  
    #continueloop = False
   if self.data == "pong":
    self.connected = True
   time.sleep(10)
   print 'keep_alive loop complete'
  
  #  s.close()  





#bind_ip = '0.0.0.0'
#bind_port = 9999

#vr = [True, True, True, True, True, True, True, True] #vr (virtual relay) initial list to hold relays states which can be altered directly to GPIOs or indirect what would required additional function to manipulate GPIOs
#vrauto = [False, False, False, False, False, False, False, False]
#relay_pins = [17, 27, 22, 5, 6, 13, 19, 26, 17] #provide desired pins number for your installation, please see GPIO pins numbers for your version of RPI

#PRP = 24
#unit_name = "Warsztat"
#units = [["Warsztat", "192.168.1.150", 9999],["Kury", "192.168.1.151", 9999],["Front","192.168.1.152", 9999]]




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

