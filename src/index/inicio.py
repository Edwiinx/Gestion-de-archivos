from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).resolve().parent.parent
ASSETS_PATH = OUTPUT_PATH / "../src/assets/frame0"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("950x600")
window.configure(bg = "#1B2838")
window.title("Registro")


canvas = Canvas(
    window,
    bg = "#1B2838",
    height = 600,
    width = 950,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    190.0,
    119.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=79.0,
    y=98.0,
    width=222.0,
    height=41.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    190.0,
    205.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=79.0,
    y=184.0,
    width=222.0,
    height=41.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    190.0,
    291.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=79.0,
    y=270.0,
    width=222.0,
    height=41.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    190.0,
    375.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=79.0,
    y=354.0,
    width=222.0,
    height=41.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    333.0,
    466.0,
    image=entry_image_5
)
entry_5 = Text(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=79.0,
    y=430.0,
    width=508.0,
    height=70.0
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    476.0,
    119.5,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_6.place(
    x=365.0,
    y=98.0,
    width=222.0,
    height=41.0
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    476.0,
    205.5,
    image=entry_image_7
)
entry_7 = Entry(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_7.place(
    x=365.0,
    y=184.0,
    width=222.0,
    height=41.0
)

entry_image_8 = PhotoImage(
    file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(
    476.0,
    291.5,
    image=entry_image_8
)
entry_8 = Entry(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_8.place(
    x=365.0,
    y=270.0,
    width=222.0,
    height=41.0
)

entry_image_9 = PhotoImage(
    file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(
    476.0,
    375.5,
    image=entry_image_9
)
entry_9 = Entry(
    bd=0,
    bg="#305E80",
    fg="#000716",
    highlightthickness=0
)
entry_9.place(
    x=365.0,
    y=354.0,
    width=222.0,
    height=41.0
)

canvas.create_rectangle(
    0.0,
    0.0,
    950.0,
    52.0,
    fill="#171D25",
    outline="")

canvas.create_text(
    32.0,
    7.0,
    anchor="nw",
    text="REGISTRO DE VIDEOJUEGO",
    fill="#FFFFFF",
    font=("Rubik Regular", 32 * -1)
)

canvas.create_text(
    73.0,
    75.0,
    anchor="nw",
    text="Código",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    359.0,
    75.0,
    anchor="nw",
    text="Desarrollador",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    359.0,
    161.0,
    anchor="nw",
    text="Publisher",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    359.0,
    246.0,
    anchor="nw",
    text="Clasificación",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    359.0,
    332.0,
    anchor="nw",
    text="Calificación promedio",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    74.0,
    161.0,
    anchor="nw",
    text="Nombre",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    74.0,
    246.0,
    anchor="nw",
    text="Fecha de lanzamiento",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    73.0,
    332.0,
    anchor="nw",
    text="Precio",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

canvas.create_text(
    73.0,
    410.0,
    anchor="nw",
    text="Descripción",
    fill="#FFFFFF",
    font=("Rubik Regular", 14 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=73.0,
    y=524.0,
    width=110.0,
    height=33.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=205.0,
    y=524.0,
    width=110.0,
    height=33.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=476.0,
    y=524.0,
    width=110.0,
    height=33.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=802.0,
    y=524.0,
    width=110.0,
    height=33.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=651.0,
    y=524.0,
    width=110.0,
    height=33.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=711.0,
    y=466.0,
    width=127.0,
    height=23.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=340.0,
    y=524.0,
    width=110.0,
    height=33.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=802.0,
    y=12.0,
    width=110.0,
    height=33.0
)
window.resizable(False, False)
window.mainloop()