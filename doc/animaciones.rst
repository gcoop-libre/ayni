Animaciones en pygame
=====================

:Autor: Hugo Ruscitti
:Licencia: GPLv3

El módulo **animation** te puede servir para crear animaciones de 
manera sencilla en tus juegos.

**animation** se puede combinar con las bibliotecas **pygame** o **pySFML**,
depende de tus necesidades.


Cuadros de animación
--------------------

Una estrategia común en la creación de animaciones es guardar todos los
cuadros de animacion en grillas. Las grillas son contenedores de varios
cuadros de animación:

    imagen1 | imagen2 | imagen3

Dentro de **animation** hay un objeto llamado **Sheet** para manejar esto, 
simplemente tienes que especificar la superficie donde está la grilla
y cuantos cuadros tiene:

.. code-block:: python

    
    image = load("frames.png")
    sheet = Sheet(image, 5)



.. code-block:: python

    
    player = Sprite()
    player.image = load("hello.png")
    player.rect = player.image.get_frame()
    player.draw(screen)


Aplicando una animacion de 5 cuadros.


.. code-block:: python

    player = Sprite()

    image = load("frames.png")
    sheet = Sheet(image, 5)

    while True:
        player.image = sheet.get_image()
        sheet.next_frame()

.. code-block:: python

    player = Sprite()

    image = load("frames.png")
    sheet = Sheet(image, 5)
    animation = Animation(sheet, 10, [2, 5, 3, 4])

    while True:
        player.image = animation.get_image()
        animation.next_frame()

