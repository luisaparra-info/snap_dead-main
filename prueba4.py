import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import cv2
import imutils




def visualizar():
    im = Image.fromarray(cv2.imread('star.png',-1))
    img = ImageTk.PhotoImage(image=im)
    lblVideo.configure(image=img)
    lblVideo.image = img
    


root = tk.Tk()

global listaMujeres 

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

listaMujeres = tk.Listbox()
listaMujeres.grid(column=0,row=0)
listaMujeres.selection_set(0)
btnIniciar = ttk.Button(root, text="INICIAR", style="C.TButton")
btnIniciar.grid(column=1, row=0, padx=5, pady=5)

btnFinalizar = ttk.Button(root, text="FINALIZAR", style="C.TButton")
btnFinalizar.grid(column=2, row=0, padx=5, pady=5)

lblVideo = tk.Label(root)
lblVideo.grid(column=0, row=1, columnspan=3)
visualizar()
root.mainloop()