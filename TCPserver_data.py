


 
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
  self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  self.connected = False
  try:
   self.s.connect((self.unit_ip, self.unit_port))
   self.s.send("ping")
   self.data = self.s.recv(buffor_size)
   if data == "pong":
    self.connected = True
  except:
   self.s.close()
 def keep_alive(self):
  while self.connected:
   try:
    self.s.send('ping')
   except:
    self.s.close()
    continueloop = False
   try:
    data = self.s.recv(self.buffer)
   except:
    self.s.close()  
    continueloop = False
   if data == "pong":
    self.connected = True
  
  
  #  #s.close()  


class unit_me:
 def __init__(self, unit_name, unit_ip, unit_port):
  self.unit_name = unit_name
  self.unit_ip = unit_ip
  self.unit_port = unit_port
  self.buffor_size = 1024
  self.vr = [True, True, True, True, True, True, True, True]
  self.vrauto = [False, False, False, False, False, False, False, False]
  self.relay_pins = [17, 27, 22, 5, 6, 13, 19, 26]
  self.PRP = 24
  self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  self.s.bind((unit_ip, unit_port)) 
  self.s.listen(15)
  print 'Listening on {}:{}'.format(self.unit_ip, self.unit_port)
  #s.close()
 def relay_switch(self, num, nval, force = False):
  if not self.vrauto[num] or force :
   self.vr[num]=bool(nval)
   GPIO.output(self.relay_pins[num],bool(nval))
 def auto_switch(self, num, nval):
  self.vrauto[num]=bool(nval)
 def relay_status(self):
  message = "Warsztat relay_status"
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


