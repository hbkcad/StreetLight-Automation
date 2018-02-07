import tkinter as tk
from tkinter import messagebox
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import ttkcalendar
import csv
import datetime, time
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

select = ""

username = ""
password = ""

username_guess=0
password_guess=0

rb_value_area1 = 0
rb_value_manual_area1 = 0

rb_value_area2 = 0
rb_value_manual_area2 = 0

class baseclass(tk.Tk):

    def __init__(self,*args,**kwargs):

        tk.Tk.__init__(self,*args,**kwargs)

        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.title("REMOTE STREETLIGHT MANAGEMENT")

        self.frames = {}

        for F in (loginPage,startpage,areaOneAuto,areaTwoAuto,areaThreeAuto,areaFourAuto,areaOneManual,areaTwoManual,areaThreeManual,areaFourManual,area1_graph):

            page_name = F.__name__

            frame = F(parent=container,controller=self)

            self.frames[page_name] = frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame("loginPage")

    def show_frame(self,page_name):
        global check
        global check2
        global check3
        global check4
        check=0
        check2=0
        check3=0
        check4=0

        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()


class loginPage(tk.Frame):
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        img1_path=r"D:\Sumo\Main Project\python files\x2.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        global username_guess
        global password_guess

        title_label=tk.Label(self,text='Please Login to continue\n')
        title_label.place(x=550,y=150)
        title_label.config(font=('calibri',(15)),bg="black",fg="red")


        #Creating the username & password entry boxes
        username_text = tk.Label(self,text="Username")
        username_text.place(x=600,y=200)
        username_text.config(font=('calibri',(18)),bg="black",fg="white")
        
        
        username_guess = tk.Entry(self)
        username_guess.place(x=580,y=250,height=30,width=150)
        
        password_text = tk.Label(self,text="Password")
        password_text.place(x=600,y=300)
        password_text.config(font=('calibri',(18)),bg="black",fg="white")
        

        
        password_guess = tk.Entry(self,show="*")
        password_guess.place(x=580,y=350,height=30,width=150)

        #attempt to login button
        attempt_login = ttk.Button(self,text="Login",
                                  command=lambda: self.try_login(controller))
        attempt_login.place(x=590,y=430,height=33,width=130)

    def try_login(self,cont):

        global username
        global password

        uname = username_guess.get()
        pwd = password_guess.get()

        if uname == username and pwd == password:

            #print("inside if")
            cont.show_frame("startpage")
            
        else:
            messagebox.showinfo(" ERROR ", "Please enter valid infomation!", icon="warning")
                


class startpage(tk.Frame):
     

    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        

        self.controller = controller


        img1_path=r"D:\Sumo\Main Project\python files\startpagenew.gif"

        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.var = tk.StringVar()
        self.dropMenu1 = tk.OptionMenu(self, self.var, "Main Road-1","Main Road-2","Area-1","Area-2", command=self.func)
        self.dropMenu1.config(font=('calibri',(15)),bg='grey',width=12)
        self.dropMenu1['menu'].config(font=('calibri',(18)),bg='white')
        self.dropMenu1.place(x=570,y=100)

        #attempt to login button
        self.attempt_login = tk.Button(self,text="Proceed",
                                  command=lambda: self.login(controller))
        
        self.attempt_login.place(x=600,y=150,height=30,width=100)

        self.logout = tk.Button(self,text="Logout",
                                  command=lambda: controller.show_frame("loginPage"))
        
        self.logout.place(x=600,y=650,height=30,width=100)

    def func(self,val):
        global select
        select=val

    def login(self,cont):
        global select
        print (select)
        
        global v_area1
        v_area1 = tk.IntVar()
        v_area1.set(1)
            
        rb1 = tk.Radiobutton(self,text="Auto",variable=v_area1,value=1,command=self.radio_select)
        rb1.place(x=650,y=350,anchor="center")
        rb2 = tk.Radiobutton(self,text="Remote Switch",variable=v_area1,value=2,command=self.radio_select)
        rb2.place(x=650,y=400,anchor="center")


        rb1.config(font=('calibri',(15)),width=10)
        rb2.config(font=('calibri',(15)),width=20,highlightcolor="green")

        back = ttk.Button(self,text="Go",
                                  command=lambda: self.movetonext(cont))
        back.place(x=595,y=450,height=35,width=110)
        
        
    def radio_select(self):
        global v_area1
        global rb_value_area1
        rb_value_area1 = v_area1.get()
        print (rb_value_area1)

    def movetonext(self,controller):

        global rb_value_area1
        global select
        
        print (rb_value_area1)
        if (rb_value_area1 == 1 and select=="Main Road-1"):
                #print ("inside area 1 auto if")
            controller.show_frame("areaOneAuto")
        if (rb_value_area1 == 2 and select=="Main Road-1"):
            controller.show_frame("areaOneManual")


        if (rb_value_area1 == 1 and select=="Main Road-2"):
                #print ("inside area 1 auto if")
            controller.show_frame("areaTwoAuto")
        if (rb_value_area1 == 2 and select=="Main Road-2"):
            controller.show_frame("areaTwoManual")


        if (rb_value_area1 == 1 and select=="Area-1"):
                #print ("inside area 1 auto if")
            controller.show_frame("areaThreeAuto")
        if (rb_value_area1 == 2 and select=="Area-1"):
            controller.show_frame("areaThreeManual")


        if (rb_value_area1 == 1 and select=="Area-2"):
                #print ("inside area 1 auto if")
            controller.show_frame("areaFourAuto")
        if (rb_value_area1 == 2 and select=="Area-2"):
            controller.show_frame("areaFourManual")


        
