import tkinter
import tkinter as tk
from  define import *

#######################
apa=commande()

app = tk.Tk ()
app.title('APASCH')

screen_x =app.winfo_screenwidth()
screen_y =app.winfo_screenheight()
window_x=800
window_y=600
posx=(screen_x//2) - (window_x//2)
posy=(screen_y//2) - (window_y//2)
geo="{}x{}+{}+{}".format(window_x,window_y,posx,posy)
app.geometry(geo)

######## widgets

#label_welcome=tkinter.Label(app,text='Bienvenue - APASCH')
#label_welcome.pack()

boutton=tkinter.Button(app,text='DEMARRER',command = apa.launch )
boutton.pack()



app.mainloop()
