from ctypes import c_buffer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from tkinter import Toplevel
from pathlib import Path
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import simpledialog
import tkinter as tk
from tkinter import Tk, messagebox, Canvas, Toplevel, Entry, Text, Button, PhotoImage, filedialog, Label, Frame, OptionMenu, StringVar, Scrollbar
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import io
import os
import threading
import time
import subprocess
import tempfile

# Variables globales
global ruta_imagen
ruta_imagen = ""
image_label = None 
selected_image_original = None
current_index = 0  
records = []  
num_registros = 0 

window = Tk()

# Frame de Registro
frame_registro = Frame(window, bg="#1B2838")
frame_registro.place(x=0, y=0, width=1080, height=600)

# Añadir el campo de entrada para entry_1
entry_1 = Entry(frame_registro, bg="white", fg="black", width=40)
entry_1.place(x=20, y=20)  

# Límites de tamaño para la imagen
max_width = 460
max_height = 215
min_width = 180
min_height = 252

# Variables de configuración
OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "../src/assets/frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Conexión a la base de datos y obtención de registros
def obtener_registros():
    global records
    try:
        conexion = mysql.connector.connect(
            host='gameshop.mysql.database.azure.com',  # El nombre del servidor de Azure          
            database='game_shop',
            user='sigma',  # Usuario de la base de datos en Azure
            password='Eskibiritoilet1*'
            
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM videojuegos")
            records = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error al obtener registros: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
obtener_registros()



# Función para mostrar el registro actual en los campos de entrada
def mostrar_registro():
    global current_index, records, image_label, ruta_imagen
    
    # Limpiar los campos de entrada
    entry_1.delete(0, "end")
    entry_2.delete(0, "end")
    entry_5.delete("1.0", "end")
    entry_4.delete(0, "end")
    entry_3.delete(0, "end")
    entry_6.delete(0, "end")
    entry_7.delete(0, "end")
    selected_option.set("")  # Limpiar clasificación etaria
    entry_9.delete(0, "end")
    
    # Limpiar la imagen antes de cargar la nueva
    if image_label:
        image_label.config(image=None)  # Elimina la imagen de la etiqueta
        image_label.image = None  # Limpia la referencia a la imagen
    
    # Si no hay registros, salir
    if not records:
        print("No hay registros para mostrar.")
        return
    
    # Si hay registros, proceder a mostrar el actual
    registro = records[current_index]
    
    # Llenar los campos con los valores del registro
    entry_1.insert(0, registro[0])  # ID
    entry_2.insert(0, registro[1])  # Nombre
    entry_5.insert("1.0", registro[2])  # Descripción
    entry_4.insert(0, registro[3])  # Precio
    entry_3.insert(0, registro[4])  # Fecha de lanzamiento
    entry_6.insert(0, registro[5])  # Desarrollador
    entry_7.insert(0, registro[6])  # Editor
    selected_option.set(registro[7])  # Clasificación etaria
    entry_9.insert(0, registro[8])  # Calificación promedio

    # Reiniciar ruta_imagen
    ruta_imagen = registro[9]  # Ruta relativa de la imagen
    if ruta_imagen and isinstance(ruta_imagen, str) and ruta_imagen.strip():  # Verifica que la ruta no esté vacía
        # Validar existencia y cargar imagen
        cargar_imagen(ruta_imagen)
    else:
        print("No se encontró una ruta de imagen válida.")


# Funciones para moverse entre registros
def mover_izquierda():
    global current_index
    if records and current_index > 0:
        current_index -= 1
        mostrar_registro()

def mover_derecha():
    global current_index
    if records and current_index < len(records) - 1:
        current_index += 1
        mostrar_registro()


# Obtener el directorio base del proyecto (Gestion-de-archivos)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))  # Subir al directorio raíz del proyecto
IMAGES_DIR = os.path.join(BASE_DIR, 'Imagenes de los juegos')  # Carpeta de imágenes dentro del proyecto

# Función para cargar la imagen desde la ruta
def cargar_imagen(nombre_imagen):
    global ruta_imagen, image_label

    if nombre_imagen and isinstance(nombre_imagen, str):
        # Crear la ruta completa a la imagen dentro del repositorio
        nueva_ruta_imagen = os.path.join(IMAGES_DIR, nombre_imagen)
        
        # Asegurarse de que la ruta sea válida y corregir las barras invertidas en sistemas Windows
        nueva_ruta_imagen = os.path.normpath(nueva_ruta_imagen)  # Ajusta las barras para cualquier sistema

        # Imprimir la ruta para depuración
        print(f"Comprobando imagen en: {nueva_ruta_imagen}")

        # Verificar si la imagen existe en la ruta generada
        if os.path.exists(nueva_ruta_imagen):
            try:
                pil_image = Image.open(nueva_ruta_imagen)
                pil_image_resized = pil_image.resize((460, 215))
                selected_image = ImageTk.PhotoImage(pil_image_resized)

                ruta_imagen = nueva_ruta_imagen  # Actualizamos la ruta relativa
                if image_label:
                    image_label.config(image=selected_image)
                    image_label.image = selected_image
                else:
                    image_label = Label(frame_registro, image=selected_image, bg="#1B2838")
                    image_label.image = selected_image
                    image_label.place(x=610.0, y=100.0)

                print(f"Imagen cargada desde: {ruta_imagen}")
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
        else:
            print(f"La imagen no existe en la ruta: {nueva_ruta_imagen}")
    else:
        print("Nombre de imagen no válido.")
        
# Función para limpiar todos los campos de entrada y la imagen
def limpiar_campos():
    entry_1.delete(0, "end")  # Limpia el campo Número
    entry_2.delete(0, "end")  # Limpia el campo Nombre
    entry_3.delete(0, "end")  # Limpia el campo Fecha de lanzamiento
    entry_4.delete(0, "end")  # Limpia el campo Precio
    entry_5.delete("1.0", "end")  # Limpia el campo Descripción (Text widget)
    entry_6.delete(0, "end")  # Limpia el campo Desarrollador
    entry_7.delete(0, "end")  # Limpia el campo Editor
    selected_option.set(opciones_clasificacion[0])  # Restablece la opción de clasificación a la inicial
    entry_9.delete(0, "end")  # Limpia el campo Calificación promedio
    
    # Limpia la imagen
    if image_label:
        image_label.config(image=None)  # Elimina la imagen del label
        image_label.image = None  # Elimina la referencia a la imagen




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
def wrap_text(text, width, font_name="Helvetica", font_size=12):
    """
    Función para ajustar el texto largo a un ancho dado, dividiendo en líneas si es necesario.
    """
    from reportlab.lib.pagesizes import letter
    import textwrap
    
    lines = textwrap.wrap(text, width=width)
    return lines

def justify_text(c, text, x_position, y_position, max_width):
    """
    Justifica el texto dentro de un ancho máximo, distribuyendo el espacio entre las palabras.
    """
    words = text.split()
    if len(words) == 1:
        # Si solo hay una palabra, no necesita justificar
        c.drawString(x_position, y_position, words[0])
        return y_position - 18  # Ajustar el espacio entre líneas

    # Calcular el espacio disponible para distribuir
    total_text_width = sum([c.stringWidth(word, "Helvetica", 12) for word in words])
    total_space = max_width - total_text_width
    spaces_needed = len(words) - 1
    space_between_words = total_space / spaces_needed if spaces_needed > 0 else total_space

    # Dibujar las palabras con el espacio distribuido
    current_x = x_position
    for i, word in enumerate(words):
        c.drawString(current_x, y_position, word)
        current_x += c.stringWidth(word, "Helvetica", 12) + space_between_words

    return y_position - 18  # Ajustar el espacio entre líneas

def crear_pdf():
    global ruta_imagen 
    
    # Verificar que la ruta de la imagen sea válida
    if not ruta_imagen or not os.path.exists(ruta_imagen):
        print(f"La ruta de la imagen no existe o es inválida: {ruta_imagen}")
        return

    # Crear el PDF en memoria
    pdf_buffer = io.BytesIO()
    c = pdf_canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    # Título y diseño del encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 40, "Registro de Juego")

    # Línea de separación
    c.setLineWidth(1)
    c.line(100, height - 50, width - 100, height - 50)

    # Inicializamos la posición vertical
    y_position = height - 80

    # Detalles del registro (con espacios ajustados)
    c.setFont("Helvetica", 12)
    
    # Ajustando el texto hacia la derecha
    offset_x = 50  # Desplazar el texto hacia la derecha
    c.drawString(100 + offset_x, y_position, "Código: ")
    c.drawString(250 + offset_x, y_position, f"{entry_1.get()}")
    y_position -= 25  # Espacio entre campos incrementado

    c.drawString(100 + offset_x, y_position, "Nombre: ")
    c.drawString(250 + offset_x, y_position, f"{entry_2.get()}")
    y_position -= 25  # Espacio entre campos incrementado

    c.drawString(100 + offset_x, y_position, "Fecha de lanzamiento: ")
    c.drawString(250 + offset_x, y_position, f"{entry_3.get()}")
    y_position -= 25  # Espacio entre campos incrementado

    c.drawString(100 + offset_x, y_position, "Precio: ")
    c.drawString(250 + offset_x, y_position, f"{entry_4.get()}")
    y_position -= 25  # Espacio entre campos incrementado

    c.drawString(100 + offset_x, y_position, "Descripción: ")
    y_position -= 0  # Mover hacia abajo para comenzar la descripción
    descripcion = entry_5.get('1.0', 'end').strip()
    descripcion_lines = wrap_text(descripcion, width=50)

    # Justificar y dibujar cada línea de la descripción
    for line in descripcion_lines:
        y_position = justify_text(c, line, 250 + offset_x, y_position, width - 359)
    
    # Si la descripción sigue siendo muy larga, añade un salto de página
    if y_position < 100:
        c.showPage()
        y_position = height - 40

    c.drawString(100 + offset_x, y_position, "Desarrollador: ")
    c.drawString(250 + offset_x, y_position, f"{entry_6.get()}")
    y_position -= 25  # Espacio entre campos incrementado

    c.drawString(100 + offset_x, y_position, "Editor: ")
    c.drawString(250 + offset_x, y_position, f"{entry_7.get()}")
    y_position -= 25  # Espacio entre campos incrementado

    c.drawString(100 + offset_x, y_position, "Clasificación: ")
    c.drawString(250 + offset_x, y_position, f"{selected_option.get()}")
    y_position -= 25  # Espacio entre campos incrementado

    c.drawString(100 + offset_x, y_position, "Calificación promedio: ")
    c.drawString(250 + offset_x, y_position, f"{entry_9.get()}")
    y_position -= 25  # Espacio entre campos incrementado

    # Ajustar el tamaño de la imagen y añadirla centrada
    try:
        selected_image = Image.open(ruta_imagen)  # Intentar abrir la imagen
        print(f"Imagen cargada para PDF: {ruta_imagen}")
        
        # Obtener el tamaño de la imagen
        img_width, img_height = selected_image.size
        aspect_ratio = img_width / img_height

        # Ajustar el tamaño de la imagen
        new_width = 200  # Ancho deseado
        new_height = new_width / aspect_ratio  # Mantener el aspecto

        # Calcular la posición centrada para la imagen
        img_x = (width - new_width) / 2  # Centrado horizontal
        img_y = y_position - new_height - 20  # Asegurarnos de que la imagen no sobrepase la página

        # Añadir la imagen al PDF
        c.drawImage(ruta_imagen, img_x, img_y, width=new_width, height=new_height)

    except Exception as e:
        print(f"Error al añadir la imagen al PDF: {e}")

    # Finalizar la página y el PDF
    c.showPage()  # Finaliza la página
    c.save()  # Guardar el PDF en el buffer de memoria
    pdf_buffer.seek(0)  # Regresar al inicio del buffer

    # Guardar el archivo PDF en un archivo temporal
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_buffer.getvalue())
            temp_file_path = temp_file.name
            print(f"Archivo PDF temporal creado en: {temp_file_path}")
        
        # Abrir el archivo PDF temporal
        if os.name == 'nt':  # Windows
            os.startfile(temp_file_path)
        elif os.name == 'posix':  # Linux o macOS
            # Cambia 'open' por 'xdg-open' para Linux
            opener = 'xdg-open' if os.uname().sysname == 'Linux' else 'open'
            subprocess.call([opener, temp_file_path])

    except Exception as e:
        print(f"Error al guardar o abrir el archivo PDF temporal: {e}")
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

