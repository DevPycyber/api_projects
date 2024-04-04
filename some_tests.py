from tkinter import *
import tkinter.colorchooser as color_choose
import tkinter.simpledialog as dialog
import tkinter.filedialog as diafile
import tkinter.scrolledtext as scroll
import tkinter.messagebox as message
app = Tk()
canvas = Canvas(app)

def close_button():
    close = message.askokcancel('Close', 'Would you like to close the program ?')
    if close:
        app.destroy()

def losange_bind(event):
    app_2 = Tk()
    app_2.geometry("400x400")
    Lab = Label(app_2, text="temperature : 27°")
    Lab.pack()
    app_2.mainloop()

canvas.create_polygon(10, 10, 200, 50, 90, 150, 50, 80, 120, 55, fill='red', outline='blue')

losange = canvas.create_polygon(50, 50, 100, 20, 150, 50, 100, 150, fill="blue", outline="purple")
canvas.move(losange, 120, 50)
app.protocol("WM_DELETE_WINDOW", close_button)
canvas.tag_bind(losange, '<Button-1>', losange_bind)
canvas.pack()

app.mainloop()