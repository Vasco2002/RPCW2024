import requests
import json

sparql_endpoint = "http://dbpedia.org/sparql"

sparql_query_template = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?film ?filmName ?actorName ?directorName ?writerName ?musicianName
WHERE {{
  ?film a dbo:Film ;
        rdfs:label ?filmName .
  OPTIONAL {{ 
    ?film dbo:starring ?actor .
    ?actor rdfs:label ?actorName .
    FILTER (lang(?actorName) = "en")
  }}
  OPTIONAL {{ 
    ?film dbo:director ?director .
    ?director rdfs:label ?directorName .
    FILTER (lang(?directorName) = "en")
  }}
  OPTIONAL {{ 
    ?film dbo:writer ?writer .
    ?writer rdfs:label ?writerName .
    FILTER (lang(?writerName) = "en")
  }}
  OPTIONAL {{ 
    ?film dbo:musicComposer ?musician .
    ?musician rdfs:label ?musicianName .
    FILTER (lang(?musicianName) = "en")
  }}
  FILTER (lang(?filmName) = "en")
}}
LIMIT {}
OFFSET {}
"""

headers = {
    "Accept": "application/sparql-results+json"
}

results_limit = 10000  # Define o número máximo de resultados por solicitação
offset = 0
all_results = []

while True:
    sparql_query = sparql_query_template.format(results_limit, offset)

    params = {
        "query": sparql_query,
        "format": "json"
    }

    response = requests.get(sparql_endpoint, params=params, headers=headers)

    if response.status_code == 200:
        results = response.json()
        if not results["results"]["bindings"]:
            break  # Se não houver mais resultados, pare o loop
        all_results.extend(results["results"]["bindings"])
        offset += results_limit
    else:
        print("Error:", response.status_code)
        print(response.text)
        break

# Processar todos os resultados como antes
films_data = {}
for result in all_results:
    film_uri = result["film"]["value"]
    film_name = result["filmName"]["value"]
    actor_name = result.get("actorName", {}).get("value", None)
    director_name = result.get("directorName", {}).get("value", None)
    writer_name = result.get("writerName", {}).get("value", None)
    musician_name = result.get("musicianName", {}).get("value", None)

    if film_uri in films_data:
        if actor_name and actor_name not in films_data[film_uri]["actors"]:
            films_data[film_uri]["actors"].append(actor_name)
        if director_name and director_name not in films_data[film_uri]["directors"]:
            films_data[film_uri]["directors"].append(director_name)
        if writer_name and writer_name not in films_data[film_uri]["writers"]:
            films_data[film_uri]["writers"].append(writer_name)
        if musician_name and musician_name not in films_data[film_uri]["musicians"]:
            films_data[film_uri]["musicians"].append(musician_name)
    else:
        films_data[film_uri] = {
            "film": film_name,
            "actors": [actor_name] if actor_name else [],
            "directors": [director_name] if director_name else [],
            "writers": [writer_name] if writer_name else [],
            "musicians": [musician_name] if musician_name else []
        }

films_list = list(films_data.values())

with open("cinema2.json", "w") as f:
    json.dump(films_list, f)