# Función para seleccionar y convertir la ruta de la imagen
def seleccionar_imagen():
    global ruta_imagen
    # Abrir cuadro de diálogo para seleccionar archivo
    ruta_absoluta = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    
    if ruta_absoluta:
        # Convertir la ruta absoluta a una ruta relativa respecto a BASE_DIR
        ruta_imagen = os.path.relpath(ruta_absoluta, IMAGES_DIR)
        
        # Mostrar la ruta relativa en la consola para depuración
        print(f"Ruta relativa generada: {ruta_imagen}")
        
        # Llamar a la función para cargar la imagen con la nueva ruta
        cargar_imagen(ruta_imagen)


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
            x_pos, y_pos = 770, 150
        
        # Redimensionar la imagen con los límites ajustados
        resized_image = selected_image_original.resize((width, height), Image.LANCZOS)
        selected_image = ImageTk.PhotoImage(resized_image)
        
        # Si image_label existe, actualízala; si no, crea una nueva
        if image_label:
            image_label.config(image=selected_image)
            image_label.image = selected_image  # Mantener la referencia
            image_label.place(x=x_pos, y=y_pos)  
        else:
            # Mostrar la imagen en el frame_registro
            image_label = Label(frame_registro, image=selected_image, bg="#1B2838")
            image_label.image = selected_image
            image_label.place(x=x_pos, y=y_pos)  

