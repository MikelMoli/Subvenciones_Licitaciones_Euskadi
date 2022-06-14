# Pasos a seguir

Terminar la extracción de datos de las webs de licitación.

# Planteamiento

Cada registro  de la webs tendrá los siguientes campos:
    
    {
        "ID": "...",
        "Poder Adjudicador": "...",
        "Ámbito": "...",
        "Entidad Impulsora": "...",
        "Órgano de Contratación": "...",
        "Entidad Tramitadora": "...",
        "Mesa de contratación": "...",
        "Tipo de poder": "...",
        "Otro tipo de poder": "...",
        "Actividad Principal": "...",
        "Otra Actividad Principal": "...",
        "El contrato es adjudicado por una central de compras": "...",
        "Obtención de documentación e información": "...",
        "Órgano de recurso": "...",
        "Servicio de información sobre recursos": "...",
    
        "Resumen Adjudicación": "...",
        "Num. licitadores presentados": "...",
        "Ofertas realizadas por PYMEs": "...",
        "Ofertas de países Union Europea": "...",
        "Ofertas terceros paises": "...",
        "Ofertas electronicas": "...",
        "Empresas Licitadoras": "...",
        "Datos de Adjudicación": "...",
        "URL": "..."
    }

# Casos a tener en cuenta:

- Dentro de las webs encontramos que la información no siempre es la misma. En algunos casos hay campos faltantes (ej. Num. licitadores presentados)
- Algunas webs tienen el link mal escrito o no existen (404)
- Hay registros sin web (www.example.com)


# Plan de ejecución

1. Realizar extracción de datos funcional para muestras muy pequeñas (10 registros) [ X ]

2. Realizar extracción de datos funcional para muestras pequeñas (100 registros) [ x ]

3. Añadir paralelización al scraping para acelerar la extracción completa [ - ]

4. Gestionar la extracción de manera resiliente y robusta. Para ello:
    
    - Guardar ficheros cada pocos registros (aprox. 10).
    - Si falla el scraping de esos datos se reintentará hasta 3 veces. 
    - En caso de que falle más de 3 veces los registros correspondientes a ese batch se guardarán. De esta manera se podrá realizar su extracción más tarde de manera independiente.

