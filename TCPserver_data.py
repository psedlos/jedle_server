
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
   self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
    self.s.connect((self.unit_ip, self.unit_port))
    self.connected = True
    self.s.send(self.unit_name + " st")
   except Exception as ex:
    print str('{:.5f} '.format(time.time())) + 'Un: Failed to connect to ' + self.unit_name + ' :: ' + ex.message
    self.s.close()
    self.connected = False
    time.sleep(15)
   else:
    print str('{:.5f} '.format(time.time())) + 'Un: init ST request sent to ' + self.unit_name
    self.continue_loop = True
    while self.continue_loop:
     try:
      self.data = self.s.recv(self.buffor_size)
     except Exception as ex:
      print str('{:.5f} '.format(time.time())) + 'Un: Failed to recv from ' + self.unit_name + ' // '+ ex.message
      self.continue_loop = False
     else:
      print str('{:.5f} '.format(time.time())) + 'Un: From ' + self.unit_name + ' recieved: ' + self.data
      if self.data is not None and len(self.data)>0:
       self.handle_command(self.data)
      else:
       self.continue_loop = False
       print str('{:.5f} '.format(time.time())) + 'Un: connection to ' + str(self.s.getsockname()) + ' (' + self.unit_name + ') terminated.'
 def handle_command(self, data):
  command = data.split(" ")
  try:
   if command[0] == self.unit_name:
    if command[1] == "relay_status":
     #here will come self update but it is hard to do it adhoc
     for i in me.client_socket_list:
      if i.getpeername()[0] != self.s.getpeername()[0]:
       try:
        i.send(data)
        print str('{:.5f} '.format(time.time())) + 'Un: ' + data + ' forwarded back to ' + str(i.getpeername())
       except Exception as ex:
        print str('{:.5f} '.format(time.time())) + 'Un: failed to forward response from ' + self.unit_name + ' with Ex: ' + ex.message
        me.client_socket_list.remove(i)
   else:
    print str('{:.5f} '.format(time.time())) + 'Un: Handle_command ' + self.unit_name + ' has receive unexpected: ' + data
  except Exception as ex:
   print str('{:.5f} '.format(time.time())) + 'Un: Handle_command ' + self.unit_name + ' has faild and riased: ' + ex.message
   print str('{:.5f} '.format(time.time())) + 'Un: ' + command
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
  self.PRPsupp = 4
  self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  self.s.bind(('0.0.0.0', unit_port)) 
  self.s.listen(15)
  self.client_socket_list = []
  print str('{:.5f} '.format(time.time())) + 'Me: Listening on {}:{}'.format(self.unit_ip, self.unit_port)
  self.setPins()
  self.mainL = threading.Thread(target=self.mainLooper, args=()).start()
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
#  print(str(messagebyte))
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
  self.key = 0
  for i in self.relay_pins:
   nval = val%2
   val = val // 2
   self.vr[self.key] = (bool(nval))
   GPIO.output(i, bool(nval))
   self.key = self.key +1
 def auto_switcher(self):
  self.light=self.readPR()
  print str('{:.5f} '.format(time.time())) + "AS: " + str(self.light)
  for i in range(8):
   if self.vrauto[i]:
    if self.light>4000:
     self.relay_switch(i,1, force = True)
    else:
     self.relay_switch(i,0, force = True)
 def readPR(self):
  self.reading=0
  GPIO.setup(self.PRPsupp, GPIO.OUT)
  GPIO.output(self.PRPsupp, GPIO.HIGH)
  GPIO.setup(self.PRP, GPIO.OUT)
  GPIO.output(self.PRP, GPIO.LOW)
  time.sleep(0.1)
  GPIO.setup(self.PRP, GPIO.IN)
  while (GPIO.input(self.PRP) == GPIO.LOW) and self.reading<20000:
   self.reading += 1
  return self.reading
 def handle_client_connection(self, client_socket):
  self.continueloop = True
  while self.continueloop:
   try:
    self.request = client_socket.recv(1024)
   except:
    client_socket.send('server killed client')
    print str('{:.5f} '.format(time.time())) + 'Me: client died'
    self.client_socket_list.remove(client_socket)
    client_socket.close()
 #  time.sleep(15)
   if self.request is not None and len(self.request)>0:
    self.dataFromClient = self.request.decode()
    self.dataFromClient = self.dataFromClient.strip()
    print str('{:.5f} '.format(time.time())) + 'Me: ' + self.dataFromClient
    self.command = self.dataFromClient.split(" ")
#    print str('{:.5f} '.format(time.time())) + self.command[0]
    if self.command[0] == self.unit_name:
     self.handle_command(client_socket, self.command)
    elif self.command[0] == "ping":
     client_socket.send("pong")
     print str('{:.5f} '.format(time.time())) + 'Me: pong send'
    elif self.command[0] == "break":
     self.continueloop = False
     print str('{:.5f} '.format(time.time())) + "Me: Connection breaked"
     client_socket.close()
    else:
     for i in him:
      if self.command[0] == i.unit_name: ###<<<---
       try:
        i.s.send(self.dataFromClient)###<<<---
        print str('{:.5f} '.format(time.time())) + 'Me: forwarded to '+ i.unit_name +': ' + self.dataFromClient
       except Exception as ex:
        print str('{:.5f} '.format(time.time())) + 'Me: Can not forward - '+ i.unit_name +' // ' + ex.message
   else:
    self.client_socket_list.remove(client_socket)
    client_socket.close()
    self.continueloop = False
    print str('{:.5f} '.format(time.time())) + 'Me: connection terminated'
 def handle_command(self, client_socket, command):
  try:
   if command[1] == "r1":
    self.relay_switch(int(command[2]),int(command[3]))
    self.send_relay_status(client_socket)
   elif command[1] == "rs":
    self.relays_switch(int(command[2]))
    self.send_relay_status(client_socket)
   elif command[1] == "st":
    self.send_relay_status(client_socket)
   elif command[1] == "rauto":
    self.auto_switch(int(command[2]), int(command[3]))
   else:
    print str('{:.5f} '.format(time.time())) + 'Me: Im stuck'
  except Exception as ex:
   print str('{:.5f} '.format(time.time())) + 'Me: handle command failed: ' + ex.message
 def mainLooper(self):
  self.mlooper = True
  while self.mlooper:
   self.auto_switcher()
   time.sleep(10)















