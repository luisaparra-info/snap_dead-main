import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    seleccionarFiltro(listaMujeres.curselection()[0])
    visualizar()

def seleccionarFiltro(seleccion):
    # Lectura de la imagen a incrustar en el video
    global filtro
    global faceClassif
    print(seleccion)
    filtro = cv2.imread('star.png', cv2.IMREAD_UNCHANGED)
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



def visualizar():
    global filtro
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
                porcion_alto = filas_image // 4

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
                result = cv2.add(bg_black, bg_frame)
                if y + porcion_alto - filas_image >= 0:
                    frame[y + porcion_alto - filas_image : y + porcion_alto, x : x + col_image] = result
                else:
                    frame[0 : y + porcion_alto, x : x + col_image] = result
                   
            
            
            im = Image.fromarray(filtro)
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
mujeres = (
    "Persona1",
    "Persona2",
    "Persona3",
    "Persona4"
)

global listaMujeres 
listaMujeres = tk.Listbox()
listaMujeres.insert("0",*mujeres)
listaMujeres.grid(column=0,row=0)
listaMujeres.selection_set(0)
btnIniciar = tk.Button(root, text="Iniciar", width=45, command=iniciar)
btnIniciar.grid(column=1, row=0, padx=5, pady=5)

btnFinalizar = tk.Button(root, text="Finalizar", width=45, command=finalizar)
btnFinalizar.grid(column=2, row=0, padx=5, pady=5)

lblVideo = tk.Label(root)
lblVideo.grid(column=0, row=1, columnspan=3)

root.mainloop()