#
# Clase que representa un instrumento en el modelo
#
# Tiene atributo:
# - nombre
# - precio de compra al inicio de semana 1
# - precio de venta al final de semana 1
# - precio de compra al inicio de semana 2
# - precio de venta al final de semana 2
# - riesgo de venta
#
class Instrumento:
	#
	# Constructor de la clase
	#
	def __init__(self, nombre, PC1, PV1, PC2, PV2, riesgo):
		self.nombre = nombre
		self.PC1 = PC1
		self.PV1 = PV1
		self.PC2 = PC2
		self.PV2 = PV2
		self.riesgo = riesgo

	#
	# Comparador de igualdad
	#
	def __eq__(self, other):
		return self.nombre == other.nombre

	#
	# Metodo de hashing
	#
	def __hash__(self):
		return hash(self.nombre)

	#
	# Conversor a string
	#
	def __str__(self):
		return self.nombre

	#
	# Devuelve la ganancia por compra venta en el subperiodo1 (en la semana 1)
	#
	def gananciaVentaSubperiodo1(self):
		return self.PV1 - self.PC1

	#
	# Devuelve la ganancia por compra venta en el subperiodo2 (en la semana 2)
	#
	def gananciaVentaSubperiodo2(self):
		return self.PV2 - self.PC2

	#
	# Devuelve la ganancia por compra venta en el periodo (en la semana 1 y 2)
	#
	def gananciaVentaPeriodo(self):
		return self.PV2 - self.PC1

#
# Comparador de instrumentos que ordena por mayor a menor ganancia usando el maximo entre subperiodo1 y periodo
#
def comparador1(instrumento1, instrumento2):
	ganancia1 = max(instrumento1.gananciaVentaSubperiodo1(), instrumento1.gananciaVentaPeriodo())
	ganancia2 = max(instrumento2.gananciaVentaSubperiodo1(), instrumento2.gananciaVentaPeriodo())

	if (ganancia1 < ganancia2):
		return -1
	else:
		if (ganancia1 > ganancia2):
			return 1
		else:
			return cmp(instrumento1.nombre, instrumento2.nombre)

#
# Comparador de instrumentos que ordena por mayor a menor ganancia usando el subperiodo2
#
def comparador2(instrumento1, instrumento2):
	ganancia1 = instrumento1.gananciaVentaSubperiodo2()
	ganancia2 = instrumento2.gananciaVentaSubperiodo2()

	if (ganancia1 < ganancia2):
		return -1
	else:
		if (ganancia1 > ganancia2):
			return 1
		else:
			return cmp(instrumento1.nombre, instrumento2.nombre)

