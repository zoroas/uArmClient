from Tkinter import *
from random import *
import pyuarm
import Instruction
from Instruction import *
from math import *
from uArmClient import *
import pickle
import tkMessageBox
import time

class App:
##    def disconnect(self):
##        if (self.myuArm <> None):
##            self.myuArm.pump_control(False)
##            self.myuArm.disconnect()

    def catchActionAdd(self):
        self.instructions.add( Catch(()) )
        self.refreshList()

    def releaseActionAdd(self):
        self.instructions.add(Release(()))
        self.refreshList()

    def gotoActionAdd(self):
        try:
            x = float(self.textGoToX.get("1.0",'end-1c'))
            print(x)
            y = float(self.textGoToY.get("1.0",'end-1c'))
            print(y)
            z = float(self.textGoToZ.get("1.0",'end-1c'))
            print(z)
            if (x >= -15 and x <= 9 and y >= -24 and y <= -6 and z >= -30 and z <= 19):
                instruction = GoTo((x, y, z))
                print (instruction.getSignature())
                self.instructions.add(instruction)
                self.refreshList()
        except:
            tkMessageBox.Message("Error on value")

    def repeatActionAdd(self):
        self.instructions.add(Repeat((self.textRepeat.get("1.0",'end-1c'))))
        self.refreshList()

    def handActionAdd(self):
        try:
            a = self.textHand.get("1.0",'end-1c')
            value = int(a)
            #print (str(value))
            if value >= 0 and value <= 180:
                self.instructions.add(Hand(value))
                self.refreshList()
        except:
            tkMessageBox.Message("Error on value")

    def endRepeatActionAdd(self):
        self.instructions.add(EndRepeat(self, ))
        self.refreshList()

    def listDeleteAction(self):
        item = self.listboxInstructions.curselection()
        del self.instructions.list[item[0]]
        print(item)
        self.refreshList()

    def getSelectionIndex(self, listbox):
        selection = listbox.curselection()
        if (len(selection) != 1):
            return -1
        return int(selection[0])

    def listUpAction(self):
        index = self.getSelectionIndex(self.listboxInstructions)
        if (index > 0):
            item = self.instructions.list[index]
            self.instructions.remove(index)
            self.instructions.insert(index - 1, item)
            self.refreshList()
            self.listboxInstructions.select_set(index - 1) #This only sets focus on the first item.
            self.listboxInstructions.event_generate("<<ListboxSelect>>")

    def listDownAction(self):
        index = self.getSelectionIndex(self.listboxInstructions)
        if (index < self.instructions.length() - 1 and index > -1):
            item = self.instructions.list[index]
            print item.getSignature()
            self.instructions.remove(index)
            self.instructions.insert(index + 1, item)
            self.refreshList()
            self.listboxInstructions.select_set(index + 1) #This only sets focus on the first item.
            self.listboxInstructions.event_generate("<<ListboxSelect>>")

    def listUpKeyPressed(self, event):
        self.listUpAction()

    def listDownKeyPressed(self, event):
        self.listDownAction()

    def listDeleteKeyPressed(self, event):
        self.listDeleteAction()

    def saveAction(self):
        with open('entry.pickle', 'wb') as f: 
            pickle.dump(self.instructions, f)
        print("Saved ...or not")

    def openAction(self):
        with open('entry.pickle', 'rb') as f:
            self.instructions = pickle.load(f)
        self.refreshList()
        print("Open ...or not")

    def verifyAction(self):
        if (self.isVerified):
            self.buttonVerify.configure(state=DISABLED)
            self.instructions.play(self.myuArm)
