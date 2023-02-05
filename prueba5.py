import tkinter
from PIL import ImageTk, Image

WIDTH, HEIGHT = 900, 900
IMG_PATH = r"cabecera.jpg"  # Note 'r' prefix.

show_screen = tkinter.Tk()
show_screen.geometry('{}x{}'.format(WIDTH, HEIGHT))
show_screen.title("LEARNTECH OPE")

# Place background image on a Label widget.
tmp_img = Image.open(IMG_PATH).resize((WIDTH, HEIGHT), Image.ANTIALIAS)
bkg_img = ImageTk.PhotoImage(tmp_img)
bkg_label = tkinter.Label(show_screen, image=bkg_img)
bkg_label.img = bkg_img  # Keep a reference in case this code put is in a function.
bkg_label.place(relx=0.5, rely=0.5, anchor='center')  # Place in center of window.

enter_field = tkinter.Entry(show_screen,width=50)
enter_field.place(x=600,y=200)

show_label = tkinter.Label(show_screen,font=("Arial Bold",10),fg="blue",
                           text="FILL THE NECESSARY DETAILS GIVEN BELOW")
show_label.place(x=600,y=0)

def clicked():
    ref = "Welcome " + enter_field.get()
    show_label.configure(text=ref)

show_button = tkinter.Button(show_screen,text="CLICK TO EXIT",
                             fg="green",command=clicked)
show_button.place(x=600,y=400)

show_screen.mainloop()

