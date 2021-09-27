from tkinter import *
from tkinter import ttk, font
import MySQLdb
import datetime as dt
import re
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import os.path as path


class Creditos:

	def creditos(self):

		# Ventana de opciones de stock
		self.ventana_ventas = self.otra_ventana(self.raiz, '+150+120', u'Opciones Créditos', 1, 1, exitgrid=True)
		self.agrega_boton(self.ventana_ventas, u'Ventas a crédito', 0, 0, self.vender_cre, grid=True, padxy=(40,40))
		self.agrega_boton(self.ventana_ventas, u'Abonos', 2, 0, self.abonos, grid=True, padxy=(40,40))
		self.final_otra_ventana(self.ventana_ventas, self.raiz)

	def abonos(self):

		self.ventana_abonos = self.otra_ventana(self.ventana_ventas, '+200+170', u'Ventana de abonos', 1, 21, exitgrid=True)

		self.etiqueta(self.ventana_abonos, u"Factura N°", 0, 0, grid=True)
		self.caja_ID_factura = self.caja_texto(self.ventana_abonos, 1.4, 35, 1, 0, grid=True)
		self.agrega_boton(self.ventana_abonos, 'Buscar Factura', 2, 0, self.buscar_factura, grid=True, pad=(5,5))

		self.lbl_factura_hallada1 = self.etiqueta(self.ventana_abonos, u"Usted no ha buscado una factura", 0, 11, grid=True, color='red')
		self.lbl_factura_hallada2 = self.etiqueta(self.ventana_abonos, u"Aún no puede abonar.", 0, 12, grid=True, color='red')
		self.lbl_factura_hallada1.grid(columnspan=3)
		self.lbl_factura_hallada2.grid(columnspan=3)

		#---- caja abono
		lbl_abono = self.etiqueta(self.ventana_abonos, u"Monto del abono", 0, 13, grid=True)
		self.monto_abono = self.caja_texto(self.ventana_abonos, 1.4, 35, 0, 14, grid=True)

		lbl_abono.grid(columnspan=3)
		self.monto_abono.grid(columnspan=3)

		#---- Radio button
		lbl_medio_pago = self.etiqueta(self.ventana_abonos, 'Medio de pago', 0, 15, grid=True)
		lbl_medio_pago.grid(columnspan=3)
		self.RB = IntVar()
		self.RB.set(0)
		RB0 = Radiobutton(self.ventana_abonos, text=u'Efectivo', variable=self.RB, value=0)
		RB1 = Radiobutton(self.ventana_abonos, text=u'Bancolombia', variable=self.RB, value=1)
		RB2 = Radiobutton(self.ventana_abonos, text=u'Nequi', variable=self.RB, value=2)
		RB3 = Radiobutton(self.ventana_abonos, text=u'Daviplata', variable=self.RB, value=3)

		RB0.grid(row=16, column=0)
		RB1.grid(row=17, column=0)
		RB2.grid(row=18, column=0)
		RB3.grid(row=19, column=0)

		RB0.grid(columnspan = 3)
		RB1.grid(columnspan = 3)
		RB2.grid(columnspan = 3)
		RB3.grid(columnspan = 3)

		#---- botón hacer un abono
		boton_abono = self.agrega_boton(self.ventana_abonos, 'Hacer un abono a esta factura', 0, 20, self.abonar, grid=True, pad=(5,5))
		boton_abono.grid(columnspan=3)

		#------------------------------------- Crea las tablas -------------------------------------------
		self.dataCols  = ('date_abono', 'abono', 'restante')
		self.tree = ttk.Treeview(self.ventana_abonos, columns=self.dataCols)

		ysb = ttk.Scrollbar(self.ventana_abonos, orient=VERTICAL, command= self.tree.yview)
		self.tree['yscroll'] = ysb.set

		# setup column headings
		self.tree.heading('#0',   text='')
		self.tree.heading('date_abono', text=u'Fecha Abono', anchor=W)
		self.tree.heading('abono', text='Abono ($)', anchor=W)
		self.tree.heading('restante', text='Saldo Crédito ($)', anchor=W)

		self.tree.column('#0',   stretch=1, width=0, anchor=W)
		self.tree.column('date_abono', stretch=1, width=130, anchor=W)
		self.tree.column('abono', stretch=1, width=120, anchor=W)
		self.tree.column('restante', stretch=1, width=150, anchor=W)

		# add tree and scrollbars to frame
		self.tree.grid(row=1, column=0, columnspan=3, rowspan=10, sticky=NSEW, padx=10, pady=10)

		ysb.grid(row=1, column=3, rowspan=10, sticky=NS, pady=10)

		# set frame resizing priorities
		self.ventana_abonos.rowconfigure(0, weight=1)
		self.ventana_abonos.columnconfigure(0, weight=1)

		self.factura_hallada = False

		self.final_otra_ventana(self.ventana_abonos, self.ventana_ventas)

	def buscar_factura(self):

		self.factura_hallada = False
		ID_factura = self.caja_ID_factura.get(1.0, "end-1c")

		if ID_factura == '':

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos 
			self.notifica = self.otra_ventana(self.ventana_abonos, '+250+220', u'Notificacion Abonos', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Por favor introduzca el número de factura del crédito.', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_abonos)

		elif ID_factura.isdigit() == False:

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
			self.notifica = self.otra_ventana(self.ventana_abonos, '+250+220', u'Notificacion Abonos', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Factura con caracteres inválidos. Sólo admite números.', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_abonos)

		else:

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			db_cursor.execute("SELECT valor_credito FROM valor_creditos WHERE id = " + ID_factura + ";")
			self.valor_credito = db_cursor.fetchall()
			db_conn.close()

			if len(self.valor_credito) == 1:

				### elimina registros de la tabla

				for record in self.tree.get_children():
					self.tree.delete(record)

				# inserta el valor de la deuda

				VALUES        = ('', '', self.valor_credito[0][0]) 
				self.tree.insert('', END, text='', values=VALUES, iid=0)

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("SELECT fecha_abono, abono, resta_credito FROM abonos_creditos WHERE valor_creditos_id = " + ID_factura + ";")
				self.abonos_factura = db_cursor.fetchall()
				db_conn.close()

				if len(self.abonos_factura) != 0:

					# introduce los datos a la tabla
					for i in range(len(self.abonos_factura)):

						fecha_abono = self.abonos_factura[i][0]
						abono       = self.abonos_factura[i][1]
						restante    = self.abonos_factura[i][2]

						VALUES        = (fecha_abono, abono, restante) 

						self.tree.insert('', END, text='', values=VALUES, iid=i+1)

				else:

					# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
					self.notifica = self.otra_ventana(self.ventana_abonos, '+250+220', u'Notificacion Abonos', 0, 2, exitgrid=True, textsalir='Continuar')
					self.etiqueta(self.notifica, u'La factura no tiene abonos', 0, 0, grid=True)
					self.final_otra_ventana(self.notifica, self.ventana_abonos)

				self.factura_hallada = True

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("SELECT clientes.nombre, clientes.celular, clientes.cedula FROM creditos INNER JOIN clientes ON creditos.clientes_id = clientes.id WHERE creditos.valor_creditos_id = " + ID_factura + ";")
				cliente_factura = db_cursor.fetchall()
				db_conn.close()

				self.lbl_factura_hallada1.configure(text=u"Factura N° " + ID_factura + " a nombre de: " + cliente_factura[0][0] + ", cel: " + str(cliente_factura[0][1]) + ", id: " + str(cliente_factura[0][2]), foreground='black')
				self.lbl_factura_hallada2.configure(text=u"Ya puede abonar.", foreground='black')

			elif len(self.valor_credito) == 0:

				self.factura_hallada = False

				for record in self.tree.get_children():
					self.tree.delete(record)

				self.lbl_factura_hallada1.configure(text=u"Su factura no ha sido hallada", foreground='red')
				self.lbl_factura_hallada2.configure(text=u"Aún no puede abonar.", foreground='red')

				# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos 
				self.notifica = self.otra_ventana(self.ventana_abonos, '+250+220', u'Notificacion Abonos', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica, u'Esta factura no existe en nuestra base de datos.', 0, 1, grid=True)
				self.final_otra_ventana(self.notifica, self.ventana_abonos)

	def abonar(self):

		monto_abono = self.monto_abono.get(1.0, "end-1c")

		if self.factura_hallada == False:

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos 
			self.notifica = self.otra_ventana(self.ventana_abonos, '+250+220', u'Notificacion Abonos', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'No se ha encontrado factura a abonar.', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_abonos)

		elif monto_abono == '':

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos 
			self.notifica = self.otra_ventana(self.ventana_abonos, '+250+220', u'Notificacion Abonos', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'No se ha introducido el monto a abonar.', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_abonos)

		elif monto_abono.isdigit() == False:

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
			self.notifica = self.otra_ventana(self.ventana_abonos, '+250+220', u'Notificacion Abonos', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Monto con caracteres inválidos. Sólo admite números.', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_abonos)

		else:

			current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			if len(self.abonos_factura) != 0:
				resta_credito = self.abonos_factura[-1][2] - int(monto_abono)
			else:
				resta_credito = self.valor_credito[0][0] - int(monto_abono)

			if resta_credito >= 0:

				ID_factura = self.caja_ID_factura.get(1.0, "end-1c")
				medio_abono = ['Efectivo', 'Bancolombia', 'Nequi', 'Daviplata'][self.RB.get()]

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("INSERT INTO abonos_creditos (fecha_abono, abono, resta_credito, valor_creditos_id, medio_abono) VALUES ('" + current_time + "', " + monto_abono + ", " + str(resta_credito) + ", " + ID_factura + ", '" + medio_abono + "');")
				db_cursor.close()
				db_conn.commit ()
				db_conn.close ()

				self.factura_hallada = False
				self.buscar_factura()
				self.monto_abono.delete('1.0', END)

			else:

				# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
				self.notifica = self.otra_ventana(self.ventana_abonos, '+250+220', u'Notificacion Abonos', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica, u'Usted está abonando más de lo que se debe, o ya la deuda está saldada por parte del cliente.', 0, 1, grid=True)
				self.final_otra_ventana(self.notifica, self.ventana_abonos)


	def vender_cre(self):

		fuente   = font.Font(weight='bold')

		self.ventana_vender = self.otra_ventana(self.ventana_ventas, '+200+170', u'Ventana de créditos', 3, 13, exitgrid=True)
		
		label_codname = ttk.Label(self.ventana_vender, text='Cod. Barras o Nombre', font=fuente, padding=(5,5))
		label_codname.grid(row=0, column=0, pady=10, padx=20)
		self.box_codname = Text(self.ventana_vender, height=1.4, width=35)
		self.box_codname.grid(row=0, column=1, pady=10, padx=20)

		self.etiqueta(self.ventana_vender, 'Total', 1170, 290)
		self.box_total = self.caja_texto(self.ventana_vender, 1.4, 15, 1270, 295)

		label_vendido = ttk.Label(self.ventana_vender, text='Canasta de créditos', font=fuente, padding=(5,5))
		label_vendido.grid(row=0, column=4, columnspan=3)

		#------------------------------------- Crea las tablas -------------------------------------------
		self.dataCols  = ('code', 'name', 'amount')
		self.dataCols2 = ('amount', 'name', 'price', 'subtot')
		self.tree = ttk.Treeview(self.ventana_vender, columns=self.dataCols)
		self.tree2= ttk.Treeview(self.ventana_vender, columns=self.dataCols2)

		ysb = ttk.Scrollbar(self.ventana_vender, orient=VERTICAL, command= self.tree.yview)
		ysb2 = ttk.Scrollbar(self.ventana_vender, orient=VERTICAL, command= self.tree2.yview)
		self.tree['yscroll'] = ysb.set
		self.tree2['yscroll'] = ysb2.set

		# setup column headings
		self.tree.heading('#0',   text='')
		self.tree.heading('code', text=u'Código', anchor=W)
		self.tree.heading('name', text='Nombre', anchor=W)
		self.tree.heading('amount', text='Disponibles', anchor=W)

		self.tree2.heading('#0',   text='')
		self.tree2.heading('amount', text=u'Cantidad', anchor=W)
		self.tree2.heading('name', text='Nombre', anchor=W)
		self.tree2.heading('price', text=u'Precio/unidad', anchor=W)
		self.tree2.heading('subtot', text=u'Subtotal', anchor=W)

		self.tree.column('#0',   stretch=1, width=0, anchor=W)
		self.tree.column('code', stretch=1, width=200, anchor=W)
		self.tree.column('name', stretch=1, width=250, anchor=W)
		self.tree.column('amount', stretch=1, width=100, anchor=W)

		self.tree2.column('#0',   stretch=1, width=0, anchor=W)
		self.tree2.column('amount', stretch=1, width=100, anchor=W)
		self.tree2.column('name', stretch=1, width=250, anchor=W)
		self.tree2.column('price', stretch=1, width=160, anchor=W)
		self.tree2.column('subtot', stretch=1, width=200, anchor=W)

		# add tree and scrollbars to frame
		self.tree.grid(row=1, column=0, columnspan=2, rowspan=10, sticky=NSEW, padx=10, pady=10)
		self.tree2.grid(row=1, column=4, columnspan=3, rowspan=2, sticky=NSEW, padx=10, pady=10)

		ysb.grid(row=1, column=2, rowspan=10, sticky=NS, pady=10)
		ysb2.grid(row=1, column=7, rowspan=2, sticky=NS, pady=10)

		#lineas separadoras
		linea_separ1 = ttk.Separator(self.ventana_vender, orient=VERTICAL)
		linea_separ1.grid(row=0, column=3, rowspan=12, sticky=NS, padx=10, pady=10)
		linea_separ2 = ttk.Separator(self.ventana_vender, orient=HORIZONTAL)
		linea_separ2.grid(row=3, column=4, columnspan=3, sticky=EW, padx=10, pady=30)
		linea_separ3 = ttk.Separator(self.ventana_vender, orient=HORIZONTAL)
		linea_separ3.grid(row=9, column=4, columnspan=3, sticky=EW, padx=10, pady=10)
		linea_separ4 = ttk.Separator(self.ventana_vender, orient=HORIZONTAL)
		linea_separ4.grid(row=12, column=0, columnspan=7, sticky=EW, padx=10, pady=10)

		# set frame resizing priorities
		self.ventana_vender.rowconfigure(0, weight=1)
		self.ventana_vender.columnconfigure(0, weight=1)

		#------------------ consulta2 nombres y codigos de barra y los pone en la tabla de disponibles --------------------------

		self.consulta2()

		# Llama el método update_tree para poner los datos iniciales
		self.update_tree2()

		# Click en uno de los registros de la tabla
		self.tree.bind("<Double-1>", self.select_vendido2)

		# si se escribe algo en la caja, que se actualice la tabla
		self.box_codname.bind("<KeyRelease>", self.check2)

		self.count = 0

		#------------------------------------- información del cliente -------------------------------------

		lbl_cliente = self.etiqueta(self.ventana_vender, 'Cliente', locate_x=5, locate_y=4, grid=True)
		lbl_cliente.grid(pady=0.2)

		lbl_name_cliente = self.etiqueta(self.ventana_vender, 'Nombre', locate_x=4, locate_y=5, grid=True)
		self.nombre_cli  = self.caja_texto(self.ventana_vender, 1.4, 45, locate_x=5, locate_y=5, grid=True)
		lbl_name_cliente.grid(pady=0.5)
		self.nombre_cli.grid(columnspan=2, pady=0.5)

		lbl_apl_cliente  = self.etiqueta(self.ventana_vender, 'Apellido', locate_x=4, locate_y=6, grid=True)
		self.apelli_cli  = self.caja_texto(self.ventana_vender, 1.4, 45, locate_x=5, locate_y=6, grid=True)
		lbl_apl_cliente.grid(pady=0.5)
		self.apelli_cli.grid(columnspan=2, pady=0.5)

		lbl_cel_cliente  = self.etiqueta(self.ventana_vender, 'Celular', locate_x=4, locate_y=7, grid=True)
		self.celular_cli = self.caja_texto(self.ventana_vender, 1.4, 45, locate_x=5, locate_y=7, grid=True)
		lbl_cel_cliente.grid(pady=0.5)
		self.celular_cli.grid(columnspan=2, pady=0.5)

		lbl_ced_cliente  = self.etiqueta(self.ventana_vender, 'Identificación', locate_x=4, locate_y=8, grid=True)
		self.cedula_cli  = self.caja_texto(self.ventana_vender, 1.4, 45, locate_x=5, locate_y=8, grid=True)
		lbl_ced_cliente.grid(pady=0.5)
		self.cedula_cli.grid(columnspan=2, pady=0.5)

		#----------------------------------------- zona de botones -------------------------------

		# Botón para cambiar precio de un producto seleccionado en la canasta de ventas
		boton_cambiaprecio = ttk.Button(self.ventana_vender, text='Cambiar precio', padding=(3,3), command=self.cambia_precio_cred)
		boton_cambiaprecio.grid(row=10, column=4, pady=10)

		# Botón para borrar todos productos que están en la canasta
		boton_vaciar = ttk.Button(self.ventana_vender, text='Vaciar Canasta', padding=(3,3), command=self.vaciar_canasta2)
		boton_vaciar.grid(row=10, column=5, pady=10)

		# Botón para borrar productos seleccionados que están en la canasta
		boton_vaciar = ttk.Button(self.ventana_vender, text='Quitar de canasta', padding=(3,3), command=self.quitar_productos_de_canasta2)
		boton_vaciar.grid(row=10, column=6, pady=10)

		# Botón para aumentar la cantidad de un item que ya está en la canasta de vendidos
		boton_aumentar = ttk.Button(self.ventana_vender, text='Aumentar cantidad', padding=(3,3), command=self.aumentar_cantidad2)
		boton_aumentar.grid(row=11, column=4, pady=10)

		# Botón para disminuir la cantidad de un item que ya está en la canasta de vendidos
		boton_disminuir = ttk.Button(self.ventana_vender, text='Disminuir cantidad', padding=(3,3), command=self.disminuir_cantidad2)
		boton_disminuir.grid(row=11, column=5, pady=10)

		# Botón para vender
		boton_vender = ttk.Button(self.ventana_vender, text='Hacer venta', padding=(3,3), command=self.necesita_cliente2)
		boton_vender.grid(row=11, column=6, pady=10)

		self.final_otra_ventana(self.ventana_vender, self.ventana_ventas)

	def disminuir_cantidad2(self):

		if len(self.tree2.selection()[:]) == 0:

			# ventana de notificacion de que se debe seleccionar algún producto para cambiar su cantidad
			self.notifica_cant = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación cantidad', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_cant, u'!!!NO SE HAN SELECCIONADO ITEMS DE LA CANASTA!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_cant, 'Seleccionar item cuya cantidad vas a cambiar', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_cant, self.ventana_vender, wait=True)

		elif len(self.tree2.selection()[:]) == 1:

			#self.consulta2()

			#self.update_tree2()

			selected     = self.tree2.focus()
			values       = self.tree2.item(selected, 'values')
			cant_canasta = int(values[0]) 
			name_canasta = values[1]
			price_canasta= values[2]

			if cant_canasta >= 2: # si la cantidad disponible es mayor a la cantidad que hay en canasta, se puede aumentar en una unidad la de la canasta

				cant_canasta = cant_canasta - 1

				self.tree2.set(selected, column='amount', value=cant_canasta)
				self.tree2.set(selected, column='subtot', value=cant_canasta*int(price_canasta))

				self.calcula_canasta2()

			elif cant_canasta == 1:

				self.tree2.delete(selected)

				self.calcula_canasta2()

		else:

			# ventana de notificacion de que se seleccionaron más de un item. Sólo se puede seleccionar uno sólo
			self.notifica_cant = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación cantidad', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_cant, u'!!!SELECCIONE UN SÓLO ITEM A CAMBIAR DE CANTIDAD!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_cant, 'Se seleccionaron varios items a cambiar de cantidad. Cambiar uno a uno de cantidad', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_cant, self.ventana_vender, wait=True)

	def aumentar_cantidad2(self):

		if len(self.tree2.selection()[:]) == 0:

			# ventana de notificacion de que se debe seleccionar algún producto para cambiar su cantidad
			self.notifica_cant = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación cantidad', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_cant, u'!!!NO SE HAN SELECCIONADO ITEMS DE LA CANASTA!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_cant, 'Seleccionar item cuya cantidad vas a cambiar', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_cant, self.ventana_vender, wait=True)

		elif len(self.tree2.selection()[:]) == 1:

			#self.consulta2()

			#self.update_tree2()

			selected     = self.tree2.focus()
			values       = self.tree2.item(selected, 'values')
			cant_canasta = int(values[0]) 
			name_canasta = values[1]
			price_canasta= values[2]

			cant_disp = self.cantidad_disponible[self.nombres_disponibles == name_canasta][0]

			if cant_disp > cant_canasta: # si la cantidad disponible es mayor a la cantidad que hay en canasta, se puede aumentar en una unidad la de la canasta

				cant_canasta = cant_canasta + 1

				self.tree2.set(selected, column='amount', value=cant_canasta)
				self.tree2.set(selected, column='subtot', value=cant_canasta*int(price_canasta))

				self.calcula_canasta2()

			else:

				# ventana de notificacion de que ya no hay más disponibilidad para aumentar la cantidad del producto seleccionado
				self.notifica_cant = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación cantidad', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica_cant, u'!!!YA NO HAY MÁS DISPONIBILIDAD DEL PRODUCTO!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica_cant, 'El producto seleccionado no tiene más dispobilidad', 0, 1, grid=True)
				self.final_otra_ventana(self.notifica_cant, self.ventana_vender, wait=True)	

		else:

			# ventana de notificacion de que se seleccionaron más de un item. Sólo se puede seleccionar uno sólo
			self.notifica_cant = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación cantidad', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_cant, u'!!!SELECCIONE UN SÓLO ITEM A CAMBIAR DE CANTIDAD!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_cant, 'Se seleccionaron varios items a cambiar de cantidad. Cambiar uno a uno de cantidad', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_cant, self.ventana_vender, wait=True)

	def cambia_precio_cred(self):

		if len(self.tree2.selection()[:]) == 0:

			# ventana de notificacion de que se debe seleccionar algún producto para quitarlo de la canasta
			self.notifica_cambioprecio = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación nuevo precio', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_cambioprecio, u'!!!NO SE HAN SELECCIONADO ITEMS DE LA CANASTA!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_cambioprecio, 'Seleccionar item cuyo precio de venta vas a cambiar', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_cambioprecio, self.ventana_vender, wait=True)

		elif len(self.tree2.selection()[:]) == 1:

			# ventana para solicitar nuevo precio
			self.ventana_new_price = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion nuevo precio', 0, 3, exitgrid=True)
			self.etiqueta(self.ventana_new_price, u'!!!INGRESE NUEVO PRECIO!!!', 0, 0, grid=True)
			self.box_newprice  = Text(self.ventana_new_price, height=1.4, width=15)
			self.box_newprice.grid(row=1, column=0, pady=10, padx=10)
			# Botón para cambiar precio
			boton_cambiaprecio2 = ttk.Button(self.ventana_new_price, text='Cambiar precio', padding=(3,3), command=self.cambia_precio2_cred)
			boton_cambiaprecio2.grid(row=2, column=0, pady=10)
			self.final_otra_ventana(self.ventana_new_price, self.ventana_vender)

		else:

			# ventana de notificacion de que se debe seleccionar algún producto para quitarlo de la canasta
			self.notifica_cambioprecio = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación nuevo precio', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_cambioprecio, u'!!!SELECCIONE UN SÓLO ITEM A CAMBIAR DE PRECIO!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_cambioprecio, 'Se seleccionaron varios items a cambiar de precio. Cambiar uno a uno de precio', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_cambioprecio, self.ventana_vender, wait=True)

	def cambia_precio2_cred(self):

		new_price = self.box_newprice.get(1.0, "end-1c")

		if new_price.isdigit() == True:
			selected  = self.tree2.focus()
			values    = self.tree2.item(selected, 'values')
			cant_disp = int(values[0])

			self.tree2.set(selected, column='price', value=int(new_price))
			self.tree2.set(selected, column='subtot', value=cant_disp*int(new_price))

			self.calcula_canasta2()

			self.ventana_new_price.destroy()

		else:
			# ventana para avisar que el nuevo precio tiene caracteres no válidos
			self.ventana_bad_price = self.otra_ventana(self.ventana_new_price, '+300+270', u'Notificacion nuevo precio', 0, 2, exitgrid=True)
			self.etiqueta(self.ventana_bad_price, u'!!!CORREGIR PRECIO INGRESADO!!!', 0, 0, grid=True)
			self.etiqueta(self.ventana_bad_price, u'Caracteres ingresados no son correctos', 0, 1, grid=True)

			self.final_otra_ventana(self.ventana_bad_price, self.ventana_new_price)

	def quitar_productos_de_canasta2(self):

		if len(self.tree2.selection()[:]) != 0:

			for x in self.tree2.selection()[:]:
				self.tree2.delete(x)

			self.calcula_canasta2()

		else:

			# ventana de notificacion de que se debe seleccionar algún producto para quitarlo de la canasta
			self.notifica_retiro = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación retira producto', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_retiro, u'!!!NO SE HAN SELECCIONADO ITEMS DE LA CANASTA!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_retiro, 'Seleccionar item a retirar de la canasta', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_retiro, self.ventana_vender, wait=True)

	def vaciar_canasta2(self):

		# vacea la canasta
		self.delete_tree22()

		# actualiza la tabla 1
		self.consulta2()
		self.update_tree2()

		# borar la caja del total
		self.box_total.delete('1.0', END)

		# elimina los registros en las cajas de la sección de clientes
		self.delete_clientes2()

	def necesita_cliente2(self):

		nombre_cliente   = self.nombre_cli.get(1.0, "end-1c")
		apellido_cliente = self.apelli_cli.get(1.0, "end-1c")
		celular_cliente  = self.celular_cli.get(1.0, "end-1c")
		cedula_cliente   = self.cedula_cli.get(1.0, "end-1c")

		if len(self.tree2.get_children()) != 0:

			#################### decide si el producto cuyo código de barras fue ingresado necesita IMEI o no #########################

			self.imei_bool_list = []

			for record in self.tree2.get_children(): # recorre cada entrada de la tabla 2

				name_vendido = self.tree2.item(record, 'values')[1]
				cant_vendido = int(self.tree2.item(record, 'values')[0])
				code_vendido = self.codes_disponibles[self.nombres_disponibles == name_vendido][0]

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("SELECT tiene_imei FROM productos WHERE codigo_barras = " + str(code_vendido) + ";")
				decide_existencia = db_cursor.fetchall()
				db_conn.close ()

				self.imei_bool_list.append(decide_existencia[0][0]) # es cero o uno (0 ó 1)

			self.imei_bool_list = np.array(self.imei_bool_list) 

			####################################################################################################################

			if np.any(self.imei_bool_list == 1) == True: # si hay almenos un producto que necesite IMEI significa que sí se necesita introducir los datos del cliente

				self.need_imei          = True # flag para decir que sí hubo productos que necesitaron imeis
				self.diligencia_cliente = True # flag para decir que sí se diligenciaron campos del cliente
				self.valida_registro_clientes_venta2()

			else: # elif nombre_cliente != '' or apellido_cliente != '' or celular_cliente != '' or cedula_cliente != '': # no hay productos que necesiten imeis pero hubo al menos un campo de la sección de clientes que fue diligenciado

				self.need_imei          = False # flag para decir que no hubo productos que necesitaron imeis
				self.diligencia_cliente = True # flag para decir que sí se diligenciaron campos del cliente
				self.valida_registro_clientes_venta2()	

			# else:

			# 	self.need_imei = False # flag para decir que no hubo productos que necesitaron imeis
			# 	self.diligencia_cliente = False # flag para decir que no se diligenciaron campos del cliente
			# 	self.new_customer = False
			# 	self.definir_imeis2()

		else:

			# Ventana de notificacion de que no hay productos en la canasta para vender
			self.notifica_no_existencia = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion productos', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_no_existencia, u'!!!ERROR!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_no_existencia, u'No hay productos en la canasta de créditos', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_no_existencia, self.ventana_vender, wait=True)

	def valida_registro_clientes_venta2(self):

		nombre_cliente   = self.nombre_cli.get(1.0, "end-1c")
		apellido_cliente = self.apelli_cli.get(1.0, "end-1c")
		celular_cliente  = self.celular_cli.get(1.0, "end-1c")
		cedula_cliente   = self.cedula_cli.get(1.0, "end-1c")

		if nombre_cliente == '' or apellido_cliente == '':

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos 
			self.notifica = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion Cliente', 0, 3, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Se requieren los datos correctos del cliente.', 0, 1, grid=True)
			self.etiqueta(self.notifica, u'Nombre y Apellido son campos necesarios', 0, 2, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_vender)

		elif bool(re.match('[a-zA-Z\s]+$', nombre_cliente)) == False or bool(re.match('[a-zA-Z\s]+$', apellido_cliente)) == False:

			# ventana de notificacion de que el nombre o el apellido del cliente fueron escritos con números
			self.notifica = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion Cliente', 0, 3, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!',  0, 0, grid=True)
			self.etiqueta(self.notifica, u'Se requieren los datos correctos del cliente.', 0, 1, grid=True)
			self.etiqueta(self.notifica, u'Nombre o Apellido errado. Tiene números', 0, 2, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_vender)

		elif cedula_cliente == '':

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
			self.notifica = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion Cliente', 0, 3, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Se requieren los datos correctos del cliente.', 0, 1, grid=True)
			self.etiqueta(self.notifica, u'Cédula es un campo necesario', 0, 2, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_vender)

		elif cedula_cliente.isdigit() == False:

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
			self.notifica = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion Cliente', 0, 3, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Se requieren los datos correctos del cliente.', 0, 1, grid=True)
			self.etiqueta(self.notifica, u'Cédula con caracteres inválidos. Sólo admite números.', 0, 2, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_vender)

		elif celular_cliente == '':

			self.celular_cli_bool = False

			texto_info = 'Nombre: '   + self.nombre_cli.get(1.0, "end-1c") + '\n'
			texto_info+= 'Apellido: ' + self.apelli_cli.get(1.0, "end-1c") + '\n'
			texto_info+= 'Celular: '  + self.celular_cli.get(1.0, "end-1c") + '\n'
			texto_info+= u'Cédula: '  + self.cedula_cli.get(1.0, "end-1c")

			self.cedula_repetida2()

		elif celular_cliente != '':

			if celular_cliente.isdigit() == True:

				self.celular_cli_bool = True

				self.cedula_repetida2()

			else:

				# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
				self.notifica = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion Cliente', 0, 3, exitgrid=True)
				self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica, u'Se requieren los datos correctos del cliente (hay productos con IMEI o usted está diligenciando datos del cliente)', 0, 1, grid=True)
				self.etiqueta(self.notifica, u'Celular con caracteres inválidos. Sólo admite números.', 0, 2, grid=True)
				self.final_otra_ventana(self.notifica, self.ventana_vender)

	def cedula_repetida2(self):

		nombre_cliente   = self.nombre_cli.get(1.0, "end-1c")
		apellido_cliente = self.apelli_cli.get(1.0, "end-1c")
		celular_cliente  = self.celular_cli.get(1.0, "end-1c")
		cedula_cliente   = self.cedula_cli.get(1.0, "end-1c")

		self.ingresa_cli_name    = nombre_cliente
		self.ingresa_cli_apellido= apellido_cliente
		self.ingresa_cli_cedula  = cedula_cliente
		self.ingresa_cli_celular = celular_cliente

		#--------------- Ahora evalua que no haya duplicidad de los datos ingresados en la base de datos ---------------------------

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT id, cedula, nombre, celular FROM clientes WHERE cedula = " + cedula_cliente + ";")
		identificacion_repetida = db_cursor.fetchall()
		db_conn.close()

		if len(identificacion_repetida) >= 1:

			self.notifica = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion Cliente', 0, 7, exitgrid=True, textsalir='Corregir datos')
			self.etiqueta(self.notifica, u'Sus datos ingresados fueron', 0, 0, grid=True).grid(columnspan=3)
			self.etiqueta(self.notifica, u'Nombre: ', 0, 1, grid=True).grid(pady=1)
			self.etiqueta(self.notifica, nombre_cliente + ' ' + apellido_cliente, 150, 52, weight='normal')
			self.etiqueta(self.notifica, u'Cédula: ', 0, 2, grid=True).grid(pady=1)
			self.etiqueta(self.notifica, cedula_cliente, 150, 85, weight='normal')
			self.etiqueta(self.notifica, u'Celular: ', 0, 3, grid=True).grid(pady=1)
			self.etiqueta(self.notifica, celular_cliente, 150, 118, weight='normal')
			self.etiqueta(self.notifica, u'Existen ' + str(len(identificacion_repetida)) + ' clientes con la misma cédula', 0, 4, grid=True, color='red').grid(columnspan=3)

			#-------------------------------- Crea las tablas -------------------------------

			columna_cliente1 = ('id', 'ident', 'name', 'cel')
			self.tree4       = ttk.Treeview(self.notifica, columns=columna_cliente1)

			ysb  = ttk.Scrollbar(self.notifica, orient=VERTICAL, command= self.tree4.yview)
			self.tree4['yscroll'] = ysb.set

			# setup column headings
			self.tree4.heading('#0',   text='')
			self.tree4.heading('id', text=u'ID', anchor=W)
			self.tree4.heading('ident', text=u'Cédula', anchor=W)
			self.tree4.heading('name', text='Nombre', anchor=W)
			self.tree4.heading('cel', text='Celular', anchor=W)

			self.tree4.column('#0',   stretch=1, width=0, anchor=W)
			self.tree4.column('id', stretch=1, width=60, anchor=W)
			self.tree4.column('ident', stretch=1, width=100, anchor=W)
			self.tree4.column('name', stretch=1, width=250, anchor=W)
			self.tree4.column('cel', stretch=1, width=100, anchor=W)

			# add tree and scrollbars to frame
			self.tree4.grid(row=5, column=0, columnspan=3, rowspan=1, sticky=NSEW, padx=10, pady=10)

			ysb.grid(row=5, column=4, rowspan=1, sticky=NS, pady=10, ipady=1)

			# set frame resizing priorities
			self.ventana_vender.rowconfigure(0, weight=1)
			self.ventana_vender.columnconfigure(0, weight=1)

			linea_separ = ttk.Separator(self.notifica, orient=HORIZONTAL)
			linea_separ.grid(row=6, column=0, columnspan=3, sticky=EW, padx=10, pady=10)

			#------------------------------- inserta los datos -------------------------------------

			for i in range(len(identificacion_repetida)):

				id_db      = str(identificacion_repetida[i][0])
				nombre_db  = identificacion_repetida[i][2]
				celular_db = str(identificacion_repetida[i][3])
				cedula_db  = str(identificacion_repetida[i][1])

				VALUES = (id_db, cedula_db, nombre_db, celular_db)

				self.tree4.insert('', END, text='', values=VALUES, iid=i)

			self.agrega_boton(self.notifica, u'Continuar con datos ingresados', 1, 7, pad=(3,3), grid=True, comando=self.new_cliente2)
			self.agrega_boton(self.notifica, u'Seleccionar datos de la tabla', 2, 7, pad=(3,3), grid=True, comando=self.old_cliente2) 
			self.final_otra_ventana(self.notifica, self.ventana_vender)

		elif len(identificacion_repetida) == 0:

			self.notifica = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion Cliente', 0, 5, exitgrid=True, textsalir='Corregir datos')
			self.etiqueta(self.notifica, u'Sus datos ingresados fueron', 0, 0, grid=True).grid(columnspan=4)
			self.etiqueta(self.notifica, u'Nombre: ', 0, 1, grid=True).grid(pady=1)
			self.etiqueta(self.notifica, nombre_cliente + ' ' + apellido_cliente, 150, 52, weight='normal')
			self.etiqueta(self.notifica, u'Cédula: ', 0, 2, grid=True).grid(pady=1)
			self.etiqueta(self.notifica, cedula_cliente, 150, 85, weight='normal')
			self.etiqueta(self.notifica, u'Celular: ', 0, 3, grid=True).grid(pady=1)
			self.etiqueta(self.notifica, celular_cliente, 150, 118, weight='normal')

			linea_separ = ttk.Separator(self.notifica, orient=HORIZONTAL)
			linea_separ.grid(row=4, column=0, columnspan=3, sticky=EW, padx=10, pady=10)

			self.agrega_boton(self.notifica, u'Validar datos', 1, 5, pad=(3,3), grid=True, comando=self.new_cliente2)

			self.final_otra_ventana(self.notifica, self.ventana_vender)

	def new_cliente2(self):

		self.new_customer = True
		self.definir_imeis2()

	def old_cliente2(self):

		self.new_customer = False

		if len(self.tree4.selection()[:]) == 0:

			# ventana de notificacion de que se debe seleccionar un cliente de la tabla
			self.ventana_old_cli = self.otra_ventana(self.notifica, '+300+270', u'Notificación Cliente', 0, 2, exitgrid=True)
			self.etiqueta(self.ventana_old_cli, u'!!!SELECCIONE UN CLIENTE DE LA TABLA!!!', 0, 0, grid=True)
			self.etiqueta(self.ventana_old_cli, 'Se debe seleccionar un cliente de la tabla', 0, 1, grid=True)
			self.final_otra_ventana(self.ventana_old_cli, self.notifica, wait=True)

		elif len(self.tree4.selection()[:]) == 1:

			selected            = self.tree4.focus()
			values              = self.tree4.item(selected, 'values')
			self.ingresa_cli_id = values[0]
			self.definir_imeis2()

		else:

			# ventana de notificacion de que se debe seleccionar un cliente de la tabla
			self.ventana_old_cli = self.otra_ventana(self.notifica_imei, '+300+270', u'Notificación Cliente', 0, 2, exitgrid=True)
			self.etiqueta(self.ventana_old_cli, u'!!!SELECCIONE UN SÓLO CLIENTE DE LA TABLA!!!', 0, 0, grid=True)
			self.etiqueta(self.ventana_old_cli, 'Seleccionar un sólo cliente de la tabla para poder continuar con la venta', 0, 1, grid=True)
			self.final_otra_ventana(self.ventana_old_cli, self.notifica, wait=True)

	def definir_imeis2(self):

		if self.diligencia_cliente == True:

			self.notifica.destroy()

		if self.need_imei == True: # si hay almenos un producto que necesite IMEI se abre entonces la ventana para preguntar por el IMEI

			####################################################################################################
			##### configura la tabla para mostrar los productos que necesitan IMEI

			# ventana para ingresar los imeis
			self.notifica_imei = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificación IMEI', 1, 6, textsalir='Cancelar', exitgrid=True)
			et1 = self.etiqueta(self.notifica_imei, u'Por favor ingrese el IMEI de los siguientes productos', 0, 0, grid=True)
			et1.grid(columnspan=3)
			et2 = self.etiqueta(self.notifica_imei, u'Seleccione el producto deseado y presione en "Escribir IMEI" uno a uno', 0, 1, grid=True)
			et2.grid(columnspan=3)

			# create the trees and scrollbars
			self.dataCols3 = ('code', 'name', 'imei')
			self.tree3= ttk.Treeview(self.notifica_imei, columns=self.dataCols3)

			ysb3 = ttk.Scrollbar(self.notifica_imei, orient=VERTICAL, command= self.tree3.yview)
			self.tree3['yscroll'] = ysb3.set

			# setup column headings
			self.tree3.heading('#0',   text='')
			self.tree3.heading('code', text=u'Código', anchor=W)
			self.tree3.heading('name', text='Nombre', anchor=W)
			self.tree3.heading('imei', text='IMEI', anchor=W)

			self.tree3.column('#0',   stretch=1, width=0, anchor=W)
			self.tree3.column('code', stretch=1, width=200, anchor=W)
			self.tree3.column('name', stretch=1, width=250, anchor=W)
			self.tree3.column('imei', stretch=1, width=250, anchor=W)

			# add tree and scrollbars to frame
			self.tree3.grid(row=2, column=0, columnspan=3, rowspan=2, sticky=NSEW, padx=10, pady=10)

			ysb3.grid(row=2, column=3, rowspan=2, sticky=NS, pady=10)

			# inea separadora
			linea_separ = ttk.Separator(self.notifica_imei, orient=HORIZONTAL)
			linea_separ.grid(row=5, column=0, columnspan=4, sticky=EW, padx=10, pady=10)

			####################################################################################################


			################ Pone la información en la tabla

			cont = 0

			for i, record in enumerate(self.tree2.get_children()): # recorre cada entrada de la tabla 2

				name_vendido = self.tree2.item(record, 'values')[1]
				cant_vendido = int(self.tree2.item(record, 'values')[0])
				code_vendido = self.codes_disponibles[self.nombres_disponibles == name_vendido][0]

				tiene_imei  = self.imei_bool_list[i]

				if tiene_imei == 1:

					for i in range(cant_vendido):

						VALUES = (code_vendido, name_vendido, None)

						self.tree3.insert('', END, text='', values=VALUES, iid= cont + i)

				cont = cont + cant_vendido

			####################################################################################################

			# Botón para alimentar imei
			boton_imei = ttk.Button(self.notifica_imei, text='Escribir/Actualizar IMEI', padding=(3,3), command=self.establecer_imei2)
			boton_imei.grid(row=4, column=0, pady=10)

			# Botón para terminar la venta
			boton_fin_venta = ttk.Button(self.notifica_imei, text='Finalizar venta', padding=(3,3), command=self.imei_correctos2)
			boton_fin_venta.grid(row=4, column=2, pady=10)

			self.final_otra_ventana(self.notifica_imei, self.ventana_vender, wait=True)

		else:

			self.vender_productos2()

	def establecer_imei2(self):

		if len(self.tree3.selection()[:]) == 0:

			# ventana de notificacion de que se debe seleccionar algún producto para quitarlo de la canasta
			self.ventana_new_imei = self.otra_ventana(self.notifica_imei, '+300+270', u'Notificación IMEI', 0, 2, exitgrid=True)
			self.etiqueta(self.ventana_new_imei, u'!!!SELECCIONE UN ITEM!!!', 0, 0, grid=True)
			self.etiqueta(self.ventana_new_imei, 'Se debe seleccionar un item para establecer el IMEI', 0, 1, grid=True)
			self.final_otra_ventana(self.ventana_new_imei, self.notifica_imei, wait=True)

		elif len(self.tree3.selection()[:]) == 1:

			selected        = self.tree3.focus()
			values          = self.tree3.item(selected, 'values')
			name_selected   = values[1]
			imei_establecer = values[2]

			if imei_establecer == 'None':

				# ventana para solicitar nuevo precio
				self.ventana_new_imei = self.otra_ventana(self.notifica_imei, '+300+270', u'Notificación IMEI', 0, 3, textsalir='Cancelar', exitgrid=True)
				self.etiqueta(self.ventana_new_imei, u'Ingrese IMEI del producto "' + name_selected + '"', 0, 0, grid=True)
				# caja para ingresar el imei
				self.box_newimei  = Text(self.ventana_new_imei, height=1.4, width=25)
				self.box_newimei.grid(row=1, column=0, pady=10, padx=10)

				# Botón para cambiar precio
				boton_cambiaimei = ttk.Button(self.ventana_new_imei, text='Confirmar', padding=(3,3), command=self.cambia_imei2)
				boton_cambiaimei.grid(row=2, column=0, pady=10)
				
				self.final_otra_ventana(self.ventana_new_imei, self.notifica_imei)

			else:

				# ventana para cambiar imei
				self.ventana_new_imei = self.otra_ventana(self.notifica_imei, '+300+270', u'Notificación IMEI', 0, 3, textsalir='Cancelar', exitgrid=True)
				self.etiqueta(self.ventana_new_imei, u'Usted va a actualizar el IMEI de "' + name_selected + '"', 0, 0, grid=True)
				# caja para ingresar el imei
				self.box_newimei  = Text(self.ventana_new_imei, height=1.4, width=25)
				self.box_newimei.grid(row=1, column=0, pady=10, padx=10)

				# Botón para cambiar imei
				boton_cambiaimei = ttk.Button(self.ventana_new_imei, text='Confirmar', padding=(3,3), command=self.cambia_imei2)
				boton_cambiaimei.grid(row=2, column=0, pady=10)
				
				self.final_otra_ventana(self.ventana_new_imei, self.notifica_imei)

		else:

			# ventana de notificacion de que se debe seleccionar algún producto para quitarlo de la canasta
			self.ventana_new_imei = self.otra_ventana(self.notifica_imei, '+300+270', u'Notificación IMEI', 0, 2, exitgrid=True)
			self.etiqueta(self.ventana_new_imei, u'!!!SELECCIONE UN SÓLO ITEM!!!', 0, 0, grid=True)
			self.etiqueta(self.ventana_new_imei, 'Establecer uno a uno el IMEI', 0, 1, grid=True)
			self.final_otra_ventana(self.ventana_new_imei, self.notifica_imei, wait=True)

	def cambia_imei2(self):

		new_imei = self.box_newimei.get(1.0, "end-1c")

		if new_imei.isdigit() == True:

			if len(new_imei) == 15:

				selected  = self.tree3.focus()
				self.tree3.set(selected, column='imei', value=int(new_imei))
				self.ventana_new_imei.destroy()

			else:

				# ventana de notificacion de que se debe seleccionar algún producto para quitarlo de la canasta
				self.notifica_bad_imei = self.otra_ventana(self.ventana_new_imei, '+350+320', u'Notificación IMEI', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica_bad_imei, u'!!!CORREGIR IMEI!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica_bad_imei, 'El IMEI no tiene 15 dígitos', 0, 1, grid=True)
				self.final_otra_ventana(self.notifica_bad_imei, self.ventana_new_imei, wait=True)

		else:
			# ventana para avisar que el nuevo precio tiene caracteres no válidos
			self.ventana_bad_imei = self.otra_ventana(self.ventana_new_imei, '+350+320', u'Notificacion IMEI errado', 0, 2, exitgrid=True)
			self.etiqueta(self.ventana_bad_imei, u'!!!CORREGIR IMEI!!!', 0, 0, grid=True)
			self.etiqueta(self.ventana_bad_imei, u'Caracteres ingresados no son correctos', 0, 1, grid=True)
			self.final_otra_ventana(self.ventana_bad_imei, self.ventana_new_imei)

	def imei_correctos2(self): # método para establecer si los imeis de los productos que se van a vender fueron introducidos correctamente y si fueron escritos todos los requeridos

		for i, record in enumerate(self.tree3.get_children()): # recorre cada entrada de la tabla 2

			flag_imeis_correctos = False

			code_evalua = self.tree3.item(record, 'values')[0]
			name_evalua = self.tree3.item(record, 'values')[1]
			imei_evalua = self.tree3.item(record, 'values')[2]

			#### evalúa que el imei no sea None

			if imei_evalua == 'None': # se constata que no falten imeis por ser introducidos

				# Ventana de notificacion de que aún faltan imeis por ser introducidos
				self.notifica_no_imei = self.otra_ventana(self.notifica_imei, '+300+270', u'Notificacion venta', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica_no_imei, u'!!!ERROR!!', 0, 0, grid=True)
				self.etiqueta(self.notifica_no_imei, 'Falta POR LO MENOS un IMEI por ser introducido', 0, 1, grid=True)
				self.final_otra_ventana(self.notifica_no_imei, self.notifica_imei, wait=True)

				break

			else:

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("SELECT stocks.id FROM stocks INNER JOIN productos ON productos.codigo_barras = stocks.codigo_barras_id WHERE stocks.estado = 'En Stock' AND productos.nombre_producto = '" + name_evalua + "' AND stocks.IMEI = " + str(imei_evalua) + ";")
				id_number  = db_cursor.fetchall()
				db_conn.close ()

				if len(id_number) == 0: # esto quiere decir que no hay un producto con el nombre deseado EN STOCK (es decir para la venta) con el imei indicado

					# Ventana de notificacion de que aún faltan imeis por ser introducidos
					self.notifica_no_imei = self.otra_ventana(self.notifica_imei, '+300+270', u'Notificacion venta a crédito', 0, 2, exitgrid=True)
					self.etiqueta(self.notifica_no_imei, u'!!!ERROR!!', 0, 0, grid=True)
					self.etiqueta(self.notifica_no_imei, 'El IMEI "' + str(imei_evalua) + '" para el producto "' + name_evalua + '" no existe en la base de datos o no está disponible para su venta', 0, 1, grid=True)
					self.final_otra_ventana(self.notifica_no_imei, self.notifica_imei, wait=True)

					break

				else:

					flag_imeis_correctos = True

		if i == len(self.tree3.get_children())-1 and flag_imeis_correctos == True:

			self.vender_productos2()

	def vender_productos2(self):

		self.current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		#--------------------------------------- Se introducen datos del cliente si es necesario -------------------------------------------------

		if self.new_customer == True:

			self.introduce_cli_db_venta2()

			#---------- consulta2 id ----------------

			nombre_cliente   = self.ingresa_cli_name
			apellido_cliente = self.ingresa_cli_apellido
			celular_cliente  = self.ingresa_cli_celular
			cedula_cliente   = self.ingresa_cli_cedula
			
			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			if	self.celular_cli_bool == True:
				db_cursor.execute("SELECT id FROM clientes WHERE cedula = " + cedula_cliente + " AND nombre = '" + nombre_cliente + " " + apellido_cliente + "' AND celular = " + celular_cliente + ";")
			else:
				db_cursor.execute("SELECT id FROM clientes WHERE cedula = " + cedula_cliente + " AND nombre = '" + nombre_cliente + " " + apellido_cliente + "';")
			self.ingresa_cli_id = db_cursor.fetchall()[0][0]
			db_conn.close()

		#-------------------------- consulta2 maximo id_venta ------------------------

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT MAX(valor_creditos_id) FROM creditos;")
		self.max_id_venta = db_cursor.fetchall()[0][0]
		db_conn.close()

		if self.max_id_venta == None: # Si no se ha registrado la primera venta
			self.max_id_venta = 0

		self.max_id_venta = self.max_id_venta + 1

		#-------------------------- extrae los datos de los IMEI introducidos en la tabla tree3

		if self.need_imei == True:

			code_imei = []
			name_imei = []
			imei_imei = []

			for i, record in enumerate(self.tree3.get_children()):

				code_imei.append(int(self.tree3.item(record, 'values')[0]))
				name_imei.append(self.tree3.item(record, 'values')[1])
				imei_imei.append(int(self.tree3.item(record, 'values')[2]))

			tabla3_dict   = {'CODE': code_imei, 'NAME': name_imei, 'IMEI': imei_imei}
			tabla3_pandas = pd.DataFrame.from_dict(tabla3_dict)

		#----------------------------------------------------------------------------------------

		self.total_cobrar = self.box_total.get(1.0, "end-1c")
		
		for rcrd, record in enumerate(self.tree2.get_children()): # recorre cada entrada de la tabla 2

			name_vendido = self.tree2.item(record, 'values')[1]
			cant_vendido = int(self.tree2.item(record, 'values')[0])
			subtotal     = int(self.tree2.item(record, 'values')[3])
			price_vendido= int(self.tree2.item(record, 'values')[2])
			code_vendido = self.codes_disponibles[self.nombres_disponibles == name_vendido][0]

			#self.total_cobrar = self.total_cobrar + subtotal

			################# esta pequeña sección es para saber si la consulta2 se hace con o sin imei  ###########################
			################# si la variable need_imei = 1 es que se necesita con imei, pero si need_imei = 0 no se necesita consulta2 con imei

			db_conn      = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor    = db_conn.cursor()
			db_cursor.execute("SELECT tiene_imei FROM productos WHERE codigo_barras = " + str(code_vendido) + ";")
			decide_existencia = db_cursor.fetchall()
			db_conn.close ()

			necesita_imei    = decide_existencia[0][0] # es cero o uno (0 ó 1)

			#----------------------------------------------------------------------------------------

			#--------------------- Cambia la disponibilidad de los productos

			if necesita_imei == 0: # no necesita imei
				
				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("SELECT stocks.id FROM stocks INNER JOIN productos ON productos.codigo_barras = stocks.codigo_barras_id WHERE stocks.estado = 'En Stock' AND productos.codigo_barras = " + str(code_vendido) + ";")
				id_query  = db_cursor.fetchall()
				db_conn.close ()

				id_number  = np.array([NN[0] for NN in id_query])

				for n in range(cant_vendido): 

					self.id_stock_venta = id_number[n]

					db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
					db_cursor  = db_conn.cursor()
					db_cursor.execute("UPDATE stocks SET estado = 'Out' WHERE id = " + str(self.id_stock_venta) + ";")
					db_cursor.execute("UPDATE stocks SET precio_venta = " + str(price_vendido) + " WHERE id = " + str(self.id_stock_venta) + ";")
					db_cursor.close()
					db_conn.commit ()
					db_conn.close()

					#------------------------ Se registra el valor de la venta -------------------------------------

					if n + rcrd == 0:
						self.registrar_valor_credito()

					#--------------------------------------- Se registra la venta ----------------------------------------------------------------------------

					self.registrar_venta2()

			elif necesita_imei == 1: # necesita imei

				imei_productos = tabla3_pandas[tabla3_pandas.CODE == code_vendido].IMEI.values ### estos son los imeis del producto cuyo codigo de barras se está evaluando

				for indx, imei_selected in enumerate(imei_productos):

					#----------------------- Consulta2 id del producto que se va a actualizar ----------------------------------

					db_conn             = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
					db_cursor           = db_conn.cursor()
					db_cursor.execute("SELECT stocks.id FROM stocks INNER JOIN productos ON productos.codigo_barras = stocks.codigo_barras_id WHERE stocks.estado = 'En Stock' AND productos.codigo_barras = " + str(code_vendido) + " AND stocks.IMEI = " + str(imei_selected) + ";")
					self.id_stock_venta = db_cursor.fetchall()[0][0]
					db_conn.close()

					#----------------------- Actualiza stocks con salida del producto -----------------------------

					db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
					db_cursor  = db_conn.cursor()
					db_cursor.execute("UPDATE stocks SET estado = 'Out' WHERE codigo_barras_id = " + str(code_vendido) + " AND IMEI = " + str(imei_selected) + ";")
					db_cursor.execute("UPDATE stocks SET precio_venta = " + str(price_vendido) + " WHERE codigo_barras_id = " + str(code_vendido) + " AND IMEI = " + str(imei_selected) + ";")
					db_cursor.close()
					db_conn.commit ()
					db_conn.close()

					#------------------------ Se registra el valor de la venta -------------------------------------

					if indx + rcrd == 0:
						self.registrar_valor_credito()

					#--------------------------------------- Se registra la venta ----------------------------------------------------------------------------

					self.registrar_venta2()

		#--------------------------------------- últimas acciones ---------------------------------------

		self.factura_cliente_credito()

		# Elimina la ventana de los imeis
		if self.need_imei == True:
			self.notifica_imei.destroy()

		# Ventana de notificacion de que la venta fue exitosa
		self.notifica_no_existencia = self.otra_ventana(self.ventana_vender, '+300+270', u'Notificacion separe', 0, 3, exitgrid=True)
		self.etiqueta(self.notifica_no_existencia, u'!!!VENTA A CRÉDITO EXITOSA!!', 0, 0, grid=True)
		self.etiqueta(self.notifica_no_existencia, 'Total a cobrar $ ' + self.total_cobrar, 0, 1, grid=True)
		self.etiqueta(self.notifica_no_existencia, 'Factura ID: ' + str(self.max_id_venta), 0, 2, grid=True)
		self.final_otra_ventana(self.notifica_no_existencia, self.ventana_vender, wait=True)

		# Elimina los registros de la tabla 2
		self.vaciar_canasta2()

	def registrar_valor_credito(self):

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("INSERT INTO valor_creditos (id, valor_credito) VALUES (" + str(self.max_id_venta) + ", " + self.total_cobrar + ");")
		db_cursor.close()
		db_conn.commit ()
		db_conn.close ()

	def registrar_venta2(self):

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		if self.diligencia_cliente == True:
			db_cursor.execute("INSERT INTO creditos (fecha_credito, stocks_id, valor_creditos_id, clientes_id) VALUES ('" + self.current_time + "', " + str(self.id_stock_venta) + ", " + str(self.max_id_venta) + ", " + str(self.ingresa_cli_id) + ");")
		else:
			db_cursor.execute("INSERT INTO creditos (fecha_credito, stocks_id, valor_creditos_id) VALUES ('" + self.current_time + "', " + str(self.id_stock_venta) + ", " + str(self.max_id_venta) + ");")
		db_cursor.close()
		db_conn.commit ()
		db_conn.close ()

	def introduce_cli_db_venta2(self):

		nombre_cliente   = self.ingresa_cli_name
		apellido_cliente = self.ingresa_cli_apellido
		celular_cliente  = self.ingresa_cli_celular
		cedula_cliente   = self.ingresa_cli_cedula

		try:

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			if	self.celular_cli_bool == True:
				db_cursor.execute("INSERT INTO clientes (nombre, celular, cedula) VALUES ('" + nombre_cliente + " " + apellido_cliente + "', " + celular_cliente + ", " + cedula_cliente + ");")
			else:
				db_cursor.execute("INSERT INTO clientes (nombre, cedula) VALUES ('" + nombre_cliente + " " + apellido_cliente + "', " + cedula_cliente + ");")
			db_cursor.close()
			db_conn.commit ()
			db_conn.close ()

		except MySQLdb.IntegrityError as e: 
			
			if format(e).find("Duplicate entry") != -1 and format(e).find(cedula_cliente) != -1: # si es igual a -1 el metodo find no halló nada

				print('La cédula del cliente ya existe')

				# ventana de notificacion de que la cédula del cliente ya existe
				self.notifica = self.otra_ventana(self.valida_vendedores, '450x150+300+270', u'Notificacion Cliente', 190, 100)
				self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 180, 10)
				self.etiqueta(self.notifica, 'Cédula del cliente ya existe. Cambiar', 25, 40)
				self.final_otra_ventana(self.notifica, self.valida_clientes)

			elif format(e).find("Duplicate entry") != -1 and format(e).find(celular_cliente) != -1: # si es igual a -1 el metodo find no halló nada

				print('El celular del cliente ya existe')

				# ventana de notificacion de que la cédula del cliente ya existe
				self.notifica = self.otra_ventana(self.valida_clientes, '450x150+300+270', u'Notificacion Cliente', 190, 100)
				self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 180, 10)
				self.etiqueta(self.notifica, 'Celular del cliente ya existe. Cambiar.', 25, 40)
				self.final_otra_ventana(self.notifica, self.valida_clientes)

	def delete_tree22(self):

		### elimina registros de la tabla
		for record in self.tree2.get_children():
			self.tree2.delete(record)

	def delete_clientes2(self):

		self.nombre_cli.delete('1.0', END)
		self.apelli_cli.delete('1.0', END)
		self.celular_cli.delete('1.0', END)
		self.cedula_cli.delete('1.0', END)

	def consulta2(self):

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT nombre_producto, codigo_barras, tiene_imei FROM productos;")
		list_items = db_cursor.fetchall()
		db_conn.close()

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT productos.codigo_barras, stocks.precio_venta, stocks.IMEI FROM stocks INNER JOIN productos ON productos.codigo_barras = stocks.codigo_barras_id WHERE stocks.estado = 'En Stock';")
		list_number = db_cursor.fetchall()
		db_conn.close ()

		self.nombres_disponibles  = np.array([NN[0] for NN in list_items]) # nombres
		codigos_disponibles       = [NN[1] for NN in list_items] #codigos
		prod_disponibles          = np.array([NN[0] for NN in list_number]) #codigos existentes
		precios                   = np.array([NN[1] for NN in list_number]) # precios de los códigos existentes
		self.imeis                = np.array([NN[2] for NN in list_number]) # imei de los productos. Si el producto no es un celular, es nan
		
		self.cantidad_disponible  = np.array([len(prod_disponibles[prod_disponibles == NN]) for NN in codigos_disponibles]) #cantidad existente de cada producto
		#self.bool_imei            = np.array([np.any(self.imeis[prod_disponibles == NN] != None) for NN in codigos_disponibles]) # esta variable me dice si algún producto con este código de barras necesita IMEI. Si es True significa que cualquier producto con dicho código debería necesitar un IMEI
		self.bool_imei            = np.array([NN[2] for NN in list_items])

		prices  = [] #precio de los productos existentes

		for NN in codigos_disponibles:
			if len(precios[prod_disponibles == NN]) >= 1:
				prices.append(precios[prod_disponibles == NN][0])
			else:
				prices.append(np.nan)

		self.codes_disponibles   = np.array(np.copy(codigos_disponibles))
		self.precios_disponibles = np.array(np.copy(prices))

		self.nombres_disponibles_update = self.nombres_disponibles
		self.codes_disponibles_update   = self.codes_disponibles
		self.cantidad_disponible_update = self.cantidad_disponible

	def check2(self, e):

		typed = self.box_codname.get(1.0, "end-1c")

		#self.consulta2()

		if typed == '':

			names = self.nombres_disponibles
			codes = self.codes_disponibles
			cant  = self.cantidad_disponible

		elif typed.isdigit() == False:

			names = []
			codes = []
			cant  = []

			for i, item in enumerate(self.nombres_disponibles):

				if typed.lower() in item.lower():

					names.append(self.nombres_disponibles[i])
					codes.append(self.codes_disponibles[i])
					cant.append(self.cantidad_disponible[i])

		elif typed.isdigit() == True:
			
			names = []
			codes = []
			cant  = []

			for i, item in enumerate(self.codes_disponibles):

				if typed in str(item):

					names.append(self.nombres_disponibles[i])
					codes.append(self.codes_disponibles[i])
					cant.append(self.cantidad_disponible[i])

		self.nombres_disponibles_update = names
		self.codes_disponibles_update   = np.array(codes)
		self.cantidad_disponible_update = np.array(cant)

		self.update_tree2()

	def select_vendido2(self, e):

		# hace consulta2 de los datos por si depronto algún otro cajero hizo una venta y los valores actuales no corresponden con los que hay en la tabla

		#self.consulta2()

		# agregar a la caja lo que se seleccionó
		selected = self.tree.focus()

		values   = self.tree.item(selected, 'values')

		code_selected   = int(values[0])
		name_selected   = values[1]
		cant_disp       = int(values[2])

		# evalúa si los datos en base de datos son los mismos que hay en la tabla. Para ello mira la cantidad del item seleccionado en base de datos

		cant_bd = self.cantidad_disponible[self.codes_disponibles == code_selected][0]

		# verifica si el código seleccionado ya se encuentra en la tabla de vendidos

		existe_en_tree2 = False

		for record in self.tree2.get_children():
			name_vendido  = self.tree2.item(record, 'values')[1]
			cant_vendido  = self.tree2.item(record, 'values')[0]
			price_vendido = self.tree2.item(record, 'values')[2]
			if name_vendido == name_selected:
				existe_en_tree2 = True
				break

		# adiciona el producto a la tabla de vendidos

		if cant_bd < cant_disp:

			# ventana de notificacion de que el producto no tiene unidades disponibles
			self.notifica_no_existencia = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion disponibilidad', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_no_existencia, u'!!!REALICE DE NUEVO SU SELECCIÓN!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_no_existencia, 'Hubo una actualización en la cantidad disponible del item seleccionado', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_no_existencia, self.ventana_vender, wait=True)

			self.consulta2()

			self.update_tree2()

		elif cant_disp == 0:

			# ventana de notificacion de que el producto no tiene unidades disponibles
			self.notifica_no_existencia = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion disponibilidad', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_no_existencia, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_no_existencia, 'El item seleccionado no tiene unidades disponibles', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_no_existencia, self.ventana_vender, wait=True)

		elif existe_en_tree2 == False: # si el producto seleccionado no existe aún en la tabla de vendidos

			precio_selected = int(self.precios_disponibles[self.codes_disponibles == code_selected][0])

			VALUES = (1, name_selected, precio_selected, precio_selected)

			self.tree2.insert('', END, text='', values=VALUES, iid=self.count)

			self.count += 1

		else: # si ya existe en la tabla de vendidos, sólo es aumentar en 1 la cantidad de vendidos

			if int(cant_vendido) == int(cant_disp):

				# ventana de notificacion de que el producto no tiene unidades disponibles
				self.notifica_no_existencia = self.otra_ventana(self.ventana_vender, '+250+220', u'Notificacion disponibilidad', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica_no_existencia, '¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica_no_existencia, 'La totalidad de disponibles de este item ya la has puesto en la canasta de separes',0, 1, grid=True)
				self.final_otra_ventana(self.notifica_no_existencia, self.ventana_vender, wait=True)

			else:

				cant_vendido = int(cant_vendido) + 1
				self.tree2.set(record, column = 'amount', value = cant_vendido)
				self.tree2.set(record, column = 'subtot', value = int(price_vendido) * cant_vendido)

		self.calcula_canasta2()

	def calcula_canasta2(self):

		self.box_total.delete('1.0', END)

		# Calcula el total de la canasta
		total_cobrar = 0
		for record in self.tree2.get_children(): # recorre cada entrada de la tabla 2
			subtotal     = int(self.tree2.item(record, 'values')[3])
			total_cobrar = total_cobrar + subtotal

		self.box_total.delete('1.0', END)
		self.box_total.insert("1.0", total_cobrar)

	def update_tree2(self):

		### elimina registros de la tabla

		for record in self.tree.get_children():
			self.tree.delete(record)

		# introduce los datos a la tabla
		for i in range(len(self.nombres_disponibles_update)):

			codigo_barras = self.codes_disponibles_update[i]
			nombre_produc = self.nombres_disponibles_update[i]
			cant_disp     = self.cantidad_disponible_update[i]

			VALUES        = (codigo_barras, nombre_produc, cant_disp) 

			self.tree.insert('', END, text='', values=VALUES, iid=i)

	def factura_cliente_credito(self):

		#------------------ Crea la carpeta donde se guarda la factura, si esta no se ha creado aún -----------------

		if path.exists(self.guarda_facturas + dt.datetime.now().strftime('%Y-%m-%d')) == False:
			os.system("mkdir " + self.guarda_facturas + dt.datetime.now().strftime('%Y-%m-%d'))

		#------------------ Parámetros variables -----------------

		ID_factura                = str(self.max_id_venta)
		fecha_factura             = self.current_time
		cliente_factura           = self.nombre_cli.get(1.0, "end-1c") + " " + self.apelli_cli.get(1.0, "end-1c")
		contacto_factura          = self.celular_cli.get(1.0, "end-1c")
		identificacion_factura    = self.cedula_cli.get(1.0, "end-1c")
		credito_o_contado_factura = u'(Crédito)'

		lista_nombres_factura  = []
		lista_barcodes_factura = []
		lista_cantidad_factura = []
		lista_valorund_factura = []
		lista_subtotal_factura = []

		for record in self.tree2.get_children(): # recorre cada entrada de la tabla 2

			cant_vendido = self.tree2.item(record, 'values')[0]
			name_vendido = self.tree2.item(record, 'values')[1]
			price_vendido= self.tree2.item(record, 'values')[2]
			subtotal     = self.tree2.item(record, 'values')[3]
			code_vendido = self.codes_disponibles[self.nombres_disponibles == name_vendido][0]

			lista_nombres_factura.append(name_vendido)
			lista_barcodes_factura.append(code_vendido)
			lista_cantidad_factura.append(cant_vendido)
			lista_valorund_factura.append(price_vendido)
			lista_subtotal_factura.append(subtotal)
		
		total_factura = self.total_cobrar

		#---------------------------------------------------------

		w, h = A4

		c = canvas.Canvas(self.guarda_facturas + dt.datetime.now().strftime('%Y-%m-%d') + "/credito_" + ID_factura + ".pdf")

		#------------- Título -------------------
		c.setFillColorRGB(0,0,0)
		c.setFont("Times-Bold", 30)
		c.drawCentredString(170, h - 70, "ULTRATECH")
		#c.setFillColorRGB(194/255,211/255,51/255)
		c.setFillColorRGB(0,0,0)
		c.setFont("Times-BoldItalic", 10)
		c.drawCentredString(170, h - 90, "Venta de repuestos al por mayor y detal - Servicio técnico")
		c.drawCentredString(170, h - 100, "Lista de precios especiales para mayoristas")

		#------------- Rectángulo -------------------
		c.setFillGray(0.85)
		c.rect(345, h - 180, 250, 180, fill=True, stroke=False)

		#------------- Ubicación -------------------
		c.setFillColorRGB(0,0,0)
		c.setFont("Helvetica-Bold", 10)
		c.drawRightString(565, h - 50, "C.C. Cundinamarqués")
		c.setFont("Courier", 10)
		c.drawRightString(565, h - 60, "Calle 13 N°14-42")
		c.setFont("Courier", 10)
		c.drawRightString(565, h - 70, "Local 120")
		c.setFont("Courier", 10)
		c.drawRightString(565, h - 80, "Bogotá D.C/Colombia")

		#------------- Contacto -------------------
		c.setFont("Helvetica-Bold", 13)
		c.drawString(380, h - 120, "Contacto")
		c.setFont("Helvetica", 12)
		c.drawString(380, h - 140, '"Guaro" / Yesid')
		c.setFont("Courier", 12)
		c.drawString(380, h - 155, 'Cel: 3118234902')

		#------------- ID Factura -------------------
		c.setFont("Helvetica-Bold", 15)
		c.drawString(50, h - 150, "Factura N°")
		c.setFont("Helvetica", 15)
		c.drawString(150, h - 150, ID_factura)

		#------------- Datos Factura -------------------
		c.setFont("Courier-Bold", 10)
		c.drawString(50, h - 165, fecha_factura)
		c.drawString(50, h - 180, "Nombre: " + cliente_factura)
		c.drawString(50, h - 195, "Cel: " + contacto_factura)
		c.drawString(50, h - 210, "Id: " + identificacion_factura)

		#---------------- Total ---------------------

		c.setFont("Courier-Bold", 15)
		c.drawString(50, h - 240, 'Total: $' + str(total_factura) + "       " + credito_o_contado_factura)
		c.line(110, h - 245, 210, h - 245)

		#------------- Recuadro Productos Facturados -------------------

		c.setFillColorRGB(93/255,173/255,226/255)
		c.roundRect(50, h - 300, 500, 30, 10, fill=True, stroke=True)
		c.roundRect(50, h - 300 - 18 * 27, 500, 18 * 27, 10, fill=False, stroke=True)
		c.setFillColorRGB(0,0,0)
		c.line(123, h - 300 - 18 * 27, 123, h-270)
		c.line(326, h - 300 - 18 * 27, 326, h-270)
		c.line(399, h - 300 - 18 * 27, 399, h-270)
		c.line(472, h - 300 - 18 * 27, 472, h-270)


		c.setFont("Courier-Bold", 10)
		c.drawCentredString(86.5, h - 290, "ID")
		c.drawCentredString(224.5, h - 290, "Descripción producto")
		c.drawCentredString(362.5, h - 290, "Cantidad")
		c.drawCentredString(435.5, h - 290, "Valor($)/und")
		c.drawCentredString(510, h - 290, "Subtotal($)")

		#------------- Productos Facturados -------------------
		c.setFont("Courier", 8)

		for i in range(len(lista_nombres_factura)):

			if i <= 26:

				c.drawCentredString(75   , h - 315 - 18*i, str(lista_barcodes_factura[i]))
				c.drawCentredString(224.5, h - 315 - 18*i, lista_nombres_factura[i])
				c.drawCentredString(362.5, h - 315 - 18*i, str(lista_cantidad_factura[i]))
				c.drawCentredString(435.5, h - 315 - 18*i, str(lista_valorund_factura[i]))
				c.drawCentredString(508.5, h - 315 - 18*i, str(lista_subtotal_factura[i]))

			#------------- Recuadro Productos Facturados -------------------

			if (i-27)%41 == 0 or i == 27:
				print('ok')
				c.showPage()

				c.setFillColorRGB(93/255,173/255,226/255)
				c.roundRect(50, h - 50, 500, 30, 10, fill=True, stroke=True)
				c.roundRect(50, h - 50 - 18 * 41, 500, 18 * 41, 10, fill=False, stroke=True)
				c.setFillColorRGB(0,0,0)
				c.line(123, h - 50 - 18 * 41, 123, h-20)
				c.line(326, h - 50 - 18 * 41, 326, h-20)
				c.line(399, h - 50 - 18 * 41, 399, h-20)
				c.line(472, h - 50 - 18 * 41, 472, h-20)

				c.setFont("Courier-Bold", 10)
				c.drawCentredString(86.5, h - 40, "ID")
				c.drawCentredString(224.5, h - 40, "Descripción producto")
				c.drawCentredString(362.5, h - 40, "Cantidad")
				c.drawCentredString(435.5, h - 40, "Valor($)/und")
				c.drawCentredString(510, h - 40, "Subtotal($)")

			#------------- Productos Facturados -------------------

			if i >= 27:
				c.setFont("Courier", 8)

				multiplicador = int((i - 27)/41)

				c.drawCentredString(75   , h - 65 - 18*(i-27-41*multiplicador), str(lista_barcodes_factura[i]))
				c.drawCentredString(224.5, h - 65 - 18*(i-27-41*multiplicador), lista_nombres_factura[i])
				c.drawCentredString(362.5, h - 65 - 18*(i-27-41*multiplicador), str(lista_cantidad_factura[i]))
				c.drawCentredString(435.5, h - 65 - 18*(i-27-41*multiplicador), str(lista_valorund_factura[i]))
				c.drawCentredString(508.5, h - 65 - 18*(i-27-41*multiplicador), str(lista_subtotal_factura[i]))

		#------------- Total -------------------

		if (i-26)%41 == 0:

			c.showPage()
			c.setFillColorRGB(0,0,0)
			c.roundRect(50, h - 50, 500, 30, 10, fill=False, stroke=True)
			c.line(123, h - 50, 123, h-20)
			c.line(326, h - 50, 326, h-20)
			c.line(399, h - 50, 399, h-20)
			c.setFillColorRGB(236/255,112/255,99/255)
			c.roundRect(472, h - 50, 77.5, 30, 10, fill=True, stroke=False)
			c.rect(399, h - 50, 80, 30, fill=True, stroke=False)
			c.line(472, h - 50, 472, h-20)

			c.setFillColorRGB(0,0,0)
			c.setFont("Helvetica-Bold", 10)
			c.drawCentredString(435.5, h - 40, "Total")
			c.setFont("Helvetica", 10)
			c.drawCentredString(508.5, h - 40, "$ " + str(total_factura))

			#------------- Recuadro advertencia -------------------

			c.setFillColorRGB( 247/255, 220/255, 111/255)
			c.roundRect(100, h - 190, 400, 110, 10, fill=True, stroke=True)
			c.setFont("Helvetica-Bold", 10)
			c.setFillColorRGB(0,0,0)
			c.drawCentredString(298, h - 102, "¡ADVERTENCIAS!")
			c.setFont("Helvetica-Bold", 10)
			c.drawString(110, h - 122, "1. En ULTRATECH")
			c.setFont("Helvetica", 10)
			c.drawString(200, h - 122, "nos gusta atenderle y satisfacer al 100% sus necesidades, para ello")
			c.drawString(110, h - 122 - 10*1, "le solicitamos atentamente revisar sus compras y hacer las aclaraciones pertinentes")
			c.drawString(110, h - 122 - 10*2, "antes de retirarse del local, ya que una vez salida la mercancía y retirada de nuestras")
			c.drawString(110, h - 122 - 10*3, "instalaciones no se aceptan reclamos, ni se hacen cambios o devoluciones.")
			c.setFont("Helvetica-Bold", 10)
			c.drawString(110, h - 122 - 10*4, "2. Productos SIN sellos ni plásticos NO TIENEN GARANTÍA.")
			c.drawCentredString(298, h - 122 - 10*6, "Muchas gracias")


		else:

			c.setFillColorRGB(236/255,112/255,99/255)
			c.roundRect(472, h - 68 - 18*40, 77.5, 18, 10, fill=True, stroke=False)
			c.rect(399, h - 68 - 18*40, 80, 18, fill=True, stroke=False)
			c.setFillColorRGB(0,0,0)
			c.line(472, h - 50 - 18 * 41, 472, h - 18 - 18 * 41)

			c.setFont("Helvetica-Bold", 10)
			c.drawCentredString(435.5, h - 65 - 18*40, "Total")
			c.setFont("Helvetica", 10)
			c.drawCentredString(508.5, h - 65 - 18*40, "$ " + str(total_factura))

			#------------- Recuadro advertencia -------------------
			c.showPage()

			c.setFillColorRGB( 247/255, 220/255, 111/255)
			c.roundRect(100, h - 130, 400, 110, 10, fill=True, stroke=True)
			c.setFont("Helvetica-Bold", 10)
			c.setFillColorRGB(0,0,0)
			c.drawCentredString(298, h - 42, "¡ADVERTENCIAS!")
			c.setFont("Helvetica-Bold", 10)
			c.drawString(110, h - 62, "1. En ULTRATECH")
			c.setFont("Helvetica", 10)
			c.drawString(200, h - 62, "nos gusta atenderle y satisfacer al 100% sus necesidades, para ello")
			c.drawString(110, h - 62 - 10*1, "le solicitamos atentamente revisar sus compras y hacer las aclaraciones pertinentes")
			c.drawString(110, h - 62 - 10*2, "antes de retirarse del local, ya que una vez salida la mercancía y retirada de nuestras")
			c.drawString(110, h - 62 - 10*3, "instalaciones no se aceptan reclamos, ni se hacen cambios o devoluciones.")
			c.setFont("Helvetica-Bold", 10)
			c.drawString(110, h - 62 - 10*4, "2. Productos SIN sellos ni plásticos NO TIENEN GARANTÍA.")
			c.drawCentredString(298, h - 62 - 10*6, "Muchas gracias")

		c.save()