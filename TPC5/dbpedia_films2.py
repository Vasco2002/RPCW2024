import requests
import json

sparql_endpoint = "http://dbpedia.org/sparql"

sparql_query_template = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?film ?filmName ?releaseDate ?duration ?actorName ?birthDate ?directorName ?writerName ?screenName ?musicianName
WHERE {{
  ?film a dbo:Film ;
        rdfs:label ?filmName .
  OPTIONAL {{
    ?film dbp:date ?releaseDate ;
          dbo:runtime ?duration.
  }}
  OPTIONAL {{
    ?film dbo:starring ?actor .
    ?actor rdfs:label ?actorName ;
           dbo:birthDate ?birthDate .
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
    ?film dbp:screenplay ?screen.
    ?screen rdfs:label ?screenName.
    FILTER (LANG(?screenName) = 'en')
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

results_limit = 10000  
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
            break  
        all_results.extend(results["results"]["bindings"])
        offset += results_limit
    else:
        print("Error:", response.status_code)
        print(response.text)
        break

films_data = {}
for result in all_results:
    film_uri = result["film"]["value"]
    film_name = result["filmName"]["value"]
    release_date = result.get("releaseDate", {}).get("value", None)
    duration = result.get("duration", {}).get("value", None)
    actor_name = result.get("actorName", {}).get("value", None)
    birth_date = result.get("birthDate", {}).get("value", None)
    director_name = result.get("directorName", {}).get("value", None)
    writer_name = result.get("writerName", {}).get("value", None)
    screen_name = result.get("screenName", {}).get("value", None)
    musician_name = result.get("musicianName", {}).get("value", None)

    if film_uri in films_data:
        if actor_name and actor_name not in [a["name"] for a in films_data[film_uri]["actors"]]:
            films_data[film_uri]["actors"].append({"name": actor_name, "birthdate": birth_date})
        if director_name and director_name not in films_data[film_uri]["directors"]:
            films_data[film_uri]["directors"].append(director_name)
        if writer_name and writer_name not in films_data[film_uri]["writers"]:
            films_data[film_uri]["writers"].append(writer_name)
        if musician_name and musician_name not in films_data[film_uri]["musicians"]:
            films_data[film_uri]["musicians"].append(musician_name)
        if screen_name and screen_name not in films_data[film_uri]["screenwriters"]:
            films_data[film_uri]["screenwriters"].append(screen_name)
        if duration and films_data[film_uri]["duration"] != float(duration):
            films_data[film_uri]["duration"] = float(duration) / 60
    else:
        films_data[film_uri] = {
            "film": film_name,
            "release date": release_date,
            "duration": float(duration) / 60 if duration else None,
            "actors": [{"name": actor_name, "birthdate": birth_date}] if actor_name else [],
            "directors": [director_name] if director_name else [],
            "writers": [writer_name] if writer_name else [],
            "musicians": [musician_name] if musician_name else [],
            "screenwriters": [screen_name] if screen_name else []
        }

films_list = list(films_data.values())

with open("cinema2.json", "w") as f:
    json.dump(films_list, f)
