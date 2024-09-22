from tkinter import *
from time import sleep


currentCellSelected = 0
root = Tk()
root.title("Testing for Sudoku")


# root.geometry("700x700")

def button_hover(e):
    btn1["bg"] = "white"
    status_bar.config(text="I'm hovering over the button !")

def mouse_leave(e):
    btn1["bg"] = "SystemButtonFace"
    status_bar.config(text="Mouse left ")


column_ans = []
row_ans = []
box_ans = []

for i in range(9):
    column_ans.append([])
    row_ans.append([])
    box_ans.append([])


def entering(given):
    print(given)

gameBoard = Frame(root)
gameBoard.grid(row=1,column=0)

consolePanel = LabelFrame(root, text="console", padx =10, pady=10)
consolePanel.grid(row=1, column=1)

class box:
    def __init__(self,box_index):
        self.index = box_index
        self.row = int(box_index / 3)
        self.column = box_index % 3
        self.loc = [self.row, self.column]
        self.bigFrame = Frame(gameBoard,width=180,height =180, bd=2, relief=SUNKEN)
        self.bigFrame.bind("<Enter>", lambda event: entering(self.index))
        self.bigFrame.grid(row=self.row, column=self.column)


box_list=[]

for i in range(9):
    box_list.append(box(i))


def selecting(cellNum):
    global currentCellSelected
    cell_list[currentCellSelected].cellCanvas["bg"] = 'SystemButtonFace'
    currentCellSelected = cellNum
    cell_list[currentCellSelected].cellCanvas["bg"] = "#FFE67B"


def check(cell_index):
    if len(set(box_ans[cell_list[cell_index].box])) == len(list(box_ans[cell_list[cell_index].box])):
        if len(set(column_ans[cell_list[cell_index].column])) == len(list(column_ans[cell_list[cell_index].column])):
            if len(set(row_ans[cell_list[cell_index].row])) == len(list(row_ans[cell_list[cell_index].row])):
                return 0
    return 1


def wronganswer():
    global currentCellSelected
    cell_list[currentCellSelected].cellCanvas.config(bg="red")
    # sleep(1)
    # cell_list[currentCellSelected].cellCanvas["bg"] = 'SystemButtonFace'


class cell:
    def __init__(self, cell_index):
        self.num = cell_index
        self.row = int(cell_index / 9)
        self.column = cell_index % 9
        self.loc = [self.row, self.column]
        self.box = 3 * int(self.row / 3) + int(self.column / 3)
        self.cellCanvas = Canvas(box_list[self.box].bigFrame, width=60, height=60, bd=1, relief=SUNKEN)
        self.cellCanvas.bind("<Button-1>", lambda event: selecting(self.num))
        self.cellCanvas.grid(row=self.row, column=self.column)
        self.guess = []
        self.tagString = "cell"+str(self.num)+"guess"
        self.ans = 0

    def guessing(self, guessNum):
        if self.ans != 0:
            self.cellCanvas.delete("ans")
            self.ans = 0
            self.createGuessDisplay()
            return

        self.appending(guessNum)
        if check(self.num):
            print("invalid guess")
            self.removing(guessNum)
            return
        self.removing(guessNum)

        self.cellCanvas.delete(self.tagString)

        if guessNum in self.guess:
            self.guess.remove(guessNum)
        else:
            self.guess.append(guessNum)
            self.guess.sort()

        self.createGuessDisplay()

    def createGuessDisplay(self):
        for i in self.guess:
            row=(i-1) % 3
            column = int((i-1)/3)
            self.cellCanvas.create_text(row*20+12,column*20+12,text=str(i),font='10',tag=self.tagString)

    def answering(self, ansNum):
        self.cellCanvas.delete(self.tagString)

        if self.ans != 0:
            self.cellCanvas.delete("ans")
            self.removing(self.ans)
            if self.ans == ansNum:
                self.ans = 0
                self.cellCanvas.delete("ans")
                self.createGuessDisplay()
            else:
                self.appending(ansNum)
                if check(self.num):
                    print("invalid answer")
                    wronganswer()
                    self.removing(ansNum)
                    return

                self.ans = ansNum
                self.createAnsDisplay()
        else:
            self.appending(ansNum)
            if check(self.num):
                print("invalid answer")
                wronganswer()
                self.removing(ansNum)
                return

            self.ans = ansNum
            self.createAnsDisplay()

    def createAnsDisplay(self):
        self.cellCanvas.create_text(35, 32, text=str(self.ans), fill="black", font=('Helvetica 25 bold'), tag="ans")

    def removing(self, given_to_remove):
        column_ans[self.column].remove(given_to_remove)
        row_ans[self.row].remove(given_to_remove)
        box_ans[self.box].remove(given_to_remove)

    def appending(self, given_to_append):
        column_ans[self.column].append(given_to_append)
        row_ans[self.row].append(given_to_append)
        box_ans[self.box].append(given_to_append)

cell_list = []

for i in range(81):
    cell_list.append(cell(i))

def Lclick(answer):
    global currentCellSelected
    cell_list[currentCellSelected].answering(answer)


def Rclick(guess):
    global currentCellSelected
    cell_list[currentCellSelected].guessing(guess)


class number_button:
    def __init__(self, number):
        self.number = number
        self.btn = Button(consolePanel, text=number, command=lambda: Lclick(number), padx=20, pady=15,
                          font=('HP Simplified', 12))
        self.btn.grid(row=number, column=1)
        self.btn.bind('<Button-3>', lambda event: Rclick(self.number))


numberButtonList = []
for i in range(9):
    i += 1
    numberButtonList.append(number_button(i))

# correct color : #DCEDC2 or light green
# wrong color : red ?

status_bar = Label(root, text="testing", bd=1, relief=SUNKEN, anchor=E, bg="black", fg="white")
status_bar.grid(row=3,  column=0, columnspan=3, ipadx=400,)

# btn1.bind("<Enter>", button_hover)
# btn1.bind("<Leave>", mouse_leave)

root.mainloop()