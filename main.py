from tkinter import *
from define import *
from test import *
from graph import  *



global choix , running , cpt,COUNT ,user , apa , ph
ph=[]
apa=Apasch()
COUNT = 0
user=commande()
cpt = 1
choix = 'cycle'
running = False


def print_text():
    print('uuuuu',choix)
    print('______',running)
    print(ph)
    if running:
        launch2(user,apa)
    window.after(1000,print_text)

def launch2 (user,apa) :
    global COUNT , ph
    print('Vous avez choisi la commande : ', choix)
    a=user.filename
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
                        label = Label(window, text= ph.tail(1))
                        #label.pack()
                        label.place(relx = 0.5,rely = 0.9,anchor = 'n')
                        window.update_idletasks()
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




def tracer (*args) :
    plot_ph().lancer_plot()

def update_choix(*args):
    global choix
    if  choix_calcul.get() == 'single' :
        choix = 'single'
        print(choix)
    elif choix_calcul.get() == 'test' :
        choix = 'test'
        print(choix)
    elif choix_calcul.get() == 'stop' :
        choix = 'stop'
        print(choix)
    else :
        choix = 'cycle'
        print(choix)
    return  choix




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




# creation de la fenetre
color_blue = '#4065A4'
window = Tk()
window.title('APASCH GUI')
window.geometry('720x480')
window.minsize(100,100)
window.config(background=color_blue)
# frame principale

frame=Frame(window,bg = color_blue)



# insertion image
width = 300
height = 300
image = PhotoImage(file="locean.png").zoom(32).subsample(32)
canvas = Canvas(frame,width=width,height=height,bg=color_blue,bd=0,highlightthickness=0)
canvas.create_image(width/2,height/2,image=image)
canvas.grid(row=0,column=0,sticky=W)

# sous boite
right_frame = Frame(frame,bg=color_blue)

# titre

label_title = Label (window,text = 'COMMANDE APASCH', font=('Helvetica',20),bg=color_blue,fg='white')
label_title.pack()




# choisir  mode de calcul
choix_calcul=StringVar()
radio1 = Radiobutton (right_frame,text='Cycle (Par défaut)',value='cycle',variable=choix_calcul,command = update_choix)
radio2 = Radiobutton (right_frame,text='Single',value='single',variable=choix_calcul,command =update_choix)
radio3 = Radiobutton (right_frame,text='Test',value='test',variable=choix_calcul,command = update_choix)
radio4 = Radiobutton (right_frame,text='Stop',value='stop',variable=choix_calcul,command = update_choix)

radio1.pack(expand = YES)
radio2.pack(expand = YES)
radio3.pack(expand = YES)
radio4.pack(expand = YES)

# creer boutton demarrer

ent = Button (right_frame,
              command = lambda : [on_start()],
              text='LANCER LE CALCUL',
              font=('Helvetica',20))
ent.pack(expand=YES)


cmd='True'
ent3 = Button (right_frame,
              command = lambda : app(),
              text='PLOT TK',
              font=('Helvetica',20))
ent3.pack(expand=YES)

ent4 = Button (right_frame,
              command = tracer,
              text='PLOT',
              font=('Helvetica',20))
ent4.pack(expand=YES)



ent5 = Button (right_frame,
              command = on_stop,
              text='CLOTURER LE CYCLE',
              font=('Helvetica',20))
ent5.pack(expand=YES)

ent2 = Button (right_frame,
              command = quit,
              text='QUITTER',
              font=('Helvetica',20))
ent2.pack(expand=YES)

window.after(1000, print_text)


right_frame.grid(row=0,column = 1 , sticky = W)
frame.pack(expand=YES)

mainloop()
