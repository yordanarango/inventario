from tkinter import *
from tkinter import ttk, font

from gui import Aplicacion

##################  VEANTANA PRINCIPAL  #######################

"Crea la ventana principal que muestra los botones de acción principales"

mi_app = Aplicacion('670x400', 'INVENTARIO MAGIC CELL')
mi_app.boton_salir(280, 350)

"Crea línea separadora"
mi_app.separ1 = ttk.Separator(mi_app.raiz, orient=HORIZONTAL)
mi_app.separ1.place(x=10, y=320, bordermode=OUTSIDE, height=10, width=650)

"Pone los botones de la acciones principales"
mi_app.agrega_boton(mi_app.raiz, u'Inventario y Estadísticas', 310, 30)
mi_app.agrega_boton(mi_app.raiz, u'Separes', 450, 130)


"#################    Despliega el botón stock     ########################"

mi_app.agrega_boton(mi_app.raiz, u'Stock', 50, 130, mi_app.stock)

"#################    Despliega el botón vendedores     ###################"

mi_app.agrega_boton(mi_app.raiz, u'Vendedores', 350, 230, mi_app.vendedores)

"#################    Despliega el botón clientes     #####################"
mi_app.agrega_boton(mi_app.raiz, u'Clientes', 250, 130, mi_app.clientes)

"#################    Despliega el botón ventas     #######################"
mi_app.agrega_boton(mi_app.raiz, u'Ventas', 110, 30, mi_app.ventas)

"#################    Despliega el botón plan separe     ###################"
mi_app.agrega_boton(mi_app.raiz, u'Créditos', 150, 230, mi_app.creditos)

"#################    Despliega la ventana principal     ###################"
mi_app.despliega_ventana()