class areaOneAuto(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        self.controller = controller

        img1_path=r"D:\Sumo\Main Project\python files\area1 light.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_image1=r"D:\Sumo\Main Project\python files\lambo2.gif"
        self.btn_img1 = tk.PhotoImage(file=button_image1)

        button_image2=r"D:\Sumo\Main Project\python files\lambo.gif"
        self.btn_img2 = tk.PhotoImage(file=button_image2)

        title_label=tk.Label(self,text='Main Road-1 Auto\n',font=("Utopia",20),fg="green")
        title_label.place(x=10,y=100)

        global IR_label1
        global IR_label2

        IR_label1=tk.Label(self,font=("Utopia",10),image=self.btn_img1,compound="center",width="20",height="30")
        IR_label1.place(x=620,y=0)
        IR_label1.place_forget()

        IR_label2=tk.Label(self,font=("Utopia",10),image=self.btn_img2,compound="center",width="20",height="30")
        IR_label2.place(x=540,y=650)
        IR_label2.place_forget()
        

        global a1l1
        global a1l2
        global a1l3
        global a1l4
        global a1l5
        global a1l6
        global a1l1a
        global a1l2a
        global a1l3a
        global a1l4a
        global a1l5a
        global a1l6a

        a1l1=tk.Label(self,text='L1')
        a1l1.place(x=550,y=0)
        a1l1a=tk.Label(self,text='L1')
        a1l1a.place(x=595,y=0)

        a1l2=tk.Label(self,text='L2')
        a1l2.place(x=550,y=130)
        a1l2a=tk.Label(self,text='L2')
        a1l2a.place(x=595,y=130)

        a1l3=tk.Label(self,text='L3')
        a1l3.place(x=550,y=260)
        a1l3a=tk.Label(self,text='L3')
        a1l3a.place(x=595,y=260)

        a1l4=tk.Label(self,text='L4')
        a1l4.place(x=550,y=380)
        a1l4a=tk.Label(self,text='L4')
        a1l4a.place(x=595,y=380)

        a1l5=tk.Label(self,text='L5')
        a1l5.place(x=550,y=500)
        a1l5a=tk.Label(self,text='L5')
        a1l5a.place(x=595,y=500)
        
        a1l6=tk.Label(self,text='L6')
        a1l6.place(x=550,y=620)  
        a1l6a=tk.Label(self,text='L6')
        a1l6a.place(x=595,y=620)

        refresh = ttk.Button(self,text="Refresh",command = lambda: self.connect(controller,parent))
        refresh.place(x=1100,y=100,height=40,width=100)

        
        back = ttk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("startpage"))
        back.place(x=0,y=0,height=40,width=100)
            
        #view_graph = ttk.Button(self,text="View graph",   command=lambda: controller.show_frame("area1_graph"))
        #view_graph.place(x=1100,y=160,height=40,width=100)


    def connect(self,cont,parent):
        global check
        global autocheck1
        autocheck1=0
        check=1
        print ("inside area 1 auto if")
        response = urlopen("http://192.168.1.63/")
        #response = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
        if autocheck1==1:
            response = urlopen("http://192.168.1.63/LED=AUTO")
        htmlString = response.read()

        print (htmlString)

        while check == 1:
            parent.update()
            page = urlopen("http://192.168.1.63/")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
            if autocheck1==1:
                page = urlopen("http://192.168.1.63/LED=AUTO")

            try:
                soup = BeautifulSoup(page.read(),"html.parser")
                print(soup)
                l1=soup.find('p',attrs={'class':'l8'})
                l1=l1.string.strip()
                
                time.sleep(2)

                ir1=soup.find('p',attrs={'class':'IR1'})
                ir1=ir1.string.strip()
                print("ir1=",ir1)

                ir2=soup.find('p',attrs={'class':'IR2'})
                ir2=ir2.string.strip()
                print("ir1=",ir2)

            except AttributeError as e:
                print(e)

            global a1l1
            global a1l2
            global a1l3
            global a1l4
            global a1l5
            global a1l6
            global a1l1a
            global a1l2a
            global a1l3a
            global a1l4a
            global a1l5a
            global a1l6a

            global IR_label1
            global IR_label2

            if ir1=='1':
                print("inside ir1 if")
                IR_label1.place(x=620,y=0)

                light1='ON'
                light2='ON'
                light3='ON'
                light4='ON'
                light5='ON'
                light6='ON'

                a1l1.config(bg = "gold")
                a1l1a.config(bg = "gold")
                a1l2.config(bg = "gold")
                a1l2a.config(bg = "gold")
                a1l3.config(bg = "gold")
                a1l3a.config(bg = "gold")
                
            else:
                IR_label1.place_forget()

                light1='MID'
                light2='MID'
                light3='MID'
                light4='MID'
                light5='MID'
                light6='MID'

                a1l1.config(bg = "light goldenrod")
                a1l1a.config(bg = "light goldenrod")
                a1l2.config(bg = "light goldenrod")
                a1l2a.config(bg = "light goldenrod")
                a1l3.config(bg = "light goldenrod")
                a1l3a.config(bg = "light goldenrod")

            if ir2=='1':
                print("inside ir2 if")
                IR_label2.place(x=520,y=650)

                light1='ON'
                light2='ON'
                light3='ON'
                light4='ON'
                light5='ON'
                light6='ON'
                light7='ON'
                light8='ON'
                light9='ON'
                light10='ON'
                light11='ON'
                light12='ON'

                a1l1.config(bg = "gold")
                a1l1a.config(bg = "gold")
                a1l2.config(bg = "gold")
                a1l2a.config(bg = "gold")
                a1l3.config(bg = "gold")
                a1l3a.config(bg = "gold")
                a1l4.config(bg = "gold")
                a1l4a.config(bg ="gold")
                a1l5.config(bg = "gold")
                a1l5a.config(bg ="gold")
                a1l6.config(bg = "gold")
                a1l6a.config(bg ="gold")
                
            else:
                IR_label2.place_forget()
            
            if l1=='2' and ir1=='0':
                
                light1='ON'
                light2='ON'
                light3='ON'
                light4='ON'
                light5='ON'
                light6='ON'
                light7='ON'
                light8='ON'
                light9='ON'
                light10='ON'
                light11='ON'
                light12='ON'

                a1l1.config(bg = "gold")
                a1l1a.config(bg = "gold")
                a1l2.config(bg = "gold")
                a1l2a.config(bg = "gold")
                a1l3.config(bg = "gold")
                a1l3a.config(bg = "gold")
                a1l4.config(bg = "gold")
                a1l4a.config(bg ="gold")
                a1l5.config(bg = "gold")
                a1l5a.config(bg ="gold")
                a1l6.config(bg = "gold")
                a1l6a.config(bg ="gold")

                
            elif l1=='1':

                IR_label1.place_forget()

                light1='MID'
                light2='MID'
                light3='MID'
                light4='MID'
                light5='MID'
                light6='MID'
                light7='MID'
                light8='MID'
                light9='MID'
                light10='MID'
                light11='MID'
                light12='MID'
                
                a1l1.config(bg = "light goldenrod")
                a1l1a.config(bg = "light goldenrod")
                a1l2.config(bg = "light goldenrod")
                a1l2a.config(bg = "light goldenrod")
                a1l3.config(bg = "light goldenrod")
                a1l3a.config(bg = "light goldenrod")
                a1l4.config(bg = "light goldenrod")
                a1l4a.config(bg ="light goldenrod")
                a1l5.config(bg = "light goldenrod")
                a1l5a.config(bg ="light goldenrod")
                a1l6.config(bg = "light goldenrod")
                a1l6a.config(bg ="light goldenrod")
                
            elif l1=='0':

                IR_label1.place_forget()
                
                light1='OFF'
                light2='OFF'
                light3='OFF'
                light4='OFF'
                light5='OFF'
                light6='OFF'
                light7='OFF'
                light8='OFF'
                light9='OFF'
                light10='OFF'
                light11='OFF'
                light12='OFF'
                
                
                a1l1.config(bg = "white")
                a1l1a.config(bg = "white")
                a1l2.config(bg = "white")
                a1l2a.config(bg = "white")
                a1l3.config(bg = "white")
                a1l3a.config(bg = "white")
                a1l4.config(bg = "white")
                a1l4a.config(bg = "white")
                a1l5.config(bg = "white")
                a1l5a.config(bg = "white")
                a1l6.config(bg = "white")
                a1l6a.config(bg = "white")
                

            lux_val=80
            i = datetime.datetime.now()
            cur_date="%s/%s/%s"%(i.day,i.month,i.year)

            cur_time=time.strftime("%X")

            print("current date: ",cur_date,"\n")
            print("current time: ",cur_time,"\n")

                   
            path = "output sample.csv"

            with open(path,'a') as csv_file: 
                c=csv.writer(csv_file)
                c.writerow(["Main Road-1",cur_date,cur_time,lux_val,light1,light2,light3,light4,light5,light6,light7,light8,light9,light10,light11,light12])

            parent.update()

class area1_graph(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        
        back = ttk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("areaOneAuto"))
        back.place(x=0,y=0,height=40,width=100)

        """
        dates = []
        times = []
        col3_list = []
        col4_list = []
        col5_list = []
        with open('output sample.csv', 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                date, time, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16 = row

                
                col4 = 1 if col4 == 'ON' else 0
                col5 = 1 if col5 == 'ON' else 0

                dates.append(date)
                times.append(time)
                col3_list.append(col3)
                col4_list.append(col4)
                col5_list.append(col5)
                f = Figure(figsize=(7,7), dpi=100)
                a=f.add_subplot(111)
                a.plot(col3_list) 

                a.set_xticks(list(range(len(dates))), dates)

                #a.set_xticks(rotation=70)
                a.set_xticklabels(dates,rotation=70)

                #plt.tight_layout()
                a.set_ylabel('LUX')
                a.set_xlabel('Date')
                canvas = FigureCanvasTkAgg(f,self)
                canvas.show()
                canvas.get_tk_widget().pack(anchor="center")
                toolbar = NavigationToolbar2TkAgg(canvas, self)
                toolbar.update()
                canvas._tkcanvas.pack(anchor="center")

        """
        


