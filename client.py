import socket
import threading
import tkinter as tk
import tkinter.font as font
from tkinter import *
from tkinter import scrolledtext


window = tk.Tk()
window.geometry('250x85')
window.title('Messaging App')
window.resizable(width=False, height=False)
window.configure(bg='#474440')

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)

enternamelabel = Label(window, text=f'Enter a Username', bg='#474440',
                       fg='#f3cea5', highlightthickness=0, font=('Arial 14'))
enternamelabel.grid(row=1, column=0, padx=10, pady=4, sticky=E)

mainfont = font.Font(family='Arial', size=15)
enternamelabel['font'] = mainfont

inputbox = Entry(window, width=15, font=('Arial 14'))
inputbox.grid(row=3, column=0, padx=14, pady=8, ipady=6, sticky=NW)

def openmainwindow():
    value = inputbox.get()
    username = value
    mainwindow = Toplevel(window)
    window.withdraw()

    mainwindow.geometry('730x515')
    mainwindow.title('Messaging App')
    mainwindow.resizable(width=False, height=False)
    mainwindow.configure(bg='#474440')

    mainwindow.columnconfigure(0, weight=1)
    mainwindow.columnconfigure(1, weight=1)
    mainwindow.columnconfigure(2, weight=1)
    mainwindow.columnconfigure(3, weight=1)

    mainwindow.rowconfigure(0, weight=1)
    mainwindow.rowconfigure(1, weight=1)
    mainwindow.rowconfigure(2, weight=1)
    mainwindow.rowconfigure(3, weight=1)

    message_box = Text(mainwindow, height=5, width=50, highlightthickness=0)
    message_box.grid(row=4, column=3, sticky=W, pady=13)

    EventText = scrolledtext.ScrolledText(
        mainwindow, height=21, width=48, highlightthickness=0)
    EventText.config(state='disabled')
    EventText.grid(row=2, column=3, sticky=W)

    

    # users = [['Will', '81.45.123.57'], ['Joe', '82.234.76.89']]

    c = socket.socket()
    HOST = '172.16.74.185'
    PORT = 1234

    print(f'Waiting For Connection...')

    try:
        c.connect((HOST, PORT))
        print('Connected to Server')
    except socket.error as e:
        print(e)

    buttonfont = font.Font(family='Arial', size=16)
    titlefont = font.Font(family='Arial', size=16)
    # usersfont = font.Font(family='Arial', size=16)

    # userbox = scrolledtext.ScrolledText(
    #     mainwindow, height=26, width=8, highlightthickness=0, bg='#f3cea5')
    # userbox.grid(row=0, column=0, sticky=W, rowspan=5, columnspan=5)

    # for i in users:
    #     userbox.insert('end', i[0] + '\n')

    # userbox.config(state='disabled')
    # userbox['font'] = usersfont

    def clientlistener():
        while True:
            reply = c.recv(1024)
            if not reply:
                break  # If no data is received break
            EventText.config(state='normal')
            EventText.insert('end', reply)
            EventText.see('end')
            EventText.config(state='disabled')

    trd1 = threading.Thread(target=clientlistener)
    trd1.start()

    def key_pressed(event):
        value = message_box.get("1.0", "end-1c")
        if len(value) == 1:
            message_box.delete('1.0', END)
            return
        fullmsg = username + ': ' + value
        c.send(fullmsg.encode('utf-8'))
        message_box.delete('1.0', END)

    def button_pressed():
        value = message_box.get("1.0", "end-1c")
        if len(value) == 0:
            message_box.delete('1.0', END)
            return
        fullmsg = username + ': ' + value + '\n'
        c.send(fullmsg.encode('utf-8'))
        message_box.delete('1.0', END)

    send_button = Button(mainwindow, text="Send", height=3, width=8, bg='#f3cea5',
                         borderwidth=0, command=button_pressed,  highlightthickness=0)
    send_button.grid(row=4, column=4)
    send_button['font'] = buttonfont

    mainwindow.bind('<Return>', key_pressed)



send_button = Button(window, text="Done", height=1, width=4, bg='#f3cea5',
                     command=openmainwindow, borderwidth=0, highlightthickness=0)
send_button.grid(row=3, column=3, padx=4)
send_button['font'] = mainfont




mainloop()






# window.mainloop()

