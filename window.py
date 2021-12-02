import tkinter.ttk
from tkinter import *
from tkinter import ttk
from commande import *
from tracer_ph import  app
from lamda import *
import threading
import time




global choix , running , cpt,COUNT ,user , apa , ph , filename

ph=[]
apa=Apasch()
COUNT = 0
user=commande()
cpt = 1
choix = 'cycle'
running = False






def tracer (*args) :
    plot_ph().lancer_plot()


# Define a function to start the loop
def on_start():
   global running,apa,COUNT
   apa=Apasch()
   COUNT = 0
   running = True
   fieldnames = ["Datetime", "Temp", "pH"]
   with open('data.txt', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

# Define a function to stop the loop
def on_stop():
   global running
   running = False

def btn_clicked():
    print("Button Clicked")




class apasch_gui () :

    def __init__(self):
        self.window = Tk()
        self.choix_calcul=StringVar(None,'cycle')
        self.type_eau=StringVar(None, "mer")
        self.window.geometry("1280x720")
        self.window.configure(bg = "#ffffff")
        canvas = Canvas(
            self.window,
            bg = "#ffffff",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)
        background_img = PhotoImage(file = f"logos_ihm/background.png")
        background = canvas.create_image(
            626.0, 360.0,
            image=background_img)
        # buttons
        self.create_button('LAUNCH CYCLE',716,441,lambda : [on_start()])
        self.create_button('CLOSE CYCLE',716,526,on_stop)
        self.create_button('EXIT',716,609,self.window.destroy)
        ## radio buttons
        # type de commande
        self.create_radio_button(None,657,185,self.update_choix,self.choix_calcul , 'cycle')
        self.create_radio_button(None,857,185,self.update_choix,self.choix_calcul , 'stop')
        self.create_radio_button(None,1042,185,self.update_choix,self.choix_calcul , 'test')
        # sea or fresh water
        self.create_radio_button(None,651,65,btn_clicked,self.type_eau , 'mer')
        self.create_radio_button(None,1042,65,btn_clicked,self.type_eau, 'douce')

        # list_box
        cmd_list=['A','B','C','E','J','K','L','M','N','Q','R','S','T']
        cmd_choose=ttk.Combobox(self.window,value=cmd_list)
        cmd_choose.current(7)
        cmd_choose.place(x=1042, y=308,width = 35,height = 25)
        self.create_button('APPLY',1120,302,lambda  : [user.cmd_simple(cmd_choose.get())],65,35,12)
        threading.Thread(target = lambda : self.window.after(1000, self.print_text)).start()
        threading.Thread(target=app).start()

       # threading.Thread(target=lambda  : [app2(file1=user.filename)]).start()

        self.window.mainloop()


    def update_choix(self,*args):
        global choix
        if  self.choix_calcul.get() == 'single' :
            choix = 'single'
            print(choix)
            name = input("What is your command? or exit: ")
            sequence = user.cmd_simple(name)
        elif self.choix_calcul.get() == 'test' :
            choix = 'test'
            print(choix)
        elif self.choix_calcul.get() == 'stop' :
            choix = 'stop'
            print(choix)
        else :
            choix = 'cycle'
            print(choix)
        return  choix



    def print_text(self):
        if running:
            threading.Thread(target= lambda : [self.launch2(user,apa)]).start()
        self.window.after(1000,self.print_text)



    def create_button(self,text,x,y,command,w=442,h=70,sizet=20):
        b = Button(
            text=text,
            font=('Helvetica',sizet),
            highlightthickness = 0,
            command = command)
        b.place(
            x=x, y=y,
            width = w,
            height = h)

    def create_radio_button(self,text,x,y,command,variable,value):
        b = Radiobutton(
            value=value,
            variable=variable,
            text=text,
            font=('Helvetica',20),
            highlightthickness = 0,
            command = command)
        b.place(
            x=x, y=y,
            width = 10,
            height = 10)

    def launch2 (self,user,apa) :
        global COUNT , ph , filename
        apa.water = self.type_eau.get()
        print('Vous avez choisi la commande : ', choix)
        filename=user.filename
        name = ''
        fieldnames = ["Datetime", "Temp", "pH"]
        if choix == "cycle":
                try:
                   # COUNT = 0
                    print(COUNT)
                    if running:
                        if user.GENERAL["PH_ACTIVE"]:
                            pH = user.modeAuto_Ph(COUNT,apa)
                            ph= pH
                            label = Label(self.window, text= ph.tail(1))
                            #label.place(relx = 0.5,rely = 0.9,anchor = 'n')
                            self.window.update_idletasks()
                            with open('data.txt', 'a') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                info = {
                                    "Datetime": pH.iloc[-1,0],
                                    "Temp": pH.iloc[-1,1],
                                    "pH": pH.iloc[-1,2]
                                }
                                csv_writer.writerow(info)
                        if user.GENERAL["ALC_ACTIVE"]:
                            alc = user.modeAuto_ALC(COUNT,apa)
                            #user.clear_screen()
                            print(alc[['DATE+HEURE','CYCLE',
                                                            'TEMP','Alc 1','Alc 2','Alc 3','Alc Sb']])
                        COUNT += 1
                except KeyboardInterrupt:
                    print("boucle interrompue")

        elif choix == "single":
                while name != "exit":
                    print(name)
                    name = input("What is your command? or exit: ")
                    sequence = user.cmd_simple(name)
        elif choix == "test":
                print(user.trame())
                print(user.tsg())
        elif choix == "stop":
                user.data_cycle




if __name__=="__main__":
    k=apasch_gui ()