class areaTwoAuto(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        self.controller = controller

        img1_path=r"D:\Sumo\Main Project\python files\area2 light.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        title_label=tk.Label(self,text='Main Road-2 Auto\n',font=("Utopia",20,),fg="green")
        title_label.place(x=10,y=100)

        button_image1=r"D:\Sumo\Main Project\python files\for2.gif"
        self.btn_img1 = tk.PhotoImage(file=button_image1)

        button_image2=r"D:\Sumo\Main Project\python files\for1.gif"
        self.btn_img2 = tk.PhotoImage(file=button_image2)

        global IR_label3
        global IR_label4

        IR_label3=tk.Label(self,font=("Utopia",10),image=self.btn_img1,compound="center",text="IR3",width="20",height="20")
        IR_label3.place(x=610,y=290)
        IR_label3.place_forget()

        IR_label4=tk.Label(self,font=("Utopia",10),image=self.btn_img1,compound="center",text="IR4",width="20",height="20")
        IR_label4.place(x=990,y=390)
        IR_label4.place_forget()
        
        global a2l1
        global a2l2
        global a2l3
        global a2l4
        global a2l5
        global a2l6
        global a2l1a
        global a2l2a
        global a2l3a
        global a2l4a
        global a2l5a
        global a2l6a

        a2l1=tk.Label(self,text='L1')
        a2l1.place(x=395,y=315)
        a2l1a=tk.Label(self,text='L1')
        a2l1a.place(x=395,y=380)

        a2l2=tk.Label(self,text='L2')
        a2l2.place(x=510,y=315)
        a2l2a=tk.Label(self,text='L2')
        a2l2a.place(x=510,y=380)

        a2l3=tk.Label(self,text='L3')
        a2l3.place(x=620,y=315)
        a2l3a=tk.Label(self,text='L3')
        a2l3a.place(x=620,y=380)

        a2l4=tk.Label(self,text='L4')
        a2l4.place(x=735,y=315)
        a2l4a=tk.Label(self,text='L4')
        a2l4a.place(x=735,y=380)

        a2l5=tk.Label(self,text='L5')
        a2l5.place(x=845,y=315)
        a2l5a=tk.Label(self,text='L5')
        a2l5a.place(x=845,y=380)

        a2l6=tk.Label(self,text='L6')
        a2l6.place(x=960,y=315)
        a2l6a=tk.Label(self,text='L6')
        a2l6a.place(x=960,y=380)


        refresh = ttk.Button(self,text="Refresh",command = lambda: self.connect(controller,parent))
        refresh.place(x=1100,y=100,height=40,width=100)

        
        back = ttk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("startpage"))
        back.place(x=0,y=0,height=40,width=100)
            
        #view_graph = ttk.Button(self,text="View graph",command=lambda: controller.show_frame("area2_graph"))
        #view_graph.place(x=1100,y=160,height=40,width=100)



    def connect(self,cont,parent):
        global check2
        check2=1
        global autocheck2
        autocheck2=0

        print ("inside area 2 auto if")
        page = urlopen("http://192.168.1.116/")
        #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")

        if autocheck2==1:
                page = urlopen("http://192.168.1.116/LED=AUTO")

        htmlString = page.read()
        print (htmlString)

        while check2 == 1:
            parent.update()
            page = urlopen("http://192.168.1.116/")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
            if autocheck2==1:
                page = urlopen("http://192.168.1.116/LED=AUTO")
            try:
                soup = BeautifulSoup(page.read(),"html.parser")
                print(soup)
                l1=soup.find('p',attrs={'class':'l8'})
                l1=l1.string.strip()
                time.sleep(2)

                ir3=soup.find('p',attrs={'class':'IR1'})
                ir3=ir3.string.strip()
                print("ir3=",ir3)

                ir4=soup.find('p',attrs={'class':'IR2'})
                ir4=ir4.string.strip()
                print("ir4=",ir4)

            except AttributeError as e:
                print(e)

            global a2l1
            global a2l2
            global a2l3
            global a2l4
            global a2l5
            global a2l6
            global a2l1a
            global a2l2a
            global a2l3a
            global a2l4a
            global a2l5a
            global a2l6a

            global IR_label3
            global IR_label4

            if ir3=='1':
                IR_label3.place(x=610,y=290)

                light5='ON'
                light6='ON'
                light7='ON'
                light8='ON'
                light9='ON'
                light10='ON'
                light11='ON'
                light12='ON'

                a2l3.config(bg="gold")
                a2l3a.config(bg="gold")
                a2l4.config(bg="gold")
                a2l4a.config(bg="gold")
                a2l5.config(bg="gold")
                a2l5a.config(bg="gold")
                a2l6.config(bg="gold")
                a2l6a.config(bg="gold")
                
            else:
                IR_label3.place_forget()

            if ir4=='1':
                IR_label4.place(x=990,y=390)

                light1='ON'
                light2='ON'
                light3='ON'
                light4='ON'
                light5='ON'
                light6='ON'
                light7='ON'
                light8='ON'
                light9='ON'
                light10='ON'
                light11='ON'
                light12='ON'
                    
                a2l1.config(bg = "gold")
                a2l1a.config(bg = "gold")
                a2l2.config(bg = "gold")
                a2l2a.config(bg = "gold")
                a2l3.config(bg = "gold")
                a2l3a.config(bg = "gold")
                a2l4.config(bg = "gold")
                a2l4a.config(bg ="gold")
                a2l5.config(bg = "gold")
                a2l5a.config(bg ="gold")
                a2l6.config(bg = "gold")
                a2l6a.config(bg ="gold")
            else:
                IR_label4.place_forget()

            if l1=='2' and ir3=='0':
                light1='ON'
                light2='ON'
                light3='ON'
                light4='ON'
                light5='ON'
                light6='ON'
                light7='ON'
                light8='ON'
                light9='ON'
                light10='ON'
                light11='ON'
                light12='ON'
                    
                a2l1.config(bg = "gold")
                a2l1a.config(bg = "gold")
                a2l2.config(bg = "gold")
                a2l2a.config(bg = "gold")
                a2l3.config(bg = "gold")
                a2l3a.config(bg = "gold")
                a2l4.config(bg = "gold")
                a2l4a.config(bg ="gold")
                a2l5.config(bg = "gold")
                a2l5a.config(bg ="gold")
                a2l6.config(bg = "gold")
                a2l6a.config(bg ="gold")
                    
                    
            elif l1=='1':

                light1='MID'
                light2='MID'
                light3='MID'
                light4='MID'
                light5='MID'
                light6='MID'
                light7='MID'
                light8='MID'
                light9='MID'
                light10='MID'
                light11='MID'
                light12='MID'
                    
                a2l1.config(bg = "light goldenrod")
                a2l1a.config(bg = "light goldenrod")
                a2l2.config(bg = "light goldenrod")
                a2l2a.config(bg = "light goldenrod")
                a2l3.config(bg = "light goldenrod")
                a2l3a.config(bg = "light goldenrod")
                a2l4.config(bg = "light goldenrod")
                a2l4a.config(bg ="light goldenrod")
                a2l5.config(bg = "light goldenrod")
                a2l5a.config(bg ="light goldenrod")
                a2l6.config(bg = "light goldenrod")
                a2l6a.config(bg ="light goldenrod")
                    
            elif l1=='0':
                light1='OFF'
                light2='OFF'
                light3='OFF'
                light4='OFF'
                light5='OFF'
                light6='OFF'
                light7='OFF'
                light8='OFF'
                light9='OFF'
                light10='OFF'
                light11='OFF'
                light12='OFF'
                    
                    
                a2l1.config(bg = "white")
                a2l1a.config(bg = "white")
                a2l2.config(bg = "white")
                a2l2a.config(bg = "white")
                a2l3.config(bg = "white")
                a2l3a.config(bg = "white")
                a2l4.config(bg = "white")
                a2l4a.config(bg = "white")
                a2l5.config(bg = "white")
                a2l5a.config(bg = "white")
                a2l6.config(bg = "white")
                a2l6a.config(bg = "white")
                            

            lux_val=80
            i = datetime.datetime.now()
            cur_date="%s/%s/%s"%(i.day,i.month,i.year)

            cur_time=time.strftime("%X")

            print("current date: ",cur_date,"\n")
            print("current time: ",cur_time,"\n")

                       
            path = "output sample.csv"

            with open(path,'a') as csv_file: 
                c=csv.writer(csv_file)
                c.writerow(["Main Road-2",cur_date,cur_time,lux_val,light1,light2,light3,light4,light5,light6,light7,light8,light9,light10,light11,light12])

                parent.update()



