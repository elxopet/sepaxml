########################################################################
# Author: Antonio Vila Juan
# Update: 06/10/2015
#
# Parseador de Remesas SEPA en texto plano a XML
# Lee le fichero generado con cualquier programa de gestión en texto 
# plano.
# Genera la estructura para las remesas en formato XML
# Crea la carpeta tmp dentro del directorio de trabajo
# Mueve el fichero origen a la carpeta tmp una vez creado el xml.
#
########################################################################


import sys,os, os.path, shutil
from lxml import etree


def cargararraycabecera01(t): 
	cabecera[0] = t[123:158] 	# Identificacion del mensaje
	cabecera[1] = t[115:123] 	# Fecha y hora de creacion
	cabecera[4] = t[45:115]		# Nombre
	cabecera[6] = t[10:26]		# Identificacion
	
def parseartotal99(t):
	a = t[19:27]    # Numero de operaciones
	cabecera[2] = int(a)
	a = t[2:17]	+ "." + t[17:19]	# Control de suma
	cabecera[3] = float(a)
	
def parsearcabecera01():
	GrpHdr = etree.SubElement(CstmrPmtRvsl, "GrpHdr")
	MsgId = etree.SubElement(GrpHdr, "MsgId")
	CreDtTm = etree.SubElement(GrpHdr, "CreDtTm")
	NbOfTxs = etree.SubElement(GrpHdr, "NbOfTxs")
	CtrlSum = etree.SubElement(GrpHdr, "CtrlSum")
	InitgPty = etree.SubElement(GrpHdr, "InitgPty")
	Nm = etree.SubElement(InitgPty, "Nm")
	Id = etree.SubElement(InitgPty, "Id")
	OrgId = etree.SubElement(Id, "OrgId")
	Othr = etree.SubElement(OrgId, "Othr")
	Id = etree.SubElement(Othr, "Id")
	
	MsgId.text = cabecera[0].strip()
	CreDtTm.text = cabecera[1].strip()
	NbOfTxs.text = cabecera[2]
	CtrlSum.text = cabecera[3].strip()
	Nm.text = cabecera[4].strip()
	Id.text = cabecera[6].strip()
	
	
