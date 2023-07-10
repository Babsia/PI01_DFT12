# PI01-DT12
Sistema de Recomendación de Películas

## Descripción
Este proyecto consiste en desarrollar un sistema de recomendación de películas basado en la similitud de puntuación entre películas. El sistema utiliza un conjunto de datos de películas limpio y procesado previamente para realizar las recomendaciones. Además, se implementa una API utilizando el framework FastAPI para brindar acceso a las funcionalidades del sistema.

## Requerimientos de Aprobación
El proyecto cumple con los siguientes requerimientos:

### Transformaciones de Datos
Se realizaron las transformaciones necesarias en los datos, incluyendo desanidación de campos anidados, rellenado de valores nulos en los campos de revenue y budget, eliminación de valores nulos en el campo de release date, y creación de la columna de retorno de inversión.
Se eliminaron las columnas no utilizadas, como video, imdb_id, adult, original_title, poster_path y homepage.
### Desarrollo de la API
Se implementaron los siguientes endpoints en la API utilizando el framework FastAPI:

peliculas_idioma(Idioma: str): Recibe un idioma como parámetro y devuelve la cantidad de películas producidas en ese idioma.

peliculas_duracion(Pelicula: str): Recibe el nombre de una película como parámetro y devuelve la duración y el año de estreno de la película.

franquicia(Franquicia: str): Recibe el nombre de una franquicia como parámetro y devuelve la cantidad de películas, la ganancia total y la ganancia promedio de la franquicia.

peliculas_pais(Pais: str): Recibe el nombre de un país como parámetro y devuelve la cantidad de películas producidas en ese país.

productoras_exitosas(Productora: str): Recibe el nombre de una productora como parámetro y devuelve el total de ingresos y la cantidad de películas realizadas por la productora.

get_director(nombre_director): Recibe el nombre de un director y devuelve el éxito del director medido a través del retorno. También devuelve una lista de películas dirigidas por ese director, incluyendo la fecha de lanzamiento, retorno individual, costo y ganancia de cada película.

### Deployment
El sistema de recomendación de películas ha sido desplegado en la plataforma de Render para que pueda ser consumido desde la web. La API está disponible a través de la siguiente URL: https://pibabsia12.onrender.com/docs

### Sistema de Recomendación
Se entrenó un modelo de machine learning para construir un sistema de recomendación de películas. El modelo utiliza la similitud de puntuación entre películas para recomendar películas similares a los usuarios. Se implementó una función adicional en la API llamada recomendacion(titulo) que recibe el nombre de una película y devuelve una lista de las 5 películas más similares en orden descendente.

## Instrucciones de Uso
Accede a la URL de la API: https://pibabsia12.onrender.com/docs

Utiliza los diferentes endpoints de la API para obtener información y realizar consultas relacionadas con las películas.

Para utilizar la función de recomendación, llama al endpoint recomendacion(titulo) y proporciona el nombre de una película como parámetro. La API devolverá una 

lista con las 5 películas más similares a la proporcionada.

## Requisitos
Python 3.7 o superior.

Bibliotecas Python: FastAPI, pandas, scikit-learn, etc.

Acceso a Internet para consumir la API.
## Contribuciones
Actualmente, no se aceptan contribuciones externas para este proyecto. Sin embargo, si tienes alguna sugerencia o mejora, no dudes en contactar al autor del proyecto.

## Autor
Nombre: Babsia Santiago

Contacto: santiagobabsia@gmail.com

## Agradecimientos
Agradecemos a todos aquellos que han contribuido a este proyecto y a las fuentes de datos utilizadas.
