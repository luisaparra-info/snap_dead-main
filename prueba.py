import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.font import Font
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

fileName = "Web.txt"
cancel = False



def save(event = 0):
    global prevImg

    if nombre.get():
        filepath = nombre.get()+ ".png"
    else:
        filepath = "camptura.png"

    print ("Output file to: " + filepath)
    prevImg.save(filepath)
   

def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    seleccionarFiltro(listaMujeres.current())
    visualizar()

def seleccionarFiltro(seleccion):
    # Lectura de la imagen a incrustar en el video
    global filtro
    global variacion_alto
    print(seleccion)
    if (seleccion==0):
        filtro = cv2.imread('star.png',-1)
        variacion_alto=0
    elif (seleccion==1):
        filtro = cv2.imread('pirate.png', -1)
    elif (seleccion==2):
        filtro = cv2.imread('sunglass.png', -1)
        variacion_alto=130
    elif (seleccion==3):
        filtro = cv2.imread('cool.png', -1)
        variacion_alto=75
def visualizar():
    global filtro
    global variacion_alto
    global cap
    global prevImg
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            faces = faceClassif.detectMultiScale(frame, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)
                # Redimensionar la imagen de entrada de acuerdo al ancho del
                # rostro detectado
                resized_image = imutils.resize(filtro, width=w)
                filas_image = resized_image.shape[0]
                col_image = w

                # Determinar una porción del alto de la imagen de entrada 
                # redimensionada
                porcion_alto = filas_image  // 4 + variacion_alto
                
                print(porcion_alto)

                dif = 0

                # Si existe suficiente espacio sobre el rostro detectado
                # para insertar la imagen de entrada resimensionada
                # se visualizará dicha imagen
                if y + porcion_alto - filas_image >= 0:

                    # Tomamos la sección de frame donde poner el filtro
                    n_frame = frame[y + porcion_alto - filas_image : y + porcion_alto, x : x + col_image]
                else:
                    # Determinamos la sección de la imagen que excede a la del video
                    dif = abs(y + porcion_alto - filas_image) 
                    # Tomamos la sección de frame, en donde se va a ubicar
                    # el gorro/tiara
                    n_frame = frame[0 : y + porcion_alto, x : x + col_image]
                # Determinamos la máscara que posee la imagen de entrada
                # redimensionada y también la invertimos
                mask = resized_image[:, :, 3]
                mask_inv = cv2.bitwise_not(mask)
            
                # Creamos una imagen con fondo negro y el filtro
                # Luego creamos una imagen en donde en el fondo esté frame
                # y en negro el filtro
                bg_black = cv2.bitwise_and(resized_image, resized_image, mask=mask)
                bg_black = bg_black[dif:, :, 0:3]
                bg_frame = cv2.bitwise_and(n_frame, n_frame, mask=mask_inv[dif:,:])
                # Sumamos las dos imágenes obtenidas
                bg_black = cv2.cvtColor(bg_black, cv2.COLOR_RGB2BGR)
                result = cv2.add(bg_black, bg_frame)
                if y + porcion_alto - filas_image >= 0:
                    frame[y + porcion_alto - filas_image : y + porcion_alto, x : x + col_image] = result
                else:
                    frame[0 : y + porcion_alto, x : x + col_image] = result
                   
            
                        
                        

            im = Image.fromarray(frame)
            prevImg=im
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(1, visualizar)
        else:
            lblVideo.image = ""
            cap.release()
def finalizar():
    global cap
    cap.release()

cap = None
root = tk.Tk()
root.title("Día Internacional de la Mujer y la Niña en la Ciencia - 1º BACH - CDyPC")
root.geometry("640x770")


image1 = Image.open("cabecera.jpg")
cabezera = ImageTk.PhotoImage(image1)

label1 = tk.Label(image=cabezera)
label1.image = cabezera

root['background']='#00a5a7'

label1.grid(row=0, column=0, columnspan=3)

mujeres = (
    "Margarita Salas",
    "Hipatia de Alejandría",
    "Marie Curie",
    "Barbara McClintock"
)
fuente = Font(family = "Roboto Cn", size = 14)
style = ttk.Style() 
style.theme_use('clam')
style.configure('C.TButton', font=fuente)
style.configure('C.TButton', relief="ridge")
style.configure('C.TButton', width=13)
style.configure('C.TButton', bd=1)
style.configure("TCombobox", fieldbackground= "orange", background= "white", arrowsize=15)

global listaMujeres 

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


lblNombre=tk.Label(root,text="Nombre", background="#00a5a7", font=fuente, anchor=tk.E)
lblNombre.grid(column=0, row=1, padx=10, pady=10)

nombre = ttk.Entry(font=fuente)
nombre.grid(column=1, row=1, columnspan=2, padx=10, pady=10)


lblEmail=tk.Label(root,text="Email", background="#00a5a7", font=fuente)
lblEmail.grid(column=0, row=2, padx=10, pady=10)

email = ttk.Entry(font=fuente)
email.grid(column=1, row=2, columnspan=2, padx=10, pady=10)

listaMujeres = ttk.Combobox(root, values=mujeres, width=20, state="readonly",font=fuente, style="TCombobox")
root.option_add('*TCombobox*Listbox.font', fuente)   # apply font to combobox list
listaMujeres.set(mujeres[0])
listaMujeres.grid(column=0,row=3,padx=5, pady=5)

btnIniciar = ttk.Button(root, text="INICIAR", command=iniciar, style="C.TButton")

btnIniciar.grid(column=1, row=3, padx=5, pady=5)

btnFinalizar = ttk.Button(root, text="FINALIZAR", command=finalizar, style="C.TButton")
btnFinalizar.grid(column=2, row=3, padx=10, pady=5)

lblVideo = tk.Label(root,height=500, background="#00a5a7")
lblVideo.grid(column=0, row=4, columnspan=3)


button = ttk.Button(root, text="SONRIE :)", command=save, style="C.TButton")
button.grid(column=0, row=5, columnspan=3)



root.mainloop()