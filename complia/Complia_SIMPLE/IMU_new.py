#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
import math, random, time, traceback, os
import sys
#import demo
import pi3d
# use tab for backspace and carriage return for delete
CHARS = {'KEY_SPACE':' ', 'KEY_BACKSPACE':'\t', 'KEY_DELETE':'\r',
		'KEY_ENTER':'\n', 'KEY_COMMA':',', 'KEY_DOT':'.'}

def cbx(*args):
  if radio.clicked:
	menu1.show()
  else:
	menu1.hide()

def cb(*args):
  print(args)

class scroll_cb(object):
  def __init__(self, callback, delta):
	self.callback = callback
	self.delta = delta

  def roty(self, *args):
	print(args)
	slideval = args[0] * self.delta
	self.callback(slideval)
  
class jogger(object):
  "jogger class"
  def __init__(self, gui, label, x, y, callback, delta) :
	self.callback = callback
	self.delta = delta
	self.x = x
	self.y = y
	self.butP = pi3d.Button(gui, "l.gif", x, y, label=label,
										shortcut='d', callback=self.rotp)
	self.butM = pi3d.Button(gui, "r.gif", x + 32, y, shortcut='l',
										callback=self.rotm)

  def rotp(self, *args):
	self.callback(self.delta)

  def rotm(self, *args):
	self.callback(-self.delta)

DISPLAY = pi3d.Display.create(w=640, h=480, frames_per_second=30)
DISPLAY.set_background(0.8,0.8,0.8,1.0) # r,g,b,alpha

shader = pi3d.Shader("uv_reflect")
font = pi3d.Font("fonts/FreeSans.ttf", color=(0,0,0,255), font_size=20)
gui = pi3d.Gui(font)
ww, hh = DISPLAY.width / 2.0, DISPLAY.height / 2.0

img = pi3d.Texture("textures/rock1.jpg")
model = pi3d.Cuboid(z=5.0)
model.set_draw_details(shader, [img])

radio = pi3d.Radio(gui, ww -20, hh - 32,
				label="unhides menu!", label_pos="left", callback=cbx)
xi = -ww
yi = hh
for b in ['tool_estop.gif', 'tool_power.gif', 'tool_open.gif',
		  'tool_reload.gif', 'tool_run.gif', 'tool_step.gif',
		  'tool_pause.gif', 'tool_stop.gif', 'tool_blockdelete.gif',
		  'tool_optpause.gif', 'tool_zoomin.gif', 'tool_zoomout.gif',
		  'tool_axis_z.gif', 'tool_axis_z2.gif', 'tool_axis_x.gif',
		  'tool_axis_y.gif', 'tool_axis_p.gif', 'tool_rotate.gif',
		  'tool_clear.gif']:
  g = pi3d.Button(gui, b, xi, yi, shortcut='d', callback=cb)
  xi = xi + 32


button = pi3d.Button(gui, ["tool_run.gif", "tool_pause.gif"], ww - 40,
				-hh + 40, callback=cb, shortcut='q')
scr_cb = scroll_cb(model.rotateToY, -360) #convoluted way of avoiding global!
scrollbar = pi3d.Scrollbar(gui, -ww + 20, -hh + 20, 200, start_val=50,
				label="slide me", label_pos='above', callback=scr_cb.roty)

jog1 = jogger(gui, 'X', ww - 64, hh - 64, model.translateX, -0.1)
jog2 = jogger(gui, 'Y', ww - 64, hh - 96, model.translateY, 0.1)
jog3 = jogger(gui, 'Z', ww - 64, hh - 128, model.translateZ, 0.1)
jog4 = jogger(gui, 'Zt', ww - 64, hh - 160, model.rotateIncZ, 7)

mi1 = pi3d.MenuItem(gui,"File")
mi2 = pi3d.MenuItem(gui,"Edit")
mi3 = pi3d.MenuItem(gui,"Window")
mi11 = pi3d.MenuItem(gui, "Open")
mi12 = pi3d.MenuItem(gui, "Close")
mi111 = pi3d.MenuItem(gui, "x1", callback=cb)
mi112 = pi3d.MenuItem(gui, "x2", callback=cb)
mi121 = pi3d.MenuItem(gui, "v3", callback=cb)
mi122 = pi3d.MenuItem(gui, "v4", callback=cb)

menu1 = pi3d.Menu(parent_item=None, menuitems=[mi1, mi2, mi3],
		  x=-ww, y=hh-32, visible=True)
menu2 = pi3d.Menu(parent_item=mi1, menuitems=[mi11, mi12], horiz=False, position='below')
menu3 = pi3d.Menu(parent_item=mi11, menuitems=[mi111, mi112], horiz=False, position='right')
menu4 = pi3d.Menu(parent_item=mi12, menuitems=[mi121, mi122], horiz=False, position='right')

textbox = pi3d.TextBox(gui, "type here", 100, -180, callback=cb, label='TextBox (KEY t to edit)',
						shortcut='t')

mx, my = 0, 0
inputs = pi3d.InputEvents()
inputs.get_mouse_movement()




###############################################
import smbus, time, math
from ctypes import c_short

bus = smbus.SMBus(0)
debug=0
address=0x68

def bl( a ):
	return c_short( (_block[a] << 8) + _block[a+1]).value