class areaThreeAuto(tk.Frame):

    def __init__(self, parent, controller):
        

        tk.Frame.__init__(self,parent)

        self.controller = controller

        img1_path=r"D:\Sumo\Main Project\python files\area3 light.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        title_label=tk.Label(self,text='Area 3 Auto\n',font=("Utopia",20,),fg="green")
        title_label.place(x=10,y=100)
        
        global a3l1
        global a3l2
        global a3l3
        global a3l4
        global a3l5
        global a3l6
        global a3l7
        global a3l8
        global a3l9
        global a3l10
        global a3l11
        global a3l12




        a3l1=tk.Label(self,text='L1')
        a3l1.place(x=635,y=145)
        
        a3l2=tk.Label(self,text='L2')
        a3l2.place(x=805,y=85)

        a3l3=tk.Label(self,text='L3')
        a3l3.place(x=745,y=150)
        
        a3l4=tk.Label(self,text='L4')
        a3l4.place(x=720,y=240)

        a3l5=tk.Label(self,text='L5')
        a3l5.place(x=655,y=245)
        
        a3l6=tk.Label(self,text='L6')
        a3l6.place(x=935,y=155)
        
        a3l7=tk.Label(self,text='L7')
        a3l7.place(x=805,y=260)
        
        a3l8=tk.Label(self,text='L8')
        a3l8.place(x=655,y=85)

        a3l9=tk.Label(self,text='L9')
        a3l9.place(x=705,y=0)
        
        a3l10=tk.Label(self,text='L10')
        a3l10.place(x=635,y=0)

        a3l11=tk.Label(self,text='L11')
        a3l11.place(x=925,y=0)
    
        a3l12=tk.Label(self,text='L12')
        a3l12.place(x=805,y=0)
   
        refresh = ttk.Button(self,text="Refresh",command = lambda: self.connect(controller,parent))
        refresh.place(x=1100,y=100,height=40,width=100)
        
        back = ttk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("startpage"))
        back.place(x=0,y=0,height=40,width=100)
            
        #view_graph = ttk.Button(self,text="View graph",command=lambda: controller.show_frame("area3_graph"))
        #view_graph.place(x=1100,y=160,height=40,width=100)


    def connect(self,cont,parent):
        global check3
        global autocheck3
        check3=1
        autocheck3=0
        print ("inside area 3 auto if")
        response = urlopen("http://192.168.1.247/")
        if autocheck3==1:
                response = urlopen("http://192.168.1.247/AUTO")

        htmlString = response.read()

        print (htmlString)

        while check3 == 1:
            parent.update()
            page = urlopen("http://192.168.1.247/")
            if autocheck3==1:
                page = urlopen("http://192.168.1.247/AUTO")

            try:
                soup = BeautifulSoup(page.read(),"html.parser")
                print(soup)
                l1=soup.find('p',attrs={'class':'l1'})
                print(l1)
                l1=l1.string.strip()
                l2=soup.find('p',attrs={'class':'l2'})
                l2=l2.string.strip()
                l3=soup.find('p',attrs={'class':'l3'})
                l3=l3.string.strip()
                l4=soup.find('p',attrs={'class':'l4'})
                l4=l4.string.strip()
                l5=soup.find('p',attrs={'class':'l5'})
                l5=l5.string.strip()
                l6=soup.find('p',attrs={'class':'l6'})
                l6=l6.string.strip()
                l7=soup.find('p',attrs={'class':'l7'})
                l7=l7.string.strip()
                l8=soup.find('p',attrs={'class':'l8'})
                l8=l8.string.strip()
                l9=soup.find('p',attrs={'class':'l9'})
                l9=l9.string.strip()
                l10=soup.find('p',attrs={'class':'l10'})
                l10=l10.string.strip()
                l11=soup.find('p',attrs={'class':'l11'})
                l11=l11.string.strip()
                l12=soup.find('p',attrs={'class':'l12'})
                l12=l12.string.strip()
                
                time.sleep(3)

            except AttributeError as e:
                print(e)

            global a3l1
            global a3l2
            global a3l3
            global a3l4
            global a3l5
            global a3l6
            global a3l7
            global a3l8
            global a3l9
            global a3l10
            global a3l11
            global a3l12

            
            if l1=='2':
                light1='ON'  
                a3l1.config(bg = "gold")
            elif l1=='1':
                light1='MID'          
                a3l1.config(bg = "light goldenrod")
            else:
                light1='OFF'               
                a3l1.config(bg = "white")
            if l2=='2':
                light2='ON'
                a3l2.config(bg = "gold")
            elif l2=='1':
                light2='MID'          
                a3l2.config(bg = "light goldenrod")
            else:
                light2='OFF'               
                a3l2.config(bg = "white")
            if l3=='2':
                light3='ON'
                a3l3.config(bg = "gold")
            elif l3=='1':
                light3='MID'          
                a3l3.config(bg = "light goldenrod")
            else:
                light3='OFF'               
                a3l3.config(bg = "white")
            if l4=='2':
                light4='ON'
                a3l4.config(bg = "gold")
            elif l4=='1':
                light4='MID'          
                a3l4.config(bg = "light goldenrod")
            else:
                light4='OFF'               
                a3l4.config(bg = "white")
            if l5=='2':
                light5='ON'
                a3l5.config(bg = "gold")
            elif l5=='1':
                light5='MID'          
                a3l5.config(bg = "light goldenrod")
            else:
                light5='OFF'               
                a3l5.config(bg = "white")
            if l6=='2':
                light6='ON'
                a3l6.config(bg = "gold")
            elif l6=='1':
                light6='MID'          
                a3l6.config(bg = "light goldenrod")
            else:
                light6='OFF'               
                a3l6.config(bg = "white")
            if l7=='2':
                light7='ON'
                a3l7.config(bg = "gold")
            elif l7=='1':
                light7='MID'          
                a3l7.config(bg = "light goldenrod")
            else:
                light7='OFF'               
                a3l7.config(bg = "white")
            if l8=='2':
                light8='ON'
                a3l8.config(bg ="gold")
            elif l8=='1':
                light8='MID'          
                a3l8.config(bg = "light goldenrod")
            else:
                light8='OFF'               
                a3l8.config(bg = "white")
            if l9=='2':
                light9='ON'
                a3l9.config(bg = "gold")
            elif l9=='1':
                light9='MID'          
                a3l9.config(bg = "light goldenrod")
            else:
                light9='OFF'               
                a3l9.config(bg = "white")
            if l10=='2':
                light10='ON'
                a3l10.config(bg ="gold")
            elif l10=='1':
                light10='MID'          
                a3l10.config(bg = "light goldenrod")
            else:
                light10='OFF'               
                a3l10.config(bg = "white")
            if l11=='2':
                light11='ON'
                a3l11.config(bg = "gold")
            elif l11=='1':
                light11='MID'          
                a3l11.config(bg = "light goldenrod")
            else:
                light11='OFF'               
                a3l11.config(bg = "white")
            if l12=='2':
                light12='ON'
                a3l12.config(bg ="gold")
            elif l12=='1':
                light12='MID'          
                a3l12.config(bg = "light goldenrod")
            else:
                light12='OFF'               
                a3l12.config(bg = "white")            

            

            lux_val=80
            i = datetime.datetime.now()
            cur_date="%s/%s/%s"%(i.day,i.month,i.year)

            cur_time=time.strftime("%X")

            print("current date: ",cur_date,"\n")
            print("current time: ",cur_time,"\n")

                   
            path = "output sample.csv"

            with open(path,'a') as csv_file: 
                c=csv.writer(csv_file)
                c.writerow(["Area-1",cur_date,cur_time,lux_val,light1,light2,light3,light4,light5,light6,light7,light8,light9,light10,light11,light12])

            parent.update()

      

class areaFourAuto(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        self.controller = controller

        img1_path=r"D:\Sumo\Main Project\python files\area4 light.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        title_label=tk.Label(self,text='Area 1 Auto\n',font=("Utopia",20,),fg="green")
        title_label.place(x=10,y=100)
        
        global a4l1
        global a4l2
        global a4l3
        global a4l4
        global a4l5
        global a4l6
        global a4l7
        global a4l8
        global a4l9
        global a4l10
        global a4l11
        global a4l12

       
        a4l1=tk.Label(self,text='L1')
        a4l1.place(x=655,y=400)
        
        a4l2=tk.Label(self,text='L2')
        a4l2.place(x=725,y=425)

        a4l3=tk.Label(self,text='L3')
        a4l3.place(x=815,y=455)
        
        a4l4=tk.Label(self,text='L4')
        a4l4.place(x=945,y=450)

        a4l5=tk.Label(self,text='L5')
        a4l5.place(x=635,y=495)
        
        a4l6=tk.Label(self,text='L6')
        a4l6.place(x=723,y=510)
        
        a4l7=tk.Label(self,text='L7')
        a4l7.place(x=660,y=580)
        
        a4l8=tk.Label(self,text='L8')
        a4l8.place(x=820,y=590)

        a4l9=tk.Label(self,text='L9')
        a4l9.place(x=955,y=590)
        
        a4l10=tk.Label(self,text='L10')
        a4l10.place(x=635,y=660)

        a4l11=tk.Label(self,text='L11')
        a4l11.place(x=720,y=660)
        
        a4l12=tk.Label(self,text='L12')
        a4l12.place(x=885,y=670)

    
          
        refresh = tk.Button(self,text="Refresh",command = lambda: self.connect(controller,parent))
        refresh.place(x=1100,y=100,height=40,width=100)

        back = tk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("startpage"))
        back.place(x=0,y=0,height=40,width=100)
            
        #view_graph = ttk.Button(self,text="View graph",command=lambda: controller.show_frame("area4_graph"))
        #view_graph.place(x=1100,y=160,height=40,width=100)


    def connect(self,cont,parent):
        global check4
        global autocheck4
        autocheck4=0
        check4=1
        print ("inside area 4 auto if")
        response = urlopen("http://192.168.1.151/")
        if autocheck4==1:
                response = urlopen("http://192.168.1.151/AUTO")

        htmlString = response.read()

        print (htmlString)

        while check4 == 1:
            parent.update()
            page = urlopen("http://192.168.1.151/")
            if autocheck4==1:
                page = urlopen("http://192.168.1.151/AUTO")
            try:
                soup = BeautifulSoup(page.read(),"html.parser")
                l1=soup.find('p',attrs={'class':'l1'})
                l1=l1.string.strip()
                l2=soup.find('p',attrs={'class':'l2'})
                l2=l2.string.strip()
                l3=soup.find('p',attrs={'class':'l3'})
                l3=l3.string.strip()
                l4=soup.find('p',attrs={'class':'l4'})
                l4=l4.string.strip()
                l5=soup.find('p',attrs={'class':'l5'})
                l5=l5.string.strip()
                l6=soup.find('p',attrs={'class':'l6'})
                l6=l6.string.strip()
                l7=soup.find('p',attrs={'class':'l7'})
                l7=l7.string.strip()
                l8=soup.find('p',attrs={'class':'l8'})
                l8=l8.string.strip()
                l9=soup.find('p',attrs={'class':'l9'})
                l9=l9.string.strip()
                l10=soup.find('p',attrs={'class':'l10'})
                l10=l10.string.strip()
                l11=soup.find('p',attrs={'class':'l11'})
                l11=l11.string.strip()
                l12=soup.find('p',attrs={'class':'l12'})
                l12=l12.string.strip()
                print(l1)
                time.sleep(5)

            except AttributeError as e:
                print(e)

            global a4l1
            global a4l2
            global a4l3
            global a4l4
            global a4l5
            global a4l6
            global a4l7
            global a4l8
            global a4l9
            global a4l10
            global a4l11
            global a4l12

            
            if l1=='2':
                light1='ON'  
                a4l1.config(bg = "gold")
            elif l1=='1':
                light1='MID'          
                a4l1.config(bg = "light goldenrod")
            else:
                light1='OFF'               
                a4l1.config(bg = "white")
            if l2=='2':
                light2='ON'
                a4l2.config(bg = "gold")
            elif l2=='1':
                light2='MID'          
                a4l2.config(bg = "light goldenrod")
            else:
                light2='OFF'               
                a4l2.config(bg = "white")
            if l3=='2':
                light3='ON'
                a4l3.config(bg = "gold")
            elif l3=='1':
                light3='MID'          
                a4l3.config(bg = "light goldenrod")
            else:
                light3='OFF'               
                a4l3.config(bg = "white")
            if l4=='2':
                light4='ON'
                a4l4.config(bg = "gold")
            elif l4=='1':
                light4='MID'          
                a4l4.config(bg = "light goldenrod")
            else:
                light4='OFF'               
                a4l4.config(bg = "white")
            if l5=='2':
                light5='ON'
                a4l5.config(bg = "gold")
            elif l5=='1':
                light5='MID'          
                a4l5.config(bg = "light goldenrod")
            else:
                light5='OFF'               
                a4l5.config(bg = "white")
            if l6=='2':
                light6='ON'
                a4l6.config(bg = "gold")
            elif l6=='1':
                light6='MID'          
                a4l6.config(bg = "light goldenrod")
            else:
                light6='OFF'               
                a4l6.config(bg = "white")
            if l7=='2':
                light7='ON'
                a4l7.config(bg = "gold")
            elif l7=='1':
                light7='MID'          
                a4l7.config(bg = "light goldenrod")
            else:
                light7='OFF'               
                a4l7.config(bg = "white")
            if l8=='2':
                light8='ON'
                a4l8.config(bg ="gold")
            elif l8=='1':
                light8='MID'          
                a4l8.config(bg = "light goldenrod")
            else:
                light8='OFF'               
                a4l8.config(bg = "white")
            if l9=='2':
                light9='ON'
                a4l9.config(bg = "gold")
            elif l9=='1':
                light9='MID'          
                a4l9.config(bg = "light goldenrod")
            else:
                light9='OFF'               
                a4l9.config(bg = "white")
            if l10=='2':
                light10='ON'
                a4l10.config(bg ="gold")
            elif l10=='1':
                light10='MID'          
                a4l10.config(bg = "light goldenrod")
            else:
                light10='OFF'               
                a4l10.config(bg = "white")
            if l11=='2':
                light11='ON'
                a4l11.config(bg = "gold")
            elif l11=='1':
                light11='MID'          
                a4l11.config(bg = "light goldenrod")
            else:
                light11='OFF'               
                a4l11.config(bg = "white")
            if l12=='2':
                light12='ON'
                a4l12.config(bg ="gold")
            elif l12=='1':
                light12='MID'          
                a4l12.config(bg = "light goldenrod")
            else:
                light12='OFF'               
                a4l12.config(bg = "white")            

                

            

            lux_val=80
            i = datetime.datetime.now()
            cur_date="%s/%s/%s"%(i.day,i.month,i.year)

            cur_time=time.strftime("%X")

            print("current date: ",cur_date,"\n")
            print("current time: ",cur_time,"\n")

                   
            path = "output sample.csv"

            with open(path,'a') as csv_file: 
                c=csv.writer(csv_file)
                c.writerow(["Area-2",cur_date,cur_time,lux_val,light1,light2,light3,light4,light5,light6,light7,light8,light9,light10,light11,light12])

            parent.update()





