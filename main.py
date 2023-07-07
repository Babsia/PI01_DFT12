from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import datetime as dt
import ast
from sklearn.neighbors import NearestNeighbors
import sklearn
import requests
from fastapi.routing import APIRouter
from fastapi import BackgroundTasks
import time
import asyncio


app = FastAPI()
async def exception_handler(request: Request, exc: Exception):
    return {"status": "success"}

df = pd.read_csv('datasets/movies_clean.csv')
df['release_date'] = pd.to_datetime(df['release_date'])
df['release_month'] = df['release_date'].dt.month_name()
df['release_day'] = df['release_date'].dt.day_name()
dfd = pd.read_csv('datasets/directors.csv')
def traductor_mes():
    meses = {'January':'Enero', 'February':'Febrero', 'March':'Marzo', 'April':'Abril', 'May':'Mayo', 'June':'Junio', 'July':'Julio', 'August':'Agosto', 'September':'Septiembre', 'October':'Octubre', 'November':'Noviembre', 'December':'Diciembre'}
    df['release_month'] = df['release_month'].map(meses)
traductor_mes()
def traductor_dia():
    dias = {'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miercoles', 'Thursday':'Jueves', 'Friday':'Viernes', 'Saturday':'Sabado', 'Sunday':'Domingo'}
    df['release_day'] = df['release_day'].map(dias)
traductor_dia()





@app.get("/franquicia/{franquicia}")
def franquicia(franquicia="Toy Story Collection"):
    # Obtiene la cantidad de películas, la ganancia total y el promedio de ganancias para la franquicia especificada
    df_franquicia = df[df['collection_name'] == franquicia]
    cantidad = len(df_franquicia)
    ganancia_total = df_franquicia['revenue'].sum()
    ganancia_promedio = df_franquicia['revenue'].mean()
    return {'franquicia':franquicia, 'cantidad':cantidad, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}
@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais="United States of America"):
    # Obtiene la cantidad de películas producidas en el país especificado
    df_pais = df[df['country'] == pais]
    cantidad = len(df_pais)
    return {'pais':pais, 'cantidad':cantidad}

#def peliculas_idioma( Idioma: str ): Se ingresa un idioma (como están escritos en el dataset, no hay que traducirlos!). Debe devolver la cantidad de películas producidas en ese idioma.
@app.get("/peliculas_idioma/{idioma}")
def peliculas_idioma(idioma="English"):
    df_idioma = df[df['spoken_languages'] == idioma]
    cantidad = len(df_idioma)
    return {'idioma':idioma, 'cantidad':cantidad}


#def peliculas_duracion( Pelicula: str ): Se ingresa una pelicula. Debe devolver la la duracion y el año.
@app.get("/peliculas_duracion/{pelicula}")
def peliculas_duracion(pelicula="Toy Story"):
    df_pelicula = df[df['title'] == pelicula]
    duracion = int(df_pelicula['runtime'].values[0]) if len(df_pelicula) > 0 else None
    anio = int(df_pelicula['release_year'].values[0]) if len(df_pelicula) > 0 else None
    return {'pelicula': pelicula, 'duracion': duracion, 'año': anio}

#def productoras_exitosas( Productora: str ): Se ingresa la productora, entregandote el revunue total y la cantidad de peliculas que realizo.
@app.get("/productoras_exitosas/{productora}")
def productoras_exitosas(productora="Pixar Animation Studios"):
    df_productora = df[df['production_companies_names'].str.contains(productora)]
    cantidad = len(df_productora)
    ganancia_total = df_productora['revenue'].sum()
    return {'productora':productora, 'ganancia_total':ganancia_total, 'cantidad':cantidad}

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director="Joe Johnston"):
    director= dfd[dfd['Director'] == nombre_director]
    if director.empty:
        return None
    movie_ids = eval(director['Movie IDs'].iloc[0])
    peliculas = df[df['id'].isin(movie_ids)]
    peliculas = peliculas[['title', 'release_date', 'return', 'budget', 'revenue']]
    peliculas = peliculas.rename(columns={'return': 'retorno'})
    peliculas['retorno'] = peliculas['retorno'].astype(float)
    peliculas['budget'] = peliculas['budget'].astype(float)
    peliculas['revenue'] = peliculas['revenue'].astype(float)
    # Ordenar las películas por retorno en orden descendente
    peliculas = peliculas.sort_values(by='retorno', ascending=False)

    # Obtener la película con mayor retorno
    pelicula_exitosa = peliculas.iloc[0]
    retorno_exitoso = pelicula_exitosa['retorno']
    titulo_exitoso = pelicula_exitosa['title']

    # Agregar la palabra "(EXITO)" al título de la película exitosa
    titulo_exitoso += " (EXITO)"
    pelicula_exitosa['title'] = titulo_exitoso

    # Convertir el DataFrame a una lista de diccionarios
    peliculas = peliculas.to_dict('records')
    

    # Insertar la película exitosa en primer lugar de la lista
    peliculas.insert(0, pelicula_exitosa)
    #eliminar la segunda pelicula para que no se repita
    peliculas.pop(1)
    if peliculas is not None:
        for pelicula in peliculas:
            print("Título:", pelicula['title'])
            print("Fecha de lanzamiento:", pelicula['release_date'])
            print("Retorno:", pelicula['retorno'])
            print("Costo:", pelicula['budget'])
            print("Ganancia:", pelicula['revenue'])
            print("-----")
    return peliculas



