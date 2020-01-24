from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import csv

semester = []
filename = None
columnNames = None
lastIndex = None

def createFile():
   global filename
   filename = fd.asksaveasfilename(defaultextension=".csv", filetypes=(("csv file", "*.csv"), ("All Files", "*.*")))
   csvfile = open(filename, "w", newline="")

   listBox.delete(0,'end')
   courseNameEntry.delete(0, END)
   comments.delete('0.0', END)

   workingHourScale.set(0)

   global semester
   semester = []

   addCourseBtn['state'] = NORMAL
   delCourseBtn['state'] = NORMAL
   courseNameEntry['state'] = NORMAL
   comments['state'] = NORMAL
   workingHourScale['state'] = NORMAL
   saveBtn['state'] = NORMAL

   csvfile.close()

def loadFile():
   global semester
   semester = []
   listBox.delete(0, END)
   courseNameEntry.delete(0, END)
   comments.delete('0.0', END)
   workingHourScale.set(0)
   global filename
   filename = fd.askopenfilename(defaultextension=".csv", filetypes=(("csv file", "*.csv"), ("All Files", "*.*")))
   with open(filename, "r") as f:
      reader = csv.reader(f, delimiter=",")
      data = list(reader)
      global columnNames
      columnNames = data[0]
      for i in data[1:]:
         course = dict(zip(columnNames, i))
         semester.append(course)

      for i in range(len(semester)):
         listBox.insert(i, semester[i].get("name"))

   addCourseBtn['state'] = NORMAL
   delCourseBtn['state'] = NORMAL
   courseNameEntry['state'] = NORMAL
   comments['state'] = NORMAL
   workingHourScale['state'] = NORMAL
   saveBtn['state'] = NORMAL

def saveFile():
   if semester == []:
      mb.showerror("Error", "Nothing to save!")
      return
   global columnNames
   if columnNames is None:
      columnNames = ['name', 'comment', 'hours']
   data = [columnNames]
   for i in semester:
      data.append(list(i.values()))

   with open(filename, "w", newline="") as csvfile: 
      writer= csv.writer(csvfile, delimiter=",")
      writer.writerows(data)

def getHelp():
   mb.showinfo("Your help", "If everything is disabled, then create new semester (file) or open existing one with 'File' menu")

def addCourse():
   listBox.insert(END, "New course")
   semester.append({'name': 'Subject', 'comment': 'Your comment', 'hours': '10'})

def deleteCourse():
   currentIndex = int(listBox.curselection()[0])
   semester.pop(currentIndex)
   listBox.delete(currentIndex)

def getData(event):
   global lastIndex
   lastIndex = int(listBox.curselection()[0])
   currentCourse = semester[lastIndex]
   courseNameEntry.delete(0, END)
   courseNameEntry.insert(0, currentCourse["name"])

   comments.delete('0.0', END)
   comments.insert('0.0', currentCourse["comment"])

   workingHourScale.set(int(currentCourse["hours"]))

def updateName():
   semester[lastIndex]["name"] = courseNameEntry.get()

   listBox.delete(lastIndex)
   listBox.insert(lastIndex, courseNameEntry.get())
   
def updateComments():
   semester[lastIndex]["comment"] = comments.get('0.0', END).strip()

def updateHours():
   semester[lastIndex]["hours"] = workingHourScale.get()

def saveChanges():
   updateName()
   updateComments()
   updateHours()

# Main Screen
root = Tk()
root.title("Informatics: My Course Tracker")
root.geometry("1000x550+100+100")

# Main Menu
menubar = Menu(root)
fileMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label="File", menu=fileMenu)
root.config(menu=menubar)
fileMenu.add_command(label="New Semester", command=createFile)
fileMenu.add_command(label="Open", command=loadFile)
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.destroy)
menubar.add_command(label="Help", command=getHelp)

addIcon = PhotoImage(file = "plus.png")
addCourseBtn = Button(root, text = "add course", image = addIcon, compound = LEFT, command = addCourse, state=DISABLED)
addCourseBtn.grid(row = 0, column = 0, sticky = W)

delIcon = PhotoImage(file = "multiply.png")
delCourseBtn = Button(root, text = "delete course", image = delIcon, compound = LEFT, command = deleteCourse, state=DISABLED)
delCourseBtn.grid(row = 0, column = 1)

listBox = Listbox(root)
listBox.bind("<<ListboxSelect>>", getData)
listBox.grid(row = 1, column = 0, columnspan=2, sticky = NSEW)

scrollbar = Scrollbar(root, orient="vertical", command=listBox.yview, borderwidth = 2)
scrollbar.grid(row = 1, column = 1, sticky = E+S+N)
listBox.config(yscrollcommand=scrollbar.set)

frame2 = Frame(root)
frame2.grid(row = 1, column = 2, sticky = N)

courseNameLabel = Label(frame2, text="Course Name")
courseNameLabel.grid(row = 0, column = 0, sticky = W)

courseNameEntry = Entry(frame2, state=DISABLED)
courseNameEntry.grid(row = 0, column = 1, sticky = NSEW)

comments = Text(frame2, state=DISABLED)
comments.grid(row = 1, column = 1, sticky = N+S)

commentsLabel = Label(frame2, text = "Comments")
commentsLabel.grid(row = 1, column = 0, sticky = W)

workingHourScale = Scale(frame2, from_=0, to=200, orient=HORIZONTAL, state=DISABLED)
workingHourScale.grid(row = 2, column = 1, sticky = EW)

workingHours = Label(frame2, text = "My working hours")
workingHours.grid(row = 2, column = 0)

saveBtn = Button(frame2, text = "Confirm changes", command = saveChanges, state=DISABLED, height = 3, width = 40)
saveBtn.grid(row = 3, column = 1, sticky = W+S)

# wait for user interactions
mainloop()