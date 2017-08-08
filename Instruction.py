from Tkinter import *
from random import *
import pyuarm
from math import *
import time


class InstructionNames:
    Catch = "Catch"
    Repeat = "Repeat"
    Release = "Release"
    EndRepeat = "EndRepeat"
    GoTo = "GoTo"
    Block = "Block" #internal repeat block
    Hand = "Hand"

class Instructions(object):
    def __init__(self):
        self.list = []

    def add(self, instruction):
        self.list.append(instruction)

    def remove(self, index):
        del self.list[index]

    def insert(self, index, instruction):
        self.list.insert(index, instruction)

    def length(self):
        return len(self.list)

    def isVerified(self):
        repeatCounter = 0
        if (self.length() == 0):
            return (False, "Add instructions to your program.")
        for instruction in self.list:
            if instruction.getName() == InstructionNames.Repeat:
                repeatCounter = repeatCounter + 1
            elif instruction.getName() == InstructionNames.EndRepeat:
                repeatCounter = repeatCounter - 1
            if repeatCounter < 0:
                return (False, "EndRepeat not expected.")
        if repeatCounter > 0:
            return (False, "EndRepeat expected.")
        return ((repeatCounter == 0), "")

    def play(self, myuArm):
        playMode = True
        currentBlock = None
        for instruction in self.list:
            if (instruction.getName() == InstructionNames.Repeat):
                playMode = False
                currentBlock = Block(instruction.getArguments())
            elif (instruction.getName() == InstructionNames.EndRepeat):
                playMode = True
                currentBlock.do(myuArm)
            else:
                if (playMode == True):
                    instruction.do(myuArm)
                    time.sleep(instruction.getDelay())
                else:
                    currentBlock.add(instruction)                    
                    

class Instruction(object):
    def __init__(self, arguments):
        self.arguments = arguments
    def getName(self):
        return self.arguments[0]  
    def getSignature(self):
        return self.arguments[0]
    def getDelay(self):
        return 1
    def getArguments(self):
        return self.arguments

class Block(Instruction):
    def __init__(self, arguments):
        self.arguments = (InstructionNames.Block, arguments[1])
        print InstructionNames.Block + " created. " + self.arguments[1]
        self.timesToDo = int(arguments[1])
        self.instructions = Instructions()
    def do(self, myuArm):
        for i in xrange(self.timesToDo):
            self.instructions.play(myuArm)
    def add(self, instruction):
        self.instructions.add(instruction)

class Release(Instruction):
    def __init__(self, arguments):
        self.arguments = (InstructionNames.Release, )
#        print InstructionNames.Release + " created."
    def do(self, myuArm):
        myuArm.pump_control(False)
        myuArm.alarm(1, 100, 100)

class Hand(Instruction):
    def __init__(self, angle):
        self.arguments = (InstructionNames.Hand, angle)
    def do(self, myuArm):
        SERVO_HAND = 3
        myuArm.write_servo_angle(SERVO_HAND, self.arguments[1], with_offset=0 )
        print (self.getSignature())
        myuArm.alarm(1, 100, 100)
    def getDelay(self):
        return 2
    def getSignature(self):
        return InstructionNames.Hand + '(' + str(self.arguments[1]) + ')'
       
class Catch(Instruction):
    def __init__(self, arguments):
        self.arguments = (InstructionNames.Catch, )
        print (InstructionNames.Catch + " created")
    def getSignature(self):
        return InstructionNames.Catch
    def do(self, myuArm):
        myuArm.pump_control(True)
        myuArm.alarm(1, 100, 100)

#fetch card position, at the table
#        fetchCard = [-0.71, -9.72, 8.7] 

#home position
#        home = [-1.49, -10.03, 18.9]
#        time_spend=5
#        self.myuArm.move_to(home[0], home[1], home[2], None, pyuarm.ABSOLUTE, time_spend, pyuarm.PATH_LINEAR, pyuarm.INTERP_EASE_INOUT_CUBIC)

#INTERP_EASE_INOUT_CUBIC, INTERP_LINEAR, INTERP_EASE_INOUT, INTERP_EASE_IN, INTERP_EASE_OUT
 #       self.myuArm.move_to(fetchCard[0], fetchCard[1], fetchCard[2], None, pyuarm.ABSOLUTE, time_spend, pyuarm.PATH_LINEAR, pyuarm.INTERP_EASE_INOUT_CUBIC)
#time.sleep(0.1)
 #       self.myuArm.pump_control(1)
 #       self.myuArm.move_to(home[0], home[1], home[2], None, pyuarm.ABSOLUTE, time_spend, pyuarm.PATH_LINEAR, pyuarm.INTERP_EASE_INOUT_CUBIC)
 #       self.myuArm.pump_control(0)

class Repeat(Instruction):
    def __init__(self, arguments):
        self.arguments = (InstructionNames.Repeat, str(arguments))
        print InstructionNames.Repeat + '(' + arguments[0] + ')'
    def getSignature(self):
        return InstructionNames.Repeat + ' (' + self.arguments[1] + ')'
    

class EndRepeat(Instruction):
    def __init__(self, arguments):
        self.arguments = (InstructionNames.EndRepeat, )
        print InstructionNames.EndRepeat

class GoTo(Instruction):
    def __init__(self, arguments):
        self.arguments = (InstructionNames.GoTo, arguments[0], arguments[1], arguments[2])
        print "Created " + self.getSignature()
    def getSignature(self):
        return InstructionNames.GoTo + ' (' + str(self.arguments[1]) + ', ' + str(self.arguments[2]) + ', '+ str(self.arguments[3]) + ')'  
    def do(self, myuArm):
        #home = [-1.49, -10.03, 18.9]
        time_spend=4
        myuArm.move_to(self.arguments[1], self.arguments[2], self.arguments[3], None, pyuarm.ABSOLUTE, time_spend, pyuarm.PATH_LINEAR, pyuarm.INTERP_EASE_INOUT_CUBIC)
        myuArm.alarm(1, 100, 100)
    def getDelay(self):
        return 4.5