#
# Clase que representa la heuristica del modelo
#
# Tiene como atributos:
#
# - capital maximo
# - riesgo maximo
# - comision acciones
# - comision bonos
# - comision fondos
#
# - lista de acciones
# - lista de bonos
# - lista de fondos
# - lista de compra de acciones en semana 1
# - lista de compra de acciones en semana 2
# - lista de compra de bonos en semana 1
# - lista de compra de bonos en semana 2
# - lista de compra de fondos en semana 1
# - lista de compra de fondos en semana 2
# - lista de venta de acciones en semana 1
# - lista de venta de acciones en semana 2
# - lista de venta de bonos en semana 1
# - lista de venta de bonos en semana 2
# - lista de venta de fondos en semana 1
# - lista de venta de fondos en semana 2
#
# - stock de acciones
# - stock de bonos
# - stock de fondos
#
class Heuristica:
	#
	# Constructor de la clase
	#
	def __init__(self):
		self.capitalMaximo = 0
		self.riesgoMaximo = 0
		self.comisionAcciones = 0
		self.comisionBonos = 0
		self.comisionFondos = 0

		self.listaAcciones = []
		self.listaBonos = []
		self.listaFondos = []

		self.listaCompraAcciones1 = {}
		self.listaCompraAcciones2 = {}
		self.listaCompraBonos1 = {}
		self.listaCompraBonos2 = {}
		self.listaCompraFondos1 = {}
		self.listaCompraFondos2 = {}
		self.listaVentaAcciones1 = {}
		self.listaVentaAcciones2 = {}
		self.listaVentaBonos1 = {}
		self.listaVentaBonos2 = {}
		self.listaVentaFondos1 = {}
		self.listaVentaFondos2 = {}

		self.stockAcciones = {}
		self.stockBonos = {}
		self.stockFondos = {}
		self.sobrante = 0
		self.maximo = 0
		self.capitalDisponiblePeriodo2 = 0

	#
	# Carga los datos de disco
	#
	def cargar(self):
		archivoDatos = open("datos.txt")
		archivoAcciones = open("acciones.txt")
		archivoBonos = open("bonos.txt")
		archivoFondos = open("fondos.txt")

		self.maximo = 0;
		self.sobrante = 0;

		self.capitalMaximo = float(archivoDatos.readline())
		self.riesgoMaximo = float(archivoDatos.readline())
		self.comisionAcciones = float(archivoDatos.readline())
		self.comisionBonos = float(archivoDatos.readline())
		self.comisionFondos = float(archivoDatos.readline())

		self.listaAcciones = []
		self.listaCompraAcciones1 = {}
		self.listaCompraAcciones2 = {}
		self.listaVentaAcciones1 = {}
		self.listaVentaAcciones2 = {}
		self.stockAcciones = {}
		for line in archivoAcciones:
			values = line.split("\t")
			if (len(values) < 6):
				print "Datos invalidos"
				continue
			instrumento = Instrumento(values[0], float(values[1]), float(values[2]), float(values[3]), float(values[4]), float(values[5]))

			self.listaAcciones.append(instrumento)
			self.listaCompraAcciones1[instrumento] = 0
			self.listaCompraAcciones2[instrumento] = 0
			self.listaVentaAcciones1[instrumento] = 0
			self.listaVentaAcciones2[instrumento] = 0
			self.stockAcciones[instrumento] = 0


		self.listaBonos = []
		self.listaCompraBonos1 = {}
		self.listaCompraBonos2 = {}
		self.listaVentaBonos1 = {}
		self.listaVentaBonos2 = {}
		self.stockBonos = {}
		for line in archivoBonos:
			values = line.split("\t")
			if (len(values) < 6):
				print "Datos invalidos"
				continue
			instrumento = Instrumento(values[0], float(values[1]), float(values[2]), float(values[3]), float(values[4]), float(values[5]))

			self.listaBonos.append(instrumento)
			self.listaCompraBonos1[instrumento] = 0
			self.listaCompraBonos2[instrumento] = 0
			self.listaVentaBonos1[instrumento] = 0
			self.listaVentaBonos2[instrumento] = 0
			self.stockBonos[instrumento] = 0

		self.listaFondos = []
		self.listaCompraFondos1 = {}
		self.listaCompraFondos2 = {}
		self.listaVentaFondos1 = {}
		self.listaVentaFondos2 = {}
		self.stockFondos = {}
		for line in archivoFondos:
			values = line.split("\t")
			if (len(values) < 6):
				print "Datos invalidos"
				continue
			instrumento = Instrumento(values[0], float(values[1]), float(values[2]), float(values[3]), float(values[4]), float(values[5]))

			self.listaFondos.append(instrumento)
			self.listaCompraFondos1[instrumento] = 0
			self.listaCompraFondos2[instrumento] = 0
			self.listaVentaFondos1[instrumento] = 0
			self.listaVentaFondos2[instrumento] = 0
			self.stockFondos[instrumento] = 0

		archivoDatos.close()
		archivoAcciones.close()
		archivoBonos.close()
		archivoFondos.close()

	#
	# Compra instrumentos al comienzo de la semana 1
	#
	def comprarInstrumentosSemana1(self):
		gastadoAcciones = self.comprarInstrumentoSemana1("acciones", self.listaAcciones, 10)
		gastadoBonos = self.comprarInstrumentoSemana1("bonos", self.listaBonos, 20)
		gastadoFondos = self.comprarInstrumentoSemana1("fondos", self.listaFondos, 30)
		return gastadoFondos + gastadoBonos + gastadoAcciones

	def comprarInstrumentoSemana1(self, tipoInstrumento, listaInstrumentosDisponibles, porcentajeMinimo):
		capitalMinimoInstrumento = self.capitalMaximo * porcentajeMinimo / 100
		listaOrdenada = sorted(listaInstrumentosDisponibles, cmp=comparador1, reverse=True)
		acumuladoCompra = 0
		listaCompraInstrumentos = {}
		if tipoInstrumento == "acciones":
			listaCompraInstrumentos = self.listaCompraAcciones1
		elif tipoInstrumento == "bonos":
			listaCompraInstrumentos = self.listaCompraBonos1
		elif tipoInstrumento == "fondos":
			listaCompraInstrumentos = self.listaCompraFondos1

		for instrumento in listaOrdenada:
			#print ("BENEFICIO DEL ACCION %s: %d" % (instrumento.nombre, max(instrumento.gananciaVentaSubperiodo1(), instrumento.gananciaVentaPeriodo())))
			if (acumuladoCompra > capitalMinimoInstrumento):
				break
			if (instrumento.riesgo > self.riesgoMaximo):
				continue
			while (acumuladoCompra <= capitalMinimoInstrumento):
				# Si comprando ese instrumento me paso de lo que tengo disponible, paso al siguiente instrumento
				if (instrumento.PC1 > self.capitalMaximo - acumuladoCompra):
					break
				acumuladoCompra += instrumento.PC1
				listaCompraInstrumentos[instrumento] += 1
			if (listaCompraInstrumentos[instrumento] > 0):
				print "[PERIODO 1 - COMPRA] INSTRUMENTO %s TOTAL GASTADO: %d" % (instrumento.nombre , acumuladoCompra)
		return acumuladoCompra

	def comprarInstrumentoSemana2(self, tipoInstrumento, listaInstrumentosDisponibles, porcentajeMinimo):
		capitalMinimoInstrumento = self.capitalDisponiblePeriodo2 * porcentajeMinimo / 100
		listaOrdenada = sorted(listaInstrumentosDisponibles, cmp=comparador2, reverse=True)
		acumuladoCompra = 0
		listaCompraInstrumentos = {}
		stockInstrumento = {}
		if tipoInstrumento == "acciones":
			listaCompraInstrumentos = self.listaCompraAcciones2
			stockInstrumento = self.stockAcciones
		elif tipoInstrumento == "bonos":
			listaCompraInstrumentos = self.listaCompraBonos2
			stockInstrumento = self.stockBonos
		elif tipoInstrumento == "fondos":
			listaCompraInstrumentos = self.listaCompraFondos2
			stockInstrumento = self.stockFondos


		for instrumento in listaOrdenada:
			#print ("BENEFICIO DEL ACCION %s: %d" % (instrumento.nombre, max(instrumento.gananciaVentaSubperiodo1(), instrumento.gananciaVentaPeriodo())))
			if (acumuladoCompra + stockInstrumento[instrumento] > capitalMinimoInstrumento):
				break
			if (instrumento.riesgo > self.riesgoMaximo):
				continue
			while (acumuladoCompra <= capitalMinimoInstrumento):
				# Si comprando ese instrumento me paso de lo que tengo disponible, paso al siguiente instrumento
				if (instrumento.PC1 > self.capitalMaximo - acumuladoCompra):
					break
				acumuladoCompra += instrumento.PC1
				listaCompraInstrumentos[instrumento] += 1
			if (listaCompraInstrumentos[instrumento] > 0):
				print "[PERIODO 2 - COMPRA] INSTRUMENTO %s TOTAL GASTADO: %d" % (instrumento.nombre , acumuladoCompra)
		return acumuladoCompra

	#
	# Compra instrumentos al comienzo de la semana 2
	#
	def comprarInstrumentosSemana2(self):
		gastadoAcciones = self.comprarInstrumentoSemana2("acciones", self.listaAcciones, 10)
		gastadoBonos = self.comprarInstrumentoSemana2("bonos", self.listaBonos, 20)
		gastadoFondos = self.comprarInstrumentoSemana2("fondos", self.listaFondos, 30)
		return gastadoFondos + gastadoBonos + gastadoAcciones

	#
	# Vende instrumentos al final de la semana 1
	#
	def venderInstrumentoSemana1(self, tipoInstrumento):
		acumuladoVenta = 0
		listaVentaInstrumento = {}
		stockInstrumento = {}
		listaCompraInstrumentos = {}
		if tipoInstrumento == "acciones":
			listaCompraInstrumentos = self.listaCompraAcciones1
			listaVentaInstrumento = self.listaVentaAcciones1
			stockInstrumento = self.stockAcciones
		elif tipoInstrumento == "bonos":
			listaCompraInstrumentos = self.listaCompraBonos1
			listaVentaInstrumento = self.listaVentaBonos1
			stockInstrumento = self.stockBonos
		elif tipoInstrumento == "fondos":
			listaCompraInstrumentos = self.listaCompraFondos1
			listaVentaInstrumento = self.listaVentaFondos1
			stockInstrumento = self.stockFondos

		for instrumento in listaCompraInstrumentos:
			# Recorremos la lista de instrumentos, a los que compramos vemos si conviene venderlos. de ser asi, lo agregamos a la lista de vendidos. caso contrario quedan en la lista de stock
			#print "[PERIODO 1 - VENTA] INSTRUMENTO %s GANANCIA SUBPERIODO1: %d  GANANCIA SUBPERIODO2: %d" % (instrumento.nombre , instrumento.gananciaVentaSubperiodo1(), instrumento.gananciaVentaSubperiodo2())

			if (listaCompraInstrumentos[instrumento] > 0 and instrumento.gananciaVentaSubperiodo1() > instrumento.gananciaVentaSubperiodo2()):
				listaVentaInstrumento[instrumento] = listaCompraInstrumentos[instrumento]
				acumuladoVenta += instrumento.PV1 * listaCompraInstrumentos[instrumento]
				stockInstrumento[instrumento] = 0
				print "[PERIODO 1 - VENTA] INSTRUMENTO %s TOTAL OBTENIDO: %d" % (instrumento.nombre , acumuladoVenta)
			elif (listaCompraInstrumentos[instrumento] > 0):
				print "[PERIODO 1 - VENTA] STOCKEAMOS INSTRUMENTO %s CANTIDAD: %d" % (instrumento.nombre , listaCompraInstrumentos[instrumento])
				stockInstrumento[instrumento] = listaCompraInstrumentos[instrumento]
		return acumuladoVenta

	def venderInstrumentoSemana2(self, tipoInstrumento):
		acumuladoVenta = 0
		listaVentaInstrumento = {}
		listaCompraInstrumentos = {}
		stockInstrumentos = {}

		if tipoInstrumento == "acciones":
			listaCompraInstrumentos = self.listaCompraAcciones2
			listaVentaInstrumento = self.listaVentaAcciones2
			stockInstrumentos = self.stockAcciones
		elif tipoInstrumento == "bonos":
			listaCompraInstrumentos = self.listaCompraBonos2
			listaVentaInstrumento = self.listaVentaBonos2
			stockInstrumentos = self.stockBonos
		elif tipoInstrumento == "fondos":
			listaCompraInstrumentos = self.listaCompraFondos2
			listaVentaInstrumento = self.listaVentaFondos2
			stockInstrumentos = self.stockFondos

		for instrumento in listaCompraInstrumentos:
			# Recorremos la lista de instrumentos, a los que compramos vemos si conviene venderlos. de ser asi, lo agregamos a la lista de vendidos. caso contrario quedan en la lista de stock
			#print "[PERIODO 1 - VENTA] INSTRUMENTO %s GANANCIA SUBPERIODO1: %d  GANANCIA SUBPERIODO2: %d" % (instrumento.nombre , instrumento.gananciaVentaSubperiodo1(), instrumento.gananciaVentaSubperiodo2())
			if (listaCompraInstrumentos[instrumento] > 0):
				acumuladoVenta += listaCompraInstrumentos[instrumento] * instrumento.PV2
				listaVentaInstrumento[instrumento] = listaCompraInstrumentos[instrumento]
				print "[PERIODO 2 - VENTA] INSTRUMENTO %s TOTAL OBTENIDO %d" % (instrumento.nombre , listaCompraInstrumentos[instrumento] * instrumento.PV2)
		
		for instrumento in stockInstrumentos:
			if (stockInstrumentos[instrumento] > 0):
				acumuladoVenta += stockInstrumentos[instrumento] * instrumento.PV2
				listaVentaInstrumento[instrumento] = stockInstrumentos[instrumento]
				print "[PERIODO 2 - VENTA STOCK] INSTRUMENTO %s TOTAL OBTENIDO: %d" % (instrumento.nombre , stockInstrumentos[instrumento] * instrumento.PV2)

		return acumuladoVenta

	#
	# Vende instrumentos al final de la semana 2
	#
	def venderInstrumentosSemana2(self):
		obtenidoAcciones = self.venderInstrumentoSemana2("acciones")
		obtenidoBonos = self.venderInstrumentoSemana2("bonos")
		obtenidoFondos = self.venderInstrumentoSemana2("fondos")
		return obtenidoFondos + obtenidoBonos + obtenidoAcciones

	def venderInstrumentosSemana1(self):
		obtenidoAcciones = self.venderInstrumentoSemana1("acciones")
		obtenidoBonos = self.venderInstrumentoSemana1("bonos")
		obtenidoFondos = self.venderInstrumentoSemana1("fondos")
		return obtenidoFondos + obtenidoBonos + obtenidoAcciones

	#
	# Calcula la maxima ganancia por ventas
	#
	def calcularFuncional(self):
		maximo = 0

		for k in self.listaCompraAcciones1:
			cantidad = self.listaCompraAcciones1[k]
			maximo -= cantidad * k.PC1
			maximo -= self.comisionAcciones * cantidad * k.PC1

		for k in self.listaCompraBonos1:
			cantidad = self.listaCompraBonos1[k]
			maximo -= cantidad * k.PC1
			maximo -= self.comisionBonos * cantidad * k.PC1

		for k in self.listaCompraFondos1:
			cantidad = self.listaCompraFondos1[k]
			maximo -= cantidad * k.PC1
			maximo -= self.comisionFondos * cantidad * k.PC1

		for k in self.listaCompraAcciones2:
			cantidad = self.listaCompraAcciones2[k]
			maximo -= cantidad * k.PC2
			maximo -= self.comisionAcciones * cantidad * k.PC2

		for k in self.listaCompraBonos2:
			cantidad = self.listaCompraBonos2[k]
			maximo -= cantidad * k.PC2
			maximo -= self.comisionBonos * cantidad * k.PC2

		for k in self.listaCompraFondos2:
			cantidad = self.listaCompraFondos2[k]
			maximo -= cantidad * k.PC2
			maximo -= self.comisionFondos * cantidad * k.PC2

		for k in self.listaVentaAcciones1:
			cantidad = self.listaVentaAcciones1[k]
			maximo += cantidad * k.PV1
			maximo -= self.comisionAcciones * cantidad * k.PV1

		for k in self.listaVentaBonos1:
			cantidad = self.listaVentaBonos1[k]
			maximo += cantidad * k.PV1
			maximo -= self.comisionBonos * cantidad * k.PV1

		for k in self.listaVentaFondos1:
			cantidad = self.listaVentaFondos1[k]
			maximo += cantidad * k.PV1
			maximo -= self.comisionFondos * cantidad * k.PV1

		for k in self.listaVentaAcciones2:
			cantidad = self.listaVentaAcciones2[k]
			maximo += cantidad * k.PV2
			maximo -= self.comisionAcciones * cantidad * k.PV2

		for k in self.listaVentaBonos2:
			cantidad = self.listaVentaBonos2[k]
			maximo += cantidad * k.PV2
			maximo -= self.comisionBonos * cantidad * k.PC2

		for k in self.listaVentaFondos2:
			cantidad = self.listaVentaFondos2[k]
			maximo += cantidad * k.PV2
			maximo -= self.comisionFondos * cantidad * k.PV2

		return maximo

	#
	# Imprime la solucion
	#
	def imprimirSolucion(self):
		print ""
		print "---------------------------------"
		print ""
		print "EN LA PRIMER SEMANA SE RECOMIENDA"

		for k in self.listaCompraAcciones1:
			cantidad = self.listaCompraAcciones1[k]
			if (cantidad > 0):
				print "COMPRAR %s UNIDADES DE ACCION %s" %(cantidad, k.nombre)
		for k in self.listaCompraBonos1:
			cantidad = self.listaCompraBonos1[k]
			if (cantidad > 0):
				print "COMPRAR %s UNIDADES DE BONO %s" %(cantidad, k.nombre)
		for k in self.listaCompraFondos1:
			cantidad = self.listaCompraFondos1[k]
			if (cantidad > 0):
				print "COMPRAR %s UNIDADES DE FONDO %s" %(cantidad, k.nombre)
		for k in self.listaVentaAcciones1:
			cantidad = self.listaVentaAcciones1[k]
			if (cantidad > 0):
				print "VENDER %s UNIDADES DE ACCION %s" %(cantidad, k.nombre)
		for k in self.listaVentaBonos1:
			cantidad = self.listaVentaBonos1[k]
			if (cantidad > 0):
				print "VENDER %s UNIDADES DE BONO %s" %(cantidad, k.nombre)
		for k in self.listaVentaFondos1:
			cantidad = self.listaVentaFondos1[k]
			if (cantidad > 0):
				print "VENDER %s UNIDADES DE FONDO %s" %(cantidad, k.nombre)

		print ""
		print "EN LA SEGUNDA SEMANA SE RECOMIENDA"

		for k in self.listaCompraAcciones2:
			cantidad = self.listaCompraAcciones2[k]
			if (cantidad > 0):
				print "COMPRAR %s UNIDADES DE ACCION %s" %(cantidad, k.nombre)
		for k in self.listaCompraBonos2:
			cantidad = self.listaCompraBonos2[k]
			if (cantidad > 0):
				print "COMPRAR %s UNIDADES DE BONO %s" %(cantidad, k.nombre)
		for k in self.listaCompraFondos2:
			cantidad = self.listaCompraFondos2[k]
			if (cantidad > 0):
				print "COMPRAR %s UNIDADES DE FONDO %s" %(cantidad, k.nombre)
		for k in self.listaVentaAcciones2:
			cantidad = self.listaVentaAcciones2[k]
			if (cantidad > 0):
				print "VENDER %s UNIDADES DE ACCION %s" %(cantidad, k.nombre)
		for k in self.listaVentaBonos2:
			cantidad = self.listaVentaBonos2[k]
			if (cantidad > 0):
				print "VENDER %s UNIDADES DE BONO %s" %(cantidad, k.nombre)
		for k in self.listaVentaFondos2:
			cantidad = self.listaVentaFondos2[k]
			if (cantidad > 0):
				print "VENDER %s UNIDADES DE FONDO %s" %(cantidad, k.nombre)

		print ""
		print "ENTRE SEMANAS SE RECOMIENDA GUARDAR EL SIGUIENTE STOCK"

		for k in self.stockAcciones:
			cantidad = self.stockAcciones[k]
			if (cantidad > 0):
				print "%s UNIDADES DE STOCK DE ACCION %s" % (cantidad, k.nombre)
		for k in self.stockBonos:
			cantidad = self.stockBonos[k]
			if (cantidad > 0):
				print "%s UNIDADES DE STOCK DE BONO %s" % (cantidad, k.nombre)
		for k in self.stockFondos:
			cantidad = self.stockFondos[k]
			if (cantidad > 0):
				print "%s UNIDADES DE STOCK DE FONDO %s" % (cantidad, k.nombre)
		print ""
		print "LA MAXIMA GANANCIA POR VENTAS ES: %s" % self.maximo

		return

	def ejecutar(self):
		self.cargar()
		totalGastadoSemana1 = self.comprarInstrumentosSemana1()
		totalVendidoSemana1 = self.venderInstrumentosSemana1()
		self.capitalDisponiblePeriodo2 = self.capitalMaximo - totalGastadoSemana1 + totalVendidoSemana1
		print "CAPITAL DISPONIBLE LUEGO DEL PRIMER PERIODO %d" % self.capitalDisponiblePeriodo2
		totalGastadoSemana2 = self.comprarInstrumentosSemana2()
		totalVendidoSemana2 = self.venderInstrumentosSemana2()
		print "CAPITAL DISPONIBLE LUEGO DEL SEGUNDO PERIODO %d" % (self.capitalDisponiblePeriodo2 - totalGastadoSemana2 + totalVendidoSemana2)
		self.maximo = self.calcularFuncional()
		self.imprimirSolucion()

heuristica = Heuristica()
heuristica.ejecutar()