class areaOneManual(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        self.controller=controller

        img1_path=r"D:\Sumo\Main Project\python files\area1 light.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        
        title_label=tk.Label(self,text='Main Road-1 Manual\n',font=("Utopia",20,),fg="green")
        title_label.place(x=10,y=100)
        

        global v_manual_area1
        v_manual_area1 = tk.IntVar()

        back = ttk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("startpage"))
        back.place(x=0,y=0,height=40,width=100)

        rb1 = tk.Radiobutton(self,text="All-On",variable=v_manual_area1,value=1,command=self.radio_select_manual)
        rb1.place(x=20,y=170)
        rb2 = tk.Radiobutton(self,text="All-Off",variable=v_manual_area1,value=2,command=self.radio_select_manual)
        rb2.place(x=20,y=200)
        rb3 = tk.Radiobutton(self,text="Auto Mode",variable=v_manual_area1,value=3,command=self.radio_select_manual)
        rb3.place(x=31,y=230)
        
        rb1.config(font=('calibri',(15)),width=12)
        rb2.config(font=('calibri',(15)),width=12)
        rb3.config(font=('calibri',(15)),width=12)
    
        refresh = ttk.Button(self,text="Refresh",command = lambda: self.refreshpage(controller,parent))
        refresh.place(x=1100,y=100,height=40,width=100)


        global a1l1m
        global a1l2m
        global a1l3m
        global a1l4m
        global a1l5m
        global a1l6m
        global a1l1am
        global a1l2am
        global a1l3am
        global a1l4am
        global a1l5am
        global a1l6am

        a1l1m=tk.Label(self,text='L1')
        a1l1m.place(x=550,y=0)
        a1l1am=tk.Label(self,text='L1')
        a1l1am.place(x=595,y=0)

        a1l2m=tk.Label(self,text='L2')
        a1l2m.place(x=550,y=130)
        a1l2am=tk.Label(self,text='L2')
        a1l2am.place(x=595,y=130)

        a1l3m=tk.Label(self,text='L3')
        a1l3m.place(x=550,y=260)
        a1l3am=tk.Label(self,text='L3')
        a1l3am.place(x=595,y=260)

        a1l4m=tk.Label(self,text='L4')
        a1l4m.place(x=550,y=380)
        a1l4am=tk.Label(self,text='L4')
        a1l4am.place(x=595,y=380)

        a1l5m=tk.Label(self,text='L5')
        a1l5m.place(x=550,y=500)
        a1l5am=tk.Label(self,text='L5')
        a1l5am.place(x=595,y=500)
        
        a1l6m=tk.Label(self,text='L6')
        a1l6m.place(x=550,y=620)  
        a1l6am=tk.Label(self,text='L6')
        a1l6am.place(x=595,y=620)


        
    def radio_select_manual(self):
        global v_manual_area1
        global rb_value_manual_area1
        rb_value_manual_area1 = v_manual_area1.get()
        print (rb_value_manual_area1)

    def webaccess(self,page,parent):
        global autocheck
        autocheck=1
        parent.update()
        try:
            soup = BeautifulSoup(page.read(),"html.parser")
            l1=soup.find('p',attrs={'class':'l8'})
            l1=l1.string.strip()

            print("l1=",l1)

        except AttributeError as e:
            print(e)

        global a1l1m
        global a1l2m
        global a1l3m
        global a1l4m
        global a1l5m
        global a1l6m
        global a1l1am
        global a1l2am
        global a1l3am
        global a1l4am
        global a1l5am
        global a1l6am

        
                  
        if l1=='2':

            print("inside l1==2")
            light1='ON'
            light2='ON'
            light3='ON'
            light4='ON'
            light5='ON'
            light6='ON'
            light7='ON'
            light8='ON'
            light9='ON'
            light10='ON'
            light11='ON'
            light12='ON'

            a1l1m.config(bg = "gold")
            a1l1am.config(bg = "gold")
            a1l2m.config(bg = "gold")
            a1l2am.config(bg = "gold")
            a1l3m.config(bg = "gold")
            a1l3am.config(bg = "gold")
            a1l4m.config(bg = "gold")
            a1l4am.config(bg ="gold")
            a1l5m.config(bg = "gold")
            a1l5am.config(bg ="gold")
            a1l6m.config(bg = "gold")
            a1l6am.config(bg ="gold")
                    
                    
        elif l1=='1':
            print("inside l1==1")
            light1='MID'
            light2='MID'
            light3='MID'
            light4='MID'
            light5='MID'
            light6='MID'
            light7='MID'
            light8='MID'
            light9='MID'
            light10='MID'
            light11='MID'
            light12='MID'
                    
            a1l1m.config(bg = "light goldenrod")
            a1l1am.config(bg = "light goldenrod")
            a1l2m.config(bg = "light goldenrod")
            a1l2am.config(bg = "light goldenrod")
            a1l3m.config(bg = "light goldenrod")
            a1l3am.config(bg = "light goldenrod")
            a1l4m.config(bg = "light goldenrod")
            a1l4am.config(bg ="light goldenrod")
            a1l5m.config(bg = "light goldenrod")
            a1l5am.config(bg ="light goldenrod")
            a1l6m.config(bg = "light goldenrod")
            a1l6am.config(bg ="light goldenrod")
                  
        else:
            print("inside l1==0")
            light1='OFF'
            light2='OFF'
            light3='OFF'
            light4='OFF'
            light5='OFF'
            light6='OFF'
            light7='OFF'
            light8='OFF'
            light9='OFF'
            light10='OFF'
            light11='OFF'
            light12='OFF'
                      
            a1l1m.config(bg = "white")
            a1l1am.config(bg = "white")
            a1l2m.config(bg = "white")
            a1l2am.config(bg = "white")
            a1l3m.config(bg = "white")
            a1l3am.config(bg = "white")
            a1l4m.config(bg = "white")
            a1l4am.config(bg = "white")
            a1l5m.config(bg = "white")
            a1l5am.config(bg = "white")
            a1l6m.config(bg = "white")
            a1l6am.config(bg = "white")
                        
        '''print("light sensor reading: ",lux_val,"\n")
        print("light 1 status: ", light1,"\n")
        print("light 2 status: ", light2,"\n")'''
        lux_val=80
        i = datetime.datetime.now()
        cur_date="%s/%s/%s"%(i.day,i.month,i.year)

        cur_time=time.strftime("%X")

        print("current date: ",cur_date,"\n")
        print("current time: ",cur_time,"\n")

               
        path = "output sample.csv"

        with open(path,'a') as csv_file: 
            c=csv.writer(csv_file)
            c.writerow(["Area-1",cur_date,cur_time,lux_val,light1,light2,light3,light4,light5,light6,light7,light8,light9,light10,light11,light12])

        return

    def refreshpage(self,cont,parent):

        global rb_value_manual_area1
        global autocheck1
        autocheck1=1

        if (rb_value_manual_area1 == 1):
            print("rb_value_manual_area1 = 1")
            page = urlopen("http://192.168.1.63/LED=ON")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
            self.webaccess(page,parent)
        
        if (rb_value_manual_area1 == 2):
            print("rb_value_manual_area1 = 2")
            page = urlopen("http://192.168.1.63/LED=OFF")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
            self.webaccess(page,parent)
        
        if (rb_value_manual_area1 == 3):
            print("rb_value_manual_area1 = 3")
            page = urlopen("http://192.168.1.63/LED=AUTO")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
            self.webaccess(page,parent)

