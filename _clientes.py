from tkinter import *
from tkinter import ttk, font
import MySQLdb
import re

class Clientes:

	def clientes(self):

		# Ventana de opciones de clientes
		self.ventana_clientes = self.otra_ventana(self.raiz, '450x300+150+120', 'Opciones Clientes', 180, 250)
		self.ventana_externa = False
		self.agrega_boton(self.ventana_clientes, u'Alimentar Clientes', 120, 30, self.alimentar_clientes)
		self.agrega_boton(self.ventana_clientes, u'Buscar Clientes', 130, 100, self.buscar_clientes)
		self.final_otra_ventana(self.ventana_clientes, self.raiz)

	# Ventana para buscar cliente

	def buscar_clientes(self):

		self.ventana_searchclientes = self.otra_ventana(self.ventana_clientes, '450x300+200+170', u'Buscar Clientes', 185, 250)
		self.etiqueta(self.ventana_searchclientes, 'Buscar por:', 30, 23)
		self.agrega_boton(self.ventana_searchclientes, 'Nombre', 130, 60, self.busca_x_nombre_cliente, pad=(3,3))
		self.agrega_boton(self.ventana_searchclientes, 'Cedula', 230, 60, self.busca_x_cedula_cliente, pad=(3,3)) # 
		self.final_otra_ventana(self.ventana_searchclientes, self.ventana_clientes)

	def busca_x_cedula_cliente(self):

		self.ventana_searchcli_x_cedula = self.otra_ventana(self.ventana_searchclientes, '560x180+250+220', u'Buscar Cliente por Cédula', 370, 90)
		self.etiqueta(self.ventana_searchcli_x_cedula, u'Cédula a encontrar', 20, 23)
		self.cedula_cli_search = self.caja_texto(self.ventana_searchcli_x_cedula, 1.4, 50, 25, 55)
		self.agrega_boton(self.ventana_searchcli_x_cedula, 'Buscar', 110, 100, self.buscacli_x_cedula, pad=(3,3)) 
		self.agrega_boton(self.ventana_searchcli_x_cedula, 'Borrar', 240, 100, self.borracli_x_cedula, pad=(3,3))

		self.final_otra_ventana(self.ventana_searchcli_x_cedula, self.ventana_searchclientes)

	def buscacli_x_cedula(self):

		cedula = self.cedula_cli_search.get(1.0, "end-1c")

		if cedula.isdigit() == True:

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			db_cursor.execute("SELECT id, cedula, nombre, celular FROM clientes WHERE cedula = " + cedula)
			self.searchcli_x_cedula = db_cursor.fetchall()
			db_conn.close ()

			cedula_cli  = '' 
			nombre_cli  = ''
			celular_cli = ''

			for i in range(len(self.searchcli_x_cedula)):

				cedula_cli += str(self.searchcli_x_cedula[i][1]) + '\n'
				nombre_cli += self.searchcli_x_cedula[i][2] + '\n'
				celular_cli+= str(self.searchcli_x_cedula[i][3]) + '\n'

			if cedula_cli == '':

				# ventana de notificacion que dice que no hay registros con dicha cedula
				self.notifica = self.otra_ventana(self.ventana_searchcli_x_cedula, '450x100+300+270', u'Notificacion búsqueda', 180, 65)
				self.etiqueta(self.notifica, u'Cédula no hallada', 45, 20)
				self.final_otra_ventana(self.notifica, self.ventana_searchcli_x_cedula)

				self.borracli_x_cedula()

			else:

				self.ventana_searchcli_x_cedula_r = self.otra_ventana(self.ventana_searchcli_x_cedula, '700x150+300+270', u'Buscar Cliente por Cédula', 390, 100)
				self.etiqueta(self.ventana_searchcli_x_cedula_r, u'Cédula', 55, 20)
				self.boxcli_cedula = self.caja_texto(self.ventana_searchcli_x_cedula_r, 1, 15, 25, 50)
				self.etiqueta(self.ventana_searchcli_x_cedula_r, u'Nombre', 300, 20)
				self.boxcli_nombre = self.caja_texto(self.ventana_searchcli_x_cedula_r, 1, 30, 200, 50)
				self.etiqueta(self.ventana_searchcli_x_cedula_r, u'Celular',550, 20)
				self.boxcli_celular = self.caja_texto(self.ventana_searchcli_x_cedula_r, 1, 15, 520, 50)
				self.agrega_boton(self.ventana_searchcli_x_cedula_r, 'Eliminar Cliente', 200, 100, self.delete_cli_cedula, pad=(3,3))

				self.boxcli_cedula.insert("1.0", cedula_cli)
				self.boxcli_nombre.insert("1.0", nombre_cli)
				self.boxcli_celular.insert("1.0", celular_cli)

				self.final_otra_ventana(self.ventana_searchcli_x_cedula_r, self.ventana_searchcli_x_cedula)

				self.borracli_x_cedula()

		else:

			# ventana de notificacion que dice que no se ha introducido un valor correcto de cédula
			self.notifica = self.otra_ventana(self.ventana_searchcli_x_cedula, '450x150+300+270', u'Notificacion búsqueda', 180, 115)
			self.etiqueta(self.notifica, u'Valor de cédula con caracteres inválidos', 45, 20)
			self.etiqueta(self.notifica, "'" + cedula + "'", 150, 50)
			self.final_otra_ventana(self.notifica, self.ventana_searchcli_x_cedula)

			self.borracli_x_cedula()

	def delete_cli_cedula(self):

		# ventana de notificacion de eliminacion exitosa del cliente de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searcli_x_cedula_r, '450x100+350+320', u'Notificacion Cliente', 180, 65)
		self.etiqueta(self.notifica, u'¿Está seguro de eliminar el cliente?', 45, 20)
		self.agrega_boton(self.notifica, 'Confirmar', 300, 65, self.delete_cli_cedula2, pad=(3,3))
		self.final_otra_ventana(self.notifica, self.ventana_searchcli_x_cedula_r)

	def delete_cli_cedula2(self):

		self.notifica.destroy()

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("DELETE FROM clientes WHERE cedula = " + str(self.searchcli_x_cedula[0][1]) + ";")
		db_cursor.close()
		db_conn.commit ()
		db_conn.close ()

		# ventana de notificacion de eliminacion exitosa del cliente de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searcli_x_cedula_r, '450x100+350+320', u'Notificacion eliminación', 180, 65)
		self.etiqueta(self.notifica, u'Cliente eliminado de la base de datos', 45, 20)
		self.final_otra_ventana(self.notifica, self.ventana_searchcli_x_cedula_r)

		self.ventana_searchcli_x_cedula_r.destroy()
		self.borracli_x_cedula()

	def borracli_x_cedula(self):

		self.cedula_cli_search.delete('1.0', END)

	def busca_x_nombre_cliente(self):

		self.ventana_searchcli_x_nombre = self.otra_ventana(self.ventana_searchclientes, '560x400+250+220', 'Buscar Cliente por Nombre', 370, 100)
		self.etiqueta(self.ventana_searchcli_x_nombre, 'Nombre a encontrar', 20, 23)
		self.nombre_cli_search = self.caja_texto(self.ventana_searchcli_x_nombre, 1.4, 50, 25, 55)
		self.agrega_boton(self.ventana_searchcli_x_nombre, 'Buscar', 110, 100, self.buscacli_x_nombre, pad=(3,3)) 
		self.agrega_boton(self.ventana_searchcli_x_nombre, 'Borrar', 240, 100, self.borracli_x_nombre, pad=(3,3))

		self.final_otra_ventana(self.ventana_searchcli_x_nombre, self.ventana_searchclientes)

	def buscacli_x_nombre(self):

		nombre = self.nombre_cli_search.get(1.0, "end-1c")

		if bool(re.match('[a-zA-Z\s]+$', nombre)) == True:

			db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
			db_cursor  = db_conn.cursor()
			#db_cursor.execute("SELECT id, cedula, nombre, celular FROM clientes WHERE nombre = '" + nombre + "'")
			db_cursor.execute("SELECT id, cedula, nombre, celular FROM clientes WHERE nombre LIKE '%" + nombre + "%'")

			self.searchcli_x_nombre = db_cursor.fetchall()
			db_conn.close ()

			cedula_cli  = '' 
			nombre_cli  = ''
			celular_cli = ''

			for i in range(len(self.searchcli_x_nombre)):

				cedula_cli += str(self.searchcli_x_nombre[i][1]) + '\n'
				nombre_cli += self.searchcli_x_nombre[i][2] + '\n'
				celular_cli+= str(self.searchcli_x_nombre[i][3]) + '\n'

			if nombre_cli == '':

				# ventana de notificacion que dice que no hay registros con dicho nombre
				self.notifica = self.otra_ventana(self.ventana_searchcli_x_nombre, '450x100+250+220', u'Notificacion búsqueda', 180, 65)
				self.etiqueta(self.notifica, u'Nombre no hallado', 45, 20)
				self.final_otra_ventana(self.notifica, self.ventana_searchcli_x_nombre)

				self.borracli_x_nombre()

			else:

				self.ventana_searchcli_x_nombre_r = self.otra_ventana(self.ventana_searchcli_x_nombre, '700x150+300+270', u'Buscar Cliente por Nombre', 390, 100)
				self.etiqueta(self.ventana_searchcli_x_nombre_r, u'Cédula', 55, 20)
				self.boxcli_cedula = self.caja_texto(self.ventana_searchcli_x_nombre_r, 1, 15, 25, 50)
				self.etiqueta(self.ventana_searchcli_x_nombre_r, u'Nombre', 300, 20)
				self.boxcli_nombre = self.caja_texto(self.ventana_searchcli_x_nombre_r, 1, 30, 200, 50)
				self.etiqueta(self.ventana_searchcli_x_nombre_r, u'Celular',550, 20)
				self.boxcli_celular = self.caja_texto(self.ventana_searchcli_x_nombre_r, 1, 15, 520, 50)
				self.agrega_boton(self.ventana_searchcli_x_nombre_r, 'Eliminar Cliente', 200, 100, self.delete_cli_nombre, pad=(3,3))

				self.boxcli_cedula.insert("1.0", cedula_cli)
				self.boxcli_nombre.insert("1.0", nombre_cli)
				self.boxcli_celular.insert("1.0", celular_cli)

				self.final_otra_ventana(self.ventana_searchcli_x_nombre_r, self.ventana_searchcli_x_nombre)

				self.borracli_x_nombre()

		else:

			# ventana de notificacion que dice que no se ha introducido un valor correcto de nombre
			self.notifica = self.otra_ventana(self.ventana_searchcli_x_nombre, '450x150+300+270', u'Notificacion búsqueda', 180, 115)
			self.etiqueta(self.notifica, u'Nombre con caracteres inválidos', 45, 20)
			self.etiqueta(self.notifica, "'" + nombre + "'", 150, 50)
			self.final_otra_ventana(self.notifica, self.ventana_searchcli_x_nombre)

			self.borracli_x_nombre()

	def delete_cli_nombre(self):

		# ventana de notificacion de eliminacion exitosa del cliente de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searchcli_x_nombre_r, '450x100+350+320', u'Notificacion eliminación', 180, 65)
		self.etiqueta(self.notifica, u'¿Está seguro de eliminar el cliente?', 45, 20)
		self.agrega_boton(self.notifica, 'Confirmar', 300, 65, self.delete_cli_nombre2, pad=(3,3))
		self.final_otra_ventana(self.notifica, self.ventana_searchcli_x_nombre_r)

	def delete_cli_nombre2(self):

		self.notifica.destroy()

		db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
		db_cursor  = db_conn.cursor()
		db_cursor.execute("DELETE FROM clientes WHERE nombre = " + str(self.searchcli_x_nombre[0][2]) + ";")
		db_cursor.close()
		db_conn.commit ()
		db_conn.close ()

		# ventana de notificacion de eliminacion exitosa del cliente de la base de datos
		self.notifica = self.otra_ventana(self.ventana_searchcli_x_nombre_r, '450x100+350+320', u'Notificacion eliminación', 180, 65)
		self.etiqueta(self.notifica, u'Cliente eliminado de la base de datos', 45, 20)
		self.final_otra_ventana(self.notifica, self.ventana_searchcli_x_nombre_r)

		self.ventana_searchcli_x_nombre_r.destroy()
		self.borracli_x_nombre()

	def borracli_x_nombre(self):

		self.nombre_cli_search.delete('1.0', END)

	# Ventana de Alimentar clientes

	def alimentar_clientes(self):

		#if self.ventana_externa == False:

		self.ventana_alimclientes = self.otra_ventana(self.ventana_clientes, '450x300+200+170', u'Alimentar Clientes', 310, 250)
		self.etiqueta(self.ventana_alimclientes, 'Nombre', 20, 23)
		self.nombre_cli = self.caja_texto(self.ventana_alimclientes, 1.4, 35, 120, 25)
		self.etiqueta(self.ventana_alimclientes, 'Apellido', 20, 55)
		self.apelli_cli = self.caja_texto(self.ventana_alimclientes, 1.4, 35, 120, 57)
		self.etiqueta(self.ventana_alimclientes, 'Celular', 20, 87)
		self.celular_cli= self.caja_texto(self.ventana_alimclientes, 1.4, 35, 120, 89)
		self.etiqueta(self.ventana_alimclientes, u'Cédula', 20, 119)
		self.cedula_cli = self.caja_texto(self.ventana_alimclientes, 1.4, 35, 120, 121)
		self.agrega_boton(self.ventana_alimclientes, 'Registrar', 50, 250, self.valida_registro_clientes, pad=(3,3))
		self.agrega_boton(self.ventana_alimclientes, 'Borrar', 180, 250, self.alimcli_del, pad=(3,3))
		self.final_otra_ventana(self.ventana_alimclientes, self.ventana_clientes)

	# ventana para validar clientes

	def valida_registro_clientes(self):

		nombre_cliente   = self.nombre_cli.get(1.0, "end-1c")
		apellido_cliente = self.apelli_cli.get(1.0, "end-1c")
		celular_cliente  = self.celular_cli.get(1.0, "end-1c")
		cedula_cliente   = self.cedula_cli.get(1.0, "end-1c")

		if nombre_cliente == '' or apellido_cliente == '':

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
			self.notifica = self.otra_ventana(self.ventana_alimclientes, '450x100+250+220', u'Notificacion Cliente', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Nombre y Apellido son campos necesarios', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimclientes)

		elif bool(re.match('[a-zA-Z\s]+$', nombre_cliente)) == False or bool(re.match('[a-zA-Z\s]+$', apellido_cliente)) == False:

			# ventana de notificacion de que el nombre o el apellido del cliente fueron escritos con números
			self.notifica = self.otra_ventana(self.ventana_alimclientes, '450x100+250+220', u'Notificacion Cliente', 190, 100)
			self.etiqueta(self.notifica, '¡¡¡ERROR!!!',  0, 0, grid=True)
			self.etiqueta(self.notifica, u'Nombre o Apellido errado. Tiene números', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimclientes)

		elif cedula_cliente == '':

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
			self.notifica = self.otra_ventana(self.ventana_alimclientes, '+250+220', u'Notificacion Cliente', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Cédula es un campo necesario', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimclientes)

		elif cedula_cliente.isdigit() == False:

			# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
			self.notifica = self.otra_ventana(self.ventana_alimclientes, '+250+220', u'Notificacion Cliente', 0, 2, exitgrid=True)
			self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
			self.etiqueta(self.notifica, u'Cédula con caracteres inválidos. Sólo admite números.', 0, 1, grid=True)
			self.final_otra_ventana(self.notifica, self.ventana_alimclientes)

		elif celular_cliente == '':

			self.celular_cli_bool = False

			texto_info = 'Nombre: '   + self.nombre_cli.get(1.0, "end-1c") + '\n'
			texto_info+= 'Apellido: ' + self.apelli_cli.get(1.0, "end-1c") + '\n'
			texto_info+= 'Celular: '  + self.celular_cli.get(1.0, "end-1c") + '\n'
			texto_info+= u'Cédula: '  + self.cedula_cli.get(1.0, "end-1c")

			self.valida_clientes = self.otra_ventana(self.ventana_alimclientes, '450x300+250+220', u'Valida Cliente', 230, 250, 'Cancelar')
			box_valida           = self.caja_texto(self.valida_clientes, 10, 40, 20, 25)
			box_valida.insert("1.0", texto_info)
			self.agrega_boton(self.valida_clientes, 'Validar Info', 100, 250, self.introduce_cli_db, pad=(3,3))		# 
			self.final_otra_ventana(self.valida_clientes, self.ventana_alimclientes)

		elif celular_cliente != '':

			if celular_cliente.isdigit() == True:

				self.celular_cli_bool = True

				texto_info = 'Nombre: '   + self.nombre_cli.get(1.0, "end-1c") + '\n'
				texto_info+= 'Apellido: ' + self.apelli_cli.get(1.0, "end-1c") + '\n'
				texto_info+= 'Celular: '  + self.celular_cli.get(1.0, "end-1c") + '\n'
				texto_info+= u'Cédula: '  + self.cedula_cli.get(1.0, "end-1c")

				self.valida_clientes = self.otra_ventana(self.ventana_alimclientes, '450x300+250+220', u'Valida Cliente', 230, 250, 'Cancelar')
				box_valida           = self.caja_texto(self.valida_clientes, 10, 40, 20, 25)
				box_valida.insert("1.0", texto_info)
				self.agrega_boton(self.valida_clientes, 'Validar Info', 100, 250, self.introduce_cli_db, pad=(3,3))
				self.final_otra_ventana(self.valida_clientes, self.ventana_alimclientes)

			else:

				# ventana de notificacion de que el nombre o el apellido del cliente no fueron escritos
				self.notifica = self.otra_ventana(self.ventana_alimclientes, '+250+220', u'Notificacion Cliente', 0, 2, exitgrid=True)
				self.etiqueta(self.notifica, u'¡¡¡ERROR!!!', 0, 0, grid=True)
				self.etiqueta(self.notifica, u'Celular con caracteres inválidos. Sólo admite números.', 0, 1, grid=True)
				self.final_otra_ventana(self.notifica, self.ventana_alimclientes)

	# funcion para borrar los campos que se han introducido en el formulario para alimentar la bd de clientes

	def alimcli_del(self):

		self.nombre_cli.delete('1.0', END)
		self.apelli_cli.delete('1.0', END)
		self.celular_cli.delete('1.0', END)
		self.cedula_cli.delete('1.0', END)

	# Introduce la info en la base de datos

	def introduce_cli_db(self):

		nombre_cliente   = self.nombre_cli.get(1.0, "end-1c")
		apellido_cliente = self.apelli_cli.get(1.0, "end-1c")
		celular_cliente  = self.celular_cli.get(1.0, "end-1c")
		cedula_cliente   = self.cedula_cli.get(1.0, "end-1c")

		try:

			if	self.celular_cli_bool == True:

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
				db_cursor.execute("INSERT INTO clientes (nombre, celular, cedula) VALUES ('" + nombre_cliente + " " + apellido_cliente + "', " + celular_cliente + ", " + cedula_cliente + ");")
				db_cursor.close()
				db_conn.commit ()
				db_conn.close ()

			elif self.celular_cli_bool == False:

				db_conn    = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
				db_cursor  = db_conn.cursor()
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

		self.valida_clientes.destroy()
		self.alimcli_del()