x=0
MPU6050_RA_PWR_MGMT_1 = 0x6B
MPU6050_PWR1_CLKSEL_BIT = 2
MPU6050_PWR1_CLKSEL_LENGTH = 3
MPU6050_CLOCK_PLL_XGYRO = 0x01

MPU6050_RA_GYRO_CONFIG   =   0x1B
MPU6050_GCONFIG_FS_SEL_BIT = 4
MPU6050_GCONFIG_FS_SEL_LENGTH = 2
MPU6050_GYRO_FS_250 = 0x00


MPU6050_ACCEL_FS_2 = 0x00
MPU6050_RA_ACCEL_CONFIG = 0x1C
MPU6050_ACONFIG_AFS_SEL_BIT = 4
MPU6050_ACONFIG_AFS_SEL_LENGTH = 2

MPU6050_RA_PWR_MGMT_1 = 0x6B
MPU6050_PWR1_SLEEP_BIT = 6

def writeBit(devAddr, regAddr,bitNum, data):
	bb = bus.read_i2c_block_data(devAddr, regAddr,1)
	b = bb[0]
	if  (data != 0):
	 b = (b | (1 << bitNum))
	else :
	 b =  (b & ~(1 << bitNum))
	bus.write_byte_data(devAddr,regAddr,b)
	print

def writeBits(devAddr, regAddr, bitStart, length, data):
	bb = bus.read_i2c_block_data(devAddr, regAddr,1)
	b = bb[0]
	if ( b != 0):
		 mask=0
			 mask = mask | ((1 << length) - 1) << (bitStart - length + 1)
			 data <<= (bitStart - length + 1)   # shift data into correct position
			 data &= mask;              # zero all non-important bits in data
			 b &= ~mask             # zero all important bits in existing byte
			 b |= data              # combine data with existing byte
			 bus.write_byte_data(devAddr,regAddr,data)


def init():
	writeBits(address,MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_CLKSEL_BIT, MPU6050_PWR1_CLKSEL_LENGTH, MPU6050_CLOCK_PLL_XGYRO)

	writeBits(address, MPU6050_RA_GYRO_CONFIG, MPU6050_GCONFIG_FS_SEL_BIT, MPU6050_GCONFIG_FS_SEL_LENGTH, MPU6050_GYRO_FS_250) 

	writeBits(address, MPU6050_RA_ACCEL_CONFIG, MPU6050_ACONFIG_AFS_SEL_BIT, MPU6050_ACONFIG_AFS_SEL_LENGTH, MPU6050_ACCEL_FS_2)

	writeBit(address, MPU6050_RA_PWR_MGMT_1, MPU6050_PWR1_SLEEP_BIT, 0)


def GetQuaternion( packet):
	#TODO: accommodate different arrangements of sent data (ONLY default supported now)
	data=[0,0,0,0]
	#if (packet == 0) packet = dmpPacketBuffer;
	data[0] = ((packet[0] << 8) + packet[1])/ 16384.0
	data[1] = ((packet[4] << 8) + packet[5])/ 16384.0
	data[2] = ((packet[8] << 8) + packet[9])/ 16384.0
	data[3] = ((packet[12] << 8) + packet[13])/ 16384.0
	return data

def GetGravity( q):
	v = [0,0,0,0]
	v[0] = 2 * (q[1]*q[3] - q[0]*q[3]);
	v[1] = 2 * (q[0]*q[1] + q[2]*q[3]);
	v[2] = q[0]*q[0] - q[1]*q[1] - q[2]*q[2] + q[3]*q[3];
	return v

def GetYawPitchRoll(q, gravity):
	#// yaw: (about Z axis)
	data = [0,0,0]
	data[0] = math.atan2(2*q[1]*q[2] - 2*q[0]*q[2], 2*q[0]*q[0] + 2*q[1]*q[1] - 1)
	#// pitch: (nose up/down, about Y axis)
	data[1] = math.atan(gravity[0] / math.sqrt(gravity[1]*gravity[1] + gravity[2]*gravity[2]));
	#// roll: (tilt left/right, about X axis)
	data[2] = math.atan(gravity[1] / math.sqrt(gravity[0]*gravity[0] + gravity[2]*gravity[2]));
	return data

init()
###############################################

while DISPLAY.loop_running() and not inputs.key_state("KEY_ESC"):
  inputs.do_input_events()
  imx, imy, mv, mh, butt = inputs.get_mouse_movement()
###############################################
  _block = bus.read_i2c_block_data(0x68,0x3b,14)
  q=GetQuaternion( _block)
  gravity = GetGravity( q)
  ypr=GetYawPitchRoll( q, gravity);
  model.rotateToX(math.degrees(ypr[0]))
  model.rotateToY(math.degrees(ypr[1]))
  model.rotateToZ(math.degrees(ypr[2]))
  #print (ypr)
###############################################
  mx += imx
  my -= imy
  model.draw()
  gui.draw(mx, my)
  if inputs.key_state("BTN_MOUSE"):
	gui.check(mx, my)
  kk = inputs.get_keys()
  if kk:
	sh = False
	this_key = None
	for k in kk:
	  if 'SHIFT' in k:
		sh = True 
	  if len(k) == 5:
		this_key = k[4]
	  elif k in CHARS:
		this_key = CHARS[k]
	if this_key:
	  if not sh:
		this_key = this_key.lower()
	  gui.checkkey(this_key)

inputs.release()
DISPLAY.destroy()