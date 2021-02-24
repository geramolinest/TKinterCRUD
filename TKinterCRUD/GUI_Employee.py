import tkinter as tk
import connectionBD as pyc
import  tkinter.messagebox as msg
import tkinter.filedialog as fd
from tkinter import ttk
import psycopg2
import os
from PIL import Image,ImageTk

def Window():
    
    window = tk.Tk()
    window.geometry("850x600")
    window.title("Employee Register")
    window.configure(bg="#FBFEFA")

     #Fondo
    #logo2 = Image.open("/home/anon23/Descargas/WallPapers/BackGround.jpg")
    #logo2 = ImageTk.PhotoImage(logo2)
    #labelBG = tk.Label(window,image = logo2,justify = tk.LEFT)
    #labelBG.image = logo2
    #labelBG.pack()

    #Labels
    label = tk.Label(window,text = "Name:",bg="#FBFEFA")
    label.place(x = 200,y = 50)
    label1 = tk.Label(window,text = "Last Name:",bg="#FBFEFA")
    label1.place(x = 50,y = 100)
    label2 = tk.Label(window,text = "Age:",bg="#FBFEFA")
    label2.place(x = 50,y = 145)
    label = tk.Label(window,text = "ID:",bg="#FBFEFA")
    label.place(x = 50,y = 50)

    #Image
    logo = Image.open("/home/anon23/Descargas/WallPapers/guy-fawkes-mask.png")
    logo = ImageTk.PhotoImage(logo)
    labelImage = tk.Label(image = logo,fg=None,bg=None)
    labelImage.image = logo
    labelImage.place(x=570,y=50)

    #Entrys
    entry = tk.Entry(window,width = 35)
    entry.place(x = 100,y=75)
    entry1 = tk.Entry(window,width = 41)
    entry1.place(x = 50,y=120)
    entry2 = tk.Entry(window,width = 41)
    entry2.place(x = 50,y=165)
    entry3 = tk.Entry(window,width = 5)
    entry3.place(x = 50,y = 75)

    def CleanControls():
        entry.delete(0,tk.END)
        entry1.delete(0,tk.END)
        entry2.delete(0,tk.END)
        entry3.delete(0,tk.END)
        entry.focus()

    def Employees():
        sql = 'SELECT id,full_name,last_name,age FROM employees ORDER BY id ASC'
        empleados = pyc.Execute_Query(sql)
        return empleados

    def SaveEmployee():
        file_emp = None
        name_file = None
        if msg.askyesno("Question",'Do you want add files for this employee?'):
            file_emp,name_file = File()      
        if pyc.SaveEmployee(entry.get(),entry1.get(),entry2.get(),entry3.get(),file_emp,name_file):
            CleanControls()
        TableEmployees()

    def TableEmployees():
        DeleteItems()
        employees = Employees()
        for employee in employees:
            table.insert('','end',values = employee)
    def DeleteItems():
        for item in table.get_children():
            table.delete(item)
          
    def OnDobleClick(event):
        employee = table.item(table.focus())['values']
        DataEmployee(employee)

    def DataEmployee(employee):
        CleanControls()
        entry.insert(0,str(employee[1]))
        entry1.insert(0,str(employee[2]))
        entry2.insert(0,str(employee[3]))
        entry3.insert(0,str(employee[0]))
    
    def DeleteEmployee():
        if pyc.Delete_Employee(entry3.get()):
            CleanControls()
        TableEmployees()

    def File():
        path_file = fd.askopenfilename()   
        name = os.path.basename(path_file)
        with open(path_file,'rb') as file:
            file_data = file.read()         
        return file_data,name
    
    def SaveFileEmployee():
        save_path = fd.askdirectory()
        pyc.File_Employee(entry3.get(),save_path)
        
    #TreeView
    table = ttk.Treeview(window,columns = (1,2,3,4),show = "headings",height = "5")    
    table.place(x = 50,y=250)
    table.heading(1,text = "ID")
    table.column(1,width = 35)
    table.heading(2,text = "Name")
    table.heading(3,text = "Last Name")
    table.heading(4,text = "Age")
    vsb = ttk.Scrollbar(orient="vertical",command=table.yview)
    vsb.place(x = 685,y =250,height = 183)  
    table.configure(yscrollcommand = vsb.set,height = 8)
    table.bind('<Double-Button-1>', OnDobleClick)


    #Button
    button = tk.Button(window,text = "Save Employee",width = 15,bg = "#79FF7B",command = SaveEmployee)
    button.place(x = 50,y= 205)
    buttonD = tk.Button(window,text = "Delete Employee",width = 15,bg = "#FFB59C",command = DeleteEmployee)
    buttonD.place(x = 200,y= 205)
    buttonF = tk.Button(window,text = "File",width = 15,bg = "#79FF7B",command = SaveFileEmployee)
    buttonF.place(x = 350,y= 205)

    TableEmployees()
    window.mainloop()

if __name__ == "__main__":
    Window()