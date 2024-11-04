from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, Label, Frame
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error

ruta_imagen = ""
image_label = None 
selected_image_original = None

# Límites de tamaño para la imagen
max_width = 460
max_height = 215
min_width = 180
min_height = 252

def seleccionar_imagen():
    global ruta_imagen, image_label, selected_image_original
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if ruta_imagen:
        print(f"Imagen seleccionada: {ruta_imagen}")
        selected_image_original = Image.open(ruta_imagen)  # Guardamos la imagen original
        update_image_label()  # Llamar a la función de actualización de imagen

def update_image_label(event=None):
    global image_label, selected_image_original
    if selected_image_original:
        # Obtener las dimensiones originales de la imagen
        original_width, original_height = selected_image_original.size
        
        # Ajustar la imagen según la orientación manteniendo la relación de aspecto
        if original_width > original_height:  # Imagen horizontal
            width = min(max_width, original_width)
            height = int(width * original_height / original_width)
            if height > max_height:
                height = max_height
                width = int(height * original_width / original_height)
            # Posición para imagen horizontal
            x_pos, y_pos = 610, 100
        else:  # Imagen vertical
            height = min(max_height, original_height)
            width = int(height * original_width / original_height)
            if width > max_width:
                width = max_width
                height = int(width * original_height / original_width)
            # Posición para imagen vertical
            x_pos, y_pos = 770, 150  # Posición diferente para imágenes verticales
        
        # Redimensionar la imagen con los límites ajustados
        resized_image = selected_image_original.resize((width, height), Image.LANCZOS)
        selected_image = ImageTk.PhotoImage(resized_image)
        
        # Si image_label existe, actualízala; si no, crea una nueva
        if image_label:
            image_label.config(image=selected_image)
            image_label.image = selected_image  # Mantener la referencia
            image_label.place(x=x_pos, y=y_pos)  # Actualizar la posición según la orientación
        else:
            # Mostrar la imagen en el frame_registro
            image_label = Label(frame_registro, image=selected_image, bg="#1B2838")
            image_label.image = selected_image
            image_label.place(x=x_pos, y=y_pos)  # Posición según la orientación

def registrar_videojuego():
    nombre = entry_2.get()
    descripcion = entry_5.get("1.0", "end-1c")  
    precio = entry_4.get()
    fecha_lanzamiento = entry_3.get()
    desarrollador = entry_6.get()
    editor = entry_7.get()
    clasificacion_etaria = entry_8.get()
    calificacion_promedio = entry_9.get()

    try:
        insertar_datos(nombre, descripcion, precio, fecha_lanzamiento, desarrollador, editor, clasificacion_etaria, calificacion_promedio, ruta_imagen)
        print("Datos insertados correctamente.")
    except Exception as e:
        print(f"Error al insertar datos: {e}")



OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "../src/assets/frame0"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def insertar_datos(nombre, descripcion, precio, fecha_lanzamiento, desarrollador, editor, clasificacion_etaria, calificacion_promedio, ruta_imagen):
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='game_shop',
            user='sigma',
            password='Eskibiritoilet1*'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            sql_insert_query = """INSERT INTO videojuegos (nombre, descripcion, precio, fecha_lanzamiento, desarrollador, editor, clasificacion_etaria, calificacion_promedio, ruta_imagen)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"""
            valores = (nombre, descripcion, precio, fecha_lanzamiento, desarrollador, editor, clasificacion_etaria, calificacion_promedio,ruta_imagen)
            cursor.execute(sql_insert_query, valores)
            conexion.commit()
            print(f"{cursor.rowcount} registro(s) insertado(s).")
    except Error as e:
        print(f"Error al insertar datos: {e}")
        raise
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()



#Esto va para el archivo de logica , lo tengo aqui porque me daba error llamar la logica a este archivo inicio

window = Tk()

