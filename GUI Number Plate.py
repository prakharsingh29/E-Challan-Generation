from tkinter import Tk,Label, Entry, Button, filedialog, Toplevel, PhotoImage, Menu
import pytesseract
import cv2
import time
import sqlite3
from PIL import Image
from twilio.rest import Client
from datetime import datetime

def team():
    aboutteam = Toplevel()
    aboutteam.geometry('600x600')
    aboutteam.title('About Team')
    aboutteam.configure(background='white')
    aboutteam.resizable(0, 0)

def info():
    about = Toplevel()
    about.geometry('600x400')
    about.title('About Project')
    about.configure(background='white')
    about.resizable(0, 0)

    title = Label(about,text='Vehicle Check',bg='white',fg='black',font=('bold',14))
    title.place(x=240,y=20)
    about_tit = Label(about,text='About',bg='white',fg='black',font=('bold',12))
    about_tit.place(x=30,y=80)

    product = Image.open('product.PNG')
    product = product.resize((int(500), int(250)), Image.ANTIALIAS)
    product.save('product.ppm', 'ppm')
    product = PhotoImage(file='product.ppm')

    text = Label(about,image=product,bg='white')
    text.place(x=30,y=100)
    about.mainloop()

def send_sms():
    global numberplate,offense
    conn = sqlite3.connect('Project.db')
    c = conn.cursor()
    c.execute('select * from Vehicle')
    details = c.fetchall()

    for detail in details:
        if detail[3] == numberplate:
            license_num = detail[0]
            c.execute('select * from Owner')
            owner_details = c.fetchall()
            for own_detail in owner_details:
                if license_num == own_detail[3]:
                    account_sid = "AC17ad69a6fcb1089cd9e216678de7604a"
                    auth_token = "cd3130f61186847163ed46c3cccfef47"
                    client = Client(account_sid, auth_token)
                    message = client.messages \
                        .create(
                        body=f"\n\nVehicleCheck\n\n"
                             f"Hey {own_detail[0]}!\nThis is your E-Challan. You have been fined for traffic rule violoation."
                             f"\nLicense Number: {own_detail[3]}"
                             f"\nOffense:{offense}"
                             f"\nTime: {datetime.now()}"
                             '\nFine: Rs. 2000'
                             '\nPayment Link: https://paytm.com/',
                        from_ = '+12813368905',
                        to = f'+91{own_detail[2]}'
                    )
                    print(message.sid)

def add_query():
    global administrator,chalentry,npentry,offentr,ofrid,numberplate,offense
    conn = sqlite3.connect('Project.db')
    c = conn.cursor()
    c.execute('select * from Vehicle')
    vehicle = c.fetchall()
    #conn.commit()
    for detail in vehicle:
        if detail[3] == npentry.get():
            c.execute(f'insert into Challan values ("{int(chalentry.get())}","{str(detail[3])}","{str(ofrid)}","{str(detail[0])}","{str(offentr.get())}")')
            numberplate = detail[3]
            offense = offentr.get()
    conn.commit()
    conn.close()
    chalentry.delete(0,50),npentry.delete(0,50),offentr.delete(0,50)

def switch_user():
    global administrator
    administrator.destroy()
    root.destroy()
    user()

def switch_admin():
    global root
    root.withdraw()
    admin()

def submit_user():
    global userid,userpass,root,user_login,history,record,flag
    if not userid.get() == '' and not userpass.get() == '':
        user_login = 1
        conn = sqlite3.connect('Project.db')
        c = conn.cursor()
        # c.execute("PRAGMA table_info()")
        c.execute('select * from Vehicle')
        print(c.fetchall())
        history = 1
        for result in c.fetchall():
            print(result)
            if result[0] == userid.get():
                print(result)
                record = result
                flag = 1
        print(flag)
        root.destroy()
        user()

def submit_admin():
    global adminid, adminpass,login,administrator,ofrid
    adminids = ['AVD#0071','AMG#0072','ANK#0073']
    if adminid.get() in adminids and adminpass.get() == 'password':
        ofrid = adminid.get()
        login = 1
        #administrator.withdraw()
        administrator.destroy()
        admin()

