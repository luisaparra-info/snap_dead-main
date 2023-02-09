import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.font import Font
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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


    frases_mujeres = (
        "Margarita Salas formó parte del primer equipo de trabajo que, en el Centro de Investigaciones Biológicas del CSIC de Madrid, introdujo un nuevo y poderoso ámbito de investigación: la biología molecular.",
        "Mae Jemison fue la primera mujer afroamericana que viajó al espacio, el 12 de septiembre de 1992.",
        "Barbara McClintock pasó a la historia por ser la primera mujer en recibir el Premio Nobel de Medicina",
        "Lise Meitner fue una física austriaca, descubridora de la fisión nuclear, un logro por el que su compañero de laboratorio Otto Hahn recibió el premio Nobel en 1944.",
        "Dozothy Czowfoot fue una química británica que identifico las estructuras tridimensionales de los cristales.",
    )
    # Iniciamos los parámetros del script
    remitente = 'luisaparra.info@gmail.com'
    destinatarios = email.get()
    asunto = 'ICV-11F - Día de la mujer y la niña en la ciencia'
    cuerpo = 'Hola '+ nombre.get()+ ". Has decidido ser "+listaMujeres.get()+". "+frases_mujeres[listaMujeres.current()]+" Un saludo y muchas gracias por participar. El equipo CDyPC - 1º Bachillerato" 
    ruta_adjunto = filepath
    nombre_adjunto = filepath
    
    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = destinatarios
    mensaje['Subject'] = asunto
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')
    
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login(remitente,'mdhkwczmqaexzwso')

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()

def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    seleccionarFiltro(listaMujeres.current())
    visualizar()

def seleccionarFiltro(seleccion):
    # Lectura de la imagen a incrustar en el video
    global filtro
    global variacion_alto
    global variacion_x
    global variacion_w

    variacion_x=0
    variacion_w=0

    print(seleccion)
    if (seleccion==0):
        filtro = cv2.imread('marga.png',-1)
        variacion_alto=70
        variacion_w=80
        variacion_x=20    
    elif (seleccion==1):
        filtro = cv2.imread('mae.png', -1)
        variacion_alto=70
        variacion_w=80
        variacion_x=40
    elif (seleccion==2):
        filtro = cv2.imread('barbara.png', -1)
        variacion_alto=70
        variacion_w=70
        variacion_x=30
    elif (seleccion==3):
        filtro = cv2.imread('lise.png', -1)
        variacion_alto=75
    elif (seleccion==4):
        filtro = cv2.imread('dorothy.png', -1)
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
                x=x - variacion_x
                w=w+ variacion_w
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)
                # Redimensionar la imagen de entrada de acuerdo al ancho del
                # rostro detectado
                
                resized_image = imutils.resize(filtro, width=w)
                print(w)
                filas_image = resized_image.shape[0]
                col_image = w

                # Determinar una porción del alto de la imagen de entrada 
                # redimensionada
                porcion_alto = filas_image  // 4 + variacion_alto
                

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
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            cap.release()
def finalizar():
    global cap
    cap.release()

cap = None
root = tk.Tk()
root.title("Día Internacional de la Mujer y la Niña en la Ciencia - 1º BACH - CDyPC")
root.geometry("640x800")


image1 = Image.open("cabecera.jpg")
cabezera = ImageTk.PhotoImage(image1)

label1 = tk.Label(image=cabezera)
label1.image = cabezera

root['background']='#00a5a7'

label1.grid(row=0, column=0, columnspan=3)

mujeres = (
    "Margarita Salas",
    "Mae Jemison",
    "Barabara McClintock",
    "Lise Meitner",
    "Dozothy Czowfoot",
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