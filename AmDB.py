from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from sqlite3 import *
import configparser
import os



def imgtoblob(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def blobtoimg(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data[0])

allimg = str()
alldata = str()
def reloaddata():
    global allimg
    global alldata
    allimg = cur.execute("SELECT image FROM AmDB").fetchall()
    alldata = cur.execute("SELECT data FROM AmDB").fetchall()
    alldata = [i[0] for i in alldata]
    n = 0
    for i in allimg:
        blobtoimg(allimg[n],str(n)+'.png')
        n+=1
    global name
    global imgblob
    global imgf
    global data
    name = ''
    imgblob = ''
    data = ''
    imgf = ''



name = ''
imgblob = ''
data = ''
imgf = ''

def add():
    def click(*args):
        text = namet.get('1.0','end')
        if text == 'Введите информацию о реке...\n':
            namet.delete('1.0','end')
    def leave(*args):
        text = namet.get('1.0','end')
        if text == '\n':
            namet.insert('1.0',"Введите информацию о реке...")
    def click1(*args):
        text = datat.get('1.0','end')
        if text == 'Введите новую информацию о реке...\n':
            datat.delete('1.0','end')
    def leave1(*args):
        text = datat.get('1.0','end')
        if text == '\n':
            datat.insert('1.0',"Введите информацию о реке...")
    
    
    def imgopen():
        filename = filedialog.askopenfilename()
        imgn['state'] = 'normal'
        imgn.insert('1.0', filename)
        global imgf
        imgf = filename
        imgn['state'] = 'disabled'
        newentry.lift()


    def send():
        global name
        name = namet.get('1.0','end')
        global imgblob
        imgblob = imgtoblob(imgf)
        global data
        data = datat.get('1.0','end')
        record()
        newentry.destroy()
        
        
        
    newentry = Toplevel(root, bg="white")
    newentry.title("Создать")
    newentry.geometry("400x300")
    ###name
    namel = Text(newentry, width=20,height=1,border=False, font=("Arial",14))
    namel.insert('1.0', "Река:")
    namel['state'] = 'disabled'
    namel.grid(row=0,sticky='NW', padx=100)
    namet = Text(newentry, height=1,borderwidth=2, font=("Arial",12))
    namet.insert('1.0',"Введите название реки...")
    namet.bind("<Button-1>",click)
    namet.bind("<Leave>",leave)
    namet.grid(row=1,sticky='E W')
    ###img
    imgl = Text(newentry, width=5, height=1,border=False,font=("Arial",14))
    imgl.insert('1.0', "Файл:")
    imgl['state'] = 'disabled'
    imgl.grid(row=2,sticky='NW')
    imgb = Button(newentry,text='File', command=imgopen, font=("Arial",14))
    imgb.grid(row=3,sticky='NW')
    imgn = Text(newentry,height=1,border=False)
    imgn.insert('1.0', "")
    imgn['state'] = 'disabled'
    imgn.grid(row=4,sticky='NW NE')
    ###data
    datal = Text(newentry, width=30,height=1,border=False,font=("Arial",14))
    datal.insert('1.0', "Информация о реке:")
    datal['state'] = 'disabled'
    datal.grid(row=5,sticky='NW', padx=100)
    datat = Text(newentry, height=1,borderwidth=2,font=("Arial",14))
    datat.insert('1.0',"Введите информацию о реке...")
    datat.bind("<Button-1>",click1)
    datat.bind("<Leave>",leave1)
    datat.grid(row=6,sticky='NE NW SE SW')
    ###button
    done = Button(newentry,text='Создать',command=send, font=("Arial",14))
    done.grid(row=7,sticky='NW')
    newentry.columnconfigure(0,weight=1)
    newentry.rowconfigure(6,weight=1)
    
def record():
    record = "INSERT INTO AmDB(id,name,image,data) VALUES(?,?,?,?)"
    cur.execute(record,(l.size(),str(name)[0:-1],imgblob,str(data)[0:-1]))
    conn.commit()
    l.insert(l.size(),name)
    reloaddata()


def delete():
    delete = "DELETE FROM AmDB WHERE id=?"
    cur.execute(delete,(id,))
    conn.commit()
    if id < l.size():
        updateid = "UPDATE AmDB SET id=? WHERE id=?"
        for i in range(id,l.size()-id,1):
                cur.execute(updateid,(i,i+1))
    conn.commit()
    l.delete(id)
    reloaddata()

def chng():
    def imgopen():
        filename = filedialog.askopenfilename()
        imgn['state'] = 'normal'
        imgn.insert('1.0', filename)
        global imgf
        imgf = filename
        imgn['state'] = 'disabled'
        newentry.lift()


    def send():
        global name
        global imgblob
        global alldata
        if l.get(id) != namet.get('1.0','end'):
            name = namet.get('1.0','end')
        else: name = alldata[id]
        l.delete(id)
        l.insert(id,name)
        if imgf != '':
            imgblob = imgtoblob(imgf)
        else: imgblob = imgtoblob(str(id)+'.png')
        global data
        data = datat.get('1.0','end')
        update = "UPDATE AmDB SET name=?, image=?, data=? WHERE id=?"
        cur.execute(update,(str(name)[0:-1],imgblob,str(data)[0:-1],id))
        conn.commit()
        reloaddata()
        newentry.destroy()
        
        
        
    newentry = Toplevel(root, bg="white")
    newentry.title("Изменить")
    newentry.geometry("400x300")
    ###name
    namel = Text(newentry, width=30,height=1,border=False, font=("Arial",14))
    namel.insert('1.0', "Название реки:")
    namel['state'] = 'disabled'
    namel.grid(row=0,sticky='NW', padx=100)
    namet = Text(newentry, height=1,borderwidth=2,font=("Arial",12))
    namet.insert('1.0',l.get(id))
    namet.grid(row=1,sticky='E W')
    ###img
    imgl = Text(newentry, width=5, height=1,border=False,font=("Arial",14))
    imgl.insert('1.0', "Файл:")
    imgl['state'] = 'disabled'
    imgl.grid(row=2,sticky='NW')
    imgb = Button(newentry,text='File', command=imgopen,font=("Arial",14))
    imgb.grid(row=3,sticky='NW')
    imgn = Text(newentry,height=1,border=False)
    imgn.insert('1.0', "")
    imgn['state'] = 'disabled'
    imgn.grid(row=4,sticky='NW NE')
    ###data
    datal = Text(newentry, width=35,height=1,border=False,font=("Arial",14))
    datal.insert('1.0', "Информация о реке:")
    datal['state'] = 'disabled'
    datal.grid(row=5,sticky='NW',padx=100)
    datat = Text(newentry, height=1,borderwidth=2,font=("Arial",14))
    datat.insert('1.0',alldata[id])
    datat.grid(row=6,sticky='NE NW SE SW')
    ###button
    done = Button(newentry,text='Создать',command=send,font=("Arial",14))
    done.grid(row=7,sticky='NW')
    newentry.columnconfigure(0,weight=1)
    newentry.rowconfigure(6,weight=1)
    


def mod():
    messagebox.showinfo(message="База данных 'Известные реки России' \n(c) Kindarov Mansur, Russia, 2023")

def nemod():
    def click():
        top.destroy()
    top = Toplevel(root)
    top.title("О программе")
    top.geometry("420x190")
    top.title("Справка")
    canvas1 = Canvas(top)
    canvas1.place(x=0,y=0,width=420,height=190)
    canvas1.create_text(10,5, text="База данных 'Известные реки России'\nПозволят: добавлять / изменять / удалять информацию.\nКлавиши программы:\nF1 - вызов справки по программе,\nF2 - добавить в базу данных,\nF3 - удалить из базы данных,\nF4 - изменить запись в базе данных,\nF10 - меню программы", font=("Times New Roman", 12), anchor='nw')
    #b = Button(text="Закрыть", command=click)
    #.place(relx=0.5, rely=0.8, anchor="nw")
    canvas1.create_window(210, 170, anchor="nw", window=Button(canvas1, text="Закрыть", command=click))
    top.resizable(width=False, height=False)


id = 0
def selected(event):
    global id
    idnew = l.curselection()
    idnew = idnew[0]
    if id != idnew:
        id = idnew
        img1 = ImageTk.PhotoImage(Image.open(str(id)+'.png'))
        image.configure(image=img1)
        image.image = img1
        ldata['state'] = 'normal'
        ldata.delete('1.0','end')
        ldata.insert('1.0', alldata[id])
        ldata['state'] = 'disabled'
        
def find():  
    def search():
        query = search_entry.get()
        if query:
            results = []
            for i in range(l.size()):
                if query.lower() in l.get(i).lower():
                    results.append(i)
            if results:
                l.selection_clear(0, END)
                l.selection_set(results[0])
                l.activate(results[0])
                l.see(results[0]) 
                artist = l.get(results[0])
                search_label.config(text=f"Река: {artist}\n")
                click() # имитировать двойной щелчок на элементе списка
                top.destroy() # закрыть окно поиска после перехода к реке
            else:
                messagebox.showinfo(message="Река не найдена.")
        else:
            messagebox.showinfo(message="Введите реку.")

    top = Toplevel(root)
    top.title("Найти")
    top.geometry("300x100")
    search_label = Label(top, text="Введите  реку...",font=("Arial",14))
    search_label.pack()
    search_entry = Entry(top,font=("Arial",14))
    search_entry.pack()
    search_button = Button(top, text="Найти", command=search, font=("Arial",14))
    search_button.pack(side=LEFT)

def click():
    index = l.curselection()[0]
    value = l.get(index)
    messagebox.showinfo(message=f"Выбрана река: {value}")


def KeyPress(k):
    if k.keysym=='Control_L':
        exit()
    elif k.keysym=="F1":
        nemod()
    elif k.keysym=='F2':
        add()
    elif k.keysym=='F3':
        delete()
    elif k.keysym=='F4':
        chng()

def exit():
    if messagebox.askyesno("Выход","Вы действительно хотитет выйти?"):
        cur.connection.close()
        for i in range(0,l.size(),1):
            os.remove(str(i)+'.png')
        root.destroy()
        
        
# Создаем config файл AmDB.ini
config = configparser.ConfigParser()
config['User'] = {'user': 'UserName', 'keyuser': 'key'}

with open('AmDB.ini', 'w') as configfile:
    config.write(configfile)


root = Tk()


mainmenu = Menu(root) 
root.config(menu=mainmenu) 
#file menu
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Найти...", command=find)
filemenu.add_separator()
filemenu.add_command(label="Добавить      F2", command=add)
filemenu.add_command(label="Удалить         F3", command=delete)
filemenu.add_command(label="Изменить      F4", command=chng)
filemenu.add_separator()
filemenu.add_command(label="Выход            Ctrl+X", command=exit)
#help menu
helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Содержание", command=nemod)
helpmenu.add_separator()
helpmenu.add_command(label="О программе", command=mod)

mainmenu.add_cascade(label="Фонд", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)


#statusbar
statusbar = Label(root,relief=SUNKEN,bg="#113F7C",fg="white",anchor="w",text="F1-справка F2-добавить F3-удалить F4-изменить F10-меню",borderwidth=0)
statusbar.grid(column=0,row=1,columnspan=3,sticky="S SW SE")



conn = connect("AmDB.db")
cur = conn.cursor()

reloaddata()
entrys = cur.execute("SELECT name FROM AmDB").fetchall()
entrys = [i[0] for i in entrys]
choicesvar = StringVar(value=entrys)
l = Listbox(root,listvariable=choicesvar, border=2, width=16)
l.grid(column=0,row=0,sticky="S N W E")

root.geometry("800x600")


###img
img = ImageTk.PhotoImage(Image.open(str(id)+'.png'))
image = Label(root,image=img,anchor='center')
image.grid(column=1,row=0)
###text
ldata = Text(root,bg="white", width=45, wrap=WORD)
ldata.insert('1.0', alldata[id])
ldata['state'] = 'disabled'
ldata.grid(column=2,row=0,sticky='N S E')



root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.columnconfigure(2,weight=1)
root.rowconfigure(0,weight=1)
#root.rowconfigure(1,weight=1)


root.title("Известные реки России")
l.bind("<<ListboxSelect>>",selected)
root.bind("<KeyPress>",KeyPress)
#root.resizable(width=False, height=False)


root.protocol("WM_DELETE_WINDOW", exit)
root.mainloop()
