#   example-tft144-grfx.py          V1.1
#   Brian Lavery (C) Oct 2014    brian (at) blavery (dot) com
#   Free software.

# Full demonstration of the "BLACK" 128x128 SPI TFT board connected to either:
#      1. Raspberry Pi
#      2. Virtual GPIO device running at 3.3V (eg Pro-mini 328)    (vGPIO 0.9.5 min)

# See the alternate pin assignments a few lines down.

# The LIBtft144 library automatically finds correct GPIO hardware for RPI's GPIO, or vGPIO on a PC
# It attempts virtual GPIO first, then defaults across to RPI's GPIO
# For vGPIO mode, you will need virtGPIO.py and vGPIOconstants.py on that RPI or PC

# THE DEMO:
# Filling screen with small font text.  Shows font character set.
# Show screen blanking control.
# "scrolling" demo. This chip-based function looks enticing, but not sure if it can be used usefully.
# Show "inversion" of screen (ie like a photographic colour negative).
# Text with choice of colours. String-based printing.
# Two sizes of font.
# Draw a BMP image to screen. Must be correctly scaled, and upside down!
# Graphics: rectangles, lines, circles
# "Bat and ball" animation

from LIBtft144 import TFT144
from time import sleep

# My tests. Two configurations. You could rewrite this and simply list your 4 pins.
print "GPIO platform found:", TFT144.GPIOplatform
# (The LIBtft144 module can tell us which GPIO system it found.)

if TFT144.GPIOplatform == "RPI-GPIO":                        # My BCM GPIO numbers
    RST = 18    # RST may use direct +3V strapping, and then be listed as 0 here. (Soft Reset used instead)
    CE =   0    # RPI GPIO: 0 or 1 for CE0 / CE1 number (NOT the pin#)
    DC =  22    # Labeled on board as "A0"   Command/Data select
    LED = 23    # LED may also be strapped direct to +3V, (and then LED=0 here). LED sinks 10-14 mA @ 3V

elif TFT144.GPIOplatform == "virtGPIO":                      # My Arduino "virtual GPIO" numbers
    RST =  8
    CE =  10    # VirtGPIO: the chosen Chip Select pin#. (different from rpi)
    DC =   9
    LED =  7

else:
    print "No GPIO found."
    exit()

#  Don't forget the other 2 SPI pins SCK and MOSI (SDA)

#  OK, GPIO (of one variety) is all ready. Now do the LCD demo:


TFT = TFT144(CE, DC, RST, LED, TFT144.ORIENTATION90)
# TFT = TFT144(CE, DC)     # the minimalist version

posx=0
posy=0
print "Display character set:"
for i in range (32,256):
   TFT.put_char(chr(i),posx,posy,TFT.WHITE,TFT.BLACK)
   posx+=6
   if posx>=121:
      posx=0
      posy+=8
for i in range (48,123):
   TFT.put_char(chr(i),posx,posy,TFT.BLUE,TFT.WHITE)
   posx+=6
   if posx>=121:
      posx=0
      posy+=8
sleep(2)

print "Screen blank"
TFT.led_on(False)
sleep(2)
TFT.led_on(True)
sleep(7)


print "Start Scroll"
# NOTE: scroll function looks tempting, but may not really have any useful application.
# It also seems not to acknowledge display orientation setting.
TFT.scroll_area(10,50)
for i in range (1,132):
   TFT.scroll_start(i)
   sleep(0.01)
for i in range (132,1,-1):
   TFT.scroll_start(i)
   sleep (0.01)
sleep(3)


TFT.put_string("<<< INVERSION >>>",TFT.textX(2),TFT.textY(15),TFT.YELLOW,TFT.RED)
# Note can use "character-based" cursor location instead of pixel-based (textX())
sleep(2)

print "INVERSION test"
for i in range (0,2):
   TFT.invert_screen()
   sleep (0.5)
   TFT.normal_screen()
   sleep (0.5)
sleep(3)

TFT.clear_display(TFT.BLUE)


print "Message:"
TFT.put_string("Hello,World!",21,22,TFT.WHITE,TFT.BLUE,7)
TFT.put_string("g'DAY", 25,80,TFT.RED, TFT.BLUE, 4)
sleep(3)

print "BMP image:"
# Prepare your little BMP image first. Correct size. 3 colour (ie 3bytes/pixel format). And rotate it!
# You may need to tinker to get it right.
if TFT.GPIOplatform == "RPI-GPIO":
    if TFT.draw_bmp("rpi2.bmp", 29,45):
        sleep(6)
else:
    # on non-RPI, let's not offend the Foundation
    if TFT.draw_bmp("gpio.bmp", 29,45):
        sleep(6)

TFT.draw_bmp("bl.bmp")
sleep(6)

print "Rectangle"
TFT.draw_filled_rectangle(0,0,128,64 ,TFT.RED)
TFT.draw_filled_rectangle(0,64,128,128,TFT.BLACK)
for i in range (4,32,4):
   TFT.draw_rectangle(i,i,128-i,64-i,TFT.rgb(i-1,i-1,i-1))

print "Line:"
TFT.draw_line(0,0,128,128,TFT.GREEN)
TFT.draw_line(0,128,128,0,TFT.GREEN)

print "Circles:"
TFT.draw_circle(64,64,63,TFT.BLUE)
TFT.draw_circle(64,64,53,TFT.BLUE)
TFT.draw_circle(64,64,43,TFT.BLUE)
TFT.draw_circle(64,64,33,TFT.BLUE)

print "Rectangles"
TFT.draw_filled_rectangle(0,64,128,128,TFT.BLACK)
TFT.draw_rectangle(0,64,127,127,TFT.BLUE)

print "Ball & Bat"
# bat and ball animation
ballX=64
ballY=96
ballSpeed=1
xDir=ballSpeed
yDir=ballSpeed
print "(CTRL-C to finish ...)"

while(1):
   TFT.draw_filled_rectangle(ballX,ballY,ballX+2,ballY+2,TFT.BLACK)
   TFT.draw_filled_rectangle(ballX-2,122,ballX+4,124,TFT.BLACK)
   ballX +=xDir
   ballY +=yDir
   if (ballX>121):
      xDir=-ballSpeed
   if (ballX<4):
      xDir=ballSpeed
   if (ballY>120):
      yDir=-ballSpeed
   if (ballY<66):
      yDir=ballSpeed
   TFT.draw_filled_rectangle(ballX,ballY,ballX+2,ballY+2,TFT.WHITE)
   TFT.draw_filled_rectangle(ballX-2,122,ballX+4,124,TFT.WHITE)
