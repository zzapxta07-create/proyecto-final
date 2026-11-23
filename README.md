# Mini Paint

Mini Paint es un programa hecho en Python que funciona de forma parecida a Paint. Permite dibujar con el mouse, usar diferentes figuras, cambiar colores y guardar los dibujos en formato PNG.

## Requisitos

Para ejecutar el programa se necesita:

- Python 3
- Pillow

Para instalar Pillow, se puede usar el siguiente comando:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar el programa

Primero se debe abrir la carpeta donde está guardado el proyecto y ejecutar:

```bash
python paint.py
```

## Funciones del programa

El programa cuenta con varias herramientas para dibujar:

- **Lápiz:** permite dibujar libremente con el mouse usando el color y grosor seleccionados.
- **Borrador:** sirve para borrar partes del dibujo. Utiliza el color blanco y tiene un grosor mayor.
- **Línea:** dibuja una línea recta entre dos puntos.
- **Rectángulo:** permite dibujar rectángulos arrastrando el mouse.
- **Círculo:** dibuja círculos tomando como centro el punto donde se hace clic.
- **Triángulo:** dibuja un triángulo isósceles según el tamaño del área seleccionada.
- **Estrella:** dibuja una estrella de cinco puntas.
- **Cubeta:** permite rellenar áreas cerradas con el color seleccionado.

También tiene otras opciones:

- **Colores:** cuenta con 10 colores diferentes: negro, blanco, rojo, verde, azul, amarillo, naranja, morado, rosado y café.
- **Grosores:** tiene tres opciones: delgado (2), medio (5) y grueso (10).
- **Nuevo:** limpia el lienzo después de confirmar la acción.
- **Guardar:** permite guardar el dibujo como una imagen PNG.

## Cómo está organizado el código

Todo el programa está escrito en un solo archivo llamado `paint.py`. El código está dividido en diferentes partes:

1. **Imports:** se importan las librerías que se utilizan en el programa: Tkinter, Pillow y math.
2. **Constantes:** se definen el ancho y alto del lienzo, los colores disponibles y los grosores del lápiz.
3. **Variables globales:** guardan información como la herramienta seleccionada, el color actual, el grosor y las posiciones del mouse.
4. **Actualizar lienzo:** la función `actualizar_lienzo()` muestra en la ventana los cambios realizados en la imagen.
5. **Funciones de dibujo:** contienen las instrucciones para dibujar las líneas, rectángulos, círculos, triángulos y estrellas. También incluyen el lápiz, el borrador y la cubeta.
6. **Eventos del mouse:** detectan cuándo se presiona, se mueve o se suelta el mouse. Con esto se puede dibujar y mostrar las figuras mientras se arrastran.
7. **Funciones de los botones:** permiten cambiar de herramienta, seleccionar colores y grosores, crear un dibujo nuevo y guardar el archivo.
8. **Ventana principal:** se crean la ventana, los botones, la barra de herramientas y el lienzo.
9. **Mainloop:** mantiene el programa abierto y permite que responda a las acciones del usuario.

## Librerías utilizadas

- **Tkinter:** se utiliza para crear la ventana, los botones y el espacio donde se dibuja.
- **Pillow:** permite crear y modificar la imagen que se guarda al finalizar el dibujo.
- **Math:** se utiliza para realizar algunos cálculos matemáticos necesarios para dibujar figuras como la estrella y el círculo.