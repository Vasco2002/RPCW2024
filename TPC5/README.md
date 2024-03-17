# Criação de um dataset JSON de Cinema

## Autor
Vasco Manuel Araújo Andrade de Oliveira

## Data
17/03/2024

## UC
RPCW

### Resumo

Neste TPC foi pedido para construir um dataset do tipo json com a seguinte informação:

Tema: Cinema
            -Filme
            -Ator
            -Realizador
            -Escritor
            -Músico
            -Argumentista

Para esse efeito foi usado a *DBPedia* realizando a seguinte query para obter todos os dados pedidos, menos os argumentistas (porque não eram dados):

SELECT ?film ?filmName ?actorName ?directorName ?writerName ?musicianName WHERE {
  ?film a dbo:Film ;
        rdfs:label ?filmName .
  OPTIONAL { 
    ?film dbo:starring ?actor .
    ?actor rdfs:label ?actorName .
  }
  OPTIONAL { 
    ?film dbo:director ?director .
    ?director rdfs:label ?directorName .
  }
  OPTIONAL { 
    ?film dbo:writer ?writer .
    ?writer rdfs:label ?writerName .
  }
  OPTIONAL { 
    ?film dbo:musicComposer ?musician .
    ?musician rdfs:label ?musicianName .
  }
  FILTER (lang(?filmName) = "en")
  FILTER (lang(?actorName) = "en")
  FILTER (lang(?directorName) = "en")
  FILTER (lang(?writerName) = "en")
  FILTER (lang(?musicianName) = "en")
}

Por fim foi feito uma script `dbpedia_films.py`, que usa os dados fornecidos pela query e mete-os no ficheiro json `cinema.json`, pondo todos os atores,
diretores, músicos e escritores em listas numa só única entrada para cada filme.

### Ficheiros

Aqui apresentam-se os ficheiros acrescentados ou modificados ao trabalho já feito na aula:

- [`dbpedia_films.py`](dbpedia_films.py): Arquivo Python que realiza consultas à DBpedia sobre filmes e as pessoas que participam nele, e armazena esses dados num arquivo JSON. 

- [`cinema.json`](cinema.json): Arquivo JSON usado para guardar a informação fornecida pelo arquivo dbpedia_films.

