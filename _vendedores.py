from tkinter import *
from tkinter import ttk, font
import MySQLdb
import re

class Vendedores:

	def vendedores(self):

		# Ventana de opciones de vendedores

		self.ventana_vendedores = self.otra_ventana(self.raiz, '450x300+150+120', 'Opciones Vendedores', 180, 250)
		self.agrega_boton(self.ventana_vendedores, u'Alimentar Vendedores', 120, 30, self.alimentar_vendedores)
		self.agrega_boton(self.ventana_vendedores, u'Buscar Vendedores', 130, 100, self.buscar_vendedores)
		self.final_otra_ventana(self.ventana_vendedores, self.raiz)

	# Ventana para buscar vendedores

	def buscar_vendedores(self):

		self.ventana_searchvendedores = self.otra_ventana(self.ventana_vendedores, '450x200+200+170', u'Buscar Vendedores', 185, 140)
		self.etiqueta(self.ventana_searchvendedores, 'Buscar por:', 30, 23)
		self.agrega_boton(self.ventana_searchvendedores, 'Nombre', 130, 60, self.busca_x_nombre_vendedor, pad=(3,3))
		self.agrega_boton(self.ventana_searchvendedores, 'Cedula', 230, 60, self.busca_x_cedula_vendedor, pad=(3,3)) # 
		self.final_otra_ventana(self.ventana_searchvendedores, self.ventana_vendedores)

	def busca_x_cedula_vendedor(self):

		self.ventana_searchvend_x_cedula = self.otra_ventana(self.ventana_searchvendedores, '560x180+250+220', u'Buscar Vendedor por Cédula', 370, 90)
		self.etiqueta(self.ventana_searchvend_x_cedula, u'Cédula a encontrar', 20, 23)
		self.cedula_vend_search = self.caja_texto(self.ventana_searchvend_x_cedula, 1.4, 50, 25, 55)
		self.agrega_boton(self.ventana_searchvend_x_cedula, 'Buscar', 110, 100, self.buscavend_x_cedula, pad=(3,3)) 
		self.agrega_boton(self.ventana_searchvend_x_cedula, 'Borrar', 240, 100, self.borravend_x_cedula, pad=(3,3))

		self.final_otra_ventana(self.ventana_searchvend_x_cedula, self.ventana_searchvendedores)

	def buscavend_x_cedula(self):

		cedula = self.cedula_vend_search.get(1.0, "end-1c")

		if cedula.isdigit() == True:

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			db_cursor.execute("SELECT id, nombre, documento_cedula, celular FROM vendedores WHERE documento_cedula = " + cedula)
			self.searchvend_x_cedula = db_cursor.fetchall()
			db_conn.close ()

			cedula_vend  = '' 
			nombre_vend  = ''
			celular_vend = ''

			for i in range(len(self.searchvend_x_cedula)):

				cedula_vend += str(self.searchvend_x_cedula[i][2]) + '\n'
				nombre_vend += self.searchvend_x_cedula[i][1] + '\n'
				celular_vend+= str(self.searchvend_x_cedula[i][3]) + '\n'

			if cedula_vend == '':

				# ventana de notificacion que dice que no hay registros con dicha cedula
				self.notifica = self.otra_ventana(self.ventana_searchvend_x_cedula, '450x100+300+270', u'Notificacion búsqueda', 180, 65)
				self.etiqueta(self.notifica, u'Cédula no hallada', 45, 20)
				self.final_otra_ventana(self.notifica, self.ventana_searchvend_x_cedula)

				self.borravend_x_cedula()

			else:

				self.ventana_searchvend_x_cedula_r = self.otra_ventana(self.ventana_searchvend_x_cedula, '700x150+300+270', u'Buscar Vendedor por Cédula', 390, 100)
				self.etiqueta(self.ventana_searchvend_x_cedula_r, u'Cédula', 55, 20)
				self.boxvend_cedula = self.caja_texto(self.ventana_searchvend_x_cedula_r, 1, 15, 25, 50)
				self.etiqueta(self.ventana_searchvend_x_cedula_r, u'Nombre', 300, 20)
				self.boxvend_nombre = self.caja_texto(self.ventana_searchvend_x_cedula_r, 1, 30, 200, 50)
				self.etiqueta(self.ventana_searchvend_x_cedula_r, u'Celular',550, 20)
				self.boxvend_celular = self.caja_texto(self.ventana_searchvend_x_cedula_r, 1, 15, 520, 50)
				self.agrega_boton(self.ventana_searchvend_x_cedula_r, 'Eliminar Vendedor', 200, 100, self.delete_vend_cedula, pad=(3,3))

				self.boxvend_cedula.insert("1.0", cedula_vend)
				self.boxvend_nombre.insert("1.0", nombre_vend)
				self.boxvend_celular.insert("1.0", celular_vend)

				self.final_otra_ventana(self.ventana_searchvend_x_cedula_r, self.ventana_searchvend_x_cedula)

				self.borravend_x_cedula()

		else:

			# ventana de notificacion que dice que no se ha introducido un valor correcto de cédula
			self.notifica = self.otra_ventana(self.ventana_searchvend_x_cedula, '450x150+300+270', u'Notificacion búsqueda', 180, 115)
			self.etiqueta(self.notifica, u'Valor de cédula con caracteres inválidos', 45, 20)
			self.etiqueta(self.notifica, "'" + cedula + "'", 150, 50)
			self.final_otra_ventana(self.notifica, self.ventana_searchvend_x_cedula)

			self.borravend_x_cedula()

	def delete_vend_cedula(self):

		# ventana de notificacion de eliminacion exitosa del vendedor de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searchvend_x_cedula_r, '450x100+350+320', u'Notificacion eliminación', 180, 65)
		self.etiqueta(self.notifica, u'¿Está seguro de eliminar al vendedor?', 45, 20)
		self.agrega_boton(self.notifica, 'Confirmar', 300, 65, self.delete_vend_cedula2, pad=(3,3))
		self.final_otra_ventana(self.notifica, self.ventana_searchvend_x_cedula_r)

	def delete_vend_cedula2(self):

		self.notifica.destroy()

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("DELETE FROM vendedores WHERE documento_cedula = " + str(self.searchvend_x_cedula[0][2]) + ";")
		db_cursor.close()
		db_conn.commit ()
		db_conn.close ()

		# ventana de notificacion de eliminacion exitosa del vendedor de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searchvend_x_cedula_r, '450x100+350+320', u'Notificacion eliminación', 180, 65)
		self.etiqueta(self.notifica, u'Vendedor eliminado de la base de datos', 45, 20)
		self.final_otra_ventana(self.notifica, self.ventana_searchvend_x_cedula_r)

		self.ventana_searchvend_x_cedula_r.destroy()
		self.borravend_x_cedula()

	def borravend_x_cedula(self):

		self.cedula_vend_search.delete('1.0', END)

	def busca_x_nombre_vendedor(self):

		self.ventana_searchvend_x_nombre = self.otra_ventana(self.ventana_searchvendedores, '560x180+250+220', 'Buscar Vendedor por Nombre', 370, 100)
		self.etiqueta(self.ventana_searchvend_x_nombre, 'Nombre a encontrar', 20, 23)
		self.nombre_vend_search = self.caja_texto(self.ventana_searchvend_x_nombre, 1.4, 50, 25, 55)
		self.agrega_boton(self.ventana_searchvend_x_nombre, 'Buscar', 110, 100, self.buscavend_x_nombre, pad=(3,3)) # 
		self.agrega_boton(self.ventana_searchvend_x_nombre, 'Borrar', 240, 100, self.borravend_x_nombre, pad=(3,3)) #

		self.final_otra_ventana(self.ventana_searchvend_x_nombre, self.ventana_searchvendedores)

	def buscavend_x_nombre(self):

		nombre = self.nombre_vend_search.get(1.0, "end-1c")

		if bool(re.match('[a-zA-Z\s]+$', nombre)) == True:

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			#db_cursor.execute("SELECT id, nombre, documento_cedula, celular FROM vendedores WHERE nombre = '" + nombre + "'")
			db_cursor.execute("SELECT id, nombre, documento_cedula, celular FROM vendedores WHERE nombre LIKE '%" + nombre + "%'")
			self.searchvend_x_nombre = db_cursor.fetchall()
			db_conn.close ()

			cedula_vend  = '' 
			nombre_vend  = ''
			celular_vend = ''

			for i in range(len(self.searchvend_x_nombre)):

				cedula_vend += str(self.searchvend_x_nombre[i][2]) + '\n'
				nombre_vend += self.searchvend_x_nombre[i][1] + '\n'
				celular_vend+= str(self.searchvend_x_nombre[i][3]) + '\n'

			if nombre_vend == '':

				# ventana de notificacion que dice que no hay registros con dicho nombre
				self.notifica = self.otra_ventana(self.ventana_searchvend_x_nombre, '450x100+300+270', u'Notificacion búsqueda', 180, 65)
				self.etiqueta(self.notifica, u'Nombre no hallado', 45, 20)
				self.final_otra_ventana(self.notifica, self.ventana_searchvend_x_nombre)

				self.borravend_x_nombre()

			else:

				self.ventana_searchvend_x_nombre_r = self.otra_ventana(self.ventana_searchvend_x_nombre, '700x150+300+270', u'Buscar Vendedor por Cédula', 390, 100)
				self.etiqueta(self.ventana_searchvend_x_nombre_r, u'Cédula', 55, 20)
				self.boxvend_cedula = self.caja_texto(self.ventana_searchvend_x_nombre_r, 1, 15, 25, 50)
				self.etiqueta(self.ventana_searchvend_x_nombre_r, u'Nombre', 300, 20)
				self.boxvend_nombre = self.caja_texto(self.ventana_searchvend_x_nombre_r, 1, 30, 200, 50)
				self.etiqueta(self.ventana_searchvend_x_nombre_r, u'Celular',550, 20)
				self.boxvend_celular = self.caja_texto(self.ventana_searchvend_x_nombre_r, 1, 15, 520, 50)
				self.agrega_boton(self.ventana_searchvend_x_nombre_r, 'Eliminar Vendedor', 200, 100, self.delete_vend_nombre, pad=(3,3))

				self.boxvend_cedula.insert("1.0", cedula_vend)
				self.boxvend_nombre.insert("1.0", nombre_vend)
				self.boxvend_celular.insert("1.0", celular_vend)

				self.final_otra_ventana(self.ventana_searchvend_x_nombre_r, self.ventana_searchvend_x_nombre)

				self.borravend_x_nombre()

		else:

			# ventana de notificacion que dice que no se ha introducido un valor correcto de nombre
			self.notifica = self.otra_ventana(self.ventana_searchvend_x_nombre, '450x150+300+270', u'Notificacion búsqueda', 180, 115)
			self.etiqueta(self.notifica, u'Nombre con caracteres inválidos', 45, 20)
			self.etiqueta(self.notifica, "'" + nombre + "'", 150, 50)
			self.final_otra_ventana(self.notifica, self.ventana_searchvend_x_nombre)

			self.borravend_x_nombre()

	def delete_vend_nombre(self):

		# ventana de notificacion de eliminacion exitosa del vendedor de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searchvend_x_nombre_r, '450x100+350+320', u'Notificacion eliminación', 180, 65)
		self.etiqueta(self.notifica, u'¿Está seguro de eliminar al vendedor?', 45, 20)
		self.agrega_boton(self.notifica, 'Confirmar', 300, 65, self.delete_vend_nombre2, pad=(3,3))
		self.final_otra_ventana(self.notifica, self.ventana_searchvend_x_nombre_r)

	def delete_vend_nombre2(self):

		self.notifica.destroy()

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("DELETE FROM vendedores WHERE nombre = " + self.searchvend_x_nombre[0][1] + ";")
		db_cursor.close()
		db_conn.commit ()
		db_conn.close ()

		# ventana de notificacion de eliminacion exitosa del vendedor de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searchvend_x_nombre_r, '450x100+350+320', u'Notificacion eliminación', 180, 65)
		self.etiqueta(self.notifica, u'Vendedor eliminado de la base de datos', 45, 20)
		self.final_otra_ventana(self.notifica, self.ventana_searchvend_x_nombre_r)

		self.ventana_searchvend_x_nombre_r.destroy()
		self.borravend_x_nombre()

	def borravend_x_nombre(self):

		self.nombre_vend_search.delete('1.0', END)

	# Ventana de Alimentar vendedores

	def alimentar_vendedores(self):

		self.ventana_alimvendedores = self.otra_ventana(self.ventana_vendedores, '450x300+200+170', u'Alimentar Vendedores', 310, 250)
		self.etiqueta(self.ventana_alimvendedores, 'Nombre', 20, 23)
		self.nombre_vend = self.caja_texto(self.ventana_alimvendedores, 1.4, 35, 120, 25)
		self.etiqueta(self.ventana_alimvendedores, 'Apellido', 20, 55)
		self.apelli_vend = self.caja_texto(self.ventana_alimvendedores, 1.4, 35, 120, 57)
		self.etiqueta(self.ventana_alimvendedores, 'Celular', 20, 87)
		self.celular_vend= self.caja_texto(self.ventana_alimvendedores, 1.4, 35, 120, 89)
		self.etiqueta(self.ventana_alimvendedores, u'Cédula', 20, 119)
		self.cedula_vend = self.caja_texto(self.ventana_alimvendedores, 1.4, 35, 120, 121)
		self.agrega_boton(self.ventana_alimvendedores, 'Registrar', 50, 250, self.valida_registro_vendedores, pad=(3,3))
		self.agrega_boton(self.ventana_alimvendedores, 'Borrar', 180, 250, self.alimvend_del, pad=(3,3))
		self.final_otra_ventana(self.ventana_alimvendedores, self.ventana_vendedores)

	# ventana para validar vendedores

	def valida_registro_vendedores(self):

		nombre_vendedor   = self.nombre_vend.get(1.0, "end-1c")
		apellido_vendedor = self.apelli_vend.get(1.0, "end-1c")
		celular_vendedor  = self.celular_vend.get(1.0, "end-1c")
		cedula_vendedor   = self.cedula_vend.get(1.0, "end-1c")


		if nombre_vendedor == '' or apellido_vendedor == '':

			# ventana de notificacion de que el nombre o el apellido del vendedor no fueron escritos
			self.notifica = self.otra_ventana(self.ventana_alimvendedores, '+250+220', u'Notificacion vendedor', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Nombre y Apellido son campos necesarios', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimvendedores)

		elif bool(re.match('[a-zA-Z\s]+$', nombre_vendedor)) == False or bool(re.match('[a-zA-Z\s]+$', apellido_vendedor)) == False:

			# ventana de notificacion de que el nombre o el apellido del vendedor fueron escritos con números
			self.notifica = self.otra_ventana(self.ventana_alimvendedores, '+250+220', u'Notificacion vendedor', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Nombre o Apellido errado. Tiene números', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimvendedores)

		elif cedula_vendedor == '':

			# ventana de notificacion de que la cédula del vendedor no fue escrito
			self.notifica = self.otra_ventana(self.ventana_alimvendedores, '+250+220', u'Notificacion vendedor', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Cédula es un campo necesario', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimvendedores)

		elif cedula_vendedor.isdigit() == False:

			# ventana de notificacion de que la cédula o el celular del vendedor fueron escritos con caracteres alfabéticos
			self.notifica = self.otra_ventana(self.ventana_alimvendedores, '+250+220', u'Notificacion vendedor', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!',  0, 0, grid=True)
			self.etiqueta(self.notifica, u'Cédula errada. Sólo admite números', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimvendedores)

		elif celular_vendedor == '':

			# despliega ventana con la informacion a confirmar

			self.celular_vend_bool = False

			texto_info = 'Nombre: '   + nombre_vendedor   + '\n'
			texto_info+= 'Apellido: ' + apellido_vendedor + '\n'
			texto_info+= 'Celular: '  + celular_vendedor  + '\n'
			texto_info+= u'Cédula: '  + cedula_vendedor

			self.valida_vendedores = self.otra_ventana(self.ventana_alimvendedores, '450x300+250+220', u'Valida Vendedor', 230, 250, 'Cancelar')
			box_valida           = self.caja_texto(self.valida_vendedores, 10, 40, 20, 25)
			box_valida.insert("1.0", texto_info)
			self.agrega_boton(self.valida_vendedores, 'Validar Info', 100, 250, self.introduce_vend_db, pad=(3,3))
			self.final_otra_ventana(self.valida_vendedores, self.ventana_alimvendedores)

		elif celular_vendedor != '':

			if celular_vendedor.isdigit() == False:

				# ventana de notificacion de que la cédula o el celular del vendedor fueron escritos con caracteres alfabéticos
				self.notifica = self.otra_ventana(self.ventana_alimvendedores, '+250+220', u'Notificacion vendedor', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, '¡¡¡ERROR!!!',  0, 0, grid=True)
				self.etiqueta(self.notifica, u'Cédula o Celular errado. Sólo admite números',  0, 1, grid=True)
				self.final_otra_ventana(self.notifica, self.ventana_alimvendedores)

			else:

				# despliega ventana con la informacion a confirmar

				self.celular_vend_bool = True

				texto_info = 'Nombre: '   + nombre_vendedor   + '\n'
				texto_info+= 'Apellido: ' + apellido_vendedor + '\n'
				texto_info+= 'Celular: '  + celular_vendedor  + '\n'
				texto_info+= u'Cédula: '  + cedula_vendedor

				self.valida_vendedores = self.otra_ventana(self.ventana_alimvendedores, '450x300+250+220', u'Valida Vendedor', 230, 250, 'Cancelar')
				box_valida           = self.caja_texto(self.valida_vendedores, 10, 40, 20, 25)
				box_valida.insert("1.0", texto_info)
				self.agrega_boton(self.valida_vendedores, 'Validar Info', 100, 250, self.introduce_vend_db, pad=(3,3))
				self.final_otra_ventana(self.valida_vendedores, self.ventana_alimvendedores)

	# funcion para borrar los campos que se han introducido en el formulario para alimentar la bd de vendedores

	def alimvend_del(self):

		self.nombre_vend.delete('1.0', END)
		self.apelli_vend.delete('1.0', END)
		self.celular_vend.delete('1.0', END)
		self.cedula_vend.delete('1.0', END)

	# Introduce la info en la base de datos

	def introduce_vend_db(self):

		nombre_vendedor   = self.nombre_vend.get(1.0, "end-1c")
		apellido_vendedor = self.apelli_vend.get(1.0, "end-1c")
		celular_vendedor  = self.celular_vend.get(1.0, "end-1c")
		cedula_vendedor   = self.cedula_vend.get(1.0, "end-1c")

		try:

			if self.celular_vend_bool == True:

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("INSERT INTO vendedores (id, nombre, celular, documento_cedula) VALUES (" + cedula_vendedor[-5:] + ", '" + nombre_vendedor + " " + apellido_vendedor + "', " + celular_vendedor + ", " + cedula_vendedor + ");")
				db_cursor.close()
				db_conn.commit ()
				db_conn.close ()

				# ventana de notificacion de que la información del vendedor ya fue introducida en la base de datos
				self.notifica = self.otra_ventana(self.valida_vendedores, '+300+270', u'Notificacion vendedor', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, u'Información capturada correctamente', 0, 0, grid=True)
				self.final_otra_ventana(self.notifica, self.valida_vendedores)

				self.alimvend_del()

			else:

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("INSERT INTO vendedores (id, nombre, documento_cedula) VALUES (" + cedula_vendedor[-5:] + ", '" + nombre_vendedor + " " + apellido_vendedor + "', " + cedula_vendedor + ");")
				db_cursor.close()
				db_conn.commit ()
				db_conn.close ()

				# ventana de notificacion de que la información del vendedor ya fue introducida en la base de datos
				self.notifica = self.otra_ventana(self.valida_vendedores, '+300+270', u'Notificacion vendedor', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, u'Información capturada correctamente', 0, 0, grid=True)
				self.final_otra_ventana(self.notifica, self.valida_vendedores)

				self.alimvend_del()

		except MySQLdb.IntegrityError as e: 
			
			if format(e).find("Duplicate entry") != -1 and format(e).find(cedula_vendedor[-5:]) != -1: # si es igual a -1 el metodo find no halló nada
				
				print('ID de vendedor ya existe')

				# ventana de notificacion de que el ID del vendedor ya existe
				self.notifica = self.otra_ventana(self.valida_vendedores, '+300+270', u'Notificacion vendedor', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, '¡¡¡ERROR!!!',   0, 0, grid=True)
				self.etiqueta(self.notifica, 'El ID del vendedor ya existe. Cambiar cédula',  0, 1, grid=True)
				self.final_otra_ventana(self.notifica, self.valida_vendedores)
		
			elif format(e).find("Duplicate entry") != -1 and format(e).find(cedula_vendedor) != -1: # si es igual a -1 el metodo find no halló nada

				print('La cédula del vendedor ya existe')

				# ventana de notificacion de que la cédula del vendedor ya existe
				self.notifica = self.otra_ventana(self.valida_vendedores, '+300+270', u'Notificacion vendedor', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, '¡¡¡ERROR!!!',  0, 0, grid=True)
				self.etiqueta(self.notifica, 'Cédula del vendedor ya existe. Cambiar', 0, 1, grid=True)
				self.final_otra_ventana(self.notifica, self.valida_vendedores)

			elif format(e).find("Duplicate entry") != -1 and format(e).find(celular_vendedor) != -1: # si es igual a -1 el metodo find no halló nada

				print('El celular del vendedor ya existe')

				# ventana de notificacion de que la cédula del vendedor ya existe
				self.notifica = self.otra_ventana(self.valida_vendedores, '+300+270', u'Notificacion vendedor', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, '¡¡¡ERROR!!!',  0, 0, grid=True)
				self.etiqueta(self.notifica, 'Celular del vendedor ya existe. Cambiar.', 0, 1, grid=True)
				self.final_otra_ventana(self.notifica, self.valida_vendedores)

		self.valida_vendedores.destroy()