def parseardetalle03(t):
	PmtInf = etree.SubElement(CstmrPmtRvsl, "PmtInf")
	PmtInfId = etree.SubElement(PmtInf, "PmtInfId")
	PmtMtd = etree.SubElement(PmtInf, "PmtMtd")
	BtchBookg = etree.SubElement(PmtInf, "BtchBookg")
	PmtInfId.text = t[10:45].strip()
	PmtMtd.text = "DD"
	BtchBookg.text = "true"
	PmtTpInf = etree.SubElement(PmtInf, "PmtTpInf")
	SvcLvl = etree.SubElement(PmtTpInf, "SvcLvl")
	Cd = etree.SubElement(SvcLvl,"Cd")
	Cd.text ="SEPA"
	LclInstrm = etree.SubElement(PmtTpInf, "LclInstrm")
	Cd = etree.SubElement(LclInstrm, "Cd")
	Cd.text ="COR1"
	SeqTp = etree.SubElement(PmtTpInf, "SeqTp")
	SeqTp.text = t[80:84].strip()
	ReqdColltnDt = etree.SubElement(PmtInf, "ReqdColltnDt")
	ReqdColltnDt.text = t[99:103] + "-" + t[103:105] + "-" + t[105:107]
	CdTr = etree.SubElement(PmtInf, "CdTr")
	Nm = etree.SubElement(CdTr, "Nm")
	Nm.text = t[118:188].strip()
	PstlAdr = etree.SubElement(CdTr, "PstlAdr")
	Ctry = etree.SubElement(PstlAdr, "Ctry")
	Ctry.text = t[328:330]
	AdrLine = etree.SubElement(PstlAdr, "AdrLine")
	AdrLine.text = t[188:238].strip()
	CdtrAcct = etree.SubElement(PmtInf, "CdtrAcct")
	Id = etree.SubElement(CdtrAcct, "Id")
	IBAN = etree.SubElement(Id, "IBAN")
	IBAN.text = t[403:437].strip()
	Ccy = etree.SubElement(CdtrAcct, "Ccy")
	Ccy.text = "EUR"
	CdtrAgt = etree.SubElement(PmtInf, "CdtrAgt")
	FinInstnId = etree.SubElement(CdtrAgt, "FinInstnId")
	BIC = etree.SubElement(FinInstnId, "BIC")
	BIC.text = "NOTPROVIDED"
	ChrgBr = etree.SubElement(PmtInf, "ChrgBr")
	ChrgBr.text = "SLEV"
	CdtrSchmeId = etree.SubElement(PmtInf, "CdtrSchmeId")
	Id = etree.SubElement(CdtrSchmeId, "Id")
	PrvtId = etree.SubElement(Id, "PrvtId")
	Othr = etree.SubElement(PrvtId, "Othr")
	Id = etree.SubElement(Othr, "Id")
	Id.text = cabecera[6].strip()
	SchmeNm = etree.SubElement(Othr, "SchmeNm")
	Prtry = etree.SubElement(SchmeNm, "Prtry")
	Prtry.text = "SEPA"
	DrctDbtTxInf = etree.SubElement(PmtInf, "DrctDbtTxInf")
	PmtId = etree.SubElement(DrctDbtTxInf, "PmtId")
	InstrId = etree.SubElement(PmtId, "InstrId")
	InstrId.text = t[26:40] + "-" + t[40:45]
	EndToEndId = etree.SubElement(PmtId, "EndToEndId")
	EndToEndId.text = t[10:45].strip()
	InstdAmt = etree.SubElement(DrctDbtTxInf, "InstdAmt") # Anyadir Ccy = "EUR"
	InstdAmt.text = t[88:99].strip()
	DrctDbtTx = etree.SubElement(DrctDbtTxInf, "DrctDbtTx")
	MndtRltdInf = etree.SubElement(DrctDbtTx, "MndtRltdInf")
	MndtId = etree.SubElement(MndtRltdInf,"MndtId")
	MndtId.text = t[45:54].strip()
	DtOfSgntr = etree.SubElement(DrctDbtTx, "DtOfSgntr")
	DtOfSgntr.text = t[99:103]+"-"+t[103:105]+"-"+t[105:107]
	AmdmntInd = etree.SubElement(DrctDbtTx, "AmdmntInd")
	AmdmntInd.text = "false"
	DbtrAgt = etree.SubElement(DrctDbtTxInf, "DbtrAgt")
	FinInstnId = etree.SubElement(DbtrAgt, "FinInstnId")
	Othr = etree.SubElement(FinInstnId, "Othr")
	Id = etree.SubElement(Othr, "Id")
	Id.text = "NOTPROVIDED"
	Dbtr = etree.SubElement(DrctDbtTxInf, "Dbtr")
	Nm = etree.SubElement(Dbtr, "Nm")
	Nm.text = t[118:188].strip()
	PstlAdr = etree.SubElement(Dbtr, "PstlAdr")
	Ctry = etree.SubElement(PstlAdr, "Ctry")
	Ctry.text = t[328:330].strip()
	AdrLine = etree.SubElement(PstlAdr, "AdrLine")
	AdrLine.text = t[188:238].strip()
	DbtrAcct = etree.SubElement(DrctDbtTxInf, "DbtrAcct")
	Id = etree.SubElement(DbtrAcct, "Id")
	IBAN = etree.SubElement(Id, "IBAN")
	IBAN.text = t[403:437].strip()
	RmtInf = etree.SubElement(DrctDbtTxInf, "RmtInf")
	Ustrd = etree.SubElement(RmtInf, "Ustrd")
	Ustrd.text = t[441:581].strip()
	
# Se carga el nombre del fichero txt
fichero = sys.argv[1]
	
# Se inicializa el array
cabecera = [""] * 17

# Se inicializa la variable root que es la que almacenara todo el xml
root = etree.Element("Document")
CstmrPmtRvsl = etree.SubElement(root, "CstmrPmtRvsl")



# Se abre el fichero para leer la primera vez
f = open(fichero)
lines = f.readlines()

#------------------------------------------------------------------------------
# Se leen las lineas una a una la primera vez para cargar la cabecera
#------------------------------------------------------------------------------
for l in lines:
	if l[:2] == "01":
		cargararraycabecera01(l)
	elif l[:2] == '99':
		parseartotal99(l)
# Se leen las lineas una a una la primera vez para cargar la cabecera		
		
# Se mueven los datos del array a xml
parsearcabecera01()	
# Se abre el fichero para leer la segunda vez
f = open("sepa.txt")
lines = f.readlines()
#------------------------------------------------------------------------------
# Se leen las lineas una a una la segunda vez para grabar el detalle
#------------------------------------------------------------------------------
for l in lines:
	if l[:2] == '03':
		parseardetalle03(l)
# Se leen las lineas una a una la segunda vez para grabar el detalle		
		
# Se graba el fichero de salida xml

if (os.path.isdir("tmp")):
	print "exite tmp"
else:
	print "no existe el directorio tmp"
	os.mkdir("tmp")

tree = etree.ElementTree(root)

# Se crea el nombre del fichero de salida.
salida = fichero[0:len(fichero)-4] + ".xml"
tree.write(salida, pretty_print=True)

# Se mueve el fichero txt a tmp
shutil.move(fichero, "tmp"+"/"+fichero)


	
	
