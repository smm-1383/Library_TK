# needed libraries
from tkinter import messagebox as mb
from tkinter import *
from PIL import Image, ImageTk, ImageOps
from datetime import datetime as dt
from random import randint
import sqlite3 as sq
import os
from winsound import PlaySound, SND_ASYNC


# needed functions
def idmake():
    return randint(1e7, 1e8)


def papersound():
    return PlaySound('./paper-away.wav', SND_ASYNC)


def get_time_str():
    return dt.now().strftime('%Y/%m/%d | %H:%M')


def connect_make():
    if not os.path.isdir('./DB'):
        os.mkdir('./DB')
    else:
        if os.path.isfile('./DB/data.db'):
            return sq.connect('./DB/data.db')
    conn = sq.connect('./DB/data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE USERS (username TEXT, password TEXT)')
    c.execute('CREATE TABLE BOOKS (idbook INTEGER, name TEXT, author TEXT, injured INTEGER, borrower TEXT, date TEXT)')
    c.execute("INSERT INTO USERS (username, password) VALUES ('lib', '54321')")
    conn.commit()
    return conn


# Login page
class Login(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open("./LoginBack.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        headingFrame1 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame1.place(relx=0.5, rely=0.2, relwidth=0.65,
                            relheight=0.066, anchor=CENTER)
        title = Label(headingFrame1, text='Login Page of Library Management', font=(
            'Courier', 20, 'bold'), bg='black', fg='yellow')
        title.place(relx=0.5, rely=0.5, anchor=CENTER)

        headingFrame2 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame2.place(relx=0.5, rely=0.6, anchor=CENTER)

        userl = Label(headingFrame2, text='Username', font=(
            'Courier', 15), bg='black', fg='yellow')
        userl.grid(row=0, column=0)

        self.useren = Entry(headingFrame2, font=('Courier', 14))
        self.useren.grid(row=0, column=1)

        passl = Label(headingFrame2, text='Password', font=(
            'Courier', 15), bg='black', fg='yellow')
        passl.grid(row=1, column=0)

        self.passen = Entry(headingFrame2, font=('Courier', 14), show='*')
        self.passen.grid(row=1, column=1)

        headingFrame3 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame3.place(relx=0.5, rely=0.8, anchor=CENTER)

        loginbtn = Button(headingFrame3, text='Login', font=('arial', 19), relief='ridge', bg='black',
                          fg='cornsilk', command=lambda: self.login(self.useren.get(), self.passen.get()))
        loginbtn.grid(row=0, column=0)

        resetbtn = Button(headingFrame3, text='Reset', font=('arial', 19), relief='ridge',
                          bg='black', fg='cornsilk', command=lambda: self.reset(self.useren, self.passen))
        resetbtn.grid(row=0, column=1)

        quitbtn = Button(self, text='QUIT', font=(
            'Courier', 13), bg='yellow', command=self.quit)
        quitbtn.place(relx=0.99, rely=0.99, anchor=SE)

        newaccbtn = Button(self, text='Make New Account', font=(
            'Courier', 13), bg='yellow', command=lambda: self.controller.show_frame(NewAcc))
        newaccbtn.place(relx=0.01, rely=0.99, anchor=SW)

    def login(self, usr, pss):
        if self.get(usr, pss):
            self.controller.username = usr
            self.controller.password = pss
            self.reset(self.useren, self.passen)
            self.controller.show_frame(Main)
        else:
            self.reset(self.useren, self.passen)
            mb.showerror(
                'Login Error', 'Login info was not correct.\nTry again!')
            self.useren.focus()

    def reset(self, *args):
        for i in args:
            i.delete(0, END)
        args[0].focus()

    def get(self, usr, pss):
        c = self.controller.conn.cursor()
        data = c.execute('SELECT * FROM USERS').fetchall()
        return (usr, pss) in data

    def quit(self):
        self.controller.destroy()

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


# Main page
class Main(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open("./MainBack.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        headingFrame1 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame1.place(relx=0.08, rely=0.1, anchor=CENTER)

        viewbtn = Button(headingFrame1, text='View Books', font=(
            'Courier', 12), bg='black', fg='yellow', command=self.view_books)
        viewbtn.grid()

        headingFrame2 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame2.place(relx=0.08, rely=0.245, anchor=CENTER)

        borrowbtn = Button(headingFrame2, text='Borrow Book', font=(
            'Courier', 12), bg='black', fg='yellow', command=lambda: self.controller.show_frame(Borrow))
        borrowbtn.grid()

        headingFrame3 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame3.place(relx=0.08, rely=0.38, anchor=CENTER)

        takebackbtn = Button(headingFrame3, text='Take Back', font=(
            'Courier', 12), bg='black', fg='yellow', command=self.take_book_back)
        takebackbtn.grid()

        headingFrame4 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame4.place(relx=0.08, rely=0.52, anchor=CENTER)

        deletebtn = Button(headingFrame4, text='Delete Book', font=(
            'Courier', 12), bg='black', fg='yellow', command=self.del_book)
        deletebtn.grid()

        headingFrame5 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame5.place(relx=0.08, rely=0.67, anchor=CENTER)

        addbtn = Button(headingFrame5, text='Add Book', font=(
            'Courier', 12), bg='black', fg='yellow', command=lambda: self.controller.show_frame(Add))
        addbtn.grid()

        headingFrame7 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame7.place(relx=0.905, rely=0.332, anchor=CENTER)

        newaccbtn = Button(headingFrame7, text='Make a\nNew Account', font=(
            'Courier', 12), bg='black', fg='yellow', command=lambda: self.controller.show_frame(NewAcc))
        newaccbtn.grid()

        headingFrame9 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame9.place(relx=0.5, rely=0.98, anchor=S)

        quitbtn = Button(headingFrame9, text='    Quit App    ', font=(
            'Courier', 18), bg='black', fg='yellow', command=self.controller.destroy)
        quitbtn.grid()

    def view_books(self):
        papersound()
        try:
            os.mkdir('./Books')
        except:
            pass

        with open('./Books/BOOKSALL.txt', 'w') as fo:
            books = self.controller.conn.cursor().execute('SELECT * FROM BOOKS')
            fo.write('\t\t'.join(['ID', 'Name', 'Author',
                     'Injured', 'Borrower', 'Date']) + '\n')
            for i in books:
                fo.write('\t\t'.join(str(j) for j in i) + '\n')
        mb.showinfo('Done', 'The txt file has been saved successfully!')

    def take_book_back(self):
        papersound()
        root = Tk()
        root.configure(bg='cadet blue')
        root.title('Delete a Book')
        root.geometry('280x32')
        root.resizable(width=False, height=False)
        idbook = Entry(root)
        idbook.grid(row=0, column=0, padx=4)
        btnchange = Button(root, text='Give Back this book.',
                           command=lambda: self.give_this_book(idbook, root))
        btnchange.grid(row=0, column=1, padx=4, pady=3)

    def give_this_book(self, iden, root):
        idbook = iden.get()
        if len(idbook) < 5:
            mb.showerror(
                'Input Error', 'ID of book should be longer than 4 characters.')
            return
        try:
            int(idbook)
        except:
            mb.showerror('Input Error', 'ID of book should be an integer.')
            return
        c = self.controller.conn.cursor()
        if (int(idbook),) not in c.execute('SELECT idbook FROM BOOKS').fetchall():
            mb.showerror(
                'Input Error', 'This id is not a id of a saved book\nYou may wanna "Add" it first.')
            return

        if not c.execute('SELECT borrower FROM BOOKS WHERE idbook=?', (idbook,)).fetchall()[0][0]:
            mb.showerror('Input Error', 'This book hasn\'t been borrowd!')
            return
        c.execute('UPDATE BOOKS SET borrower=? WHERE idbook=?', ('', idbook))
        self.controller.conn.commit()
        mb.showinfo('Done', 'The Book took back successfully!')
        root.destroy()

    def del_book(self):
        papersound()
        root = Tk()
        root.configure(bg='cadet blue')
        root.title('Delete a Book')
        root.geometry('275x32')
        root.resizable(width=False, height=False)
        idbook = Entry(root)
        idbook.grid(row=0, column=0, padx=4)
        btnchange = Button(root, text='Delete Back this book.',
                           command=lambda: self.delete_this_book(idbook, root))
        btnchange.grid(row=0, column=1, padx=4, pady=3)

    def delete_this_book(self, idbook, r):
        try:
            idb = int(idbook.get())
        except:
            mb.showerror('Input Error', 'ID is an integer.')
            return
        c = self.controller.conn.cursor()
        if (idb,) not in c.execute('SELECT idbook FROM BOOKS').fetchall():
            mb.showerror('Input Error', 'The entered id isn\'t valid.')
            return
        c.execute('DELETE FROM BOOKS WHERE idbook=?', (f'{idb}',))
        self.controller.conn.commit()
        mb.showinfo('Info', 'The book deleted successfully.')
        r.destroy()

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


# NewAccount page
class NewAcc(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open("./NewAccBack.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        infoframe = Frame(self, bg="#FFBB00", bd=5)
        infoframe.place(relx=0.48, rely=0.4, anchor=CENTER)

        Username = StringVar()
        Password = StringVar()
        Password_re = StringVar()

        usernamelabel = Label(infoframe, text='Username', font=(
            'Courier', 14), bg='black', fg='yellow')
        usernamelabel.grid(row=0, column=0)

        usernameentry = Entry(
            infoframe, textvariable=Username, font=('Courier', 14))
        usernameentry.grid(row=0, column=1)

        passwordlabel = Label(infoframe, text='Password', font=(
            'Courier', 14), bg='black', fg='yellow')
        passwordlabel.grid(row=1, column=0)

        passwordentry = Entry(infoframe, textvariable=Password,
                              font=('Courier', 14), show='*')
        passwordentry.grid(row=1, column=1)

        password_re_label = Label(infoframe, text='Password', font=(
            'Courier', 14), bg='black', fg='yellow')
        password_re_label.grid(row=2, column=0)

        password_re_entry = Entry(
            infoframe, textvariable=Password_re, font=('Courier', 14), show='*')
        password_re_entry.grid(row=2, column=1)

        Label(infoframe, text='Repeat the password to confirm it.',
              width=30, font=('arial', 13)).grid(row=3, columnspan=2)

        headingFrame1 = Frame(self, bg="#FFBB00", bd=5)
        headingFrame1.place(relx=0.5, rely=0.92, anchor=CENTER)

        makebtn = Button(headingFrame1, text='  Make  ', font=('Courier', 18), bg='black', fg='yellow',
                         command=lambda: self.makeacc(Username.get(), Password.get(), Password_re.get()))
        makebtn.grid(row=0, column=0)

        resetbtn = Button(headingFrame1, text='  Reset  ', font=('Courier', 18), bg='black',
                          fg='yellow', command=lambda: self.reset(usernameentry, passwordentry, password_re_entry))
        resetbtn.grid(row=0, column=1)

        backbtn = Button(self, text='Back', font=('arial', 12), bg='black', fg='yellow', relief='ridge', bd=3, command=lambda: (
            self.controller.show_frame(Login), self.reset(usernameentry, passwordentry, password_re_entry)))
        backbtn.place(relx=0.89, rely=0.9)

    def makeacc(self, usr, pss, rpss):
        if pss != rpss:
            mb.showerror('Inputs Error',
                         'Passwords doesn\'t match.\nTry Again!')
            return
        if len(pss) < 5 or len(usr) < 5:
            mb.showerror(
                'Input Error', 'Passwords and Usernames should at least be 5 characters.\nTry a longer one!')
            return
        c = self.controller.conn.cursor()
        users = c.execute('SELECT username FROM USERS').fetchall()
        if (usr,) in users:
            mb.showerror(
                'Input Error', 'Selected username is already taken.\nPick another one!')
            return
        c.execute(
            'INSERT INTO USERS (username, password) VALUES (?, ?)', (usr, pss))
        self.controller.conn.commit()
        mb.showinfo('Info', 'New account is maden successfully.')

    def reset(self, *args):
        for i in args:
            i.delete(0, END)
        args[0].focus()

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


# Add page
class Add(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open("./AddBack.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        headingFrame1 = Frame(self, bg="#84412e", bd=5, padx=8, pady=1)
        headingFrame1.place(relx=0.517, rely=0.285, anchor=CENTER)

        idbookl = Label(headingFrame1, text='idbook'.title(),
                        font=('Courier', 15), bg='black', fg='yellow')
        idbookl.grid(row=0, column=0, sticky=W)

        namel = Label(headingFrame1, text='name'.title(),
                      font=('Courier', 15), bg='black', fg='yellow')
        namel.grid(row=1, column=0, sticky=W)

        authorl = Label(headingFrame1, text='author'.title(),
                        font=('Courier', 15), bg='black', fg='yellow')
        authorl.grid(row=2, column=0, sticky=W)

        injuredl = Label(headingFrame1, text='injured'.title(),
                         font=('Courier', 15), bg='black', fg='yellow')
        injuredl.grid(row=3, column=0, sticky=W)

        borrowerl = Label(headingFrame1, text='borrower'.title(), font=(
            'Courier', 15), bg='black', fg='yellow')
        borrowerl.grid(row=4, column=0, sticky=W)

        idbooken = Entry(headingFrame1, font=('arial', 12))
        idbooken.grid(row=0, column=1, sticky=E)

        nameen = Entry(headingFrame1, font=('arial', 12))
        nameen.grid(row=1, column=1, sticky=E)

        authoren = Entry(headingFrame1, font=('arial', 12))
        authoren.grid(row=2, column=1, sticky=E)

        checkvar = IntVar()
        injureden = Checkbutton(headingFrame1, bg='#84412e', variable=checkvar)
        injureden.grid(row=3, column=1)

        borroweren = Entry(headingFrame1, font=('arial', 12))
        borroweren.grid(row=4, column=1, sticky=E)

        headingFrame2 = Frame(self, bg="#84412e", padx=10, pady=6)
        headingFrame2.place(relx=0.518, rely=0.55, anchor=S)

        addbtn = Button(headingFrame2, text='   Add   ', font=('Courier', 16), bg='black', fg='yellow', command=lambda: self.add(
            idbooken.get(), nameen.get(), authoren.get(), checkvar.get(), borroweren.get()))
        addbtn.grid(row=0, column=0)

        resetbtn = Button(headingFrame2, text='   Reset   ', font=('Courier', 16), bg='black', fg='yellow', command=lambda: (
            injureden.deselect(), self.reset(idbooken, nameen, authoren, borroweren)))
        resetbtn.grid(row=0, column=1)

        backbtn = Button(self, text='Back', font=('arial', 12), bg='yellow', relief='ridge', bd=3, command=lambda: (
            self.controller.show_frame(Main), injureden.deselect(), self.reset(idbooken, nameen, authoren, borroweren)))
        backbtn.place(relx=0.9, rely=0.9, anchor=NW)

    def reset(self, *args):
        for i in args:
            i.delete(0, END)
        args[0].focus()

    def add(self, idbook, name, author, injured, borrower):
        if len(idbook) < 5:
            mb.showerror(
                'Input Error', 'ID of book should be longer than 4 characters.')
            return
        c = self.controller.conn.cursor()
        ids = c.execute('SELECT idbook FROM BOOKS').fetchall()
        if (int(idbook),) in ids:
            mb.showerror(
                'Input Error', 'The id of book is already taken.\nTry anotherone!')
            return
        c.execute('INSERT INTO BOOKS (idbook, name, author, injured, borrower, date) VALUES (?, ?, ?, ?, ?, ?)',
                  (idbook, name, author, str(injured), borrower, get_time_str()))
        self.controller.conn.commit()
        mb.showinfo('success', 'The operation was successfully.')

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


# Borrow page
class Borrow(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open("./BorrowBack.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        headingFrame1 = Frame(self, bg="yellow", bd=5)
        headingFrame1.place(relx=0.3, rely=0.4, anchor=CENTER)

        idl = Label(headingFrame1, text='ID of book:', font=('arial', 14))
        idl.grid(row=0, column=0)

        iden = Entry(headingFrame1, font=('arial', 14))
        iden.grid(row=0, column=1)

        findbtn = Button(headingFrame1, text='Find this book', font=(
            'arial', 12), command=lambda: self.get(iden.get()))
        findbtn.grid(row=1, columnspan=2)

        backbtn = Button(self, text='Back', font=('arial', 12), bg='yellow', relief='ridge',
                         bd=3, command=lambda: (self.controller.show_frame(Main), iden.delete(0, END)))
        backbtn.place(relx=0.9, rely=0.9, anchor=NW)

    def get(self, idb):
        try:
            self.headingFrame2.destroy()
        except:
            pass
        if len(idb) < 5:
            mb.showerror(
                'Input Error', 'ID of book should be longer than 4 characters.')
            return
        c = self.controller.conn.cursor()
        bks = c.execute('SELECT * FROM BOOKS WHERE idbook=?',
                        (idb,)).fetchall()
        if not bks:
            mb.showerror('Input Error', 'The entered ID isn\'t valid.')
            return

        self.show_book(bks[0])

    def show_book(self, book):
        self.headingFrame2 = Frame(self, bg="#FFBB00", bd=5)
        self.headingFrame2.place(relx=0.09, rely=0.46, anchor=NW)
        idb, name, author, injured, borrower, date = book

        if borrower:
            borrower = f'NO, Has been borrowed by {borrower}.'
        else:
            borrower = 'Yes, Available.'

        injured = {1: 'Yes', 0: 'No'}[injured]

        idl = Label(self.headingFrame2, text='ID', font=(
            'Courier', 14), bg='black', fg='yellow')
        iden = Label(self.headingFrame2, text=f'{idb}', font=(
            'arial', 14), bg='powder blue')
        idl.grid(row=0, column=0, sticky='W')
        iden.grid(row=0, column=1, sticky='E')

        namel = Label(self.headingFrame2, text='Name', font=(
            'Courier', 14), bg='black', fg='yellow')
        nameen = Label(self.headingFrame2, text=name,
                       font=('arial', 14), bg='powder blue')
        namel.grid(row=1, column=0, sticky='W')
        nameen.grid(row=1, column=1, sticky='E')

        authorl = Label(self.headingFrame2, text='Author',
                        font=('Courier', 14), bg='black', fg='yellow')
        authoren = Label(self.headingFrame2, text=author,
                         font=('arial', 14), bg='powder blue')
        authorl.grid(row=2, column=0, sticky='W')
        authoren.grid(row=2, column=1, sticky='E')

        injuredl = Label(self.headingFrame2, text='Is Injured?',
                         font=('Courier', 14), bg='black', fg='yellow')
        injureden = Label(self.headingFrame2, text=injured,
                          font=('arial', 14), bg='powder blue')
        injuredl.grid(row=3, column=0, sticky='W')
        injureden.grid(row=3, column=1, sticky='E')

        availablel = Label(self.headingFrame2, text='Is Available?', font=(
            'Courier', 14), bg='black', fg='yellow')
        availableen = Label(self.headingFrame2, text=borrower,
                            font=('arial', 14), bg='powder blue')
        availablel.grid(row=4, column=0, sticky='W')
        availableen.grid(row=4, column=1, sticky='E')

        datel = Label(self.headingFrame2, text='Date of last call',
                      font=('Courier', 14), bg='black', fg='yellow')
        dateen = Label(self.headingFrame2, text=date,
                       font=('arial', 14), bg='powder blue')
        datel.grid(row=5, column=0, sticky='W')
        dateen.grid(row=5, column=1, sticky='E')

        a = borrower.startswith('N')

        borrowbtn = Button(self.headingFrame2, text='Borrow this book.', font=(
            'Courier', 15), bg='yellow', width=35, command=lambda: self.borrow_book(idb, nameen.get()))
        borrowbtn.grid(row=6, columnspan=2)
        if a:
            borrowbtn.config(state=DISABLED)
        else:
            namel = Label(self.headingFrame2, text='Your Name: ',
                          font=('Courier', 14), bg='black', fg='yellow')
            nameen = Entry(self.headingFrame2, font=('arial', 14), width=25)
            namel.grid(row=7, column=0, sticky=W)
            nameen.grid(row=7, column=1, sticky=E)

    def borrow_book(self, idbook, name):
        if not name:
            mb.showerror('Input Error', 'Please enter your name!')
            return
        c = self.controller.conn.cursor()
        c.execute('UPDATE BOOKS SET borrower=? WHERE idbook=?', (name, idbook))
        self.controller.conn.commit()
        mb.showinfo('Done', 'The book is ready to borrow.')

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


# Main window of app
class Root(Tk):
    def __init__(self, *args, **keywargs):
        self.conn = connect_make()
        Tk.__init__(self, *args, **keywargs)
        self.geometry('800x600')
        self.resizable(width=False, height=False)
        self.title('Libray Management')
        self.iconbitmap('./icon.ico')

        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Main, Add, NewAcc, Borrow):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            self.show_frame(F, False)

        self.show_frame(Login, False)

    def show_frame(self, cont, sound=True):
        if sound:
            papersound()
        self.frames[cont].tkraise()


# run the app
app = Root()
app.mainloop()
