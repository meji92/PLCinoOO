import time
import serial

class plc:
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    InputPins = 0
    OutputPins = 0
    #The array with the inputs. From 0 to nInputs-1
    inputs = []
    #Auxiliary array with the previous scan inputs
    inputsPrev = []
    #The array with the outputs
    outputs = []
    #Auxiliary array with previous outputs
    outputsPrev = []
    #The array with the marks values
    marks = []
    #Aux array that contain the last mark values
    marksPrev = []
    #Array with the timers values
    timers = []
    #Array with the target time of the timer
    timerAux = []
    #Aux array that contain the last timers values
    timersPrev = []
    #Array with the counters values
    counts = []
    #Aux arrays for the counters
    countAux = []
    countPrevCU = []
    countPrevCD = []
    countPrevR = []
    countsPrev = []
    # Aux var to read and write
    s = ""

    ############################# SET FUNCTIONS ###################################
    # Set the number of inputs, outputs, marks, timers and counters
    # INPUTS AND OUTPUTS MUST BE SET IN .INO FILE WITH THE SAME VALUES
    def __init__(self,nInputs,nOutputs,nMarks,nTimers,nCounts,serialnumber):
        self.InputPins = nInputs
        self.OutputPins = nOutputs
        self.ser = serial.Serial('/dev/'+serialnumber, 9600)
        #self.ser = serial.Serial(serialnumber, 9600)

        for i in range(0,nInputs):
            self.inputs.append(0)
            self.inputsPrev.append(0)

        for i in range(0,nOutputs):
            self.outputs.append(0)

        for i in range(0,nMarks):
            self.marks.append(0)
            self.marksPrev.append(0)

        for i in range(0,nTimers):
            self.timers.append(0)
            self.timerAux.append(0)
            self.timersPrev.append(0)

        for i in range(0,nCounts):
            self.counts.append(0)
            self.countAux.append(0)
            self.countPrevCU.append(0)
            self.countPrevCD.append(0)
            self.countPrevR.append(0)
            self.countsPrev.append(0)

    # Add a new mark and return the position in the array of marks
    def addMark (self):
        self.marks.append(0)
        self.marksPrev.append(0)
        return self.marks.__len__()-1

    # Add a new timer and return the position in the array of timers
    def addTimer(self):
        self.timers.append(0)
        self.timerAux.append(0)
        return self.timers.__len__()-1

    # Add a new counter and return the position in the array of counters
    def addCount(self):
        self.counts.append(0)
        self.countAux.append(0)
        self.countPrevCU.append(0)
        self.countPrevCD.append(0)
        self.countPrevR.append(0)
        return self.counts.__len__()-1

    def getPLC(self):
        return self.OutputPins,self.InputPins

    def getOutput(self,index):
        return self.outputs[index]

    def getMarks(self):
        s = ""
        for item in self.marks:
            s = s+ str(item)
        return s

    def getTimers(self):
        s = ""
        for item in self.timers:
            s = s+ str(item)
        return s

    def getCounters(self):
        s = ""
        for item in self.counts:
            s = s+ str(item)
        return s

    def setInput(self, index, value):
        self.inputs[index]= value

    #Set the inputs like the given in newInputs with this structure: ;0,1;2,0;3,1; where ;Number of input, value; Number of input, value; ......
    def setInputs(self,newInputs):
        while (newInputs.__len__()>1):
            aux = newInputs[0:newInputs.find(';')]
            newInputs = newInputs [newInputs.find(';')+1:newInputs.__len__()]
            aux2 = newInputs[0:newInputs.find(';')]
            newInputs = newInputs [newInputs.find(';')+1:newInputs.__len__()]
            if (int(aux)<=self.inputs.__len__()):
                self.inputs[int(aux)]=int(aux2)

    ############################# CONTACTS ###################################
    # Contact. imtcq sets the tipe of var value: i(input), m(mark), t(timer), c(counter), q(input)
    def contact(self, input, var, imtcq):
        if (imtcq == "i")|(imtcq == "I"):
            if (self.inputs[var] == 1):
                return input
            else:
                return 0

        if (imtcq == "m")|(imtcq == "M"):
            if (self.marks[var] == 1):
                return input
            else:
                return 0

        if (imtcq == "t")|(imtcq == "T"):
            if (self.timers[var] == 1):
                return input
            else:
                return 0

        if (imtcq == "c")|(imtcq == "C"):
            if self.counts[var] == 1:
                return input
            else:
                return 0

        if (imtcq == "q")|(imtcq == "Q"):
            if self.counts[var] == 1:
                return self.outputs[var]
            else:
                return 0

    def contactNot(self, input, var, imtcq):
        if (imtcq == "i")|(imtcq == "I"):
            if (self.inputs[var] == 0):
                return input
            else:
                return 0

        if (imtcq == "m")|(imtcq == "M"):
            if (self.marks[var] == 0):
                return input
            else:
                return 0

        if (imtcq == "t")|(imtcq == "T"):
            if (self.timers[var] == 0):
                return input
            else:
                return 0

        if (imtcq == "c")|(imtcq == "C"):
            if (self.counts[var] == 0):
                return input
            else:
                return 0

        if (imtcq == "q")|(imtcq == "Q"):
            if self.counts[var] == 0:
                return input
            else:
                return 0

    #Return 1 with a positive flank, 0 in other case.
    def contactPos(self, input, var, imtcq):
        if (imtcq == "i")|(imtcq == "I"):
            if (self.inputs[var] == 1)&(self.inputsPrev[var] == 0):
                self.inputsPrev[var] = self.inputs[var]
                return input
            else:
                self.inputsPrev[var] = self.inputs[var]
                return 0

        if (imtcq == "m")|(imtcq == "M"):
            if (self.marks[var] == 1)&(self.marksPrev[var] == 0):
                self.marksPrev[var] = self.marks[var]
                return input
            else:
                self.marksPrev[var] = self.marks[var]
                return 0

        if (imtcq == "t")|(imtcq == "T"):
            if (self.timers[var] == 1)&(self.timersPrev[var] == 0):
                self.timersPrev[var] = self.timers[var]
                return input
            else:
                self.timersPrev[var] = self.timers[var]
                return 0

        if (imtcq == "c")|(imtcq == "C"):
            if (self.counts[var] == 1)&(self.countsPrev[var] == 0):
                self.countsPrev[var] = self.counts[var]
                return input
            else:
                self.countsPrev[var] = self.counts[var]
                return 0

        if (imtcq == "q")|(imtcq == "Q"):
            if (self.inputs[var] == 1)&(self.inputsPrev[var] == 0):
                self.inputsPrev[var] = self.inputs[var]
                return input
            else:
                self.inputsPrev[var] = self.inputs[var]
                return 0

    #Return 1 with a negative flank, 0 in other case
    def contactNeg(self, input, var, imtcq):
        if (imtcq == "i")|(imtcq == "I"):
            if (self.inputs[var] == 0)&(self.inputsPrev[var] == 1):
                self.inputsPrev[var] = self.inputs[var]
                return input
            else:
                self.inputsPrev[var] = self.inputs[var]
                return 0

        if (imtcq == "m")|(imtcq == "M"):
            if (self.marks[var] == 0)&(self.marksPrev[var] == 1):
                self.marksPrev[var] = self.marks[var]
                return input
            else:
                self.marksPrev[var] = self.marks[var]
                return 0

        if (imtcq == "t")|(imtcq == "T"):
            if (self.timers[var] == 0)&(self.timersPrev[var] == 1):
                self.timersPrev[var] = self.timers[var]
                return input
            else:
                self.timersPrev[var] = self.timers[var]
                return 0

        if (imtcq == "c")|(imtcq == "C"):
            if (self.counts[var] == 0)&(self.countsPrev[var] == 1):
                self.countsPrev[var] = self.counts[var]
                return input
            else:
                self.countsPrev[var] = self.counts[var]
                return 0

        if (imtcq == "q")|(imtcq == "Q"):
            if (self.inputs[var] == 0)&(self.inputsPrev[var] == 1):
                self.inputsPrev[var] = self.inputs[var]
                return input
            else:
                self.inputsPrev[var] = self.inputs[var]
                return 0

    ############################# LOGIC ###################################
    # Needed because logical not return true or false
    def nott (self, input):
        if (input == 0):
            return 1
        else:
            return 0

    ############################# COILS ###################################
    #Asign the imput to output or mark value
    def coil(self, input, var, qm):
        if (qm == "q")|(qm == "Q"):
            self.outputs[var] = input
        if (qm == "m")|(qm == "M"):
            self.marks[var] = input

    def coilInv(self, input, var, qm):
        if (qm == "q")|(qm == "Q"):
            self.outputs[var] = self.nott(input)
        if (qm == "m")|(qm == "M"):
            self.marks[var] = self.nott(input)

    #Set the output or mark value
    def coilSet(self, input, var, qm):
        if (qm == "q")|(qm == "Q"):
            if (input == 1):
                self.outputs[var] = 1
        if (qm == "m")|(qm == "M"):
            if (input == 1):
                self.marks[var] = 1

    #Reset the coil value
    def coilReset(self, input, var, qm):
        if (qm == "q")|(qm == "Q"):
            if (input == 1):
                self.outputs[var] = 0
        if (qm == "m")|(qm == "M"):
            if (input == 1):
                self.marks[var] = 0

    ############################# TIMERS ###################################
    # ON Timer block. pt = number of seconds. var = number of the timer
    def ton(self, input, pt, var):
        if (input == 1):
            if (self.timerAux[var] == 0):
                self.timerAux[var] = time.time()+pt
            elif(self.timerAux[var] <= time.time()):
                self.timers[var] = 1
        else:
            self.timerAux[var] = 0
            self.timers[var] = 0

    # OFF Timer block.
    def toff(self, input, pt, var):
        if (input == 1):
            if (self.timerAux[var] == 0):
                self.timerAux[var] = time.time()+pt
                self.timers[var] = 1
            elif(self.timerAux[var] <= time.time()):
                self.timers[var] = 0
        else:
            self.timerAux[var] = 0
            self.timers[var] = 0

    ############################# COUNTERS ###################################
    # Counter block. CU: increment, CD: decrease, R: reset, PV: target, VAR: counter number
    def counter(self, cu, cd, r, pv, var):
        if (r == 1)&(self.countPrevR[var]!= 1):
            self.countAux[var] = 0
        else:
            if (cu == 1)&(self.countPrevCU[var]!= 1):
                self.countAux[var] = self.countAux[var] +1

            if (cd == 1)&(self.countPrevCD[var]!= 1):
                self.countAux[var] = self.countAux[var] - 1

            if (self.countAux[var] >= pv):
                self.counts[var] = 1
            else:
                self.counts[var] = 0

        self.countPrevCU[var]= cu
        self.countPrevCD[var]= cd
        self.countPrevR[var]= r

    ############################# COMUNICATION FUNCTIONS ###################################
    # Read the input pins state
    def get(self):
        self.ser.write("0")
        return self.ser.readline()

    # Write the output pins
    def set(self, pinstring):
        # INPUT EXAMPLE >> "1000000000000000000" >> "1" + 18 pins
        self.ser.write(pinstring)

