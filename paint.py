import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageTk, ImageColor
import math


ANCHO = 800
ALTO = 500

COLORES = {
    "negro":    "#000000",
    "blanco":   "#ffffff",
    "rojo":     "#e53935",
    "verde":    "#43a047",
    "azul":     "#1e88e5",
    "amarillo": "#fdd835",
    "naranja":  "#fb8c00",
    "morado":   "#8e24aa",
    "rosado":   "#ec407a",
    "cafe":     "#6d4c41",
}

GROSORES = {"Delgado": 2, "Medio": 5, "Grueso": 10}


herramienta_actual = "lapiz"
color_actual = "#000000"
grosor_actual = 2

imagen = Image.new("RGB", (ANCHO, ALTO), "white")
draw = ImageDraw.Draw(imagen)

foto_lienzo = None
punto_inicial = None
previa_id = None
ultimo_x = None
ultimo_y = None
botones_herramientas = {}


def actualizar_lienzo():
    global foto_lienzo
    foto_lienzo = ImageTk.PhotoImage(imagen)
    lienzo.itemconfig(imagen_en_canvas, image=foto_lienzo)


def dibujar_linea(x1, y1, x2, y2):
    draw.line([(x1, y1), (x2, y2)], fill=color_actual, width=grosor_actual)


def dibujar_rectangulo(x1, y1, x2, y2):
    izq, der = min(x1, x2), max(x1, x2)
    arr, aba = min(y1, y2), max(y1, y2)
    draw.rectangle([izq, arr, der, aba], outline=color_actual, width=grosor_actual)


def dibujar_circulo(x1, y1, x2, y2):
    radio = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    draw.ellipse(
        [x1 - radio, y1 - radio, x1 + radio, y1 + radio],
        outline=color_actual,
        width=grosor_actual,
    )


def dibujar_triangulo(x1, y1, x2, y2):
    izq, der = min(x1, x2), max(x1, x2)
    arr, aba = min(y1, y2), max(y1, y2)
    cx = (izq + der) // 2
    puntos = [(cx, arr), (der, aba), (izq, aba)]
    draw.line(puntos + [puntos[0]], fill=color_actual, width=grosor_actual, joint="curve")


def dibujar_estrella(x1, y1, x2, y2):
    radio_ext = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    radio_int = radio_ext * 0.4
    puntos = []
    for i in range(10):
        angulo = math.radians(-90 + i * 36)
        if i % 2 == 0:
            r = radio_ext
        else:
            r = radio_int
        puntos.append((x1 + r * math.cos(angulo), y1 + r * math.sin(angulo)))
    draw.line(puntos + [puntos[0]], fill=color_actual, width=grosor_actual, joint="curve")


def rellenar(x, y):
    color_rgb = ImageColor.getrgb(color_actual)
    pixel_actual = imagen.getpixel((x, y))
    if pixel_actual == color_rgb:
        return
    ImageDraw.floodfill(imagen, (x, y), color_rgb)


def lapiz(x, y):
    global ultimo_x, ultimo_y
    r = grosor_actual // 2
    if ultimo_x is not None:
        draw.line([(ultimo_x, ultimo_y), (x, y)], fill=color_actual, width=grosor_actual)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color_actual)
    ultimo_x = x
    ultimo_y = y


def borrador(x, y):
    global ultimo_x, ultimo_y
    grosor = grosor_actual * 3
    r = grosor // 2
    if ultimo_x is not None:
        draw.line([(ultimo_x, ultimo_y), (x, y)], fill="white", width=grosor)
    draw.ellipse([x - r, y - r, x + r, y + r], fill="white")
    ultimo_x = x
    ultimo_y = y


def al_presionar_mouse(evento):
    global punto_inicial, ultimo_x, ultimo_y
    punto_inicial = (evento.x, evento.y)
    ultimo_x = None
    ultimo_y = None
    if herramienta_actual == "lapiz":
        lapiz(evento.x, evento.y)
        actualizar_lienzo()
    elif herramienta_actual == "borrador":
        borrador(evento.x, evento.y)
        actualizar_lienzo()
    elif herramienta_actual == "cubeta":
        rellenar(evento.x, evento.y)
        actualizar_lienzo()


def al_mover_mouse(evento):
    global previa_id
    if punto_inicial is None:
        return
    x1, y1 = punto_inicial
    x2, y2 = evento.x, evento.y
    if herramienta_actual == "lapiz":
        lapiz(x2, y2); actualizar_lienzo(); return
    if herramienta_actual == "borrador":
        borrador(x2, y2); actualizar_lienzo(); return
    if previa_id is not None:
        lienzo.delete(previa_id)
    if herramienta_actual == "linea":
        previa_id = lienzo.create_line(x1, y1, x2, y2, fill=color_actual, width=grosor_actual)
    elif herramienta_actual == "rectangulo":
        previa_id = lienzo.create_rectangle(x1, y1, x2, y2, outline=color_actual, width=grosor_actual)
    elif herramienta_actual == "circulo":
        r = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        previa_id = lienzo.create_oval(x1 - r, y1 - r, x1 + r, y1 + r,
                                       outline=color_actual, width=grosor_actual)
    elif herramienta_actual == "triangulo":
        izq, der = min(x1, x2), max(x1, x2)
        arr, aba = min(y1, y2), max(y1, y2)
        cx = (izq + der) // 2
        previa_id = lienzo.create_polygon(cx, arr, der, aba, izq, aba,
                                          outline=color_actual, width=grosor_actual, fill="")
    elif herramienta_actual == "estrella":
        re_ = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        ri_ = re_ * 0.4
        puntos = []
        for i in range(10):
            ang = math.radians(-90 + i * 36)
            r = re_ if i % 2 == 0 else ri_
            puntos.append(x1 + r * math.cos(ang))
            puntos.append(y1 + r * math.sin(ang))
        previa_id = lienzo.create_polygon(puntos, outline=color_actual, width=grosor_actual, fill="")


