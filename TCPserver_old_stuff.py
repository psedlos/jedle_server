


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
  





