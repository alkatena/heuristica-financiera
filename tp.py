#
# Clase que representa un instrumento en el modelo
#
# Tiene atributo:
# - nombre
# - precio de compra al inicio de semana 1
# - precio de venta al final de semana 1
# - precio de compra al inicio de semana 2
# - precio de venta al final de semana 2
#
class Instrumento:
	#
	# Constructor de la clase
	#
	def __init__(self, nombre, PC1, PV1, PC2, PV2):
		self.nombre = nombre
		self.PC1 = PC1
		self.PV1 = PV1
		self.PC2 = PC2
		self.PV2 = PV2

	#
	# Comparador de igualdad
	#
	def __eq__(self, other):
		return self.nombre == other.nombre

	#
	# Conversor a string
	#
	def __str__():
		return self.nombre

	#
	# Devuelve la ganancia por compra venta en el subperiodo1 (en la semana 1)
	#
	def gananciaVentaSubperiodo1():
		return self.PV1 - self.PC1

	#
	# Devuelve la ganancia por compra venta en el subperiodo2 (en la semana 2)
	#
	def gananciaVentaSubperiodo2():
		return self.PV2 - self.PC2

	#
	# Devuelve la ganancia por compra venta en el periodo (en la semana 1 y 2)
	#
	def gananciaVentaPeriodo():
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

	#
	# Carga los datos de disco
	#
	def cargar():
		archivoDatos = open("datos.txt")
		archivoAcciones = open("acciones.txt")
		archivoBonos = open("bonos.txt")
		archivoFondos = open("fondos.txt")

		self.capitalMaximo = float(archivoDatos.readline())
		self.riesgoMaximo = float(archivoDatos.readline())
		self.comisionAcciones = float(archivoDatos.readline())
		self.comisionBonos = float(archivoDatos.readline())
		self.comisionFondos = float(archivoDatos.readline())

		self.listaAcciones.clear()
		self.listaCompraAcciones1.clear()
		self.listaCompraAcciones2.clear()
		self.listaVentaAcciones1.clear()
		self.listaVentaAcciones2.clear()
		self.stockAcciones.clear()
		for line in archivoAcciones:
			values = line.split("\t")
			instrumento = Instrumento(values[0], float(values[1]), float(values[2]), float(values[3]), float(values[4]))
			self.listaAcciones.append(instrumento)
			self.listaCompraAcciones1[instrumento] = 0
			self.listaCompraAcciones2[instrumento] = 0
			self.listaVentaAcciones1[instrumento] = 0
			self.listaVentaAcciones2[instrumento] = 0
			self.stockAcciones[instrumento] = 0


		self.listaBonos.clear()
		self.listaCompraBonos1.clear()
		self.listaCompraBonos2.clear()
		self.listaVentaBonos1.clear()
		self.listaVentaBonos2.clear()
		self.stockBonos.clear()
		for line in archivoBonos:
			values = line.split("\t")
			instrumento = Instrumento(values[0], float(values[1]), float(values[2]), float(values[3]), float(values[4]))
			self.listaBonos.append(instrumento)
			self.listaCompraBonos1[instrumento] = 0
			self.listaCompraBonos2[instrumento] = 0
			self.listaVentaBonos1[instrumento] = 0
			self.listaVentaBonos2[instrumento] = 0
			self.stockBonos[instrumento] = 0

		self.listaFondos.clear()
		self.listaCompraFondos1.clear()
		self.listaCompraFondos2.clear()
		self.listaVentaFondos1.clear()
		self.listaVentaFondos2.clear()
		self.stockFondos.clear()
		for line in archivoFondos:
			values = line.split("\t")
			instrumento = Instrumento(values[0], float(values[1]), float(values[2]), float(values[3]), float(values[4]))
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
	def comprarInstrumentosSemana1():
		return

	#
	# Compra instrumentos al comienzo de la semana 2
	#
	def comprarInstrumentosSemana2():
		return

	#
	# Vende instrumentos al final de la semana 1
	#
	def venderInstrumentosSemana1():
		return

	#
	# Vende instrumentos al final de la semana 2
	#
	def venderInstrumentosSemana2():
		return

	#
	# Calcula la maxima ganancia por ventas
	#
	def calcularMaximo():
		return

	#
	# Imprime la solucion
	#
	def imprimirSolucion():
		return
