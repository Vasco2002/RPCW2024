import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD

# Carregar o grafo RDF existente
g = Graph()
g.parse("cinema.ttl")

# Definir o namespace do seu grafo RDF
cinema = Namespace("http://rpcw.di.uminho.pt/2024/cinema/")

# Função para formatar URIs
def format_uri(name):
    return URIRef(cinema + name.replace(' ', '_').replace('"', '').replace('%', ''))

# Abrir o arquivo JSON e ler os dados
with open("cinema2.json", "r") as json_file:
    data = json.load(json_file)

# Iterar sobre cada entrada no arquivo JSON e adicionar as informações ao grafo RDF
for movie in data:
    film_uri = format_uri(movie['film'])
    g.add((film_uri, RDF.type, OWL.NamedIndividual))
    g.add((film_uri, RDF.type, cinema.Film))
    g.add((film_uri, cinema.title, Literal(movie['film'], datatype=XSD.string)))

    for actor in movie['actors']:
        actor_uri = format_uri(actor['name'])
        g.add((actor_uri, RDF.type, OWL.NamedIndividual))
        g.add((actor_uri, RDF.type, cinema.Actor))
        g.add((actor_uri, cinema.name, Literal(actor['name'], datatype=XSD.string)))
        g.add((actor_uri, cinema.birthdate, Literal(actor['birthdate'], datatype=XSD.date)))
        g.add((film_uri, cinema.hasActor, actor_uri))

    for director in movie['directors']:
        director_uri = format_uri(director)
        g.add((director_uri, RDF.type, OWL.NamedIndividual))
        g.add((director_uri, RDF.type, cinema.Director))
        g.add((director_uri, cinema.name, Literal(director, datatype=XSD.string)))
        g.add((film_uri, cinema.hasDirector, director_uri))

    for writer in movie['writers']:
        writer_uri = format_uri(writer)
        g.add((writer_uri, RDF.type, OWL.NamedIndividual))
        g.add((writer_uri, RDF.type, cinema.Writer))
        g.add((writer_uri, cinema.name, Literal(writer, datatype=XSD.string)))
        g.add((film_uri, cinema.hasWriter, writer_uri))

    for musician in movie['musicians']:
        musician_uri = format_uri(musician)
        g.add((musician_uri, RDF.type, OWL.NamedIndividual))
        g.add((musician_uri, RDF.type, cinema.Musician))
        g.add((musician_uri, cinema.name, Literal(musician, datatype=XSD.string)))
        g.add((film_uri, cinema.hasMusic, musician_uri))

    for screenwriter in movie['screenwriters']:
        screenwriter_uri = format_uri(screenwriter)
        g.add((screenwriter_uri, RDF.type, OWL.NamedIndividual))
        g.add((screenwriter_uri, RDF.type, cinema.Screenwriter))
        g.add((screenwriter_uri, cinema.name, Literal(screenwriter, datatype=XSD.string)))
        g.add((film_uri, cinema.hasScreenwriter, screenwriter_uri))

# Salvar o grafo RDF atualizado
g.serialize(destination="cinema_populated.ttl", format="turtle")
