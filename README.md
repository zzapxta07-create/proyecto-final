# Mini Paint

Un programa tipo Paint hecho en Python para un trabajo de clase. Permite dibujar
figuras basicas, pintar a mano alzada, rellenar areas y guardar el dibujo como
imagen PNG.

## Requisitos e instalacion

- Python 3
- Pillow (PIL)

Para instalar las dependencias:

```
pip install -r requirements.txt
```

## Como ejecutarlo

```
python paint.py
```

## Funciones

- **Lapiz libre**: dibuja a mano alzada con el color y grosor elegidos.
- **Borrador**: igual que el lapiz pero siempre en blanco y tres veces mas grueso.
- **Linea**: recta entre dos puntos.
- **Rectangulo**: contorno de un rectangulo, funciona arrastrando en cualquier
  direccion.
- **Circulo**: contorno de un circulo, el centro es donde haces click.
- **Triangulo**: isosceles, dentro del rectangulo que forma el arrastre.
- **Estrella**: de 5 puntas, calculada con seno y coseno.
- **Cubeta**: rellena un area cerrada con el color actual.
- **10 colores** en la paleta: negro, blanco, rojo, verde, azul, amarillo, naranja,
  morado, rosado y cafe.
- **3 grosores**: Delgado (2), Medio (5), Grueso (10).
- **Nuevo**: borra el dibujo (pregunta antes).
- **Guardar**: exporta el dibujo como archivo PNG.

## Como funciona el codigo

El archivo `paint.py` esta ordenado en bloques:

1. **Imports**: Tkinter para la ventana, Pillow para la imagen y `math` para los
   calculos de la estrella y el circulo.
2. **Constantes**: tamano de la hoja, diccionario de colores y diccionario de
   grosores.
3. **Variables globales**: la herramienta y color actuales, la imagen de Pillow
   donde se dibuja todo, la PhotoImage que se muestra, el punto donde empezo el
   arrastre y la ultima posicion del mouse.
4. **`actualizar_lienzo()`**: toma la imagen de Pillow y la muestra en el Canvas
   de Tkinter. Se llama cada vez que se dibuja algo definitivo.
5. **Funciones de dibujo**: una por cada figura (`dibujar_linea`,
   `dibujar_rectangulo`, `dibujar_circulo`, `dibujar_triangulo`,
   `dibujar_estrella`), mas `lapiz`, `borrador` y `rellenar`. Todas dibujan sobre
   la imagen de Pillow usando `ImageDraw`.
6. **Eventos del mouse**: `al_presionar_mouse` guarda el punto inicial,
   `al_mover_mouse` muestra una vista previa en el Canvas (o dibuja el lapiz),
   y `al_soltar_mouse` dibuja la figura definitiva sobre la imagen de Pillow.
7. **Funciones de botones**: cambian herramienta, color, grosor, limpian la hoja
   o guardan la imagen.
8. **Creacion de la ventana**: la barra de herramientas, el Canvas y la etiqueta
   de estado.
9. **`ventana.mainloop()`**: mantiene la ventana abierta.

La idea central es que hay DOS cosas: la imagen de Pillow (lo "oficial", lo que
se guarda) y el Canvas de Tkinter (lo que ve el usuario). El Canvas solo muestra
la imagen de Pillow. Mientras el usuario arrastra el mouse con una figura, se
dibuja una vista previa temporal sobre el Canvas; cuando suelta el mouse, la
figura se pinta de verdad en la imagen de Pillow y se actualiza el Canvas.

## Preguntas que me puede hacer el profesor

**1. Por que se usa Pillow ademas de Tkinter?**
Tkinter puede dibujar lineas y figuras en un Canvas, pero no puede guardar ese
Canvas como imagen (PNG, JPG, etc) de forma simple. Pillow permite crear una
imagen "de verdad" en memoria, dibujar sobre ella y guardarla en disco. Por eso
Tkinter se usa solo para mostrar, y Pillow es donde se guarda todo el dibujo.