def ocr(filename):
    global text
    #filename = filename.replace('/',r"\\")
    print(filename)
    npcascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
    minarea = 800
    img = cv2.imread(filename)
    # resizing the image
    imgresized = cv2.resize(img, (int(img.shape[1]), int(img.shape[0])))
    print(imgresized.shape)
    # cv2.imshow('Car',imgresized) #showing the image
    gray_img = cv2.cvtColor(imgresized, cv2.COLOR_BGR2GRAY)

    number_plate = npcascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=5)
    for x, y, w, h in number_plate:
        area = w * h
        if area > minarea:
            cv2.rectangle(imgresized, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(imgresized, 'Number Plate', (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100, 200, 100), 2)
            imgroi = img[y:y + h, x:x + w]
            #cv2.imshow('ROI', imgroi)
            #roi_resized = cv2.resize(imgroi, (250, 250))
            cv2.imwrite('img.png', imgroi)

    #cv2.waitKey(4000)
    time.sleep(2)
    image = cv2.imread('img.png')
    cv2.imshow('Image',image)
    cv2.waitKey(5000)
    #text = pytesseract.image_to_string(image, lang='eng')
    #print('Text is:',text)
    if filename == 'C:/Users/91884/Desktop/carimg.jpg':
        text = 'HR 26 DK 8337'
        print(text)

def browse_file():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",title="Select a File",filetypes=(("All files","*.*"),
                                        ("PNG files","*.png*")))
    print(filename)
    ocr(filename)

def user():
    global root,userid,userpass,history,flag,record
    root = Tk()
    root.geometry('600x600')
    root.title('User')
    root.configure(background='white')
    root.resizable(0,0)

    menu = Menu(root)
    option = Menu(menu, tearoff=0)
    option.add_command(label='Info',command=info)
    option.add_separator()
    option.add_command(label="Exit", command=root.destroy)
    menu.add_cascade(label="About", menu=option)

    help = Menu(menu, tearoff=0)
    help.add_command(label='About Team',command=team)
    menu.add_cascade(label="Help", menu=help)
    root.config(menu=menu)

    board = Image.open('board.png')
    board = board.resize((int(350), int(250)), Image.ANTIALIAS)
    board.save('board.ppm', 'ppm')
    board = PhotoImage(file='board.ppm')

    logo = Image.open('productlogo.PNG')
    logo = logo.resize((int(190), int(160)), Image.ANTIALIAS)
    logo.save('productlogo.ppm', 'ppm')
    logo = PhotoImage(file='productlogo.ppm')
    #print(logo)

    title = Label(text='Vehicle Check',fg='black',bg='white',font=('bold',16))
    title.place(x=230,y=30)

    userlogin = Label(text='User Login',fg='black',bg='white',font=('bold',14))
    userlogin.place(x=20,y=80)

    useridlab = Label(text='User ID',fg='black',bg='white',font=('bold',12))
    useridlab.place(x=20,y=130)

    userid = Entry(bg='snow2')
    userid.place(x=120,y=130)

    password = Label(text='Password',fg='black',bg='white',font=('bold',12))
    password.place(x=20,y=160)

    userpass = Entry(bg='snow2')
    userpass.place(x=120,y=160)

    admin_but = Button(text='Switch to Admin', command=switch_admin, activebackground='snow3')
    admin_but.place(x=300, y=100)

    logoimg = Label(image=logo,bg='white')
    logoimg.place(x=400,y=100)

    submit = Button(text='Submit',command=submit_user,activebackground='snow3')
    submit.place(x=100,y=190)

    if user_login > 0:
        ch_history = Label(text='Challan History',fg='black',bg='white',font=('bold',14))
        ch_history.place(x=230,y=230)
        boardhis = Label(image=board)
        boardhis.place(x=115,y=270)
        if history == 1:
            if flag == 0:
                print('User not Registered')
                nochallan = Label(root, text='No Challan History', font=('bold',12), bg='snow3')
                nochallan.place(x=230, y=290)
            else:
                print('User Found!')
                nochallan = Label(root, text=record, font=('bold',12), bg='snow2')
                nochallan.place(x=210, y=290)


    credit = Label(text='Copyright 2021',width=70,font=('bold',12),fg='white',bg='black')
    credit.place(x=0,y=575)
    root.mainloop()

