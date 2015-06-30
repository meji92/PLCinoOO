from PlcinoObject import *

InputPins = 6
OutputPins = 6
# Set the PLC with : 6 inputs, 6 outputs, 500 marks, 500 timers, 500 counters and USB was in /dev/ttyACM1
# The inputs and outputs must be the same that there are in .ino file
plc11 = plc(InputPins,OutputPins,500,500,500,"ttyACM1");

def run():
	global InputPins
	global OutputPins
	time.sleep(2) # 2 seconds because arduino uno is a little bit slow
	while True:
		s = plc11.get()
		for i in range(0,InputPins):
			plc11.setInput(i, int(s[i]))
		print "Inputs: "+str.__getslice__(s,0,InputPins)
		s = ""

		# PROGRAM //////////////////////////////////////////////////////////////////////
        ########### Blinked led example ###################
        #
        # In this example, the blinked led is in output[0] = pin 2 in arduino (0 and 1 are tx and rx)
        #
        #   m0      ___t0__
        # --| |-----|   tON|
        #           |      |
        #         1-|______|
        #
        #   t0               ___t1__
        # --| |--------------|   tON|
        #         |          |      |
        #         |        1-|______|
        #         |
        #         |           q0
        #         |----------(  )
        #
        #                     m0
        # -------------------( S )
        #
        #   t1                m0
        # --| |--------------( R )
        #
        ####################################################


		plc11.ton(plc11.contact(1,0,"m"),1,0)# Set the timer with input = value of mark 0, pt = 1, number of this timer 0
		plc11.ton(plc11.contact(1,0,"t"),1,1)# Set the timer with: input = value of timer 0, pt = 1 second, number of this timer = 1
		plc11.coil(plc11.contact(1,0,"t"),0,"q")# Set the coil with: input = value of timer 0, number of output/mark = 0, type = output
		plc11.coilSet(1,0,"m")# Set the mark 0 allwais (input is 1)
		plc11.coilReset(plc11.contact(1,1,"t"),0,"m")# Reset the mark 0 when timer1 = 1


		for i in range(0,OutputPins):
			s = s+ str(plc11.getOutput(i))
		out = "1"+s
		plc11.set(out)
		print "Outputs: "+s
		s = ""

run()

