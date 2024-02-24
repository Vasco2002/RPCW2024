import json

def tipo_instrumento(nome):
    sopros = ["clarinete", "contrabaixo", "corne inglês", "eufónio", "fagote", "flauta", "fliscorne", "oboé", "orgão", "saxofone", "trombone", "trompa", "trompete", "tuba"]
    cordas = ["violino", "violoncelo", "contrabaixo", "violão", "guitarra", "baixo", "harpa", "bandolim", "viola de arco"]

    nome = nome.lower()

    if nome in sopros:
        return "Sopro"
    elif nome in cordas:
        return "Cordas" 
    else:
        return "Outro"

def tipo_curso(nome):

    if nome.startswith("CB"):
        return "Básico"
    else: 
        return "Supletivo"



f = open("db.json", encoding='utf-8')
bd = json.load(f)
f.close()

alunos = bd["alunos"]

cursos_dict = {}
for curso in bd["cursos"]:
    cursos_dict[curso["id"]] = {
        "designacao": curso["designacao"],
        "duracao": curso["duracao"],
        "id_instrumento": curso["instrumento"]["id"]
    }

instrumentos = bd["instrumentos"]

instrumentos_dict = {}
for instrumento in bd["instrumentos"]:
    instrumentos_dict[instrumento["id"]] = {
        "nome": instrumento["#text"]
    }

print("""@prefix : <http://www.semanticweb.org/vasco/ontologies/2024/1/untitled-ontology-10/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/vasco/ontologies/2024/1/untitled-ontology-10/> .

<http://rpcw.di.uminho.pt/2024/escola_musica> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/escola_musica#ensinaInstrumento
:ensinaInstrumento rdf:type owl:ObjectProperty ;
                   rdfs:domain :Curso ;
                   rdfs:range :Instrumento .


###  http://rpcw.di.uminho.pt/2024/escola_musica#pertenceCurso
:pertenceCurso rdf:type owl:ObjectProperty ;
               owl:inverseOf :temCurso ;
               rdfs:domain :Curso ;
               rdfs:range :Aluno .


###  http://rpcw.di.uminho.pt/2024/escola_musica#temCurso
:temCurso rdf:type owl:ObjectProperty ;
          rdfs:domain :Aluno ;
          rdfs:range :Curso .


###  http://rpcw.di.uminho.pt/2024/escola_musica#temInstrumento
:temInstrumento rdf:type owl:ObjectProperty ;
                rdfs:domain :Aluno ;
                rdfs:range :Instrumento .


###  http://rpcw.di.uminho.pt/2024/escola_musica#temTipo
:temTipo rdf:type owl:ObjectProperty ;
         rdfs:domain :Instrumento ;
         rdfs:range :Tipo .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/escola_musica#anoCurso
:anoCurso rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno ;
          rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/escola_musica#curso
:curso rdf:type owl:DatatypeProperty ;
       rdfs:domain :Curso ;
       rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/escola_musica#dataNasc
:dataNasc rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/escola_musica#designacao
:designacao rdf:type owl:DatatypeProperty ;
            rdfs:domain :Curso ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/escola_musica#duracao
:duracao rdf:type owl:DatatypeProperty ;
         rdfs:domain :Curso ;
         rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/escola_musica#id
:id rdf:type owl:DatatypeProperty ;
    rdfs:domain :Aluno ;
    rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/escola_musica#id_instrumento
:id_instrumento rdf:type owl:DatatypeProperty ;
                rdfs:domain :Instrumento ;
                rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/escola_musica#instrumento
:instrumento rdf:type owl:DatatypeProperty ;
             rdfs:domain :Instrumento ;
             rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/escola_musica#nome
:nome rdf:type owl:DatatypeProperty ;
      rdfs:domain :Aluno ;
      rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/escola_musica#Aluno
:Aluno rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/escola_musica#Básico
:Básico rdf:type owl:Class ;
        rdfs:subClassOf :Curso ;
        owl:disjointWith :Supletivo .


###  http://rpcw.di.uminho.pt/2024/escola_musica#Cordas
:Cordas rdf:type owl:Class ;
        rdfs:subClassOf :Tipo .


###  http://rpcw.di.uminho.pt/2024/escola_musica#Curso
:Curso rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/escola_musica#Instrumento
:Instrumento rdf:type owl:Class ;
             owl:equivalentClass [ rdf:type owl:Restriction ;
                                   owl:onProperty :temTipo ;
                                   owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
                                   owl:onClass :Tipo
                                 ] .


###  http://rpcw.di.uminho.pt/2024/escola_musica#Outro
:Outro rdf:type owl:Class ;
       rdfs:subClassOf :Tipo .


###  http://rpcw.di.uminho.pt/2024/escola_musica#Sopro
:Sopro rdf:type owl:Class ;
       rdfs:subClassOf :Tipo .


###  http://rpcw.di.uminho.pt/2024/escola_musica#Supletivo
:Supletivo rdf:type owl:Class ;
           rdfs:subClassOf :Curso .


###  http://rpcw.di.uminho.pt/2024/escola_musica#Tipo
:Tipo rdf:type owl:Class ;
      rdfs:subClassOf :Instrumento .


#################################################################
#    Individuals
#################################################################""")

for aluno in alunos:
    aluno_curso_id = aluno['curso']
    registo = f"""

###  http://rpcw.di.uminho.pt/2024/escola_musica#{aluno['id']}
:{aluno['id']} rdf:type owl:NamedIndividual ,
                :Aluno ;
       :temCurso :{aluno['curso']} ;
       :temInstrumento :{aluno['instrumento'].replace(" ","_")} ;
       :anoCurso "{aluno['anoCurso']}"^^xsd:int ;
       :dataNasc "{aluno['dataNasc']}" ;
       :id "{aluno['id']}" ;
       :nome "{aluno['nome']}" .


###  http://rpcw.di.uminho.pt/2024/escola_musica#{aluno['curso']}
:{aluno['curso']} rdf:type owl:NamedIndividual ,
              :{tipo_curso(aluno['curso'])} ;
     :ensinaInstrumento :{instrumentos_dict[cursos_dict[aluno_curso_id]["id_instrumento"]]["nome"].replace(" ","_")} ;
     :pertenceCurso :{aluno['id']} ;
     :curso "{aluno['curso']}" ;
     :designacao "{cursos_dict[aluno['curso']]["designacao"]}" ;
     :duracao "{cursos_dict[aluno['curso']]["duracao"]}"^^xsd:int .

"""
    
    print(registo)

for instrumento in instrumentos:
    registo = f"""

###  http://rpcw.di.uminho.pt/2024/escola_musica#{instrumento['#text']}
:{instrumento['#text'].replace(" ","_")} rdf:type owl:NamedIndividual ,
                   :{tipo_instrumento(instrumento['#text'])} ;
          :id_instrumento "{instrumento['id']}" ;
          :instrumento "{instrumento['#text']}" .
"""
    
    print(registo)



print("""#################################################################
#    General axioms
#################################################################

[ rdf:type owl:AllDisjointClasses ;
  owl:members ( :Cordas
                :Outro
                :Sopro
              )
] .


###  Generated by the OWL API (version 4.5.26.2023-07-17T20:34:13Z) https://github.com/owlcs/owlapi""")