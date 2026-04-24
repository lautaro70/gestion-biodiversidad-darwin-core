# Dataset iNaturalist

## Información General
- **Nombre del Dataset:** iNaturalist Research-grade Observations
- **Institución Proveedora:** iNaturalist
- **Cantidad de registros:** No especifica
- **Cobertura temporal:** desde 17-09-1768 hasta 16-02-2026
- **Separador de campos utilizado en los archivos:** ","
- **Codificación de caracteres (encoding):** UTF-8
- **Tipo de licencia:** Creative Commons Attribution-NonCommercial License
- **Frecuencia de actualización:**  semanal
- **Cobertura Geografica:** Global 

## Archivos del dataset
- **observations.csv:** archivo principal con los registros de observaciones de especies
- **media.csv:** imágenes asociadas a cada observación
- **dna_derived_data.csv:** debería contener secuencias de ADN asociadas a observaciones, pero contiene registros de imágenes como los de media.csv
- **eml.xml:** descripción general del dataset, licencia y cobertura
- **meta.xml:** describe la estructura de los archivos y cómo interpretarlos

## Descripción de atributos

|Atributo | Descripción |  Ejemplo |
|---|---|---|
|id | Identificador numerico único del registro | 42369866 |
|ocurrenceID | URL única que identifica la observación | https://www.inaturalist.org/observations/42369866 |
|basisOfRecord | Tipo de registro (como se obtuvo) | HumanObservation |
|modified | Fecha de última Modifcación | 2020-10-27T19:46:33Z |
|institutionCode | Código de la Institución | iNaturalist |
|collectionCode | Nombre de la colección | Observations |
|datasetName | Nombre del Dataset | iNaturalist research-grade observations |
|informationWithheld | Información omitida por privacidad | Coordinate uncertainty increased to 29304m |
|catalogNumber | Número de catálogo del registro | 42369866 |
|references | URL de referencia de la observación | https://www.inaturalist.org/observations/42369866 |
|ocurrenceRemarks | Comentarios sobre la observación | no hay |
|recordedBy | nombre del observador  | Pablo H Capovilla |
|recordedByID | ID del observador | https://orcid.org/0000-0003-0179-3180 |
|identifiedBy | nombre de quien identificó la especie | Pablo H Capovilla |
|identifiedByID | ID de quien identificó la especie | https://orcid.org/0000-0003-0179-3180 |
|captive | Indica si el organismo es silvestre o cautivo | wild |
|eventDate | Fecha y Hora de la observación | 2018-03-31T08:09:00-03:00 |
|eventTime | Hora de la observación | 08:09:00-03:00 |
|verbatimEventDate | Fecha en formato original del observador | 2018/03/31 8:09 AM -0300 |
|verbatimLocality | Descripcion textual del lugar | Gral Obligado, Santa Fe, Argentina |
|decimalLatitude | Latitud en decimales | -28.5015951692 |
|decimalLongitude | Longitud en decimales | -59.2650295264 |
|coordinateUncertaintyInMeters | Incertidumbre de la coordenada en metros | 15 | 
|geodeticDatum | Sistema de referencia de coordenadas | EPSG:4326 |
|countryCode | Código del país | AR |
|stateProvince | Provincia o estado | Santa Fe |
|identificationID | Identificador de la identificación taxonómica | 95899387 |
|dateIdentified | Fecha en que se identificó la especie | 2020-04-17T04:09:14Z |
|identificationRemarks |  Comentarios sobre la identificación | no hay |
|taxonID | Identificador numérico del taxón | 15764 |
|scientificName | Nombre científico de la especie | Thamnophilus doliatus |
|taxonRank | Rango taxonómico | species |
|kingdom | Reino | Animalia |
|phylum | Filo | Chordata |
|class | Clase | Aves |
|order | Orden | Passeriformes |
|family | Familia | Thamnophilidae |
|genus | Género | Thamnophilus |
|license | Licencia del registro | https://creativecommons.org/licenses/by/4.0/ |
|rightsHolder | Titular de los derechos | Pablo H Capovilla |
|inaturalistLogin | Usuario de iNaturalist del observador | pablohcapovilla |
|publishingCountry | País publicador | AR |
|projectId | Proyecto de iNaturalist asociado | https://www.inaturalist.org/projects/global-roadkill-observations |
|sex | Sexo del organismo | male |
|lifeStage | Etapa de vida del organismo | adult |
|reproductiveCondition | Condición reproductiva | flowers |
|vitality | Estado vital del organismo | alive |
|dynamicProperties | Propiedades adicionales en formato JSON | {"evidenceOfPresence":"organism"} |