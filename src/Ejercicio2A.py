from pathlib import Path
import csv

def mostrar_primeras_filas_Conicet ():
	base = Path(__file__).parent 
	ruta = base.parent / 'raw_datasets' / 'IADIZA-CONICET' / 'IADIZA-CONICET' / 'occurrence.txt'
	with open(ruta, 'r') as Conicet_dataset:
		csv_reader_Conicet = csv.reader(Conicet_dataset, delimiter='\t')
		header = next(csv_reader_Conicet)
		
		for i,row in enumerate(csv_reader_Conicet):
			print (row)
			if i >= 9:
				break
			
def mostrar_primeras_filas_Inaturalist ():
	base = Path(__file__).parent 
	ruta = base.parent / 'raw_datasets' / 'Inaturalist' / 'Inaturalist' / 'observations.csv'
	with open(ruta, 'r') as Inaturalist_dataset:
		csv_reader_Inaturalist = csv.reader(Inaturalist_dataset, delimiter=',')
		header = next(csv_reader_Inaturalist)
		
		for i,row in enumerate(csv_reader_Inaturalist):
			print (row)
			if i >= 9:
				break

def mostrar_primeras_filas_XenoCanto ():
	base = Path(__file__).parent 
	ruta = base.parent / 'raw_datasets' / 'XenoCanto' / 'XenoCanto' / 'Occurrence.txt'
	with open(ruta, 'r',encoding='utf-8') as XenoCanto_dataset:
		csv_reader_XenoCanto = csv.reader(XenoCanto_dataset, delimiter=',')
		header = next(csv_reader_XenoCanto)
		
		for i,row in enumerate(csv_reader_XenoCanto):
			print (row)
			if i >= 9:
				break

# INICIO DEL INCISO 2b 
#Hacer una funcion con las columnas de los datasets

def columnas_dataset(dataset): 
    base = Path(__file__).parent 
    
    if dataset == "IADIZA":
        ruta = base.parent / 'raw_datasets' / 'IADIZA-CONICET' / 'occurrence.txt'
        sep = '\t'
    elif dataset == "Inaturalist":
        ruta = base.parent / 'raw_datasets' / 'Inaturalist' / 'observations.csv'
        sep = ','
    elif dataset == "XenoCanto":
        ruta = base.parent / 'raw_datasets' / 'XenoCanto' / 'Occurrence.txt'
        sep = ','
    else:
        return "Dataset no reconocido"
    #EL encoding utf-8 es para que se lean los caracteres especiales 
    with open(ruta, 'r', encoding='utf-8') as archivo_abierto:
        lector_csv = csv.reader(archivo_abierto, delimiter=sep)
		#El lector agarra el archivo para que python lo entienda y lo separe con el separador
        columnas = next(lector_csv) 
		#El next devuelve la primera fila del dataset que mandamos para tener los nombres de las columnas
    return columnas

#print(columnas_dataset("IADIZA"))