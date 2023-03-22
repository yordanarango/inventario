from tkinter import *
from tkinter import ttk, font
import MySQLdb
#from tkinter.messagebox import showinfo
#import evdev
#from evdev import *
#from tkinter.messagebox import showinfo
import datetime as dt
import numpy as np
import random
import string

class Stock:

	def stock(self):

		# Ventana de opciones de stock

		self.ventana_stock = self.otra_ventana(self.raiz, '+150+120', 'Opciones Stock', 1, 2, exitgrid=True)
		self.agrega_boton(self.ventana_stock, u'Items', 0, 0, self.items, padxy=(40,40), grid=True)
		self.agrega_boton(self.ventana_stock, u'Existencias', 2, 0, self.existencias, padxy=(40,40), grid=True)
		self.agrega_boton(self.ventana_stock, u'Facturas', 1, 1, self.facturas, padxy=(40,40), grid=True)
		self.final_otra_ventana(self.ventana_stock, self.raiz)


	#---------------------------------------------------------------------------------------------
	#-------------------------------- Ventana de opciones de facturas -------------------------------
	#---------------------------------------------------------------------------------------------

	def facturas(self):

		self.ventana_prod = self.otra_ventana(self.ventana_stock, '+200+170', 'Opciones Facturas', 0, 2, exitgrid=True)
		self.agrega_boton(self.ventana_prod, u'Generar Factura', 0, 0,  grid=True)#self.genera_factura
		self.agrega_boton(self.ventana_prod, u'Pagar Factura'  , 0, 1, grid=True)# self.pagar_factura
		self.agrega_boton(self.ventana_prod, u'Buscar Factura' , 0, 1,  grid=True)#self.buscar_factura
		self.final_otra_ventana(self.ventana_prod, self.ventana_stock)

	#---------------------------------------------------------------------------------------------
	#-------------------------------- Ventana de opciones de items -------------------------------
	#---------------------------------------------------------------------------------------------

	def items(self):

		self.ventana_prod = self.otra_ventana(self.ventana_stock, '+200+170', 'Opciones Items', 0, 2, exitgrid=True)
		self.agrega_boton(self.ventana_prod, u'Alimentar Items', 0, 0, self.alimentar_bd, grid=True)
		self.agrega_boton(self.ventana_prod, u'Buscar Items'   , 0, 1, self.busca_item, grid=True)
		self.final_otra_ventana(self.ventana_prod, self.ventana_stock)

	# Ventana de Alimentar base de datos

	def alimentar_bd(self):

		# self.ventana_alimbd = self.otra_ventana(self.ventana_prod, '450x300+250+220', u'Alimentar Base de Datos', 310, 250)
		# self.etiqueta(self.ventana_alimbd, 'Cod. Barras', 20, 23)
		# self.codigo_bd = self.caja_texto(self.ventana_alimbd, 1.4, 35, 140, 25)
		# #self.codigo_bd.bind('<Double-1>', self.read_barcode)
		# self.etiqueta(self.ventana_alimbd, 'Nombre', 20, 55)
		# self.producto_bd = self.caja_texto(self.ventana_alimbd, 1.4, 35, 140, 57)
		# self.agrega_boton(self.ventana_alimbd, 'Registrar', 50, 250, self.registra_bd, pad=(3,3)) # 
		# self.agrega_boton(self.ventana_alimbd, 'Borrar', 180, 250, self.alimbd_del, pad=(3,3)) #
		# self.final_otra_ventana(self.ventana_alimbd, self.ventana_prod)

		self.ventana_alimbd = self.otra_ventana(self.ventana_prod, '+250+220', u'Alimentar Base de Datos', 0, 3, exitgrid=True)
		self.etiqueta(self.ventana_alimbd, 'Cod. Barras', 0, 0, grid=True)
		self.codigo_bd = self.caja_texto(self.ventana_alimbd, 1.4, 35, 1, 0, grid=True)
		self.codigo_bd.grid(columnspan=2)
		#self.codigo_bd.bind('<Double-1>', self.read_barcode)
		self.etiqueta(self.ventana_alimbd, 'Nombre', 0, 1, grid=True)
		self.producto_bd = self.caja_texto(self.ventana_alimbd, 1.4, 35, 1, 1, grid=True)
		self.producto_bd.grid(columnspan=2)
		##### Radio button
		#self.etiqueta(self.ventana_alimbd, 'Requiere IMEI?', 0, 2, grid=True)
		#self.RB = IntVar()
		#self.RB.set(0)
		#RB1 = Radiobutton(self.ventana_alimbd, text=u'Sí', variable=self.RB, value=1)
		#RB2 = Radiobutton(self.ventana_alimbd, text=u'No', variable=self.RB, value=0)
		#RB1.grid(row=2, column=1)
		#RB2.grid(row=2, column=2)
		#################
		self.agrega_boton(self.ventana_alimbd, 'Registrar', 1, 3, self.registra_bd, pad=(3,3), grid=True) # 
		self.agrega_boton(self.ventana_alimbd, 'Borrar', 2, 3, self.alimbd_del, pad=(3,3), grid=True) #
		self.final_otra_ventana(self.ventana_alimbd, self.ventana_prod)

	def registra_bd(self):

		barcode     = self.codigo_bd.get(1.0, "end-1c")
		nombre_prod = self.producto_bd.get(1.0, "end-1c")

		if barcode == '' or nombre_prod == '':

			# ventana de notificacion de que el código de barras o el nombre no fue escrito
			self.notifica_new_product = self.otra_ventana(self.ventana_alimbd, '500x100+300+270', u'Notificacion nuevo producto', 180, 65)
			self.etiqueta(self.notifica_new_product, u'Código de barras y Nombre deben ser escritos', 45, 20)
			self.final_otra_ventana(self.notifica_new_product, self.ventana_alimbd)

		elif barcode.isdigit() == False:

			# ventana de notificacion de que el código de barras tiene caracteres alfabéticos o caracteres especiales
			self.notifica_new_product = self.otra_ventana(self.ventana_alimbd, '550x100+300+270', u'Notificacion nuevo producto', 250, 65)
			self.etiqueta(self.notifica_new_product, u'Código de barras con caracteres no válidos. Corregir', 45, 20)
			self.final_otra_ventana(self.notifica_new_product, self.ventana_alimbd)

		else:
		
			try:

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				#db_cursor.execute("INSERT INTO productos (codigo_barras, nombre_producto, tiene_imei) VALUES (" + barcode + ", '" + nombre_prod + "', " + str(self.RB.get()) + ");")
				db_cursor.execute("INSERT INTO productos (codigo_barras, nombre_producto, tiene_imei) VALUES (" + barcode + ", '" + nombre_prod + "', 0);")
				db_cursor.close()
				db_conn.commit ()
				db_conn.close ()

				# ventana de notificacion de que el nuevo producto ha sido introducido exitosamente a la base de datos
				self.notifica_new_product = self.otra_ventana(self.ventana_alimbd, '450x100+300+270', u'Notificacion nuevo producto', 180, 65)
				self.etiqueta(self.notifica_new_product, 'Nuevo item registrado exitosamente', 45, 20)
				self.final_otra_ventana(self.notifica_new_product, self.ventana_alimbd)

				self.alimbd_del()

			except MySQLdb.IntegrityError as e: 
				
				print(format(e))
				
				if format(e).find("Duplicate entry") != -1 and format(e).find(barcode) != -1: # si es igual a -1 el metodo find no halló nada
					
					print('El codigo de barras ya existe en base de datos')

					# ventana de notificacion de que el nuevo producto no pudo ser introducido exitosamente a la base de datos ya que el código de barras ya existe
					self.notifica_new_product = self.otra_ventana(self.ventana_alimbd, '480x150+300+270', u'Notificacion nuevo producto', 190, 100)
					self.etiqueta(self.notifica_new_product, '¡¡¡ERROR!!!', 180, 10)
					self.etiqueta(self.notifica_new_product, 'El codigo de barras ya existe en base de datos', 25, 40)
					self.final_otra_ventana(self.notifica_new_product, self.ventana_alimbd)
			
				elif format(e).find("Duplicate entry") != -1 and format(e).find(nombre_prod) != -1: # si es igual a -1 el metodo find no halló nada

					print('El nombre ya existe en base de datos')

					# ventana de notificacion de que el nuevo producto no pudo ser introducido exitosamente a la base de datos ya que el nombre ya existe
					self.notifica_new_product = self.otra_ventana(self.ventana_alimbd, '450x150+300+270', u'Notificacion nuevo producto', 190, 100)
					self.etiqueta(self.notifica_new_product, '¡¡¡ERROR!!!', 180, 10)
					self.etiqueta(self.notifica_new_product, 'El nombre ya existe en base de datos', 25, 40)
					self.final_otra_ventana(self.notifica_new_product, self.ventana_alimbd)

	# funcion para borrar los campos que se han introducido en el formulario para alimentar la bd de vendedores

	def alimbd_del(self):

		self.codigo_bd.delete('1.0', END)
		self.producto_bd.delete('1.0', END)
		#self.RB.set(0)

	def busca_item(self):

		self.ventana_busca_disp = self.otra_ventana(self.ventana_prod, '560x180+250+220', u'Buscar Item por código', 370, 90)
		self.etiqueta(self.ventana_busca_disp, u'Cod. Barras', 20, 23)
		self.codbar_busq = self.caja_texto(self.ventana_busca_disp, 1.4, 50, 25, 55)
		self.agrega_boton(self.ventana_busca_disp, 'Buscar', 110, 90, self.search_item, pad=(3,3))
		self.agrega_boton(self.ventana_busca_disp, 'Borrar', 240, 90, self.borra_codbar, pad=(3,3))
		self.final_otra_ventana(self.ventana_busca_disp, self.ventana_prod)

	def search_item(self):

		code = self.codbar_busq.get(1.0, "end-1c")

		if code.isdigit() == True:

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			db_cursor.execute("SELECT codigo_barras, nombre_producto FROM productos WHERE codigo_barras = " + code)
			self.searchprod = db_cursor.fetchall()
			db_conn.close ()

			codigo_barras = '' 

			for i in range(len(self.searchprod)):

				codigo_barras += str(self.searchprod[i][0]) + '\n'

			if codigo_barras == '':

				# ventana de notificacion que dice que no hay registros con dicho código de barras
				self.notifica = self.otra_ventana(self.ventana_busca_disp, '450x100+300+270', u'Notificacion búsqueda', 180, 65)
				self.etiqueta(self.notifica, u'Código no hallado', 150, 20)
				self.final_otra_ventana(self.notifica, self.ventana_busca_disp)

			else:

				#self.ventana_searchitem_x_codigo_r = self.otra_ventana(self.ventana_busca_disp, '550x150+300+270', u'Buscar Item por código', 300, 100)
				self.ventana_searchitem_x_codigo_r = self.otra_ventana(self.ventana_busca_disp, '+300+270', u'Buscar Item por código', 300, 100)

				# create the tree and scrollbars
				self.dataCols = (u'code', 'name')
				self.tree = ttk.Treeview(self.ventana_searchitem_x_codigo_r, columns=self.dataCols)

				ysb = ttk.Scrollbar(self.ventana_searchitem_x_codigo_r, orient=VERTICAL, command= self.tree.yview)
				self.tree['yscroll'] = ysb.set

				# setup column headings
				self.tree.heading('#0',   text='')
				self.tree.heading('code', text=u'Código', anchor=W)
				self.tree.heading('name', text='Nombre', anchor=W)

				self.tree.column('#0',   stretch=1, width=0, anchor=W)
				self.tree.column('code', stretch=1, width=200, anchor=W)
				self.tree.column('name', stretch=1, width=250, anchor=W)

				# add tree and scrollbars to frame
				self.tree.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
				ysb.grid(row=0, column=1, sticky=NS)

				# set frame resizing priorities
				self.ventana_searchitem_x_codigo_r.rowconfigure(0, weight=1)
				self.ventana_searchitem_x_codigo_r.columnconfigure(0, weight=1)

				for i in range(len(self.searchprod)):

					codigo_barras = self.searchprod[i][0]
					nombre_produc = self.searchprod[i][1]

					VALUES        = (codigo_barras, nombre_produc) 

					self.tree.insert('', END, text='', values=VALUES, iid=i)

				remove_record = ttk.Button(self.ventana_searchitem_x_codigo_r, text='Eliminar Items Seleccionadas', padding=(3,3), command=self.delete_item)
				remove_record.grid(row=1, column=0, pady=20)

				cierra = ttk.Button(self.ventana_searchitem_x_codigo_r, text='Salir', padding=(3,3), command=self.ventana_searchitem_x_codigo_r.destroy)
				cierra.grid(row=2, column=0, pady=10)

				self.final_otra_ventana(self.ventana_searchitem_x_codigo_r, self.ventana_busca_disp)

		else:

			# ventana de notificacion que dice que no se ha introducido un valor correcto de cédula
			self.notifica = self.otra_ventana(self.ventana_busca_disp, '450x150+300+270', u'Notificacion búsqueda', 180, 115)
			self.etiqueta(self.notifica, u'Valor de código con caracteres inválidos', 45, 20)
			self.etiqueta(self.notifica, "'" + code + "'", 150, 50)
			self.final_otra_ventana(self.notifica, self.ventana_busca_disp)

	def delete_item(self):

		if len(self.tree.selection()) != 0:

			# ventana de notificacion de eliminacion exitosa del item de la base de datos
			self.notifica = self.otra_ventana(self.ventana_searchitem_x_codigo_r, '450x100+350+320', u'Notificacion Item', 180, 65, textsalir='Cancelar')
			self.etiqueta(self.notifica, u'¿Está seguro de eliminar el Item?', 45, 20)
			self.agrega_boton(self.notifica, 'Confirmar', 300, 65, self.delete_item2, pad=(3,3))
			self.final_otra_ventana(self.notifica, self.ventana_searchitem_x_codigo_r)

		else:

			# ventana de notificacion de eliminacion exitosa del item de la base de datos
			self.notifica = self.otra_ventana(self.ventana_searchitem_x_codigo_r, '450x100+350+320', u'Notificacion Item', 180, 65)
			self.etiqueta(self.notifica, u'No se seleccionó ningún Item', 45, 20)
			self.final_otra_ventana(self.notifica, self.ventana_searchitem_x_codigo_r)

	def delete_item2(self):

		self.notifica.destroy()

		for i in self.tree.selection()[:]:

			codigo_barras     = self.searchprod[int(i)][0]

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			db_cursor.execute("DELETE FROM productos WHERE codigo_barras = " + str(codigo_barras) + ";")
			db_cursor.close()
			db_conn.commit ()
			db_conn.close ()

		# ventana de notificacion de eliminacion exitosa del item de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searchitem_x_codigo_r, '450x100+350+320', u'Notificacion Item', 180, 65)
		self.etiqueta(self.notifica, u'Item eliminado de la base de datos', 45, 20)
		self.final_otra_ventana(self.notifica, self.ventana_searchitem_x_codigo_r)

		self.ventana_searchitem_x_codigo_r.destroy()
		self.borra_codbar()

	def borra_codbar(self):

		self.codbar_busq.delete('1.0', END)




	#---------------------------------------------------------------------------------------------
	#-------------------------------- Ventana de opciones de existencias -------------------------
	#---------------------------------------------------------------------------------------------

	def existencias(self):

		self.ventana_exist = self.otra_ventana(self.ventana_stock, '+200+170', 'Opciones Existencias', 0, 2, exitgrid=True)
		self.agrega_boton(self.ventana_exist, u'Alimentar Existencias', 0, 0, self.credito_contado, grid=True)
		self.agrega_boton(self.ventana_exist, u'Buscar Existencias En Stock'   , 0, 1, self.busca_exist, grid=True)
		self.final_otra_ventana(self.ventana_exist, self.ventana_stock)

	# ventana de buscar existencias

	def busca_exist(self):

		self.ventana_busca_disp = self.otra_ventana(self.ventana_exist, '+250+220', u'Buscar Existencia en Stock', 1, 11, exitgrid=True)
		self.etiqueta(self.ventana_busca_disp, u'Cod. Barras ó Nombre del producto', 0, 0, grid=True)
		self.box_codname = self.caja_texto(self.ventana_busca_disp, 1.4, 50, 1, 0, grid=True)

		#------------------------------------- Crea las tablas -------------------------------------------
		self.dataCols  = ('code', 'name', 'amount')
		self.tree = ttk.Treeview(self.ventana_busca_disp, columns=self.dataCols)

		ysb = ttk.Scrollbar(self.ventana_busca_disp, orient=VERTICAL, command= self.tree.yview)
		self.tree['yscroll'] = ysb.set

		# setup column headings
		self.tree.heading('#0',   text='')
		self.tree.heading('code', text=u'Código', anchor=W)
		self.tree.heading('name', text='Nombre', anchor=W)
		self.tree.heading('amount', text='Disponibles', anchor=W)

		self.tree.column('#0',   stretch=1, width=0, anchor=W)
		self.tree.column('code', stretch=1, width=200, anchor=W)
		self.tree.column('name', stretch=1, width=250, anchor=W)
		self.tree.column('amount', stretch=1, width=100, anchor=W)

		# add tree and scrollbars to frame
		self.tree.grid(row=1, column=0, columnspan=2, rowspan=10, sticky=NSEW, padx=10, pady=10)

		ysb.grid(row=1, column=2, rowspan=10, sticky=NS, pady=10)

		# set frame resizing priorities
		self.ventana_busca_disp.rowconfigure(0, weight=1)
		self.ventana_busca_disp.columnconfigure(0, weight=1)

		#------------------ consulta2 nombres y codigos de barra y los pone en la tabla de disponibles --------------------------

		self.consulta()

		# Llama el método update_tree para poner los datos iniciales
		self.update_tree()

		# si se escribe algo en la caja, que se actualice la tabla
		self.box_codname.bind("<KeyRelease>", self.check)

		#----------------------- Agrega botones --------------------------

		boton_buscar = self.agrega_boton(self.ventana_busca_disp, 'Buscar', 0, 11, self.verify_busca_stock, pad=(3,3), grid=True)

		self.final_otra_ventana(self.ventana_busca_disp, self.ventana_exist)

	def verify_busca_stock(self):

		if len(self.tree.selection()) == 0:

			# ventana de notificacion de eliminacion de que no se seleccionó ningún producto
			self.notifica = self.otra_ventana(self.ventana_busca_disp, '+350+320', u'Notificacion Busqueda en Stock', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'No se seleccionó ningún producto', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_busca_disp)

		elif len(self.tree.selection()) == 1:

			self.search_exist()

		elif len(self.tree.selection()) >= 2:

			# ventana de notificacion de que se seleccionaron más de un producto
			self.notifica = self.otra_ventana(self.ventana_busca_disp, '+350+320', u'Notificacion Busqueda en Stock', 0, 3, exitgrid=True, textsalir='Cancelar')
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Por favor seleccione un sólo producto', 0, 1, grid=True)
			self.etiqueta(self.notifica, u'Se seleccionaron dos o más productos', 0, 2, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_busca_disp)

	def search_exist(self):

		# agregar a la caja lo que se seleccionó
		selected = self.tree.focus()
		values   = self.tree.item(selected, 'values')

		code = values[0]

		print(code)

		#if code.isdigit() == True:

		db_conn         = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor       = db_conn.cursor()
		db_cursor.execute("SELECT productos.codigo_barras, productos.nombre_producto, stocks.valor_compra, stocks.precio_venta, stocks.precio_minimo_venta, stocks.proveedor, stocks.id_factura, stocks.adquisicion, stocks.fecha_entrada, stocks.id FROM stocks INNER JOIN productos ON productos.codigo_barras = stocks.codigo_barras_id WHERE productos.codigo_barras = " + code + " AND estado = 'En Stock';")
		self.searchprod = db_cursor.fetchall()
		db_conn.close ()

		if len(self.searchprod) == 0:

			# ventana de notificacion que dice que no hay registros con dicho código de barras
			self.notifica = self.otra_ventana(self.ventana_busca_disp, '+300+270', u'Notificacion Existencia en Stock', 0, 1, exitgrid=True)
			self.etiqueta(self.notifica, u'El producto seleccionado no tiene productos disponibles', 0, 0, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_busca_disp)

		else:

			self.ventana_searchexist_x_codigo_r = self.otra_ventana(self.ventana_busca_disp, '+300+270', u'Notificación Existencia en Stock', 390, 100) # '1200x150+300+270'

			# create the tree and scrollbars
			self.dataCols = (u'code', 'name', 'v_compra', 'p_venta', 'p_minimo', 'provee', 'id_factura', 'adquisi', 'fecha')
			self.tree2 = ttk.Treeview(self.ventana_searchexist_x_codigo_r, columns=self.dataCols)

			ysb = ttk.Scrollbar(self.ventana_searchexist_x_codigo_r, orient=VERTICAL, command= self.tree2.yview)
			self.tree2['yscroll'] = ysb.set

			# setup column headings
			self.tree2.heading('#0'        , text='')
			self.tree2.heading('code'      , text='Codigo', anchor=W)
			self.tree2.heading('name'      , text='Nombre', anchor=W)
			self.tree2.heading('v_compra'  , text='Valor Compra', anchor=W)
			self.tree2.heading('p_venta'   , text='Precio Venta', anchor=W)
			self.tree2.heading('p_minimo'  , text='Precio Min.', anchor=W)
			self.tree2.heading('provee'    , text='Proveedor', anchor=W)
			self.tree2.heading('id_factura', text='Id. Factura', anchor=W)
			self.tree2.heading('adquisi'   , text='Adquisición', anchor=W)
			self.tree2.heading('fecha'     , text='Fecha Entrada', anchor=W)


			self.tree2.column('#0'        , stretch=1, width=0, anchor=W)
			self.tree2.column('code'      , stretch=1, width=150, anchor=W)
			self.tree2.column('name'      , stretch=1, width=250, anchor=W)
			self.tree2.column('v_compra'  , stretch=1, width=150, anchor=W)
			self.tree2.column('p_venta'   , stretch=1, width=150, anchor=W)
			self.tree2.column('p_minimo'  , stretch=1, width=150, anchor=W)
			self.tree2.column('provee'    , stretch=1, width=200, anchor=W)
			self.tree2.column('id_factura', stretch=1, width=150, anchor=W)
			self.tree2.column('adquisi'   , stretch=1, width=120, anchor=W)
			self.tree2.column('fecha'     , stretch=1, width=230, anchor=W)

			# add tree2 and scrollbars to frame
			self.tree2.grid(row=0, column=0, sticky=NSEW, pady=10, padx=10)
			ysb.grid(row=0, column=1, sticky=NS)

			# set frame resizing priorities
			self.ventana_searchexist_x_codigo_r.rowconfigure(0, weight=1)
			self.ventana_searchexist_x_codigo_r.columnconfigure(0, weight=1)

			#self.agrega_boton(self.ventana_searchexist_x_codigo_r, u'Eliminar Existencia', 200, 100, self.delete_existencia, pad=(3,3))

			for i in range(len(self.searchprod)):

				codigo_barras = self.searchprod[i][0]
				nombre_produc = self.searchprod[i][1]
				valor_produc  = self.searchprod[i][2]
				precio_produc = self.searchprod[i][3]
				precio_min    = self.searchprod[i][4]
				provee        = self.searchprod[i][5]
				id_factura    = self.searchprod[i][6]
				adquisi       = self.searchprod[i][7]
				fecha_entra   = self.searchprod[i][8]

				VALUES        = (codigo_barras, nombre_produc, valor_produc, precio_produc, precio_min, provee, id_factura, adquisi, fecha_entra) 

				self.tree2.insert('', END, text='', values=VALUES, iid=i)

			remove_record = ttk.Button(self.ventana_searchexist_x_codigo_r, text='Eliminar Existencias Seleccionadas', padding=(3,3), command=self.delete_existencia)
			remove_record.grid(row=1, column=0, pady=20)

			cierra = ttk.Button(self.ventana_searchexist_x_codigo_r, text='Salir', padding=(3,3), command=self.ventana_searchexist_x_codigo_r.destroy)
			cierra.grid(row=2, column=0, pady=10)

			self.final_otra_ventana(self.ventana_searchexist_x_codigo_r, self.ventana_busca_disp)

		# else:

		# 	# ventana de notificacion que dice que no se ha introducido un valor correcto de cédula
		# 	self.notifica = self.otra_ventana(self.ventana_busca_disp, '+300+270', u'Notificacion Existencia', 0, 1, exitgrid=True)
		# 	self.etiqueta(self.notifica, u'Valor de código con caracteres inválidos', 0, 0, grid=True)
		# 	self.etiqueta(self.notifica, "'" + code + "'", 150, 50, grid=True)
		# 	self.final_otra_ventana(self.notifica, self.ventana_busca_disp)

	def delete_existencia(self):

		if len(self.tree2.selection()) != 0:

			# ventana de notificacion de eliminacion exitosa del item de la base de datos
			self.notifica = self.otra_ventana(self.ventana_searchexist_x_codigo_r, '+350+320', u'Notificacion Existencia', 0, 3, exitgrid=True, textsalir='Cancelar')
			self.etiqueta(self.notifica, u'¿Está seguro de eliminar la(s) existencia(s)?', 0, 1, grid=True)
			self.agrega_boton(self.notifica, 'Confirmar', 0, 2, self.delete_existencia2, pad=(3,3), grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_searchexist_x_codigo_r)

		else:

			# ventana de notificacion de eliminacion exitosa del item de la base de datos
			self.notifica = self.otra_ventana(self.ventana_searchexist_x_codigo_r, '+350+320', u'Notificacion Existencia', 0, 1, exitgrid=True)
			self.etiqueta(self.notifica, u'No se seleccionó ninguna existencia.', 0, 0, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_searchexist_x_codigo_r)

	def delete_existencia2(self):

		self.notifica.destroy()

		for i in self.tree2.selection()[:]:

			ID         = self.searchprod[int(i)][9]

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			db_cursor.execute("DELETE FROM stocks WHERE id = " + str(ID) + ";")
			db_cursor.close()
			db_conn.commit ()
			db_conn.close ()

		# ventana de notificacion de eliminacion exitosa de la existencia de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searchexist_x_codigo_r, '+350+320', u'Notificacion Existencia', 0, 1, exitgrid=True)
		self.etiqueta(self.notifica, u'Existencia eliminada de la base de datos', 0, 0, grid=True)
		self.final_otra_ventana(self.notifica, self.ventana_searchexist_x_codigo_r)

		self.ventana_searchexist_x_codigo_r.destroy()

		self.consulta()
		self.update_tree()

	# Ventana de Alimentar existencias

	def credito_contado(self):

		self.ventana_cred_cont = self.otra_ventana(self.ventana_exist, '+250+220', u'Alimentar Existencias', 1, 1, exitgrid=True)
		self.agrega_boton(self.ventana_cred_cont, 'Productos de contado', 0, 0, self.alimentar_stock, padxy=(40,40), grid=True)
		self.agrega_boton(self.ventana_cred_cont, 'Productos a crédito' , 2, 0, self.generar_factura, padxy=(40,40), grid=True)
		self.final_otra_ventana(self.ventana_cred_cont, self.ventana_exist)

	def generar_factura(self):

		self.ventana_cred_cont.destroy()

		self.ventana_alimstock = self.otra_ventana(self.ventana_exist, '+250+220', u'Alimentar Factura', 4, 18, 'Cancelar', exitgrid=True)

		#------------------------------------- Crea las cajas de texto para la factura -----------------------------------------------

		self.etiqueta(self.ventana_alimstock, u'Fecha en factura [Año-mes-dia]', 0, 0, grid=True)
		self.fecha_factura = self.caja_texto(self.ventana_alimstock, 1.4, 25, 1, 0, grid=True)
		self.fecha_factura.grid(columnspan=2)
		self.etiqueta(self.ventana_alimstock, u'Valor factura', 0, 1, grid=True)
		self.valor_factura = self.caja_texto(self.ventana_alimstock, 1.4, 25, 1, 1, grid=True)
		self.valor_factura.grid(columnspan=2)
		self.etiqueta(self.ventana_alimstock, u'Proveedor', 0, 2, grid=True)
		self.proveedor_factura = self.caja_texto(self.ventana_alimstock, 1.4, 25, 1, 2, grid=True)
		self.proveedor_factura.grid(columnspan=2)
		self.etiqueta(self.ventana_alimstock, u'Código factura', 0, 3, grid=True)
		self.codigo_factura = self.caja_texto(self.ventana_alimstock, 1.4, 25, 1, 3, grid=True)
		self.codigo_factura.grid(columnspan=2)

		#------------------------------------- Crea las cajas de texto para la alimentar las existencias -----------------------------------------------

		self.etiqueta(self.ventana_alimstock, u'Cód. Barras', 5, 0, grid=True)
		self.codigo_stock = self.caja_texto(self.ventana_alimstock, 1.4, 25, 6, 0, grid=True)
		self.codigo_stock.grid(columnspan=2)
		self.etiqueta(self.ventana_alimstock, u'Valor de compra/unidad', 5, 1, grid=True)
		self.valor_compra_stock = self.caja_texto(self.ventana_alimstock, 1.4, 25, 6, 1, grid=True)
		self.valor_compra_stock.grid(columnspan=2)
		self.etiqueta(self.ventana_alimstock, u'Cantidad', 5, 2, grid=True)
		self.cantidad_entra_stock = self.caja_texto(self.ventana_alimstock, 1.4, 25, 6, 2, grid=True)
		self.cantidad_entra_stock.grid(columnspan=2)

		self.conteo = 0

		#------------------------------------- Crea las caja para el total -----------------------------------------------

		self.etiqueta(self.ventana_alimstock, u'Total', 6, 15, grid=True)
		self.box_total = self.caja_texto(self.ventana_alimstock, 1.4, 25, 7, 15, grid=True)
		#self.codigo_stock.grid(columnspan=2)

		#------------------------------------- Crea la tabla de proveedores -------------------------------------------
		dataCols  = ('name_proveedor')
		dataCols2 = ('name_prod', 'cod_barras', 'valor_compra', 'cantidad', 'precio_venta', 'subtotal')

		self.tree = ttk.Treeview(self.ventana_alimstock, columns=dataCols)
		self.tree2= ttk.Treeview(self.ventana_alimstock, columns=dataCols2)

		ysb = ttk.Scrollbar(self.ventana_alimstock, orient=VERTICAL, command= self.tree.yview)
		ysb2 = ttk.Scrollbar(self.ventana_alimstock, orient=VERTICAL, command= self.tree2.yview)

		self.tree['yscroll'] = ysb.set
		self.tree2['yscroll'] = ysb2.set

		# setup column headings
		self.tree.heading('#0',   text='')
		self.tree.heading('name_proveedor', text='Nombre Proveedor', anchor=W)

		self.tree2.heading('#0',   text='')
		self.tree2.heading('name_prod', text='Producto', anchor=W)
		self.tree2.heading('cod_barras', text='Cod. Barras', anchor=W)
		self.tree2.heading('valor_compra', text='Valor de compra/unidad', anchor=W)
		self.tree2.heading('cantidad', text='Cantidad', anchor=W)
		self.tree2.heading('precio_venta', text='Precio venta', anchor=W)
		self.tree2.heading('subtotal', text='Subtotal', anchor=W)

		self.tree.column('#0'            , stretch=1, width=0, anchor=W)
		self.tree.column('name_proveedor', stretch=1, width=600, anchor=W)

		self.tree2.column('#0'          , stretch=1, width=0, anchor=W)
		self.tree2.column('name_prod'  , stretch=1, width=200, anchor=W)
		self.tree2.column('cod_barras'  , stretch=1, width=180, anchor=W)
		self.tree2.column('valor_compra', stretch=1, width=180, anchor=W)
		self.tree2.column('cantidad'    , stretch=1, width=80, anchor=W)
		self.tree2.column('precio_venta', stretch=1, width=150, anchor=W)
		self.tree2.column('subtotal'    , stretch=1, width=120, anchor=W)


		# add tree and scrollbars to frame
		self.tree.grid(row=5, column=0, columnspan=3, rowspan=10, sticky=NSEW, padx=10, pady=10)
		self.tree2.grid(row=5, column=5, columnspan=3, rowspan=10, sticky=NSEW, padx=10, pady=10)

		ysb.grid(row=5, column=3, rowspan=10, sticky=NS, pady=10)
		ysb2.grid(row=5, column=8, rowspan=10, sticky=NS, pady=10)

		#lineas separadoras
		linea_separ1 = ttk.Separator(self.ventana_alimstock, orient=VERTICAL)
		linea_separ1.grid(row=0, column=4, rowspan=16, sticky=NS, padx=10, pady=10)
		linea_separ2 = ttk.Separator(self.ventana_alimstock, orient=HORIZONTAL)
		linea_separ2.grid(row=4, column=5, columnspan=3, sticky=EW, padx=10, pady=30)
		linea_separ3 = ttk.Separator(self.ventana_alimstock, orient=HORIZONTAL)
		linea_separ3.grid(row=16, column=0, columnspan=8, sticky=EW, padx=10, pady=30)

		# set frame resizing priorities
		self.ventana_alimstock.rowconfigure(0, weight=1)
		self.ventana_alimstock.columnconfigure(0, weight=1)

		#------------------ consulta proveedores --------------------------

		self.consulta_proveedor()

		# Llama el método update_tree para poner los datos de proveedores
		self.update_tabla_proveedor()

		# Click en uno de los registros de la tabla
		self.tree.bind("<Double-1>", self.select_proveedor)

		# si se escribe algo en la caja, que se actualice la tabla
		self.proveedor_factura.bind("<KeyRelease>", self.check_proveedor)

		#------------------------------------ botones ------------------------------

		self.agrega_boton(self.ventana_alimstock, 'Ingresar Factura', 4, 17, self.verifica_factura, pad=(3,3), grid=True) 
		boton_borra_datos_factura = self.agrega_boton(self.ventana_alimstock, 'Borrar Datos Factura', 0, 15, self.delete_factura, pad=(3,3), grid=True)
		boton_borra_datos_factura.grid(columnspan=3)
		boton_codigo_aleatorio = self.agrega_boton(self.ventana_alimstock, 'Generar Código de Factura', 1, 4, self.generar_codigo_factura, pad=(3,3), grid=True)
		boton_codigo_aleatorio.grid(columnspan=2)
		boton_agrega_prod = self.agrega_boton(self.ventana_alimstock, 'Agregar producto', 6, 3, self.agrega_producto, pad=(3,3), grid=True)
		boton_agrega_prod.grid(columnspan=2)
		self.agrega_boton(self.ventana_alimstock, 'Borrar escrito', 5, 3, self.delete_productos_factura, pad=(3,3), grid=True)
		self.agrega_boton(self.ventana_alimstock, 'Quitar producto', 5, 15, self.quitar_productos, pad=(3,3), grid=True)

		self.final_otra_ventana(self.ventana_alimstock, self.ventana_exist)

	def quitar_productos(self):

		if len(self.tree2.selection()[:]) != 0:

			for x in self.tree2.selection()[:]:
				self.tree2.delete(x)

			self.calcula_prod_factura()

		else:

			# ventana de notificacion de que se debe seleccionar algún producto para quitarlo de la canasta
			self.notifica_retiro = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificación Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica_retiro, u'!!!NO SE HAN SELECCIONADO PRODUCTOS DE LA CANASTA!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica_retiro, 'Seleccionar producto a retirar de la canasta', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica_retiro, self.ventana_alimstock, wait=True)

	def agrega_producto(self):

		barcode           = self.codigo_stock.get(1.0, "end-1c")
		precio            = self.valor_compra_stock.get(1.0, "end-1c")
		amount            = self.cantidad_entra_stock.get(1.0, "end-1c")

		if barcode == '':

			# ventana de notificacion de que el barcode está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Código de barras vacío. Campo requerido', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif barcode.isdigit() == False: # si no fuera digito la consulta en base de datos no se podría hacer y tampoco se dejaría ingresar el producto a la bd

			# ventana de notificacion de que el barcode está errado
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Código de barras errado. Caracteres inválidos', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif precio == '':

			# ventana de notificacion de que el precio está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Valor de compra vacío. Campo requerido', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif precio.isdigit() == False:

			# ventana de notificacion de que el precio está errado
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Valor de compra errado. Caracteres inválidos', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif amount == '':

			# ventana de notificacion de que la cantidad está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Cantidad vacía. Campo requerido', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif amount.isdigit() == False:

			# ventana de notificacion de que la cantidad está errado
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Cantidad errada. Caracteres inválidos', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		else:

			#----------------------- decide si el producto cuyo código de barras fue ingresado existe o no -------------------------

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			db_cursor.execute("SELECT nombre_producto FROM productos WHERE codigo_barras = " + barcode + ";")
			decide_existencia = db_cursor.fetchall()
			db_conn.close ()

			item_existe = False

			if len(decide_existencia) == 1:
				item_existe     = True
				self.nombre_producto = decide_existencia[0][0]

			#------------------------- inserta los datos si el item existe ----------------------------------

			if item_existe == True:

				self.minimum_price_factura()

			else:

				# ventana de notificacion de que el item no existe
				self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 3, exitgrid=True)
				self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica, u'El código de barras ingresado no existe en la base de datos', 0, 1, grid=True)
				self.etiqueta(self.notifica, u'Alimentar primero el item', 0, 2, grid=True)
				self.final_otra_ventana(self.notifica, self.ventana_alimstock)

	def inserta_producto(self):

		barcode = self.codigo_stock.get(1.0, "end-1c")
		precio  = self.valor_compra_stock.get(1.0, "end-1c")
		amount  = self.cantidad_entra_stock.get(1.0, "end-1c")
		valor   = self.precio_venta_stock.get(1.0, "end-1c")

		VALUES  = (self.nombre_producto, barcode, precio, amount, valor, int(precio)*int(amount)) 

		self.tree2.insert('', END, text='', values=VALUES, iid=self.conteo)

		self.ventana_mp.destroy()
		self.calcula_prod_factura()
		self.delete_productos_factura()
		self.conteo = self.conteo + 1

	def minimum_price_factura(self):

		barcode = self.codigo_stock.get(1.0, "end-1c")
		amount  = int(self.cantidad_entra_stock.get(1.0, "end-1c"))
		precio  = int(self.valor_compra_stock.get(1.0, "end-1c"))

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT precio_minimo_venta FROM productos WHERE codigo_barras = " + barcode)
		mp         = db_cursor.fetchall()[0][0]
		db_conn.close ()

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT id FROM stocks WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock'")
		disp       = db_cursor.fetchall()
		db_conn.close ()

		if mp == None:
			self.precio_minimo_stocks = precio
		else:
			self.precio_minimo_stocks = (mp * len(disp) + precio * amount)/(len(disp) + amount)

		self.ventana_mp = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Precio de venta', 1, 5, 'Cancelar', exitgrid=True)
		self.etiqueta(self.ventana_mp, u'Precio mínimo de venta:', 0, 0, grid=True).grid(columnspan=3)
		self.etiqueta(self.ventana_mp, u'$ ' + str(self.precio_minimo_stocks)[:10], 1, 1, grid=True, color='red', weight='bold')
		self.etiqueta(self.ventana_mp, u'Seleccione un precio de venta', 0, 2, grid=True).grid(columnspan=3)
		self.precio_venta_stock = self.caja_texto(self.ventana_mp, 1.4, 35, 0, 3, grid=True)
		self.precio_venta_stock.grid(columnspan=3)
		self.agrega_boton(self.ventana_mp, 'Validar', 1, 4, self.inserta_producto, grid=True)
		self.final_otra_ventana(self.ventana_mp, self.ventana_alimstock)

	def verifica_factura(self):

		date_bill  = self.fecha_factura.get(1.0, "end-1c")
		value_bill = self.valor_factura.get(1.0, "end-1c")

		try:
			right_date = True
			date_bill    = dt.datetime.strptime(date_bill, '%Y-%m-%d').strftime('%Y-%m-%d')
		except:
			right_date = False

		if date_bill == '':

			# ventana de notificacion de que el barcode está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Código de barras vacío. Campo requerido', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif right_date == False:

			# ventana de notificacion de que el barcode está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Factura', 0, 4, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'La fecha de la factura no tiene el formato adecuado', 0, 1, grid=True)
			self.etiqueta(self.notifica, u'Un ejemplo de fecha válido es:', 0, 2, grid=True)
			self.etiqueta(self.notifica, u'2000-05-31', 0, 3, grid=True, color='red')
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif value_bill == '':

			# ventana de notificacion de que el barcode está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Factura', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Valor de la factura vacío. Campo requerido', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif value_bill.isdigit() == False: # si no fuera digito la consulta en base de datos no se podría hacer y tampoco se dejaría ingresar el producto a la bd

			# ventana de notificacion de que el barcode está errado
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Factura', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Valor de factura errado. Caracteres inválidos.', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif value_bill == '':

			# ventana de notificacion de que el barcode está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Factura', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Proveedor vacío. Campo requerido', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		else:

			self.coinciden_totales()

	def verifica_codigo_factura(self):

		code_bill = self.codigo_factura.get(1.0, "end-1c")

		db_conn     = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor   = db_conn.cursor()
		db_cursor.execute("SELECT id_factura_credito FROM adquisiciones_credito")
		id_facturas = db_cursor.fetchall()
		db_conn.close()

		id_facturas = np.array([fct[0] for fct in id_facturas])

		if len(id_facturas) == 0:
			self.registra_factura()
		if np.any(id_facturas == code_bill) == True:
			# ventana de notificacion de que el id de la factura ya existe en base de datos
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificación Factura', 0, 3, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'El código de la factura ya existe en base de datos', 0, 1, grid=True)
			self.etiqueta(self.notifica, u'Por favor rectifique el código o genere uno nuevo.', 0, 2, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)
		else:
			self.registra_factura()

	def coinciden_totales(self):

		total_suma    = int(self.box_total.get(1.0, "end-1c"))
		total_factura = int(self.valor_factura.get(1.0, "end-1c"))

		if total_suma == total_factura:
			self.verifica_codigo_factura()
		else:
			# ventana de notificacion de que el barcode está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificación Factura', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'La cuenta de la factura no coincide con el total de los productos', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

	def registra_factura(self):

		#--------------------------------------- primero registra la factura -------------------------------------------

		date_bill    = self.fecha_factura.get(1.0, "end-1c")
		date_bill    = dt.datetime.strptime(date_bill, '%Y-%m-%d').strftime('%Y-%m-%d')
		current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		valor_bill   = self.valor_factura.get(1.0, "end-1c")
		provee_bill  = self.proveedor_factura.get(1.0, "end-1c")
		code_bill    = self.codigo_factura.get(1.0, "end-1c")

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("INSERT INTO adquisiciones_credito (id_factura_credito, valor_factura, fecha_factura, fecha_ingreso_factura, pagada, proveedor) VALUES ('" + code_bill + "', " + valor_bill + ", '" + date_bill + "', '" + current_time + "', 0, '" + provee_bill + "');")
		db_cursor.close()
		db_conn.commit ()
		db_conn.close ()

		#--------------------------------------- luego registra los productos -------------------------------------------

		for record in self.tree2.get_children(): # recorre cada entrada de la tabla 2
			barcode       = self.tree2.item(record, 'values')[1]
			precio        = self.tree2.item(record, 'values')[2]
			amount        = self.tree2.item(record, 'values')[3]
			costo         = self.tree2.item(record, 'values')[4]
			precio_minimo = str(self.precio_minimo_stocks)
			state         = 'En Stock'

			for i in range(int(amount)):
				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("INSERT INTO stocks (codigo_barras_id, fecha_entrada, valor_compra, estado, proveedor, precio_venta, adquisicion, precio_minimo_venta, id_factura) VALUES (" + barcode + ", '" + current_time + "', " + precio + ", '" + state + "', '" + provee_bill + "', " + costo + ", 'credito', " + precio_minimo + ", '" + code_bill + "');")
				db_cursor.execute("UPDATE stocks SET precio_venta = " + costo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
				db_cursor.execute("UPDATE stocks SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
				db_cursor.execute("UPDATE productos SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras = " + barcode + ";")
				db_cursor.close()
				db_conn.commit ()
				db_conn.close ()

		self.delete_productos_factura()
		self.delete_factura()
		self.consulta_proveedor()
		self.update_tabla_proveedor()
		### elimina registros de la tabla
		for record in self.tree2.get_children():
			self.tree2.delete(record)
		self.box_total.delete('1.0', END)

		# ventana de notificacion de que la factura se ingresó exitosamente
		self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificación Factura', 0, 2, exitgrid=True)
		self.etiqueta(self.notifica, 'Factura exitosa', 0, 0, grid=True)
		self.etiqueta(self.notifica, u'Su factura fue ingresada exitosamente', 0, 1, grid=True)
		self.final_otra_ventana(self.notifica, self.ventana_alimstock)


	def check_proveedor(self, e):

		typed = self.proveedor_factura.get(1.0, "end-1c")

		if typed == '':

			names_provee = self.proveedores_disponibles

		else:

			names_provee = []

			for i, item in enumerate(self.proveedores_disponibles):

				matched_list          = [character in item for character in typed]
				string_contains_chars = all(matched_list)

				if string_contains_chars == True:

					names_provee.append(self.proveedores_disponibles[i])

		self.proveedores_disponibles_update = names_provee

		self.update_tabla_proveedor()

	def select_proveedor(self, e):

		#----------------------- proveedor seleccionado ------------------------------------------------------
		selected    = self.tree.focus()
		values      = self.tree.item(selected, 'values')
		name_provee = values[0]

		#----------------------- pone el nombre del proveedor seleccionado en la caja ------------------------
		self.proveedor_factura.delete('1.0', END)
		self.proveedor_factura.insert("1.0", name_provee)

	def update_tabla_proveedor(self):

		### elimina registros de la tabla
		for record in self.tree.get_children():
			self.tree.delete(record)

		# introduce los datos a la tabla
		for i in range(len(self.proveedores_disponibles_update)):
			nombre_provee = self.proveedores_disponibles_update[i]
			VALUES        = (nombre_provee)
			self.tree.insert('', END, text='', values=VALUES, iid=i)

	def consulta_proveedor(self):

		# ----------------- consulta proveedores en la tabla adquisiciones credito ---------------------
		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT proveedor FROM adquisiciones_credito;")
		list_proveedores1 = db_cursor.fetchall()
		db_conn.close()

		if len(list_proveedores1) == 0:
			provee1 = []
		else:
			provee1 = [p[0] for p in list_proveedores1]

		# ----------------- consulta proveedores en la tabla stocks ---------------------
		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT proveedor FROM stocks WHERE proveedor IS NOT NULL;")
		list_proveedores2 = db_cursor.fetchall()
		db_conn.close()

		if len(list_proveedores2) == 0:
			provee2 = []
		else:
			provee2 = [p[0] for p in list_proveedores2]

		#------------------- junta los proveedores de las dos tablas y descarta los repetidos
		provee = provee1 + provee2
		provee = list(set(provee))

		self.proveedores_disponibles        = np.array(provee)
		self.proveedores_disponibles_update = np.array(provee)

	def generar_codigo_factura(self):

		N = 3

		codigo_aleatorio1 = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(N))
		codigo_aleatorio2 = ''.join(random.SystemRandom().choice(string.digits) for _ in range(N))

		self.codigo_aleatorio = codigo_aleatorio1 + codigo_aleatorio2

		self.codigo_factura.delete('1.0', END)
		self.codigo_factura.insert("1.0", self.codigo_aleatorio)

		# se notifica el código nuevo
		self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Código Factura', 0, 3, exitgrid=True)
		self.etiqueta(self.notifica, '¡¡Su código de factura fue generado!!', 0, 0, grid=True)
		self.etiqueta(self.notifica, u'Por favor adjúntelo a la factura física como sigue', 0, 1, grid=True, color='red')
		self.etiqueta(self.notifica, self.codigo_aleatorio, 0, 2, grid=True, color='blue')
		self.final_otra_ventana(self.notifica, self.ventana_alimstock)

	def delete_factura(self):

		self.proveedor_factura.delete('1.0', END)
		self.valor_factura.delete('1.0', END)
		self.fecha_factura.delete('1.0', END)
		self.codigo_factura.delete('1.0', END)

	def delete_productos_factura(self):

		self.codigo_stock.delete('1.0', END)
		self.valor_compra_stock.delete('1.0', END)
		self.cantidad_entra_stock.delete('1.0', END)

	def calcula_prod_factura(self):

		self.box_total.delete('1.0', END)

		# Calcula el total de la canasta
		total_cobrar = 0
		for record in self.tree2.get_children(): # recorre cada entrada de la tabla 2
			subtotal     = int(self.tree2.item(record, 'values')[5])
			total_cobrar = total_cobrar + subtotal

		self.box_total.delete('1.0', END)
		self.box_total.insert("1.0", total_cobrar)


	def alimentar_stock(self):

		self.ventana_cred_cont.destroy()

		self.ventana_alimstock = self.otra_ventana(self.ventana_exist, '600x300+250+220', u'Alimentar Existencias', 310, 250)
		self.etiqueta(self.ventana_alimstock, 'Cod. Barras', 20, 23)
		self.codigo_stock = self.caja_texto(self.ventana_alimstock, 1.4, 35, 250, 25)
		self.etiqueta(self.ventana_alimstock, u'Valor de compra/unidad', 20, 55)
		self.valor_compra_stock = self.caja_texto(self.ventana_alimstock, 1.4, 35, 250, 57)
		#self.etiqueta(self.ventana_alimstock, u'Precio venta', 20, 87)
		#self.precio_venta_stock = self.caja_texto(self.ventana_alimstock, 1.4, 35, 250, 89)
		self.etiqueta(self.ventana_alimstock, u'Cantidad', 20, 87)
		self.cantidad_entra_stock = self.caja_texto(self.ventana_alimstock, 1.4, 35, 250, 89)
		self.etiqueta(self.ventana_alimstock, u'Proveedor', 20, 119)
		self.proveedor_stock = self.caja_texto(self.ventana_alimstock, 1.4, 35, 250, 121)
		self.etiqueta(self.ventana_alimstock, u'(Opcional) IMEI', 20, 151)
		self.imei_entra_stock = self.caja_texto(self.ventana_alimstock, 1.4, 35, 250, 153)
		self.agrega_boton(self.ventana_alimstock, 'Registrar', 50, 250, self.registra_stock, pad=(3,3)) # 
		self.agrega_boton(self.ventana_alimstock, 'Borrar', 180, 250, self.alimstock_del, pad=(3,3)) #
		self.final_otra_ventana(self.ventana_alimstock, self.ventana_exist)

	def registra_stock(self):

		barcode           = self.codigo_stock.get(1.0, "end-1c")
		precio            = self.valor_compra_stock.get(1.0, "end-1c")
		amount            = self.cantidad_entra_stock.get(1.0, "end-1c")
		IMEI              = self.imei_entra_stock.get(1.0, "end-1c")
		PROVEE            = self.proveedor_stock.get(1.0, "end-1c")
		state             = 'En Stock'

		if barcode == '':

			# ventana de notificacion de que el barcode está vacío
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Código de barras vacío. Campo requerido', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif barcode.isdigit() == False: # si no fuera digito la consulta en base de datos no se podría hacer y tampoco se dejaría ingresar el producto a la bd

			# ventana de notificacion de que el barcode está errado
			self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Código de barras errado. Caracteres inválidos', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimstock)

		elif barcode.isdigit() == True: 

			#################### decide si el producto cuyo código de barras fue ingresado existe o no #########################

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			db_cursor.execute("SELECT tiene_imei, nombre_producto FROM productos WHERE codigo_barras = " + barcode + ";")
			decide_existencia = db_cursor.fetchall()
			db_conn.close ()

			item_existe = False

			if len(decide_existencia) >= 1:
				item_existe = True
				tiene_imei  = decide_existencia[0][0]

			####################################################################################################################

			if item_existe == True:

				if precio == '':

					# ventana de notificacion de que el precio está vacío
					self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
					self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
					self.etiqueta(self.notifica, u'Valor de compra vacío. Campo requerido', 0, 1, grid=True)
					self.final_otra_ventana(self.notifica, self.ventana_alimstock)

				elif precio.isdigit() == False:

					# ventana de notificacion de que el precio está errado
					self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
					self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
					self.etiqueta(self.notifica, u'Valor de compra errado. Caracteres inválidos', 0, 1, grid=True)
					self.final_otra_ventana(self.notifica, self.ventana_alimstock)

				elif amount == '':

					# ventana de notificacion de que la cantidad está vacío
					self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
					self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
					self.etiqueta(self.notifica, u'Cantidad vacía. Campo requerido', 0, 1, grid=True)
					self.final_otra_ventana(self.notifica, self.ventana_alimstock)

				elif amount.isdigit() == False:

					# ventana de notificacion de que la cantidad está errado
					self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
					self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
					self.etiqueta(self.notifica, u'Cantidad errada. Caracteres inválidos', 0, 1, grid=True)
					self.final_otra_ventana(self.notifica, self.ventana_alimstock)

				elif tiene_imei == 1:

					if IMEI == '':

						# ventana de notificacion de que la cantidad está errada
						self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
						self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
						self.etiqueta(self.notifica, u'El IMEI de este artículo es requerido', 0, 1, grid=True)
						self.final_otra_ventana(self.notifica, self.ventana_alimstock)

					elif int(amount) >= 2:

						# ventana de notificacion de que la cantidad está errada
						self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
						self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
						self.etiqueta(self.notifica, u'Se están introduciendo ' + amount + u' artículos con el mismo IMEI', 0, 1, grid=True)
						self.final_otra_ventana(self.notifica, self.ventana_alimstock)

					elif PROVEE == '':

						if len(IMEI) == 15:

							if IMEI.isdigit() == True:

								self.imei_bool   = True
								self.provee_bool = False

								self.minimum_price()

							else:

								# ventana de notificacion de que el IMEI tiene caracteres errados
								self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
								self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
								self.etiqueta(self.notifica, u'El IMEI tiene caracteres errados. Sólo dígitos son aceptados.', 0, 1, grid=True)
								self.final_otra_ventana(self.notifica, self.ventana_alimstock)	

						else:

							# ventana de notificacion de que el IMEI no tiene 15 dígitos
							self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
							self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
							self.etiqueta(self.notifica, u'El IMEI no tiene 15 dígitos', 0, 1, grid=True)
							self.final_otra_ventana(self.notifica, self.ventana_alimstock)

					elif PROVEE != '':

						if len(IMEI) == 15:

							if IMEI.isdigit() == True:

								self.imei_bool   = True
								self.provee_bool = True

								self.minimum_price()

							else:

								# ventana de notificacion de que el IMEI tiene caracteres errados
								self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
								self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
								self.etiqueta(self.notifica, u'El IMEI tiene caracteres errados. Sólo dígitos son aceptados.', 0, 1, grid=True)
								self.final_otra_ventana(self.notifica, self.ventana_alimstock)	

						else:

							# ventana de notificacion de que el IMEI no tiene 15 dígitos
							self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
							self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
							self.etiqueta(self.notifica, u'El IMEI no tiene 15 dígitos', 0, 1, grid=True)
							self.final_otra_ventana(self.notifica, self.ventana_alimstock)

				elif tiene_imei == 0:

					if IMEI != '':

						# ventana de notificacion de que el IMEI no es requerido
						self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 2, exitgrid=True)
						self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
						self.etiqueta(self.notifica, u'NO se requiere IMEI en este artículo.', 0, 1, grid=True)
						self.final_otra_ventana(self.notifica, self.ventana_alimstock)

					elif PROVEE == '':

						self.imei_bool   = False
						self.provee_bool = False

						self.minimum_price()


					elif PROVEE != '':

						self.imei_bool   = False
						self.provee_bool = True

						self.minimum_price()

			else:

				# ventana de notificacion de que el item no existe
				self.notifica = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Notificacion Existencias', 0, 3, exitgrid=True)
				self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica, u'El código de barras ingresado no existe en la base de datos', 0, 1, grid=True)
				self.etiqueta(self.notifica, u'Alimentar primero el item', 0, 2, grid=True)
				self.final_otra_ventana(self.notifica, self.ventana_alimstock)

	def minimum_price(self):

		barcode = self.codigo_stock.get(1.0, "end-1c")
		amount  = int(self.cantidad_entra_stock.get(1.0, "end-1c"))
		precio  = int(self.valor_compra_stock.get(1.0, "end-1c"))

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT precio_minimo_venta FROM productos WHERE codigo_barras = " + barcode)
		mp         = db_cursor.fetchall()[0][0]
		db_conn.close ()

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("SELECT id FROM stocks WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock'")
		disp       = db_cursor.fetchall()
		db_conn.close ()

		if mp == None:
			self.precio_minimo_stocks = precio
		else:
			self.precio_minimo_stocks = (mp * len(disp) + precio * amount)/(len(disp) + amount)

		self.ventana_mp = self.otra_ventana(self.ventana_alimstock, '+300+270', u'Precio de venta', 1, 5, 'Cancelar', exitgrid=True)
		self.etiqueta(self.ventana_mp, u'Precio mínimo de venta:', 0, 0, grid=True).grid(columnspan=3)
		self.etiqueta(self.ventana_mp, u'$ ' + str(self.precio_minimo_stocks)[:10], 1, 1, grid=True, color='red', weight='bold')
		self.etiqueta(self.ventana_mp, u'Seleccione un precio de venta', 0, 2, grid=True).grid(columnspan=3)
		self.precio_venta_stock = self.caja_texto(self.ventana_mp, 1.4, 35, 0, 3, grid=True)
		self.precio_venta_stock.grid(columnspan=3)
		self.agrega_boton(self.ventana_mp, 'Validar', 1, 4, self.registra_exist, grid=True)
		self.final_otra_ventana(self.ventana_mp, self.ventana_alimstock)

	def registra_exist(self):

		barcode           = self.codigo_stock.get(1.0, "end-1c")
		precio            = self.valor_compra_stock.get(1.0, "end-1c")
		costo             = self.precio_venta_stock.get(1.0, "end-1c")
		amount            = self.cantidad_entra_stock.get(1.0, "end-1c")
		IMEI              = self.imei_entra_stock.get(1.0, "end-1c")
		PROVEE            = self.proveedor_stock.get(1.0, "end-1c")
		state             = 'En Stock'

		self.current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		self.texto_info = 'Codigo: '             + barcode + '\n'
		self.texto_info+= 'Valor de compra: '    + precio  + '\n'
		self.texto_info+= 'Precio de venta: '    + costo   + '\n'
		self.texto_info+= 'Cantidad: '           + amount  + '\n'
		self.texto_info+= 'IMEI: '               + IMEI    + '\n'
		self.texto_info+= 'Proveedor: '          + PROVEE  + '\n'
		self.texto_info+= 'Fecha: '              + self.current_time

		if costo == '':

			# ventana de notificacion de que el precio está vacío
			self.notifica = self.otra_ventana(self.ventana_mp, '+350+320', u'Notificacion Precio Venta', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Precio de venta vacío. Campo requerido', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_mp)

		elif costo.isdigit() == False:

			# ventana de notificacion de que el precio está errado
			self.notifica = self.otra_ventana(self.ventana_mp, '+350+320', u'Notificacion Precio Venta', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Precio de venta errado. Caracteres inválidos', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_mp)

		elif costo.isdigit() == True:

			self.valida_exist = self.otra_ventana(self.ventana_mp, '+350+320', u'Valida Existencias', 0, 2, 'Cancelar', exitgrid=True)
			box_valida        = self.caja_texto(self.valida_exist, 10, 40, 0, 0, grid=True)
			box_valida.insert("1.0", self.texto_info)
			self.agrega_boton(self.valida_exist, 'Validar Info', 0, 1, self.registra_exist2, pad=(3,3), grid=True)
			self.final_otra_ventana(self.valida_exist, self.ventana_mp)

	def registra_exist2(self):

		barcode           = self.codigo_stock.get(1.0, "end-1c")
		precio            = self.valor_compra_stock.get(1.0, "end-1c")
		costo             = self.precio_venta_stock.get(1.0, "end-1c")
		amount            = self.cantidad_entra_stock.get(1.0, "end-1c")
		IMEI              = self.imei_entra_stock.get(1.0, "end-1c")
		PROVEE            = self.proveedor_stock.get(1.0, "end-1c")
		precio_minimo     = str(self.precio_minimo_stocks)
		state             = 'En Stock'

		try:

			if self.imei_bool == True and self.provee_bool == True:

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("INSERT INTO stocks (codigo_barras_id, fecha_entrada, valor_compra, IMEI, estado, proveedor, precio_venta, adquisicion, precio_minimo_venta) VALUES (" + barcode + ", '" + self.current_time + "', " + precio + ", " + IMEI + ", '" + state + "', '" + PROVEE + "', " + costo + ", 'contado', " + precio_minimo + ");")
				db_cursor.execute("UPDATE stocks SET precio_venta = " + costo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
				db_cursor.execute("UPDATE stocks SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
				db_cursor.execute("UPDATE productos SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras = " + barcode + ";")
				db_cursor.close()
				db_conn.commit ()
				db_conn.close ()

				# ventana de notificacion de que el nuevo producto ha sido introducido exitosamente a la base de datos
				self.notifica_new_product = self.otra_ventana(self.valida_exist, '+400+370', u'Notificacion Existencias', 0, 1, exitgrid=True)
				self.etiqueta(self.notifica_new_product, 'Existencia registrada exitosamente', 0, 0, grid=True)
				self.final_otra_ventana(self.notifica_new_product, self.valida_exist)

			elif self.imei_bool == False and self.provee_bool == False:

				for i in range(int(amount)):

					db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
					db_cursor  = db_conn.cursor()
					db_cursor.execute("INSERT INTO stocks (codigo_barras_id, fecha_entrada, valor_compra, estado, precio_venta, adquisicion, precio_minimo_venta) VALUES (" + barcode + ", '" + self.current_time + "', " + precio + ", '" + state + "', " + costo + ", 'contado', " + precio_minimo + ");")
					db_cursor.execute("UPDATE stocks SET precio_venta = " + costo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
					db_cursor.execute("UPDATE stocks SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
					db_cursor.execute("UPDATE productos SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras = " + barcode + ";")
					db_cursor.close()
					db_conn.commit ()
					db_conn.close ()

				# ventana de notificacion de que el nuevo producto ha sido introducido exitosamente a la base de datos
				self.notifica_new_product = self.otra_ventana(self.valida_exist, '+400+370', u'Notificacion Existencias', 0, 1, exitgrid=True)
				self.etiqueta(self.notifica_new_product, 'Existencia registrada exitosamente', 0, 0, grid=True)
				self.final_otra_ventana(self.notifica_new_product, self.valida_exist)

			elif self.imei_bool == False and self.provee_bool == True:

				for i in range(int(amount)):

					db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
					db_cursor  = db_conn.cursor()
					db_cursor.execute("INSERT INTO stocks (codigo_barras_id, fecha_entrada, valor_compra, estado, proveedor, precio_venta, adquisicion, precio_minimo_venta) VALUES (" + barcode + ", '" + self.current_time + "', " + precio + ", '" + state + "', '" + PROVEE + "', " + costo + ", 'contado', " + precio_minimo + ");")
					db_cursor.execute("UPDATE stocks SET precio_venta = " + costo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
					db_cursor.execute("UPDATE stocks SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
					db_cursor.execute("UPDATE productos SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras = " + barcode + ";")
					db_cursor.close()
					db_conn.commit ()
					db_conn.close ()

				# ventana de notificacion de que el nuevo producto ha sido introducido exitosamente a la base de datos
				self.notifica_new_product = self.otra_ventana(self.valida_exist, '+400+370', u'Notificacion Existencias', 0, 1, exitgrid=True)
				self.etiqueta(self.notifica_new_product, 'Existencia registrada exitosamente', 0, 0, grid=True)
				self.final_otra_ventana(self.notifica_new_product, self.valida_exist)

			elif self.imei_bool == True and self.provee_bool == False:

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("INSERT INTO stocks (codigo_barras_id, fecha_entrada, valor_compra, IMEI, estado, precio_venta, adquisicion, precio_minimo_venta) VALUES (" + barcode + ", '" + self.current_time + "', " + precio + ", " + IMEI + ", '" + state + "', " + costo + ", 'contado', " + precio_minimo + ");")
				db_cursor.execute("UPDATE stocks SET precio_venta = " + costo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
				db_cursor.execute("UPDATE stocks SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras_id = " + barcode + " AND estado = 'En Stock';")
				db_cursor.execute("UPDATE productos SET precio_minimo_venta = " + precio_minimo + " WHERE codigo_barras = " + barcode + ";")
				db_cursor.close()
				db_conn.commit ()
				db_conn.close ()

				# ventana de notificacion de que el nuevo producto ha sido introducido exitosamente a la base de datos
				self.notifica_new_product = self.otra_ventana(self.valida_exist, '+400+370', u'Notificacion Existencias', 0, 1, exitgrid=True)
				self.etiqueta(self.notifica_new_product, 'Existencia registrada exitosamente', 0, 0, grid=True)
				self.final_otra_ventana(self.notifica_new_product, self.valida_exist)

			self.alimstock_del()
			self.ventana_mp.destroy()
			self.valida_exist.destroy()

		except MySQLdb.IntegrityError as e: 
			
			if format(e).find("`inventario`.`stocks`, CONSTRAINT `stocks_productos` FOREIGN KEY (`codigo_barras_id`) REFERENCES `productos` (`codigo_barras`)") != -1: # si es igual a -1 el metodo find no halló nada

				"Se supone que no se debe llegar a este if nunca porque en el método que llama a este método ya está el condicional de que si el código no existe no se puede seguir adelante con la introducción de los datos en la bd. Pero en todo caso se deja este condicional como otra forma de hacerlo y de tener más control sobre lo que entra a la bd"
				# ventana de notificacion de que el nuevo producto no pudo ser introducido exitosamente a la base de datos ya que el código de barras no existe
				self.notifica_new_product = self.otra_ventana(self.valida_exist, '600x170+350+320', u'Notificacion Stock', 0, 3, exitgrid=True)
				self.etiqueta(self.notifica_new_product, '¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica_new_product, 'El codigo de barras no existe en base de datos.', 0, 1, grid=True)
				self.etiqueta(self.notifica_new_product, 'Alimentar primero el item', 0, 2, grid=True)
				self.final_otra_ventana(self.notifica_new_product, self.valida_exist)
		
			elif format(e).find("Duplicate entry '" + IMEI + "' for key 'stocks.IMEI_UNIQUE'") != -1: # si es igual a -1 el metodo find no halló nada

				# ventana de notificacion de que el nuevo producto no pudo ser introducido exitosamente a la base de datos ya que el IMEI está repetido
				self.notifica_new_product = self.otra_ventana(self.valida_exist, '560x170+350+320', u'Notificacion Stock', 0, 3, exitgrid=True)
				self.etiqueta(self.notifica_new_product, '¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica_new_product, 'El IMEI digitado ya existe en Base de Datos', 0, 1, grid=True)
				self.etiqueta(self.notifica_new_product, 'Revise su IMEI digitado', 0, 2, grid=True)
				self.final_otra_ventana(self.notifica_new_product, self.valida_exist)

	def alimstock_del(self):

		self.codigo_stock.delete('1.0', END)
		self.valor_compra_stock.delete('1.0', END)
		#self.precio_venta_stock.delete('1.0', END)
		self.cantidad_entra_stock.delete('1.0', END)
		self.imei_entra_stock.delete('1.0', END)
		self.proveedor_stock.delete('1.0', END)




	# def read_barcode(self, EVN):

	# 	self.barcode_stock = self.otra_ventana(self.ventana_alimbd, '450x300+200+170', u'Código Barras Stock', 310, 250)
	# 	self.etiqueta(self.barcode_stock, u'Lea el código de barras', 20, 23)
	# 	self.barcode_lbl   = self.etiqueta(self.barcode_stock, u'?', 20, 55)
	# 	#self.label_stock = ttk.Label(self.barcode_stock, text=" ")
	# 	#self.label_stock.pack()
	# 	#self.barcode_stock.bind('<Key>', self.get_key)
	# 	self.final_otra_ventana(self.barcode_stock, self.ventana_alimbd)


	# def read_barcode(self, EVN):

	# 	device = InputDevice('/dev/input/event4')

	# 	self.current_barcode = ''
	# 	print ("Reading barcodes from device")

	# 	for i, evento in enumerate(device.read_loop()):
	# 		if evento.type == evdev.ecodes.EV_KEY and evento.value == 1:
	# 			keycode = categorize(evento).keycode
	# 			if keycode[4:].isdigit() == True and int(keycode[4:])//10 == 0:
	# 				self.current_barcode += keycode[4:]
	# 			else:
	# 				break

	# 	self.codigo_bd.delete('1.0', END)
	# 	self.codigo_bd.insert("1.0", self.current_barcode)
	# 	#self.codigo_bd.mark_set("insert", "insert-10c")
	# 	#self.codigo_bd.see("end")
	# 	self.codigo_bd.mark_set("insert", "2.0,1.0")
	# 	#self.producto_bd.focus_set()
	# 	print(self.current_barcode)


	# def get_key(self, event):

	# 	self.code = ''

	# 	if event.char in '0123456789':
	# 		self.code += event.char
	# 		#print('>', self.code)
	# 		self.barcode_lbl['text'] = self.code
	# 		print(self.code)
	# 		#self.etiqueta(self.barcode_stock, self.code, 20, 55)

	# 	elif event.keysym == 'Return':
	# 		#print('result:', self.code)
	# 		showinfo('Code', self.code)


	#def registra_stock(self):

	#	self.prueba_stock.insert("1.0", self.codigo_bd.get(1.0, "end-1c"))