def al_soltar_mouse(evento):
    global punto_inicial, previa_id
    if punto_inicial is None:
        return
    x1, y1 = punto_inicial
    x2, y2 = evento.x, evento.y
    if previa_id is not None:
        lienzo.delete(previa_id)
        previa_id = None
    if herramienta_actual == "linea":
        dibujar_linea(x1, y1, x2, y2); actualizar_lienzo()
    elif herramienta_actual == "rectangulo":
        dibujar_rectangulo(x1, y1, x2, y2); actualizar_lienzo()
    elif herramienta_actual == "circulo":
        dibujar_circulo(x1, y1, x2, y2); actualizar_lienzo()
    elif herramienta_actual == "triangulo":
        dibujar_triangulo(x1, y1, x2, y2); actualizar_lienzo()
    elif herramienta_actual == "estrella":
        dibujar_estrella(x1, y1, x2, y2); actualizar_lienzo()
    punto_inicial = None


def seleccionar_herramienta(nombre):
    global herramienta_actual
    herramienta_actual = nombre
    for n, boton in botones_herramientas.items():
        if n == nombre:
            boton.config(relief="sunken", bg="#cccccc")
        else:
            boton.config(relief="raised", bg="SystemButtonFace")
    actualizar_estado()


def cambiar_color(nuevo_color):
    global color_actual
    color_actual = nuevo_color
    etiqueta_color.config(bg=nuevo_color)
    actualizar_estado()


def cambiar_grosor(valor):
    global grosor_actual
    grosor_actual = valor
    actualizar_estado()


def nuevo():
    global imagen, draw
    quiere = messagebox.askyesno("Nuevo", "Seguro que queres borrar todo?")
    if not quiere:
        return
    imagen = Image.new("RGB", (ANCHO, ALTO), "white")
    draw = ImageDraw.Draw(imagen)
    actualizar_lienzo()


def guardar():
    archivo = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagen PNG", "*.png"), ("Todos los archivos", "*.*")],
    )
    if not archivo:
        return
    imagen.save(archivo)


def actualizar_estado():
    etiqueta_estado.config(
        text="Herramienta: " + herramienta_actual +
             "  |  Color: " + color_actual +
             "  |  Grosor: " + str(grosor_actual)
    )


ventana = tk.Tk()
ventana.title("Mini Paint")
ventana.resizable(False, False)

barra = tk.Frame(ventana, bd=2, relief="groove")
barra.pack(side="top", fill="x")

tk.Label(barra, text="Herramientas:", font=("Arial", 9, "bold")).pack(side="left", padx=4)
lista_herramientas = ["lapiz", "borrador", "linea", "rectangulo", "circulo",
                      "triangulo", "estrella", "cubeta"]
for h in lista_herramientas:
    b = tk.Button(barra, text=h, width=10, command=lambda n=h: seleccionar_herramienta(n))
    b.pack(side="left", padx=1, pady=2)
    botones_herramientas[h] = b

tk.Label(barra, text="  Colores:", font=("Arial", 9, "bold")).pack(side="left", padx=4)
for nombre, color in COLORES.items():
    tk.Button(barra, bg=color, width=2, height=1,
              command=lambda c=color: cambiar_color(c)).pack(side="left", padx=1)

etiqueta_color = tk.Label(barra, text="  ", bg=color_actual, width=3, relief="sunken")
etiqueta_color.pack(side="left", padx=6)

tk.Label(barra, text="  Grosor:", font=("Arial", 9, "bold")).pack(side="left", padx=4)
for nombre, valor in GROSORES.items():
    tk.Button(barra, text=nombre, width=8,
              command=lambda v=valor: cambiar_grosor(v)).pack(side="left", padx=1)

tk.Label(barra, text="  Archivo:", font=("Arial", 9, "bold")).pack(side="left", padx=4)
tk.Button(barra, text="Nuevo", width=8, command=nuevo).pack(side="left", padx=1)
tk.Button(barra, text="Guardar", width=8, command=guardar).pack(side="left", padx=1)

lienzo = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg="white", cursor="pencil")
lienzo.pack(side="top")

foto_lienzo = ImageTk.PhotoImage(imagen)
imagen_en_canvas = lienzo.create_image(0, 0, anchor="nw", image=foto_lienzo)

lienzo.bind("<Button-1>", al_presionar_mouse)
lienzo.bind("<B1-Motion>", al_mover_mouse)
lienzo.bind("<ButtonRelease-1>", al_soltar_mouse)

etiqueta_estado = tk.Label(ventana, text="", anchor="w", bd=1, relief="sunken")
etiqueta_estado.pack(side="bottom", fill="x")

seleccionar_herramienta("lapiz")

ventana.mainloop()
