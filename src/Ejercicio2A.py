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
			