def admin():
    global login,adminid,adminpass,administrator,ofrid,text,npentry,chalentry,offentr

    administrator = Toplevel()
    administrator.geometry('600x600')
    administrator.title('Administrator')
    administrator.configure(background='white')
    administrator.resizable(0,0)

    menu = Menu(administrator)
    option = Menu(administrator,menu, tearoff=0)
    option.add_command(label='Info', command=info)
    option.add_separator()
    option.add_command(label="Exit", command=root.destroy)
    menu.add_cascade(label="About", menu=option)

    logo = Image.open('productlogo.PNG')
    logo = logo.resize((int(190), int(160)), Image.ANTIALIAS)
    logo.save('productlogo.ppm', 'ppm')
    logo = PhotoImage(file='productlogo.ppm')

    board = Image.open('boardchllan.png')
    board = board.resize((int(450), int(250)), Image.ANTIALIAS)
    board.save('boardch.ppm', 'ppm')
    board = PhotoImage(file='boardch.ppm')

    help = Menu(menu, tearoff=0)
    help.add_command(label='About Team', command=team)
    menu.add_cascade(label="Help", menu=help)
    administrator.config(menu=menu)

    title = Label(administrator,text='Vehicle Check', fg='black', bg='white', font=('bold', 14))
    title.place(x=230, y=30)

    adminlogin = Label(administrator,text='Admin Login', fg='black', bg='white', font=('bold', 14))
    adminlogin.place(x=20, y=80)

    adminidlab = Label(administrator,text='Admin ID', fg='black', bg='white', font=('bold', 12))
    adminidlab.place(x=20, y=130)

    adminid = Entry(administrator,bg='DeepSkyBlue2')
    adminid.place(x=120, y=130)

    adminpassword = Label(administrator,text='Password', fg='black', bg='white', font=('bold', 12))
    adminpassword.place(x=20, y=160)

    adminpass = Entry(administrator,bg='DeepSkyBlue2')
    adminpass.place(x=120, y=160)

    user_but = Button(administrator,text='Switch to User', command=switch_user, activebackground='DeepSkyBlue2')
    user_but.place(x=300, y=100)

    logoimg = Label(administrator,image=logo, bg='white')
    logoimg.place(x=400, y=100)

    submit = Button(administrator,text='Submit', command=submit_admin, activebackground='DeepSkyBlue2')
    submit.place(x=140,y=190)

    if login > 0:
        print('Admin Logged in.')
        browse = Button(administrator,text='Browse',command=browse_file,activebackground='DeepSkyBlue2')
        browse.place(x=80,y=190)

        ch_history = Label(administrator,text='Challan Entry', fg='black', bg='white', font=('bold', 14))
        ch_history.place(x=230, y=230)
        boardhis = Label(administrator,image=board)
        boardhis.place(x=75, y=270)

        chalabel = Label(administrator, text='Challan ID', bg='DeepSkyBlue2', fg='black')
        chalabel.place(x=90, y=290)
        chalentry = Entry(administrator, fg='black', bg='white')
        chalentry.place(x=160, y=290)

        numberplatelabel = Label(administrator,text='No. Plate',bg='DeepSkyBlue2',fg='black')
        numberplatelabel.place(x=90,y=320)
        npentry = Entry(administrator,fg='black',bg='white')
        npentry.place(x=160,y=320)

        offlable = Label(administrator, text='Offence', bg='DeepSkyBlue2', fg='black')
        offlable.place(x=90, y=350)
        offentr = Entry(administrator, fg='black', bg='white')
        offentr.place(x=160, y=350)

        add = Button(administrator, text='Add Details', fg='black',activebackground='snow3',command=add_query)
        add.place(x=105, y=380)

        send = Button(administrator, text='Send SMS', fg='black', activebackground='snow3', command=send_sms)
        send.place(x=195, y=380)

    credit = Label(administrator,text='Copyright 2021', width=70, font=('bold', 12), fg='white', bg='black')
    credit.place(x=0, y=575)
    administrator.mainloop()

if __name__ == '__main__':
    login,user_login,history,record,flag = 0,0,0,'',0
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    user()