#            self.isVerified = False
            self.buttonVerify.configure(state=NORMAL, background='cadetblue')
        else:
            result = self.instructions.isVerified()
            self.isVerified = result[0]
            if (self.isVerified == True):
                self.buttonVerify.config(text = "Play")
            else:
                self.labelVerifyResult.config(text = result[1])
        
    def refreshList(self):
        self.isVerified = False
        self.labelVerifyResult.config(text= "")
        self.buttonVerify.config(text = "Verify")
        self.listboxInstructions.delete(0, END)
        for instruction in self.instructions.list:
            self.listboxInstructions.insert('end', instruction.getSignature())

    def refreshColors(self):
        self.text1.configure(fg = self.textboxBackground)
        self.text2.configure(fg = self.textboxBackground)
        self.window.update()

    def indexInside(self, aList, aTuple):
        index = 0
        for row in aList:
            if row[0] == aTuple[0] :
                return index
            index = index + 1
        return -1


    def connect(self):
        try:
            self.myuArm = pyuarm.uArm(debug=True)
            print self.myuArm
        except:
            print "Couldn't get a connection to the uArm"
            return
    
    def __init__(self, window):
        self.myuArm = None 
        WINDOW_BACKGROUND = '#2f4f4f'
        TEXT_BACKGROUND = 'white'
        TEXTBOX_BACKGROUND = 'white'
        ALARM_BACKGROUND = 'red'

        try:
            self.connect()
            time.sleep(0.5)

            #home position
            if (self.myuArm <> None):
                home = [-1.49, -10.03, 18.9]
                time_spend=5
                self.myuArm.move_to(home[0], home[1], home[2], None, pyuarm.ABSOLUTE, time_spend, pyuarm.PATH_LINEAR, pyuarm.INTERP_EASE_INOUT_CUBIC)
                #time.sleep(5)
                #self.myuArm.pump_control(False)
                #time.sleep(2)
                #SERVO_HAND = 3
            # myuArm.write_servo_angle(SERVO_HAND, self.arguments[1], 0 )
             #time.sleep(2)

            ## list of instructions
            self.instructions = Instructions()
            self.isVerified = False;
            self.window = window
            self.window.title('uArm CAISL client')
            width = 740
            height = 600
            self.window.resizable(0,0)
            window.minsize(width=width, height=height)
            self.canvas = Canvas(window, width=width, height=height, bg=WINDOW_BACKGROUND)
            self.outerFrame = Frame(self.canvas, bg=WINDOW_BACKGROUND)
            self.frameDetail = Frame(self.outerFrame, bg=WINDOW_BACKGROUND)

            # canvas GoTo
            self.canvasGoTo = Frame(self.frameDetail, bg=WINDOW_BACKGROUND)
            self.canvasGoTo.grid(row=0, column=0, padx=6, pady=6, sticky = W, columnspan=4)

            self.buttonGoTo = Button(self.canvasGoTo, command=self.gotoActionAdd, width=15, text='GoTo')
            self.buttonGoTo.grid(column = 0, row=0, padx=6, pady=6, sticky = W)
        
            self.labelGoToX = Label(self.canvasGoTo, text= "x:", bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.labelGoToX.grid(row=0, column=1, sticky = E, padx=6, pady=6)

            self.textGoToX = Text(self.canvasGoTo, height=1, padx = 6, pady=6, bg = TEXTBOX_BACKGROUND, width=5)
            self.textGoToX.insert(END, '-1.49')
            self.textGoToX.grid(row=0, column=2, sticky = W, padx=6, pady=6)

            self.labelGoToY = Label(self.canvasGoTo, text= "y:",bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.labelGoToY.grid(row=0, column=3, sticky = E, padx=6, pady=6)

            self.textGoToY = Text(self.canvasGoTo, height=1, padx = 6, pady=6, bg = TEXTBOX_BACKGROUND, width=5)
            self.textGoToY.insert(END, '-10.03')
            self.textGoToY.grid(row=0, column=4, sticky = W, padx=6, pady=6)

            self.labelGoToZ = Label(self.canvasGoTo, text= "z:", bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.labelGoToZ.grid(row=0, column=5, sticky = E, padx=6, pady=6)

            self.textGoToZ = Text(self.canvasGoTo, height=1, padx = 6, pady=6, bg = TEXTBOX_BACKGROUND, width=5)
            self.textGoToZ.insert(END, '18.9')
            self.textGoToZ.grid(row=0, column=6, sticky = W, padx=6, pady=6)

            self.labelLimitX = Label(self.canvasGoTo, text= "[-15, 9]", bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.labelLimitX.grid(row=1, column=2, sticky = E, padx=0, pady=0)

            self.labelLimitY = Label(self.canvasGoTo, text= "[-24, -6]", bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.labelLimitY.grid(row=1, column=4, sticky = E, padx=0, pady=0)

            self.labelLimitY = Label(self.canvasGoTo, text= "[8, 19]", bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.labelLimitY.grid(row=1, column=6, sticky = E, padx=0, pady=0)

            # Repeat
            self.buttonRepeat = Button(self.frameDetail, command=self.repeatActionAdd, width=15, text='Repeat')
            self.buttonRepeat.grid(row=1, column = 0, padx=12, pady=6, sticky = W)

            self.textRepeat = Text(self.frameDetail, height=1, padx = 6, pady=6, bg = TEXTBOX_BACKGROUND, width=3)
            self.textRepeat.insert(END, '2')
            self.textRepeat.grid(row=1, column = 1, sticky = W, padx=6, pady=6)

            self.buttonEndRepeat = Button(self.frameDetail, command=self.endRepeatActionAdd, width=15, text='EndRepeat')
            self.buttonEndRepeat.grid(row=1, column = 2, padx=6, pady=6, sticky = W)

            # Hand
            self.buttonHand = Button(self.frameDetail, command=self.handActionAdd, width=15, text='Hand')
            self.buttonHand.grid(row=2, column = 0, padx=12, pady=6, sticky = W)
            #self.buttonHand.configure(state=DISABLED)

            self.textHand = Text(self.frameDetail, height=1, padx = 6, pady=6, bg = TEXTBOX_BACKGROUND, width=3)
            self.textHand.insert(END, '0')
            self.textHand.grid(row=2, column = 1, sticky = W, padx=6, pady=6)

            self.labelLimitHand = Label(self.frameDetail, text= "[0, 180]", bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.labelLimitHand.grid(row=2, column=2, sticky = W, padx=0, pady=0)

            # Catch and Release
#            self.canvasButtons = Frame(self.frameDetail, bg='')
#            self.canvasButtons.grid(row=2, column=0, columnspan=2, padx=6, pady=6)

            self.buttonCatch = Button(self.frameDetail, command=self.catchActionAdd, width=15, text='Catch')
            self.buttonCatch.grid(row=3, column = 0, padx=12, pady=6, sticky = W)

            self.buttonRelease = Button(self.frameDetail, command=self.releaseActionAdd, width=15, text='Release')
            self.buttonRelease.grid(row=3, column = 1, padx=6, pady=6, sticky = W)

            # List buttons
            self.itemButtonsList = LabelFrame(self.frameDetail, text="Selected", padx=5, pady=5, bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.itemButtonsList.grid(row=4, column=0, padx=12, pady=12, columnspan=3)

            self.buttonDelete = Button(self.itemButtonsList, command=self.listDeleteAction, width=15, text='Delete (Del)')
            self.buttonDelete.grid(row=0, column=0, padx=6) #grid(column = 0, row=4, padx=12, pady=6, sticky = W)

            self.buttonListUp = Button(self.itemButtonsList, command=self.listUpAction, width=15, text='Move Up (Ctrl+Q)')
            self.buttonListUp.grid(row=0, column=1, padx=6)

            self.buttonListDown = Button(self.itemButtonsList, command=self.listDownAction, width=15, text='Move Down (Ctrl+A)')
            self.buttonListDown.grid(row=0, column=2,padx=6)

            ## Program butons
            self.programButtonsList = LabelFrame(self.frameDetail, fg=TEXT_BACKGROUND)
            self.programButtonsList.config(text="Program", padx=5, pady=5, bg=WINDOW_BACKGROUND)
            self.programButtonsList.grid(column=0, row=5, padx=12, pady=12, columnspan=3)
            self.buttonVerify = Button(self.programButtonsList, command=self.verifyAction, width=15, text='Verify')
            self.buttonVerify.grid(row=0, column=0,padx=6)
            self.labelVerifyResult = Label(self.programButtonsList, text= "",bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND, width = 42)
            self.labelVerifyResult.grid(row=0, column=1,padx=6)

            if (self.myuArm == None):
                self.programButtonsList.config(bg=ALARM_BACKGROUND)
                self.labelVerifyResult.config(bg=ALARM_BACKGROUND)
                self.labelVerifyResult.config(text='uArm not connected. Please connect uArm and restart.')

            ## File butons
            self.fileButtonsList = LabelFrame(self.frameDetail, text="File", padx=5, pady=5, bg=WINDOW_BACKGROUND, fg=TEXT_BACKGROUND)
            self.fileButtonsList.grid(column=0, row=6, padx=12, pady=12, columnspan=3)
            self.buttonSave = Button(self.fileButtonsList, command=self.saveAction, width=15, text='Save')
            self.buttonSave.grid(row=0, column=0,padx=6)
            self.buttonOpen = Button(self.fileButtonsList, command=self.openAction, width=15, text='Open')
            self.buttonOpen.grid(row=0, column=1,padx=6)

            self.listFrame = Frame(self.outerFrame, bg='')
            self.scrollbar = Scrollbar(self.listFrame)
            self.scrollbar.pack(side=RIGHT, fill=Y)
     
            self.listboxInstructions = Listbox(self.listFrame, height=35, width=35, yscrollcommand=self.scrollbar.set)
            self.listboxInstructions.pack(side=LEFT, fill=BOTH)
            self.listboxInstructions.bind_all('<Delete>', self.listDeleteKeyPressed)
            self.listboxInstructions.bind_all('<Control-q>', self.listUpKeyPressed)
            self.listboxInstructions.bind_all('<Control-a>', self.listDownKeyPressed)

            self.myList = []

            self.canvas.pack(fill=X)
            self.outerFrame.place(x=20, y=20)
            self.listFrame.grid(row=0, column=0, sticky=W+N)
            self.frameDetail.grid(row=0, column=1, sticky= W+N)
        except:
            return

root = Tk()
my_gui = App(root)
root.mainloop()
root.withdraw()