# Función para monitorear nuevos registros en la base de datos
actualizando_registros = False

def monitorear_registros():
    global num_registros, actualizando_registros
    while True:
        try:
            conexion = mysql.connector.connect(
            host='gameshop.mysql.database.azure.com',
            database='game_shop',
            user='sigma',
            password='Eskibiritoilet1*'
            )
            if conexion.is_connected():
                cursor = conexion.cursor()
                cursor.execute("SELECT COUNT(*) FROM videojuegos")
                nuevo_num_registros = cursor.fetchone()[0]

                if nuevo_num_registros > num_registros:
                    if not actualizando_registros:  # Solo actualizar si no se está actualizando actualmente
                        actualizando_registros = True
                        print("Nuevo registro detectado. Actualizando...")
                        obtener_registros()  # Actualiza records con los nuevos datos
                        num_registros = nuevo_num_registros 
                        actualizando_registros = False
        except mysql.connector.Error as e:
            print(f"Error en el monitoreo de registros: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
        time.sleep(2)  # Revisa la base de datos cada 2 segundos

# Iniciar el hilo de monitoreo
hilo_monitoreo = threading.Thread(target=monitorear_registros, daemon=True)
hilo_monitoreo.start()

# Función para registrar un videojuego en la base de datos
def registrar_videojuego():
    if (not entry_1.get() or not entry_2.get() or not entry_5.get("1.0", "end-1c").strip() or 
        not entry_4.get() or not entry_3.get() or not entry_6.get() or 
        not entry_7.get() or not selected_option.get() or not entry_9.get() or not ruta_imagen):
        
        messagebox.showwarning("Campos vacíos", "Por favor, llene todos los campos antes de registrar el videojuego.")
        return

    try:
        conexion = mysql.connector.connect(
            host='gameshop.mysql.database.azure.com',  
            database='game_shop',
            user='sigma',
            password='Eskibiritoilet1*'
        )
        
        if conexion.is_connected():
            cursor = conexion.cursor()

            sql = """INSERT INTO videojuegos (id_videojuego, nombre, descripcion, precio, fecha_lanzamiento, desarrollador, editor, clasificacion_etaria, calificacion_promedio, ruta_imagen) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            datos = (
                entry_1.get(),  
                entry_2.get(),
                entry_5.get("1.0", "end-1c"),
                entry_4.get(),
                entry_3.get(),
                entry_6.get(),
                entry_7.get(),
                selected_option.get(),
                entry_9.get(),
                ruta_imagen  
            )

            cursor.execute(sql, datos)
            conexion.commit()
            messagebox.showinfo("Éxito", "El videojuego se ha registrado exitosamente.")
            print("Registro exitoso")
    except Error as e:
        messagebox.showerror("Error", f"Error al registrar el videojuego: {e}")
        print(f"Error al registrar el videojuego: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#Esto va para el archivo de logica , lo tengo aqui porque me daba error llamar la logica a este archivo inicio

window.geometry("1080x600")
window.configure(bg = "#1B2838")
window.title("Registro")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (1080 // 2)  # Centrar horizontalmente
y = (screen_height // 2) - (600 // 2)  # Centrar verticalmente
window.geometry(f"1080x600+{x}+{y}")


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
# Función para permitir solo números en el Entry
def only_numbers(event):
    # Comprobar si la tecla presionada es un dígito o una tecla de control (backspace, delete)
    if event.char.isdigit() or event.keysym in ["BackSpace", "Delete"]:
        return
    else:
        # Si no es un número, se ignora el evento (previene la entrada)
        return "break"
entry_1 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_1.place(x=79.0, y=98.0, width=222.0, height=41.0)
entry_1.bind("<KeyPress>", only_numbers)

# Función para buscar el registro con el código ingresado en entry_1
def buscar_videojuego_por_codigo():
    codigo = entry_1.get()

    # Verificar que se haya ingresado un código
    if not codigo:
        messagebox.showinfo("Error", "Ingrese un código para buscar el registro.")
        return

    try:
        conexion = mysql.connector.connect(
            host='gameshop.mysql.database.azure.com',  # El nombre del servidor de Azure          
            database='game_shop',
            user='sigma',  # Usuario de la base de datos en Azure
            password='Eskibiritoilet1*'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Consultar el registro por el código
            sql = "SELECT nombre, descripcion, precio, fecha_lanzamiento, desarrollador, editor, clasificacion_etaria, calificacion_promedio, ruta_imagen FROM videojuegos WHERE id_videojuego = %s"
            cursor.execute(sql, (codigo,))
            registro = cursor.fetchone()

            if registro:
                # Mostrar los datos en los campos de entrada
                entry_2.delete(0, "end")
                entry_2.insert(0, registro[0])  # nombre

                entry_5.delete("1.0", "end")
                entry_5.insert("1.0", registro[1])  # descripcion

                entry_4.delete(0, "end")
                entry_4.insert(0, registro[2])  # precio

                entry_3.delete(0, "end")
                entry_3.insert(0, registro[3])  # fecha_lanzamiento

                entry_6.delete(0, "end")
                entry_6.insert(0, registro[4])  # desarrollador

                entry_7.delete(0, "end")
                entry_7.insert(0, registro[5])  # editor

                selected_option.set(registro[6])  # clasificacion_etaria

                entry_9.delete(0, "end")
                entry_9.insert(0, registro[7])  # calificacion_promedio

                ruta_imagen = registro[8]
                if isinstance(ruta_imagen, str) and ruta_imagen:
                    cargar_imagen(ruta_imagen)
                else:
                    print("No se encontró una ruta de imagen válida.")
            else:
                messagebox.showinfo("Error", f"No se encontró ningún registro con el código {codigo}.")

    except Error as e:
        print(f"Error al buscar el videojuego: {e}")
        messagebox.showerror("Error", f"Error al buscar el videojuego: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(190.0, 205.5, image=entry_image_2)
entry_2 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_2.place(x=79.0, y=184.0, width=222.0, height=41.0)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(190.0, 291.5, image=entry_image_3)
def on_entry_click(event):
    """Función que se llama cuando el usuario hace clic en el Entry."""
    if entry_3.get() == 'yyyy-mm-dd':
        entry_3.delete(0, tk.END)  # Borra el placeholder
        entry_3.config(fg="#000716")  # Cambia el color del texto

def on_focusout(event):
    """Función que se llama cuando el Entry pierde el foco."""
    if entry_3.get() == '':
        entry_3.insert(0, 'yyyy-mm-dd')  # Muestra el placeholder
        entry_3.config(fg="#000716")  # Cambia el color del placeholder

def validate_input(event):
    """Función que valida la entrada del Entry."""
    if event.char.isdigit() or event.char == '-' or event.keysym in ["BackSpace", "Delete"]:
        # Permitir entrada, pero limitar la longitud a 10 caracteres
        if len(entry_3.get()) < 10 or event.keysym in ["BackSpace", "Delete"]:
            return  # Permitir la entrada
    return "break"  # Bloquear la entrada no válid
entry_3 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_3.place(x=79.0, y=270.0, width=222.0, height=41.0)
entry_3.insert(0, 'yyyy-mm-dd')  # Inserta el placeholder
entry_3.bind('<FocusIn>', on_entry_click)  # Bind para hacer clic en el Entry
entry_3.bind('<FocusOut>', on_focusout)  # Bind para cuando pierde foco
entry_3.bind('<KeyPress>', validate_input)  # Validación en KeyPress

entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(190.0, 375.5, image=entry_image_4)
def only_numbers_and_dot(event):
    # Permitir dígitos, el punto (.), y teclas de control (BackSpace, Delete, Left, Right)
    if event.char.isdigit() or event.char == ".":
        # Si es un punto, asegurarse de que solo haya uno en el campo
        if event.char == "." and entry_4.get().count(".") >= 1:
            return "break"
        
        # Si ya existe un punto, limitar a dos dígitos decimales
        if "." in entry_4.get():
            decimal_part = entry_4.get().split(".")[1]
            if len(decimal_part) >= 2:
                return "break"
        return
    elif event.keysym in ["BackSpace", "Delete", "Left", "Right"]:
        return
    else:
        return "break"
entry_4 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_4.place(x=79.0, y=354.0, width=222.0, height=41.0)
entry_4.bind("<KeyPress>", only_numbers_and_dot)

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
# Lista de opciones
opciones_clasificacion = ["E", "E10+", "T", "M", "A", "RP"]
# Variable para almacenar el valor seleccionado
selected_option = StringVar()
selected_option.set(opciones_clasificacion[0])  # Valor inicial
entry_8 = OptionMenu(frame_registro, selected_option, *opciones_clasificacion)
entry_8.config(bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_8.place(x=365.0, y=270.0, width=222.0, height=41.0)

entry_image_9 = PhotoImage(file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(476.0, 375.5, image=entry_image_9)
def only_numbers_and_dot(event):
    # Permitir dígitos, el punto (.), y teclas de control (BackSpace, Delete, Left, Right)
    if event.char.isdigit() or event.char == ".":
        # Si es un punto, asegurarse de que solo haya uno en el campo
        if event.char == "." and entry_9.get().count(".") >= 1:
            return "break"
        
        # Si ya existe un punto, limitar a dos dígitos decimales
        if "." in entry_9.get():
            decimal_part = entry_9.get().split(".")[1]
            if len(decimal_part) >= 2:
                return "break"
        
        return
    elif event.keysym in ["BackSpace", "Delete", "Left", "Right"]:
        return
    else:
        return "break"
entry_9 = Entry(frame_registro, bd=0, bg="#305E80", fg="#000716", highlightthickness=0)
entry_9.place(x=365.0, y=354.0, width=222.0, height=41.0)
entry_9.bind("<KeyPress>", only_numbers_and_dot)

canvas_superior = Canvas(frame_registro, width=1080, height=60, bg="#171D25", highlightthickness=0)
canvas_superior.place(x=0, y=0)

# Labels
canvas_superior.create_text(32.0, 15.0,  anchor="nw",text="REGISTRO DE VIDEOJUEGO",fill="#FFFFFF",font=("Rubik Regular", 20))
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

def editar_videojuego():
    global current_index, records

    if not records:
        print("No hay registros para editar.")
        return

    registro_actual = records[current_index]

    # Verificar si hay cambios en los campos
    cambios = (
        entry_1.get() != registro_actual[0] or
        entry_2.get() != registro_actual[1] or
        entry_5.get("1.0", "end-1c") != registro_actual[2] or
        entry_4.get() != registro_actual[3] or
        entry_3.get() != registro_actual[4] or
        entry_6.get() != registro_actual[5] or
        entry_7.get() != registro_actual[6] or
        selected_option.get() != registro_actual[7] or
        entry_9.get() != registro_actual[8] or
        ruta_imagen != registro_actual[9]
    )

    # Si no hay cambios, preguntar si el usuario quiere editar
    if not cambios:
        codigo = entry_1.get()
        respuesta = messagebox.askyesno("Confirmación", f"¿Desea editar el registro número {codigo}?")
        if not respuesta:
            return
        else:
            messagebox.showinfo("Edición habilitada", "Ahora puede realizar cambios y presionar de nuevo para actualizar.")
            return  # Salir de la función y permitir al usuario hacer cambios

    # Confirmar antes de actualizar si ya hay cambios
    respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea actualizar el registro con los cambios realizados?")
    if not respuesta:
        return

    # Realizar la actualización
    try:
        conexion = mysql.connector.connect(
            host='gameshop.mysql.database.azure.com',  # El nombre del servidor de Azure          
            database='game_shop',
            user='sigma',  # Usuario de la base de datos en Azure
            password='Eskibiritoilet1*'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Actualizar el registro en la base de datos
            sql = """UPDATE videojuegos SET nombre = %s, descripcion = %s, precio = %s, fecha_lanzamiento = %s,
                     desarrollador = %s, editor = %s, clasificacion_etaria = %s, calificacion_promedio = %s,
                     ruta_imagen = %s WHERE id_videojuego = %s"""
            datos = (
                entry_2.get(),
                entry_5.get("1.0", "end-1c"),
                entry_4.get(),
                entry_3.get(),
                entry_6.get(),
                entry_7.get(),
                selected_option.get(),
                entry_9.get(),
                ruta_imagen,
                entry_1.get()
            )

            cursor.execute(sql, datos)
            conexion.commit()
            print("Registro actualizado exitosamente.")
            messagebox.showinfo("Éxito", "Registro actualizado exitosamente.")
    except Error as e:
        print(f"Error al actualizar el videojuego: {e}")
        messagebox.showerror("Error", f"Error al actualizar el videojuego: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

button_2 = Button(
    frame_registro,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=editar_videojuego,
    relief="flat"
)
button_2.place(x=205.0, y=524.0, width=110.0, height=33.0)


button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
def eliminar_videojuego():
    global current_index, records

    if not records:
        print("No hay registros para eliminar.")
        return

    
    respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que quieres eliminar este registro?")
    if not respuesta:
        return

    
    codigo_videojuego = records[current_index][0]

    try:
        conexion = mysql.connector.connect(
            host='gameshop.mysql.database.azure.com',  # El nombre del servidor de Azure          
            database='game_shop',
            user='sigma',  # Usuario de la base de datos en Azure
            password='Eskibiritoilet1*'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()

            
            sql = "DELETE FROM videojuegos WHERE id_videojuego = %s"
            cursor.execute(sql, (codigo_videojuego,))
            conexion.commit()
            print(f"Registro con ID {codigo_videojuego} eliminado exitosamente.")
            messagebox.showinfo("Éxito", "Registro eliminado exitosamente.")

            
            records.pop(current_index)

            if current_index >= len(records):
                current_index = len(records) - 1  

            if records:
                mostrar_registro()  
            else:
                limpiar_campos()  

    except Error as e:
        print(f"Error al eliminar el videojuego: {e}")
        messagebox.showerror("Error", f"Error al eliminar el videojuego: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
button_3 = Button(frame_registro, image=button_image_3, borderwidth=0, highlightthickness=0, command=eliminar_videojuego, relief="flat")
button_3.place(x=476.0, y=524.0, width=110.0, height=33.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(frame_registro, image=button_image_4, borderwidth=0, highlightthickness=0, command=crear_pdf, relief="flat")
button_4.place(x=700.0, y=524.0, width=110.0, height=33.0)


# Configuración del botón para buscar
button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    frame_registro,
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=buscar_videojuego_por_codigo,
    relief="flat"
)
button_5.place(x=800.0, y=12.0, width=110.0, height=33.0)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(frame_registro, image=button_image_6, borderwidth=0, highlightthickness=0, command=seleccionar_imagen, relief="flat")
button_6.place(x=800.0, y=466.0, width=127.0, height=23.0)

button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
button_7 = Button(frame_registro, image=button_image_7, borderwidth=0, highlightthickness=0, command=limpiar_campos, relief="flat")
button_7.place(x=340.0, y=524.0, width=110.0, height=33.0)

button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
button_8 = Button(frame_registro, image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: frame_catalogo.lift(), relief="flat")
button_8.place(x=932.0, y=12.0, width=110.0, height=33.0)

button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
button_9 = Button(frame_registro, image=button_image_9, borderwidth=0, highlightthickness=0, command=mover_derecha, relief="flat")
button_9.place(x=980.0, y=516.0, width=44.0, height=43.0)

button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
button_10 = Button(frame_registro, image=button_image_10, borderwidth=0, highlightthickness=0, command=mover_izquierda,  relief="flat")
button_10.place(x=939.0, y=516.0, width=44.0, height=43.0)


# Frame de Catálogo
frame_catalogo = Frame(window, bg="#1B2838")
frame_catalogo.place(x=0, y=0, width=1080, height=600)

# Iniciar mostrando el frame de registro
frame_registro.lift()

# Obtener y mostrar los videojuegos en el catálogo
def obtener_videojuegos():
    conexion = mysql.connector.connect(
        host='gameshop.mysql.database.azure.com',  
        database='game_shop',
        user='sigma',  
        password='Eskibiritoilet1*'
    )
    threading.Thread(target=monitorear_registros, daemon=True).start()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, desarrollador, editor, clasificacion_etaria, calificacion_promedio, ruta_imagen FROM videojuegos")
    videojuegos = cursor.fetchall()
    conexion.close()

    return videojuegos

# Función para crear el efecto hover
def mostrar_detalles(event, detalles_frame):
    detalles_frame.place(relx=0.5, rely=0.5, anchor="center")

def ocultar_detalles(event, detalles_frame):
    detalles_frame.place_forget()

canvas_superior2 = Canvas(frame_catalogo, width=1080, height=60, bg="#171D25", highlightthickness=0)
canvas_superior2.place(x=0, y=0)

# Título del Frame Catálogo
titulo = Label(
    canvas_superior2,
    text="Catálogo de Videojuegos",
    font=("Rubik Regular", 32),
    bg="#171D25",
    fg="#FFFFFF"
)
titulo.pack(pady=10)

# Frame para contener las tarjetas y el scrollbar
contenedor_tarjetas = Frame(frame_catalogo, bg="#1B2838")
contenedor_tarjetas.place(x=0, y=80, width=1080, height=540)

# Canvas y Scrollbar para las tarjetas
canvas_tarjetas = Canvas(contenedor_tarjetas, bg="#1B2838", highlightthickness=0)
scroll_y = Scrollbar(contenedor_tarjetas, orient="vertical", command=canvas_tarjetas.yview)
frame_tarjetas = Frame(canvas_tarjetas, bg="#1B2838")

# Configuración del scrollbar en el Canvas
canvas_tarjetas.create_window((0, 0), window=frame_tarjetas, anchor="nw")
canvas_tarjetas.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")
canvas_tarjetas.pack(side="left", fill="both", expand=True)

# Función para actualizar el tamaño del canvas
def ajustar_scroll(event):
    canvas_tarjetas.configure(scrollregion=canvas_tarjetas.bbox("all"))

frame_tarjetas.bind("<Configure>", ajustar_scroll)

videojuegos = obtener_videojuegos()
for idx, (nombre, desarrollador, editor, clasificacion, calificacion, ruta_imagen) in enumerate(videojuegos):
    row = idx // 2
    col = idx % 2

    # Crear la tarjeta
    tarjeta = Frame(frame_tarjetas, bg="#305E80", width=540, height=300, relief="ridge", bd=2)
    tarjeta.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    # Usar la función cargar_imagen para cargar la imagen
    try:
        # Si se tiene la ruta relativa desde la base de datos
        cargar_imagen(ruta_imagen)
        imagen = Image.open(os.path.join(IMAGES_DIR, ruta_imagen))  # Usamos la ruta relativa ajustada
        imagen = imagen.resize((460, 215), Image.LANCZOS)
        img = ImageTk.PhotoImage(imagen)
        etiqueta_imagen = Label(tarjeta, image=img, bg="#305E80")
        etiqueta_imagen.image = img
        etiqueta_imagen.pack()
    except Exception as e:
        etiqueta_imagen = Label(tarjeta, text="Sin Imagen", width=34, height=8, bg="#444444", fg="White")
        etiqueta_imagen.pack()

    # Crear el frame de detalles que aparecerá al hover
    detalles_frame = Frame(tarjeta, bg="#444444", width=340, height=160)
    Label(detalles_frame, text=f"Desarrollador: {desarrollador}", bg="#444444", fg="White").pack(pady=5)
    Label(detalles_frame, text=f"Editor: {editor}", bg="#444444", fg="white").pack()

    # Eventos para mostrar/ocultar el frame de detalles
    etiqueta_imagen.bind("<Enter>", lambda e, frame=detalles_frame: mostrar_detalles(e, frame))
    etiqueta_imagen.bind("<Leave>", lambda e, frame=detalles_frame: ocultar_detalles(e, frame))

    # Frame inferior para nombre, clasificación, y calificación
    info_frame = Frame(tarjeta, bg="#305E80")
    info_frame.pack(fill="x", pady=(5, 0))
    Label(info_frame, text=nombre, font=("Rubik Regular", 12), bg="#305E80", fg="#FFFFFF").pack(side="top", pady=(0, 5))
    Label(info_frame, text=clasificacion, font=("Rubik Regular", 11), bg="#305E80", fg="#B0C4DE").pack(side="left", padx=10)
    Label(info_frame, text=f"{calificacion}/10", font=("Rubik Regular", 11), bg="#305E80", fg="#B0C4DE").pack(side="right", padx=10)

# Botón para regresar al frame de registro
button_regresar = Button(frame_catalogo,text="Regresar",command=lambda: frame_registro.lift(),  bg="#001B48",fg="#FFFFFF",font=("Rubik Regular", 12), relief="flat")
button_regresar.place(x=932, y=12, width=110, height=33)


window.resizable(False, False)
window.mainloop()