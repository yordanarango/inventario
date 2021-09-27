from tkinter import *
from tkinter import ttk, font

## modules of the application

import _clientes
import _creditos
import _stock
import _vendedores
import _ventas

class Aplicacion(_clientes.Clientes, _vendedores.Vendedores, _ventas.Ventas, _creditos.Creditos, _stock.Stock):
	
	def __init__(self, dimensiones, titulo):
	    
		# dimensiones: dimensiones que va a tener la ventana en formato string
		# titulo     : titulo de la ventana en formato string

		# En el ejemplo se utiliza el prefijo 'self' para
		# declarar algunas variables asociadas al objeto 
		# ('mi_app')  de la clase 'Aplicacion'. Su uso es 
		# imprescindible para que se pueda acceder a sus
		# valores desde otros métodos:

		self.raiz = Tk()
		self.raiz.geometry(dimensiones)

		# Impide que los bordes puedan desplazarse para
		# ampliar o reducir el tamaño de la ventana 'self.raiz':

		self.raiz.resizable(width=False,height=False)

		# Titulo de la ventana

		self.raiz.title(titulo)


		# define las credenciales de la base de datos

		self.host   = "localhost"
		self.user   = "narlu"
		self.passwd = "prueba_31A"
		self.dbname = "inventario_yesid"

		self.guarda_facturas = "/home/yordan/YORDAN/inventario_donhector/facturas/"



	def despliega_ventana(self):

		self.raiz.mainloop()


	def agrega_boton(self, padre, nombre_boton, locate_x, locate_y, comando=None, frame=False, pad=(40,20), padxy=(10,10), grid=False):

		# Agrega botón a la ventana

		# padre         : la ventana padre
		# nombre_boton  : string con el nombre del boton
		# locate_x      : ubicacion en la ventana del boton en el eje x
		# locate_y      : ubicacion en la ventana del boton en el eje y
		# comando       : introduce la función que va a realizar el botón cuando este se presione
		# frame         : boolean que dice si se está utilizando un marco o no

		# Define el widget Button

		if comando:

			#if frame == True:
				#self.boton = ttk.Button(self.marco, text=nombre_boton, padding=(40,20), command=comando)
			#else:
			boton = ttk.Button(padre, text=nombre_boton, padding=pad, command=comando)

		else:

			#if frame == True:
				#self.boton = ttk.Button(self.marco, text=nombre_boton, padding=pad)
			#else:
			boton = ttk.Button(padre, text=nombre_boton, padding=pad)

		# Coloca el botón 'self.binfo' en locate_x y locate_y

		if grid == False:
			boton.place(x=locate_x, y=locate_y)
		else:
			boton.grid(row=locate_y, column=locate_x, pady=padxy[1], padx=padxy[0])

		return boton

		#boton.grid_propagate(0)

	def boton_salir(self, locate_x, locate_y, frame=False):

		#locate_x      : ubicacion en la ventana del boton en el eje x
		#locate_y      : ubicacion en la ventana del boton en el eje y
		#frame         : es un boolean que dice si va a hacer un marco el que va a contener los widgets o no

		if frame == True:
			self.bsalir = ttk.Button(self.marco, text='Salir', command=self.raiz.destroy)
		else:
			self.bsalir = ttk.Button(self.raiz, text='Salir', command=self.raiz.destroy)
		                         
		# Coloca el botón 'self.bsalir' a la derecha del 
		# objeto anterior.
		                         
		self.bsalir.place(x=locate_x, y=locate_y)

	def marco_create(self, padre, BORDERWIDTH, RELIEF, PADDING, HEIGHT, WIDTH):

		# padre: ventana donde se pondrá el marco
		# BORDERWIDTH: ancho del borde del marco
		# RELIEF     : flat (llano), raised (elevado), sunken (hundido), groove (hendidura) y ridge
		# PADDING    : añade espacio extra interior para que los widgets no queden pegados al borde del marco
		# HEIGHT     : Altura del marco
		# WIDTH      : Ancho del marco

		self.marco = ttk.Frame(padre, borderwidth=BORDERWIDTH, relief=RELIEF, padding=PADDING, height=HEIGHT, width=WIDTH)

	def otra_ventana(self, padre, pos_dim, titulo, x_salir, y_salir, textsalir='Salir', exitgrid=False):

		# padre    : ventana padre
		# pos_dim  : string posición y dimensiones de la ventana
		# titulo   : string del titulo de la ventana
		# x_salir  : ubicacion en la ventana del boton salir en el eje x
		# y_salir  : ubicacion en la ventana del boton salir en el eje y
		# textsalir: el nombre del botón para cerrar la ventana
		# exitgrid : if True, the exit button will be placed with grid method, if False it will be placed with place method

		# construye la ventana

		dialogo = Toplevel()

		# ubica y da dimensiones a la ventana

		dialogo.geometry(pos_dim)

		# pone titulo a la ventana

		dialogo.title(titulo)
		
		# boton para cerrar la ventana

		boton_sale = ttk.Button(dialogo, text=textsalir, command=dialogo.destroy)
		if exitgrid == False:
			boton_sale.place(x=x_salir, y=y_salir)
		else:
			boton_sale.grid(row=y_salir, column=x_salir, pady=10, padx=10)

		return dialogo

	def final_otra_ventana(self, padre, abuelo, wait=False):

		#padre : ventana secundaria
		#abuelo: ventana de la cual se despliega la ventana secundaria

		# Convierte la ventana 'self.dialogo' en 
		# transitoria con respecto a su ventana maestra 
		# 'self.raiz'.
		# Una ventana transitoria siempre se dibuja sobre
		# su maestra y se ocultará cuando la maestra sea
		# minimizada. Si el argumento 'master' es
		# omitido el valor, por defecto, será la ventana
		# madre.

		#boton = ttk.Button(self.dialogo, text=self.alimcli_ttl, padding=(40,20))
		#boton.place(x=self.alimcli_x, y=self.alimcli_y)

		padre.transient(master=abuelo)

		# El método grab_set() asegura que no haya eventos 
		# de ratón o teclado que se envíen a otra ventana 
		# diferente a 'self.dialogo'. Se utiliza para 
		# crear una ventana de tipo modal que será 
		# necesario cerrar para poder trabajar con otra
		# diferente. Con ello, también se impide que la 
		# misma ventana se abra varias veces. 

		if wait == True:

			padre.wait_visibility()

		padre.grab_set()

		# Cuando la ejecución del programa llega a este 
		# punto se utiliza el método wait_window() para
		# esperar que la ventana 'self.dialogo' sea 
		# destruida. 

		abuelo.wait_window(padre)

	def etiqueta(self, padre, texto, locate_x, locate_y, grid=False, color='black', weight='bold'):

		# padre: ventana padre donde se va a poner la etiqueta
		# texto: texto de la etiqueta en string
		# locate_x: ubicacion de la etiqueta en x
		# locate_y: ubicacion de la etiqueta en y

		fuente   = font.Font(weight=weight)
		etiqueta = ttk.Label(padre, text=texto, font=fuente, padding=(5,5))

		if grid == False:
			etiqueta.place(x=locate_x, y=locate_y)
		else:
			etiqueta.grid(row=locate_y, column=locate_x, pady=10, padx=10)

		etiqueta.config(foreground=color)

		return etiqueta

	def caja_texto(self, padre, h, w, locate_x, locate_y, grid=False):

		# padre: ventana padre
		# h    : altura de la ventana
		# w    : anco de la ventana
		# locate_x: ubicacion de la etiqueta en x
		# locate_y: ubicacion de la etiqueta en y

		textbox  = Text(padre, height=h, width=w)
		if grid == False:
			textbox.place(x=locate_x, y=locate_y)
		else:
			textbox.grid(row=locate_y, column=locate_x, pady=10, padx=10)
		return textbox