class areaTwoManual(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        self.controller=controller

        img1_path=r"D:\Sumo\Main Project\python files\area2 light.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        global v_manual_area2
        v_manual_area2 = tk.IntVar()
        

        back = ttk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("startpage"))
        back.place(x=0,y=0,height=40,width=100)

        rb1 = tk.Radiobutton(self,text="All-On",variable=v_manual_area2,value=1,command=self.radio_select_manual)
        rb1.place(x=20,y=170)
        rb2 = tk.Radiobutton(self,text="All-Off",variable=v_manual_area2,value=2,command=self.radio_select_manual)
        rb2.place(x=20,y=200)
        rb3 = tk.Radiobutton(self,text="Auto Mode",variable=v_manual_area2,value=3,command=self.radio_select_manual)
        rb3.place(x=31,y=230)
        
        rb1.config(font=('calibri',(15)),width=12)
        rb2.config(font=('calibri',(15)),width=12)
        rb3.config(font=('calibri',(15)),width=12)
    
        refresh = ttk.Button(self,text="Refresh",command = lambda: self.refreshpage(controller,parent))
        refresh.place(x=1100,y=100,height=40,width=100)

        

        global a2l1m
        global a2l2m
        global a2l3m
        global a2l4m
        global a2l5m
        global a2l6m
        global a2l1am
        global a2l2am
        global a2l3am
        global a2l4am
        global a2l5am
        global a2l6am

        a2l1m=tk.Label(self,text='L1')
        a2l1m.place(x=395,y=315)
        a2l1am=tk.Label(self,text='L1')
        a2l1am.place(x=395,y=380)

        a2l2m=tk.Label(self,text='L2')
        a2l2m.place(x=510,y=315)
        a2l2am=tk.Label(self,text='L2')
        a2l2am.place(x=510,y=380)

        a2l3m=tk.Label(self,text='L3')
        a2l3m.place(x=620,y=315)
        a2l3am=tk.Label(self,text='L3')
        a2l3am.place(x=620,y=380)

        a2l4m=tk.Label(self,text='L4')
        a2l4m.place(x=735,y=315)
        a2l4am=tk.Label(self,text='L4')
        a2l4am.place(x=735,y=380)

        a2l5m=tk.Label(self,text='L5')
        a2l5m.place(x=845,y=315)
        a2l5am=tk.Label(self,text='L5')
        a2l5am.place(x=845,y=380)

        a2l6m=tk.Label(self,text='L6')
        a2l6m.place(x=960,y=315)
        a2l6am=tk.Label(self,text='L6')
        a2l6am.place(x=960,y=380)

        
    def webaccess(self,page,parent):
        parent.update()
        try:
            soup = BeautifulSoup(page.read(),"html.parser")
            l1=soup.find('p',attrs={'class':'l8'})
            l1=l1.string.strip()
                
                
        except AttributeError as e:
            print(e)

        global a2l1m
        global a2l2m
        global a2l3m
        global a2l4m
        global a2l5m
        global a2l6m
        global a2l1am
        global a2l2am
        global a2l3am
        global a2l4am
        global a2l5am
        global a2l6am
            
        if l1=='2':
            light1='ON'
            light2='ON'
            light3='ON'
            light4='ON'
            light5='ON'
            light6='ON'
            light7='ON'
            light8='ON'
            light9='ON'
            light10='ON'
            light11='ON'
            light12='ON'

            a2l1m.config(bg = "gold")
            a2l1am.config(bg = "gold")
            a2l2m.config(bg = "gold")
            a2l2am.config(bg = "gold")
            a2l3m.config(bg = "gold")
            a2l3am.config(bg = "gold")
            a2l4m.config(bg = "gold")
            a2l4am.config(bg ="gold")
            a2l5m.config(bg = "gold")
            a2l5am.config(bg ="gold")
            a2l6m.config(bg = "gold")
            a2l6am.config(bg ="gold")                        
                    
        elif l1=='1':
            light1='MID'
            light2='MID'
            light3='MID'
            light4='MID'
            light5='MID'
            light6='MID'
            light7='MID'
            light8='MID'
            light9='MID'
            light10='MID'
            light11='MID'
            light12='MID'

            a2l1m.config(bg = "light goldenrod")
            a2l1am.config(bg = "light goldenrod")
            a2l2m.config(bg = "light goldenrod")
            a2l2am.config(bg = "light goldenrod")
            a2l3m.config(bg = "light goldenrod")
            a2l3am.config(bg = "light goldenrod")
            a2l4m.config(bg = "light goldenrod")
            a2l4am.config(bg ="light goldenrod")
            a2l5m.config(bg = "light goldenrod")
            a2l5am.config(bg ="light goldenrod")
            a2l6m.config(bg = "light goldenrod")
            a2l6am.config(bg ="light goldenrod")
                
        else:
            light1='OFF'
            light2='OFF'
            light3='OFF'
            light4='OFF'
            light5='OFF'
            light6='OFF'
            light7='OFF'
            light8='OFF'
            light9='OFF'
            light10='OFF'
            light11='OFF'
            light12='OFF'                    
                    
            a2l1m.config(bg = "white")
            a2l1am.config(bg = "white")
            a2l2m.config(bg = "white")
            a2l2am.config(bg = "white")
            a2l3m.config(bg = "white")
            a2l3am.config(bg = "white")
            a2l4m.config(bg = "white")
            a2l4am.config(bg = "white")
            a2l5m.config(bg = "white")
            a2l5am.config(bg = "white")
            a2l6m.config(bg = "white")
            a2l6am.config(bg = "white")            
            
        lux_val=90
        i = datetime.datetime.now()
        cur_date="%s/%s/%s"%(i.day,i.month,i.year)
        cur_time=time.strftime("%X")

        print("current date: ",cur_date,"\n")
        print("current time: ",cur_time,"\n")
        print("area2")

                   
        path = "output sample.csv"

        with open(path,'a') as csv_file: 
            c=csv.writer(csv_file)
            c.writerow(["Area-2",cur_date,cur_time,lux_val,light1,light2,light3,light4,light5,light6,light7,light8,light9,light10,light11,light12])

        parent.update()
        return

        
    def radio_select_manual(self):
        global v_manual_area2
        global rb_value_manual_area2
        rb_value_manual_area2 = v_manual_area2.get()
        print (rb_value_manual_area2)

    def refreshpage(self,cont,parent):

        global rb_value_manual_area2
        global autocheck2
        autocheck2=1

        if (rb_value_manual_area2 == 1):
            print("rb_value_manual_area1 = 1")
            page = urlopen("http://192.168.1.116/LED=ON")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
            self.webaccess(page,parent)
        
        if (rb_value_manual_area2 == 2):
            print("rb_value_manual_area1 = 2")
            page = urlopen("http://192.168.1.116/LED=OFF")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
            self.webaccess(page,parent)
        
        if (rb_value_manual_area2 == 3):
            print("rb_value_manual_area1 = 3")
            page = urlopen("http://192.168.1.116/LED=AUTO")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/test.html")
            self.webaccess(page,parent)



