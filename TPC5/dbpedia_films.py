import requests
import json

sparql_endpoint = "http://dbpedia.org/sparql"

sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?film ?filmName ?releaseDate ?duration ?actorName ?birthDate ?directorName ?writerName ?screenName ?musicianName
WHERE {
  ?film a dbo:Film ;
        rdfs:label ?filmName .
  OPTIONAL {
    ?film dbp:date ?releaseDate ;
          dbo:runtime ?duration.
  }
  OPTIONAL { 
    ?film dbo:starring ?actor .
    ?actor rdfs:label ?actorName ;
           dbo:birthDate ?birthDate .
    FILTER (lang(?actorName) = "en")
  }
  OPTIONAL { 
    ?film dbo:director ?director .
    ?director rdfs:label ?directorName .
    FILTER (lang(?directorName) = "en")
  }
  OPTIONAL { 
    ?film dbo:writer ?writer .
    ?writer rdfs:label ?writerName .
    FILTER (lang(?writerName) = "en")
  }
  OPTIONAL {
    ?film dbp:screenplay ?screen.
    ?screen rdfs:label ?screenName.
    FILTER (LANG(?screenName) = 'en')
  }
  OPTIONAL { 
    ?film dbo:musicComposer ?musician .
    ?musician rdfs:label ?musicianName .
    FILTER (lang(?musicianName) = "en")
  }
  FILTER (lang(?filmName) = "en")
}
"""

headers = {
    "Accept": "application/sparql-results+json"
}

params = {
    "query": sparql_query,
    "format": "json"
}

response = requests.get(sparql_endpoint, params=params, headers=headers)

if response.status_code == 200:
    results = response.json()
    films_data = {}
    for result in results["results"]["bindings"]:
        film_uri = result["film"]["value"]
        film_name = result["filmName"]["value"]
        release_date = result["releaseDate"]["value"] if "releaseDate" in result else None
        duration = result["duration"]["value"] if "duration" in result else None
        actor_name = result.get("actorName", {}).get("value", None)
        birth_date = result.get("birthDate", {}).get("value", None)
        director_name = result.get("directorName", {}).get("value", None)
        writer_name = result.get("writerName", {}).get("value", None)
        musician_name = result.get("musicianName", {}).get("value", None)

        if film_uri in films_data:
            if actor_name and actor_name not in films_data[film_uri]["actors"]:
                films_data[film_uri]["actors"].append({"name": actor_name, "birthdate": birth_date})
            if director_name and director_name not in films_data[film_uri]["directors"]:
                films_data[film_uri]["directors"].append(director_name)
            if writer_name and writer_name not in films_data[film_uri]["writers"]:
                films_data[film_uri]["writers"].append(writer_name)
            if musician_name and musician_name not in films_data[film_uri]["musicians"]:
                films_data[film_uri]["musicians"].append(musician_name)
            if duration and films_data[film_uri]["duration"] != float(duration):
                films_data[film_uri]["duration"] = float(duration) / 60
        else:
            films_data[film_uri] = {
                "film": film_name,
                "release date": release_date,
                "duration": [float(duration) / 60] if duration else [],
                "actors": [{"name": actor_name, "birthdate": birth_date}] if actor_name else [],
                "directors": [director_name] if director_name else [],
                "writers": [writer_name] if writer_name else [],
                "musicians": [musician_name] if musician_name else []
            }

    films_list = list(films_data.values())

    with open("cinema.json", "w") as f:
        json.dump(films_list, f)

else:
    print("Error:", response.status_code)
    print(response.text)