window.geometry("1080x600")
window.configure(bg = "#1B2838")
window.title("Registro")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (950 // 2)  # Centrar horizontalmente
y = (screen_height // 2) - (600 // 2)  # Centrar verticalmente
window.geometry(f"1080x600+{x}+{y}")

# Frame de Registro
frame_registro = Frame(window, bg="#1B2838")
frame_registro.place(x=0, y=0, width=1080, height=600)

# Canvas para el Frame de Registro
canvas = Canvas(
    frame_registro,
    bg="#1B2838",
    height=600,
    width=950,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Entries 
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(190.0, 119.5, image=entry_image_1)
entry_1 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_1.place(x=79.0, y=98.0, width=222.0, height=41.0)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(190.0, 205.5, image=entry_image_2)
entry_2 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_2.place(x=79.0, y=184.0, width=222.0, height=41.0)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(190.0, 291.5, image=entry_image_3)
entry_3 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_3.place(x=79.0, y=270.0, width=222.0, height=41.0)

entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(190.0, 375.5, image=entry_image_4)
entry_4 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_4.place(x=79.0, y=354.0, width=222.0, height=41.0)

entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(333.0, 466.0, image=entry_image_5)
entry_5 = Text(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_5.place(x=79.0, y=430.0, width=508.0, height=70.0)

entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(476.0, 119.5, image=entry_image_6)
entry_6 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_6.place(x=365.0, y=98.0, width=222.0, height=41.0)

entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(476.0, 205.5, image=entry_image_7)
entry_7 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_7.place(x=365.0, y=184.0, width=222.0, height=41.0)

entry_image_8 = PhotoImage(file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(476.0, 291.5, image=entry_image_8)
entry_8 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_8.place(x=365.0, y=270.0, width=222.0, height=41.0)

entry_image_9 = PhotoImage(file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(476.0, 375.5, image=entry_image_9)
entry_9 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_9.place(x=365.0, y=354.0, width=222.0, height=41.0)

# Labels
canvas.create_text(32.0, 7.0, anchor="nw", text="REGISTRO DE VIDEOJUEGO", fill="#FFFFFF", font=("Rubik Regular", 32 * -1))
canvas.create_text(73.0, 75.0, anchor="nw", text="Código", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))
canvas.create_text(359.0, 75.0, anchor="nw", text="Desarrollador", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))
canvas.create_text(359.0, 161.0, anchor="nw", text="Publisher", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))
canvas.create_text(359.0, 246.0, anchor="nw", text="Clasificación", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))
canvas.create_text(359.0, 332.0, anchor="nw", text="Calificación promedio", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))
canvas.create_text(74.0, 161.0, anchor="nw", text="Nombre", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))
canvas.create_text(74.0, 246.0, anchor="nw", text="Fecha de lanzamiento", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))
canvas.create_text(73.0, 332.0, anchor="nw", text="Precio", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))
canvas.create_text(73.0, 410.0, anchor="nw", text="Descripción", fill="#FFFFFF", font=("Rubik Regular", 14 * -1))

# Botones
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(frame_registro, image=button_image_1, borderwidth=0, highlightthickness=0, command=registrar_videojuego, relief="flat")
button_1.place(x=73.0, y=524.0, width=110.0, height=33.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(frame_registro, image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_2 clicked"), relief="flat")
button_2.place(x=205.0, y=524.0, width=110.0, height=33.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(frame_registro, image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: print("button_3 clicked"), relief="flat")
button_3.place(x=476.0, y=524.0, width=110.0, height=33.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(frame_registro, image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: print("button_4 clicked"), relief="flat")
button_4.place(x=802.0, y=524.0, width=110.0, height=33.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(frame_registro, image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: print("button_5 clicked"), relief="flat")
button_5.place(x=651.0, y=524.0, width=110.0, height=33.0)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(frame_registro, image=button_image_6, borderwidth=0, highlightthickness=0, command=seleccionar_imagen, relief="flat")
button_6.place(x=800.0, y=466.0, width=127.0, height=23.0)

button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
button_7 = Button(frame_registro, image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: print("button_7 clicked"), relief="flat")
button_7.place(x=340.0, y=524.0, width=110.0, height=33.0)

button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
button_8 = Button(frame_registro, image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: frame_catalogo.lift(), relief="flat")
button_8.place(x=932.0, y=12.0, width=110.0, height=33.0)

button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
button_9 = Button(frame_registro, image=button_image_9, borderwidth=0, highlightthickness=0, command=lambda: print("button_9 clicked"), relief="flat")
button_9.place(x=980.0, y=516.0, width=44.0, height=43.0)

button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
button_10 = Button(frame_registro, image=button_image_10, borderwidth=0, highlightthickness=0, command=lambda: print("button_10 clicked"), relief="flat")
button_10.place(x=939.0, y=516.0, width=44.0, height=43.0)

# Frame de Catálogo
frame_catalogo = Frame(window, bg="#1B2838")
frame_catalogo.place(x=0, y=0, width=1080, height=600)

# Iniciar mostrando el frame de registro
frame_registro.lift()


# Título del Frame Catálogo
Label(
    frame_catalogo,
    text="Catálogo de Videojuegos",
    font=("Rubik Regular", 32),
    bg="#1B2838",
    fg="#FFFFFF"
).place(x=32, y=10)

# Crear una cuadrícula de "tarjetas" de videojuegos
for i in range(3):
    for j in range(3):
        tarjeta = Label(
            frame_catalogo,
            text=f"Juego {i * 3 + j + 1}",
            font=("Rubik Regular", 14),
            bg="#305E80",
            fg="#FFFFFF",
            width=20,
            height=5,
            relief="ridge"
        )
        tarjeta.grid(row=i, column=j, padx=20, pady=20, sticky="nsew", in_=frame_catalogo) 

# Botón para regresar al frame de registro
button_regresar = Button(
    frame_catalogo,
    text="Regresar",
    command=lambda: frame_registro.lift(),  # Cambiar al frame de registro
    bg="#001B48",
    fg="#FFFFFF",
    font=("Rubik Regular", 12),
    relief="flat"
)
button_regresar.place(x=802, y=12, width=110, height=33)
window.resizable(False, False)
window.mainloop()