class areaThreeManual(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        self.controller=controller

        img1_path=r"D:\Sumo\Main Project\python files\area3 light.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        global v_manual_area3
        v_manual_area3 = tk.IntVar()
        

        back = ttk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("startpage"))
        back.place(x=0,y=0,height=40,width=100)

        rb1 = tk.Radiobutton(self,text="All-On",variable=v_manual_area3,value=1,command=self.radio_select_manual)
        rb1.place(x=20,y=170)
        rb2 = tk.Radiobutton(self,text="All-Off",variable=v_manual_area3,value=2,command=self.radio_select_manual)
        rb2.place(x=20,y=200)
        rb3 = tk.Radiobutton(self,text="Auto Mode",variable=v_manual_area3,value=3,command=self.radio_select_manual)
        rb3.place(x=31,y=230)
        
        rb1.config(font=('calibri',(15)),width=12)
        rb2.config(font=('calibri',(15)),width=12)
        rb3.config(font=('calibri',(15)),width=12)
    
        refresh = ttk.Button(self,text="Refresh",command = lambda: self.refreshpage(controller,parent))
        refresh.place(x=1100,y=100,height=40,width=100)

        

           
        global a3l1m
        global a3l2m
        global a3l3m
        global a3l4m
        global a3l5m
        global a3l6m
        global a3l7m
        global a3l8m
        global a3l9m
        global a3l10m
        global a3l11m
        global a3l12m


       

        a3l1m=tk.Label(self,text='L1')
        a3l1m.place(x=635,y=145)
        
        a3l2m=tk.Label(self,text='L2')
        a3l2m.place(x=655,y=245)

        a3l3m=tk.Label(self,text='L3')
        a3l3m.place(x=745,y=150)
        
        a3l4m=tk.Label(self,text='L4')
        a3l4m.place(x=720,y=240)

        a3l5m=tk.Label(self,text='L5')
        a3l5m.place(x=805,y=85)
        
        a3l6m=tk.Label(self,text='L6')
        a3l6m.place(x=805,y=260)
        
        a3l7m=tk.Label(self,text='L7')
        a3l7m.place(x=935,y=155)
        
        a3l8m=tk.Label(self,text='L8')
        a3l8m.place(x=655,y=85)

        a3l9m=tk.Label(self,text='L9')
        a3l9m.place(x=635,y=0)
        
        a3l10m=tk.Label(self,text='L10')
        a3l10m.place(x=705,y=0)

        a3l11m=tk.Label(self,text='L11')
        a3l11m.place(x=805,y=0)
    
        a3l12m=tk.Label(self,text='L12')
        a3l12m.place(x=925,y=0)



    def radio_select_manual(self):
        global v_manual_area3
        global rb_value_manual_area3
        rb_value_manual_area3 = v_manual_area3.get()
        print (rb_value_manual_area3)

    def webaccess(self,page,parent):
        parent.update()
        try:
            soup = BeautifulSoup(page.read(),"html.parser")
            print(soup)
            l1=soup.find('p',attrs={'class':'l1'})
            print(l1)
            l1=l1.string.strip()
            l2=soup.find('p',attrs={'class':'l2'})
            l2=l2.string.strip()
            l3=soup.find('p',attrs={'class':'l2'})
            l3=l3.string.strip()
            l3=soup.find('p',attrs={'class':'l3'})
            l3=l3.string.strip()
            l4=soup.find('p',attrs={'class':'l4'})
            l4=l4.string.strip()
            l5=soup.find('p',attrs={'class':'l5'})
            l5=l5.string.strip()
            l6=soup.find('p',attrs={'class':'l6'})
            l6=l6.string.strip()
            l7=soup.find('p',attrs={'class':'l7'})
            l7=l7.string.strip()
            l8=soup.find('p',attrs={'class':'l8'})
            l8=l8.string.strip()
            l9=soup.find('p',attrs={'class':'l9'})
            l9=l9.string.strip()
            l10=soup.find('p',attrs={'class':'l10'})
            l10=l10.string.strip()
            l11=soup.find('p',attrs={'class':'l11'})
            l11=l11.string.strip()
            l12=soup.find('p',attrs={'class':'l12'})
            l12=l12.string.strip()
            time.sleep(2)

        except AttributeError as e:
            print(e)

            
        global a3l1m
        global a3l2m
        global a3l3m
        global a3l4m
        global a3l5m
        global a3l6m
        global a3l7m
        global a3l8m
        global a3l9m
        global a3l10m
        global a3l11m
        global a3l12m

        
                  
        if l1=='2':
            light1='ON'  
            a3l1m.config(bg = "gold")
        elif l1=='1':
            light1='MID'          
            a3l1m.config(bg = "light goldenrod")
        else:
            light1='OFF'               
            a3l1m.config(bg = "white")
        if l2=='2':
            light2='ON'
            a3l2m.config(bg = "gold")
        elif l2=='1':
            light2='MID'          
            a3l2m.config(bg = "light goldenrod")
        else:
            light2='OFF'               
            a3l2m.config(bg = "white")
        if l3=='2':
            light3='ON'
            a3l3m.config(bg = "gold")
        elif l3=='1':
            light3='MID'          
            a3l3m.config(bg = "light goldenrod")
        else:
            light3='OFF'               
            a3l3m.config(bg = "white")
        if l4=='2':
            light4='ON'
            a3l4m.config(bg = "gold")
        elif l4=='1':
            light4='MID'          
            a3l4m.config(bg = "light goldenrod")
        else:
            light4='OFF'               
            a3l4m.config(bg = "white")
        if l5=='2':
            light5='ON'
            a3l5m.config(bg = "gold")
        elif l5=='1':
            light5='MID'          
            a3l5m.config(bg = "light goldenrod")
        else:
            light5='OFF'               
            a3l5m.config(bg = "white")
        if l6=='2':
            light6='ON'
            a3l6m.config(bg = "gold")
        elif l6=='1':
            light6='MID'          
            a3l6m.config(bg = "light goldenrod")
        else:
            light6='OFF'               
            a3l6m.config(bg = "white")
        if l7=='2':
            light7='ON'
            a3l7m.config(bg = "gold")
        elif l7=='1':
            light7='MID'          
            a3l7m.config(bg = "light goldenrod")
        else:
            light7='OFF'               
            a3l7m.config(bg = "white")
        if l8=='2':
            light8='ON'
            a3l8m.config(bg ="gold")
        elif l8=='1':
            light8='MID'          
            a3l8m.config(bg = "light goldenrod")
        else:
            light8='OFF'               
            a3l8m.config(bg = "white")
        if l9=='2':
            light9='ON'
            a3l9m.config(bg = "gold")
        elif l9=='1':
            light9='MID'          
            a3l9m.config(bg = "light goldenrod")
        else:
            light9='OFF'               
            a3l9m.config(bg = "white")
        if l10=='2':
            light10='ON'
            a3l10m.config(bg ="gold")
        elif l10=='1':
            light10='MID'          
            a3l10m.config(bg = "light goldenrod")
        else:
            light10='OFF'               
            a3l10m.config(bg = "white")
        if l11=='2':
            light11='ON'
            a3l11m.config(bg = "gold")
        elif l11=='1':
            light11='MID'          
            a3l11m.config(bg = "light goldenrod")
        else:
            light11='OFF'               
            a3l11m.config(bg = "white")
        if l12=='2':
            light12='ON'
            a3l12m.config(bg ="gold")
        elif l12=='1':
            light12='MID'          
            a3l12m.config(bg = "light goldenrod")
        else:
            light12='OFF'               
            a3l12m.config(bg = "white")        

            

        lux_val=80
        i = datetime.datetime.now()
        cur_date="%s/%s/%s"%(i.day,i.month,i.year)

        cur_time=time.strftime("%X")

        print("current date: ",cur_date,"\n")
        print("current time: ",cur_time,"\n")

                   
        path = "output sample.csv"
        with open(path,'a') as csv_file:
            c=csv.writer(csv_file)
            c.writerow(["Area-3",cur_date,cur_time,lux_val,light1,light2,light3,light4,light5,light6,light7,light8,light9,light10,light11,light12])            

        return

    def refreshpage(self,cont,parent):

        global rb_value_manual_area3
        global autocheck3
        autocheck3=1

        if (rb_value_manual_area3 == 1):
            print("rb_value_manual_area1 = 1")
            page = urlopen("http://192.168.1.247/LED=ON")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/web%20access%20page.html")
            self.webaccess(page,parent)
        
        if (rb_value_manual_area3 == 2):
            print("rb_value_manual_area1 = 2")
            page = urlopen("http://192.168.1.247/LED=OFF")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/web%20access%20page.html")
            self.webaccess(page,parent)
        
        if (rb_value_manual_area3 == 3):
            print("rb_value_manual_area1 = 3")
            page = urlopen("http://192.168.1.247/AUTO")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/web%20access%20page.html")
            self.webaccess(page,parent)