@app.get("/peliculas_recomendadas/{pelicula}")
def Movies_ML(selected_title):
    df = pd.read_csv('datasets/movies_clean.csv')
    #cambiamos los datos nulos de tagline por un string vacio
    df['tagline'] = df['tagline'].fillna('')
    
    #columnas importantes
    df = df.dropna(subset=['overview', 'tagline', 'genre_names', 'title', 'id'])
    
    
    generos_df = df['genre_names'].str.join(sep='|').str.get_dummies()
    
    
    selected_genres = df.loc[df['title'] == selected_title]['genre_names'].values
    if len(selected_genres) == 0:
        return "No se encontró la película " + selected_title
    #calculamos la similitud de generos entre peliculas
    selected_genres = ast.literal_eval(selected_genres[0])
    df['genre_similarity'] = df['genre_names'].apply(lambda x: len(set(selected_genres) & set(ast.literal_eval(x))) / len(set(selected_genres) | set(ast.literal_eval(x))))
    
    #Se crea una variable binaria llamada 'same_series' que indica si las películas pertenecen a la misma serie. 
    #Esto se determina verificando si el título seleccionado se encuentra en el título de otras películas.
    df['same_series'] = df['title'].apply(lambda x: 1 if selected_title.lower() in x.lower() else 0)
    
   
    features_df = pd.concat([generos_df, df['vote_average'], df['genre_similarity'], df['same_series']], axis=1)
#Se utiliza el algoritmo de k-NN (k-Nearest Neighbors) para encontrar películas similares.
#  Se establece el valor de k en 6. Se entrena el modelo k-NN utilizando el dataframe features_df. 
# Luego, se encuentra el índice de las películas más similares a la película seleccionada utilizando
#  el método kneighbors y se guarda en la variable indices.
    
    k = 6
    knn = NearestNeighbors(n_neighbors=k+1, algorithm='auto')
    knn.fit(features_df)
    indices = knn.kneighbors(features_df.loc[df['title'] == selected_title])[1].flatten()
    recommended_movies = list(df.iloc[indices]['title'])

    
    selected_score = df.loc[df['title'] == selected_title]['vote_average'].values[0]
    recommended_movies = sorted(recommended_movies, key=lambda x: (df.loc[df['title'] == x]['same_series'].values[0], df.loc[df['title'] == x]['vote_average'].values[0], df.loc[df['title'] == x]['genre_similarity'].values[0]), reverse=True)
    recommended_movies = [movie for movie in recommended_movies if movie != selected_title]
   # Se crea una lista de películas recomendadas a partir de los índices encontrados en el paso anterior.
   # La lista contiene los títulos de las películas correspondientes a los índices.

   
    if len(recommended_movies) == 0:
        return "No se encontraron películas similares a " + selected_title
    else:
        output_str = f"Película seleccionada: {selected_title} ({selected_score}):\nPelículas Recomendadas:\n"
        for i, pelicula in enumerate(recommended_movies[:5]):
            score = df.loc[df['title'] == pelicula]['vote_average'].values[0]
            genres = df.loc[df['title'] == pelicula]['genre_names'].values[0]
            gen_str = ', '.join(ast.literal_eval(genres))

            output_str += f"-{pelicula}  | Géneros: {gen_str} | Puntaje: {score} |\n"
            if i == 4:
                break
        return output_str












