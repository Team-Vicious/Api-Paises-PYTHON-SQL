import json
import requests
import pymysql


#conexión a la base de datos
db = pymysql.connect(autocommit=True,
            host='localhost',
			user='root',
			password='',
			db='ddbb_laboratorio')
print(db)

puntero= db.cursor()


for id in range(301):
        
        
    #obtengo el dato de la url
    datosUrl = requests.get('https://restcountries.eu/rest/v2/callingcode/'+str(id))

    if(datosUrl.status_code!=404):

         #lee el Json que trae con request y lo almacena en datosUrl        
        dato= json.loads(datosUrl.content)

         #ingreso los datos en sus respectivas tablas
        codigoPais = dato[0]['callingCodes'][0],
        nombrePais = dato[0]['name'],
        capitalPais = dato[0]['capital'],
        region = dato[0]['region'],
        poblacion= dato[0]['population'],
        latitud = dato[0]['latlng'][0],
        longitud = dato[0]['latlng'][1]

#ingreso las query
        pais = puntero.execute(
        "SELECT * FROM pais WHERE codigoPais = %s", codigoPais)

        if(pais):
            puntero.execute('UPDATE pais SET nombrePais= %s,capitalPais= %s,region=%s,poblacion= %s,latitud=%s,longitud=%s WHERE codigoPais = %s',
            (codigoPais,nombrePais, capitalPais, region, poblacion, latitud, longitud))
            print("Datos actualizados correctamente")
        else:
            puntero.execute('INSERT INTO pais(codigoPais,nombrePais,capitalPais,region,poblacion,latitud,longitud) values (%s,%s,%s,%s,%s,%s,%s)',
            (codigoPais,nombrePais, capitalPais, region, poblacion, latitud, longitud))
            print("Datos insertados correctamente")
        
         