**2. Como funciona la cubeta (floodfill)?**
El algoritmo empieza en el pixel donde hiciste click. Si ese pixel es de un color
determinado, se cambia al nuevo color y se expande a los pixeles vecinos
(arriba, abajo, izquierda, derecha) que tengan el mismo color original. Asi se
va expandiendo hasta chocar con pixeles de otro color, que funcionan como borde.
Pillow lo hace con `ImageDraw.floodfill(imagen, (x, y), color)`.

**3. Como se calcula la estrella?**
Una estrella de 5 puntas tiene 10 vertices: 5 puntas (lejos del centro) y 5
valles (cerca del centro). Se usa un `for` de 10 iteraciones. En cada paso se
calcula un angulo (empezando en -90 grados y sumando 36 cada vez) y se alterna
entre el radio externo (las puntas) y el radio interno (los valles, que es 40%
del externo). Con `math.cos` y `math.sin` se obtienen las coordenadas (x, y)
de cada vertice alrededor del centro.

**4. Como funciona la vista previa?**
Mientras el usuario arrastra el mouse para dibujar una figura, el programa
dibuja esa figura TEMPORALMENTE sobre el Canvas de Tkinter (con `create_line`,
`create_rectangle`, etc.). En cada movimiento del mouse se borra la vista previa
anterior y se dibuja una nueva. Cuando el usuario suelta el mouse, se borra la
vista previa y se dibuja la figura definitiva sobre la imagen de Pillow.

**5. Por que hay variables globales?**
Porque el programa esta escrito con funciones sueltas (sin clases). Las
funciones necesitan compartir informacion: la herramienta elegida, el color, la
imagen actual, el punto donde empezo el arrastre, etc. Al no haber una clase que
guarde ese estado, se usan variables globales. Es la forma mas simple para un
programa pequeno. En un proyecto mas grande se usarian clases.

**6. Que hace `mainloop`?**
Es el "bucle principal" de Tkinter. Mantiene la ventana abierta y escuchando lo
que hace el usuario (clicks, teclas, movimientos del mouse). Cada vez que pasa
algo, Tkinter llama a la funcion correspondiente. Sin `mainloop`, la ventana se
abriria y se cerraria inmediatamente porque el programa terminaria.

**7. Por que se guarda la PhotoImage en una variable?**
Porque Python tiene un recolector de basura: borra automaticamente los objetos
que ya no estan en uso. Si la `PhotoImage` solo existiera dentro de una funcion,
Python la borraria apenas la funcion termina, y el Canvas quedaria en blanco
aunque la imagen se haya "mostrado". Guardandola en una variable global, Python
ve que sigue en uso y no la borra.

**8. Que pasa si arrastro el rectangulo hacia la izquierda o hacia arriba?**
Funciona bien, porque dentro de `dibujar_rectangulo` se usan `min` y `max` para
reordenar las coordenadas. Asi el punto de arriba-izquierda y el de
abajo-derecha siempre quedan correctos, sin importar en que direccion se
arrastre. Si no se hiciera esto, Pillow daria error o no dibujaria nada.

**9. Como funciona el borrador?**
El borrador es exactamente igual que el lapiz libre, pero fuerza el color a
blanco (que es el color de fondo de la hoja) y usa un grosor tres veces mayor.
Asi "borrar" es solo "pintar de blanco encima". No es un borrador real que
elimine pixeles, sino que los sobreescribe.

**10. Que son los eventos del mouse?**
Son las acciones que Tkinter detecta en el Canvas. Los tres principales son:
- `<Button-1>`: cuando se presiona el boton izquierdo del mouse.
- `<B1-Motion>`: cuando se mueve el mouse con el boton izquierdo presionado
  (arrastre).
- `<ButtonRelease-1>`: cuando se suelta el boton izquierdo.
Cada uno llama a una funcion propia (`al_presionar_mouse`, `al_mover_mouse`,
`al_soltar_mouse`) que recibe un objeto `evento` con la posicion (x, y) del
mouse en ese momento.