class areaFourManual(tk.Frame):

     def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        self.controller=controller

        img1_path=r"D:\Sumo\Main Project\python files\area4 light.gif"
        img1 = tk.PhotoImage(file=img1_path)
        background_label = tk.Label(self,image=img1)
        background_label.image = img1
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        global v_manual_area4
        v_manual_area4 = tk.IntVar()
        

        back = ttk.Button(self,text="Back",
                                      command=lambda: controller.show_frame("startpage"))
        back.place(x=0,y=0,height=40,width=100)

        rb1 = tk.Radiobutton(self,text="All-On",variable=v_manual_area4,value=1,command=self.radio_select_manual)
        rb1.place(x=20,y=170)
        rb2 = tk.Radiobutton(self,text="All-Off",variable=v_manual_area4,value=2,command=self.radio_select_manual)
        rb2.place(x=20,y=200)
        rb3 = tk.Radiobutton(self,text="Auto Mode",variable=v_manual_area4,value=3,command=self.radio_select_manual)
        rb3.place(x=31,y=230)
        
        rb1.config(font=('calibri',(15)),width=12)
        rb2.config(font=('calibri',(15)),width=12)
        rb3.config(font=('calibri',(15)),width=12)
    
        refresh = ttk.Button(self,text="Refresh",command = lambda: self.refreshpage(controller))
        refresh.place(x=1100,y=100,height=40,width=100)
        view_graph = ttk.Button(self,text="View graph",
                                      command=lambda: controller.show_frame("area4_graph"))
        view_graph.place(x=1100,y=160,height=40,width=100)



        

        global a4l1m
        global a4l2m
        global a4l3m
        global a4l4m
        global a4l5m
        global a4l6m
        global a4l7m
        global a4l8m
        global a4l9m
        global a4l10m
        global a4l11m
        global a4l12m

       
        a4l1m=tk.Label(self,text='L1')
        a4l1m.place(x=655,y=400)
        
        a4l2m=tk.Label(self,text='L2')
        a4l2m.place(x=725,y=425)

        a4l3m=tk.Label(self,text='L3')
        a4l3m.place(x=815,y=455)
        
        a4l4m=tk.Label(self,text='L4')
        a4l4m.place(x=945,y=450)

        a4l5m=tk.Label(self,text='L5')
        a4l5m.place(x=635,y=495)
        
        a4l6m=tk.Label(self,text='L6')
        a4l6m.place(x=723,y=510)
        
        a4l7m=tk.Label(self,text='L7')
        a4l7m.place(x=660,y=580)
        
        a4l8m=tk.Label(self,text='L8')
        a4l8m.place(x=820,y=590)

        a4l9m=tk.Label(self,text='L9')
        a4l9m.place(x=955,y=590)
        
        a4l10m=tk.Label(self,text='L10')
        a4l10m.place(x=635,y=660)

        a4l11m=tk.Label(self,text='L11')
        a4l11m.place(x=720,y=660)
        
        a4l12m=tk.Label(self,text='L12')
        a4l12m.place(x=885,y=670)

    




     def radio_select_manual(self):

        global v_manual_area4
        global rb_value_manual_area4
        rb_value_manual_area4 = v_manual_area4.get()
        print (rb_value_manual_area4)

     def webaccess(self,page):
        try:
            soup = BeautifulSoup(page.read(),"html.parser")
            print(soup)
            l1=soup.find('p',attrs={'class':'l1'})
            print(l1)
            l1=l1.string.strip()
            l2=soup.find('p',attrs={'class':'l2'})
            l2=l2.string.strip()
            l3=soup.find('p',attrs={'class':'l3'})
            l3=l3.string.strip()
            l4=soup.find('p',attrs={'class':'l4'})
            l4=l4.string.strip()
            l5=soup.find('p',attrs={'class':'l5'})
            l5=l5.string.strip()
            l6=soup.find('p',attrs={'class':'l6'})
            l6=l6.string.strip()
            l7=soup.find('p',attrs={'class':'l7'})
            l7=l7.string.strip()
            l8=soup.find('p',attrs={'class':'l8'})
            l8=l8.string.strip()
            l9=soup.find('p',attrs={'class':'l9'})
            l9=l9.string.strip()
            l10=soup.find('p',attrs={'class':'l10'})
            l10=l10.string.strip()
            l11=soup.find('p',attrs={'class':'l11'})
            l11=l11.string.strip()
            l12=soup.find('p',attrs={'class':'l12'})
            l12=l12.string.strip()
            print(l1)
            time.sleep(5)

        except AttributeError as e:
            print(e)

            
        global a4l1m
        global a4l2m
        global a4l3m
        global a4l4m
        global a4l5m
        global a4l6m
        global a4l7m
        global a4l8m
        global a4l9m
        global a4l10m
        global a4l11m
        global a4l12m

        
                  
        if l1=='2':
            light1='ON'  
            a4l1m.config(bg = "gold")
        elif l1=='1':
            light1='MID'          
            a4l1m.config(bg = "light goldenrod")
        else:
            light1='OFF'               
            a4l1m.config(bg = "white")
        if l2=='2':
            light2='ON'
            a4l2m.config(bg = "gold")
        elif l2=='1':
            light2='MID'          
            a4l2m.config(bg = "light goldenrod")
        else:
            light2='OFF'               
            a4l2m.config(bg = "white")
        if l3=='2':
            light3='ON'
            a4l3m.config(bg = "gold")
        elif l3=='1':
            light3='MID'          
            a4l3m.config(bg = "light goldenrod")
        else:
            light3='OFF'               
            a4l3m.config(bg = "white")
        if l4=='2':
            light4='ON'
            a4l4m.config(bg = "gold")
        elif l4=='1':
            light4='MID'          
            a4l4m.config(bg = "light goldenrod")
        else:
            light4='OFF'               
            a4l4m.config(bg = "white")
        if l5=='2':
            light5='ON'
            a4l5m.config(bg = "gold")
        elif l5=='1':
            light5='MID'          
            a4l5m.config(bg = "light goldenrod")
        else:
            light5='OFF'               
            a4l5m.config(bg = "white")
        if l6=='2':
            light6='ON'
            a4l6m.config(bg = "gold")
        elif l6=='1':
            light6='MID'          
            a4l6m.config(bg = "light goldenrod")
        else:
            light6='OFF'               
            a4l6m.config(bg = "white")
        if l7=='2':
            light7='ON'
            a4l7m.config(bg = "gold")
        elif l7=='1':
            light7='MID'          
            a4l7m.config(bg = "light goldenrod")
        else:
            light7='OFF'               
            a4l7m.config(bg = "white")
        if l8=='2':
            light8='ON'
            a4l8m.config(bg ="gold")
        elif l8=='1':
            light8='MID'          
            a4l8m.config(bg = "light goldenrod")
        else:
            light8='OFF'               
            a4l8m.config(bg = "white")
        if l9=='2':
            light9='ON'
            a4l9m.config(bg = "gold")
        elif l9=='1':
            light9='MID'          
            a4l9m.config(bg = "light goldenrod")
        else:
            light9='OFF'               
            a4l9m.config(bg = "white")
        if l10=='2':
            light10='ON'
            a4l10m.config(bg ="gold")
        elif l10=='1':
            light10='MID'          
            a4l10m.config(bg = "light goldenrod")
        else:
            light10='OFF'               
            a4l10m.config(bg = "white")
        if l11=='2':
            light11='ON'
            a4l11m.config(bg = "gold")
        elif l11=='1':
            light11='MID'          
            a4l11m.config(bg = "light goldenrod")
        else:
            light11='OFF'               
            a4l11m.config(bg = "white")
        if l12=='2':
            light12='ON'
            a4l12m.config(bg ="gold")
        elif l12=='1':
            light12='MID'          
            a4l12m.config(bg = "light goldenrod")
        else:
            light12='OFF'               
            a4l12m.config(bg = "white")            

            

        lux_val=80
        i = datetime.datetime.now()
        cur_date="%s/%s/%s"%(i.day,i.month,i.year)

        cur_time=time.strftime("%X")

        print("current date: ",cur_date,"\n")
        print("current time: ",cur_time,"\n")

                   
        path = "output.csv"

        with open(path,'a') as csv_file:
            c=csv.writer(csv_file)
            c.writerow(["Area-4",cur_date,cur_time,lux_val,light1,light2,light3,light4,light5,light6,light7,light8,light9,light10,light11,light12])
        return


     def refreshpage(self,cont):

        global rb_value_manual_area4
        global autocheck4
        autocheck4=1

        if (rb_value_manual_area4 == 1):
            print("rb_value_manual_area1 = 1")
            page = urlopen("http://192.168.1.151/LED=ON")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/web%20access%20page.html")
            self.webaccess(page)
        
        if (rb_value_manual_area4 == 2):
            print("rb_value_manual_area1 = 2")
            page = urlopen("http://192.168.1.151/LED=OFF")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/web%20access%20page.html")
            self.webaccess(page)
        
        if (rb_value_manual_area4 == 3):
            print("rb_value_manual_area1 = 3")
            page = urlopen("http://192.168.1.151/AUTO")
            #page = urlopen("file:///D:/Sumo/Main%20Project/python%20files/web%20access%20page.html")
            self.webaccess(page)



if __name__ == "__main__":
    
    app = baseclass()    
    app.state('zoomed')
    app.mainloop()
