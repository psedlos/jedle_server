



#bind_ip = '0.0.0.0'
#bind_port = 9999

#vr = [True, True, True, True, True, True, True, True] #vr (virtual relay) initial list to hold relays states which can be altered directly to GPIOs or indirect what would required additional function to manipulate GPIOs
#vrauto = [False, False, False, False, False, False, False, False]
#relay_pins = [17, 27, 22, 5, 6, 13, 19, 26, 17] #provide desired pins number for your installation, please see GPIO pins numbers for your version of RPI

#PRP = 24
#unit_name = "Warsztat"
#units = [["Warsztat", "192.168.1.150", 9999],["Kury", "192.168.1.151", 9999],["Front","192.168.1.152", 9999]]

class unit:
 def __init__(self, unit_name, unit_ip, unit_port):
  self.unit_name = unit_name
  self.unit_ip = unit_ip
  self.unit_port = unit_port
  self.buffor_size = 1024
  self.vr = [True, True, True, True, True, True, True, True]
  self.vrauto = [False, False, False, False, False, False, False, False]
  self.connected = False
  self.try_to_connect_again = True
  self.continue_loop = True
  self.demon = threading.Thread(target = self.unit_demonized, args = ()).start()
 def unit_demonized(self):
  while self.try_to_connect_again:#I assumed that it will be some separated thread.....
   try:
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((self.unit_ip, self.unit_port))
    self.connected = True
    self.s.send(self.unit_name + " st")
    print 'ST request sent to ' + self.unit_name
    while self.continue_loop:
     self.data = self.s.recv(self.buffor_size)
     print 'From ' + self.unit_name + ' recieved: ' + self.data
     #self.data = self.data.strip()
     self.handle_command(self.data)
   except Exception as ex:
    print 'exception has been raised and him.s.closed() ::' + ex.message
    self.s.close()
    self.connected = False
    time.sleep(15)
 def handle_command(self, data):
  command = data.split(" ")
  print command[0] + '  ' + self.unit_name
  try:
   if command[0] == self.unit_name:
    print command[1] + '  ' + "relay_status"
    if command[1] == "relay_status":
     #here will come self update but it is hard to do it adhoc
     print len(me.client_socket_list)
     for i in me.client_socket_list:
      try:
       print i.getsockname()
       i.send(data)
       print data + ' forwarded back'
      except Exception as ex:
       print 'failed to forward response from ' + self.unit_name + ' with Ex: ' + ex
       me.client_socket_list.remove(i)
   else:
    print self.unit_name + ' send some forwarded message. Is there more then one master?'
  except Exception as ex:
   print 'Handle_command for unit ' + self.unit_name + ' has faild and riased: ' + ex
   print command
 def relay_switch(self, num, nval, force = False):
  if not self.vrauto[num] or force :
   self.vr[num]=bool(nval)
 def auto_switch(self, num, nval):
  self.vrauto[num]=bool(nval)






class unit_me:
 def __init__(self, unit_name, unit_ip, unit_port):
  self.unit_name = unit_name
  self.unit_ip = unit_ip
  self.unit_port = unit_port
  self.buffor_size = 1024
  self.vr = [True, True, True, True, True, True, True, True]
  self.vrauto = [False, False, False, False, False, False, False, False]
  self.relay_pins = [21, 20, 16, 12, 25, 24, 23, 18]
  self.PRP = 17
  self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  self.s.bind((unit_ip, unit_port)) 
  self.s.listen(15)
  self.client_socket_list = []
  print 'Listening on {}:{}'.format(self.unit_ip, self.unit_port)
  #s.close()
 def relay_switch(self, num, nval, force = False):
  if not self.vrauto[num] or force :
   self.vr[num]=bool(nval)
   GPIO.output(self.relay_pins[num],bool(nval))
 def auto_switch(self, num, nval):
  self.vrauto[num]=bool(nval)
 def relay_status(self):
  message = self.unit_name + " relay_status"
  for i in self.vr:
   message = message + " " + str(int(i))
  message = message + " auto"
  for i in self.vrauto:
   message = message + " " + str(int(i))
  message = message + "\n"
  messagebyte = message.encode()
  print(str(messagebyte))
  return messagebyte
 def send_relay_status(self, client_socket):
  rel_stat = self.relay_status()
  try:
   client_socket.send(rel_stat)
  except:
   client_socket.close()
 def setPins(self):
  GPIO.setmode(GPIO.BCM)
  for i in self.relay_pins:
   GPIO.setup(i, GPIO.OUT)
  self.relays_switch(0)
 def relays_switch(self, val):
  key = 0
  for i in self.relay_pins:
   nval = val%2
   val = val // 2
   self.vr[key] = (bool(nval))
   GPIO.output(i, bool(nval))
   key = key +1
 def auto_switcher(self):
  light=self.readPR()
  for i in range(8):
   if self.vrauto[i]:
    if light>4000:
     self.relay_switch(i,1, force = True)
    else:
     self.relay_switch(i,0, force = True)
 def readPR(self):
  reading=0
  GPIO.setup(self.PRP, GPIO.OUT)
  GPIO.output(self.PRP, GPIO.LOW)
  time.sleep(0.1)
  GPIO.setup(self.PRP, GPIO.IN)
  while (GPIO.input(self.PRP) == GPIO.LOW) or reading<20000:
   reading += 1
  return reading













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
