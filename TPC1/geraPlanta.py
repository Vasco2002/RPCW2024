import json

f = open("plantas.json", encoding='utf-8')
bd = json.load(f)
f.close()

print("""@prefix : <http://rpcw.di.uminho.pt/2024/1/plantas/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/1/plantas/> .

<http://rpcw.di.uminho.pt/2024/1/plantas> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/1/plantas#temEspécie
:temEspécie rdf:type owl:ObjectProperty ;
            rdfs:domain :Planta ;
            rdfs:range :Espécie .


###  http://rpcw.di.uminho.pt/2024/1/plantas/contem
:contem rdf:type owl:ObjectProperty ;
        owl:inverseOf :temRua ;
        rdfs:domain :Rua ;
        rdfs:range :Planta .


###  http://rpcw.di.uminho.pt/2024/1/plantas/temRua
:temRua rdf:type owl:ObjectProperty ;
        rdfs:domain :Planta ;
        rdfs:range :Rua .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/1/plantas/Caldeira
:Caldeira rdf:type owl:DatatypeProperty ;
          rdfs:domain :Planta ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Código_de_rua
:Código_de_rua rdf:type owl:DatatypeProperty ;
               rdfs:domain :Rua ;
               rdfs:range xsd:long .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Data_de_Plantação
:Data_de_Plantação rdf:type owl:DatatypeProperty ;
                   rdfs:domain :Planta ;
                   rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Data_de_actualização
:Data_de_actualização rdf:type owl:DatatypeProperty ;
                      rdfs:domain :Planta ;
                      rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Espécie
:Espécie rdf:type owl:DatatypeProperty ;
         rdfs:domain :Espécie ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Estado
:Estado rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Freguesia
:Freguesia rdf:type owl:DatatypeProperty ;
           rdfs:domain :Rua ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Gestor
:Gestor rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Id
:Id rdf:type owl:DatatypeProperty ;
    rdfs:domain :Planta ;
    rdfs:range xsd:long .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Implantação
:Implantação rdf:type owl:DatatypeProperty ;
             rdfs:domain :Planta ;
             rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Local
:Local rdf:type owl:DatatypeProperty ;
       rdfs:domain :Rua ;
       rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Nome_Científico
:Nome_Científico rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Espécie ;
                 rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Número_de_Registo
:Número_de_Registo rdf:type owl:DatatypeProperty ;
                   rdfs:domain :Planta ;
                   rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Número_de_intervenções
:Número_de_intervenções rdf:type owl:DatatypeProperty ;
                        rdfs:domain :Planta ;
                        rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Origem
:Origem rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Rua
:Rua rdf:type owl:DatatypeProperty ;
     rdfs:domain :Rua ;
     rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Tutor
:Tutor rdf:type owl:DatatypeProperty ;
       rdfs:domain :Planta ;
       rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/1/plantas#Espécie
:Espécie rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Planta
:Planta rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/1/plantas/Rua
:Rua rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################""")

for planta in bd:
    if planta['Código de rua'] == "":
        planta['Código de rua'] = "Sem_Código_de_rua"
    if planta['Espécie'] == "A identificar":
        planta['Espécie'] = "a identificar"
    registo = f"""

###  http://rpcw.di.uminho.pt/2024/1/plantas#{planta['Espécie']}
:{planta['Espécie'].replace(" ","_")} rdf:type owl:NamedIndividual ;
                :Espécie "{planta['Espécie']}" ;
                :Nome_Científico "{planta['Nome Científico']}" .


###  http://rpcw.di.uminho.pt/2024/1/plantas#{planta['Código de rua']}
<http://rpcw.di.uminho.pt/2024/1/plantas#{planta['Código de rua']}> rdf:type owl:NamedIndividual ,
                                                           :Rua ;
                                                  :contem <http://rpcw.di.uminho.pt/2024/1/plantas#{planta['Id']}> ;
                                                  :Código_de_rua "{planta['Código de rua']}"^^xsd:long ;
                                                  :Freguesia "{planta['Freguesia']}" ;
                                                  :Local "{planta['Local']}" ;
                                                  :Rua "{planta['Rua'].replace('"',"")}" .


###  http://rpcw.di.uminho.pt/2024/1/plantas#{planta['Id']}
<http://rpcw.di.uminho.pt/2024/1/plantas#{planta['Id']}> rdf:type owl:NamedIndividual ,
                                                            :Planta ;
                                                   :temEspécie :{planta['Espécie'].replace(" ","_")} ;
                                                   :temRua <http://rpcw.di.uminho.pt/2024/1/plantas#{planta['Código de rua']}> ;
                                                   :Caldeira "{planta['Caldeira']}" ;
                                                   :Data_de_Plantação "{planta['Data de Plantação']}" ;
                                                   :Data_de_actualização "{planta['Data de actualização']}" ;
                                                   :Estado "{planta['Estado']}" ;
                                                   :Gestor "{planta['Gestor']}" ;
                                                   :Id "{planta['Id']}"^^xsd:long ;
                                                   :Implantação "{planta['Implantação']}" ;
                                                   :Local "{planta['Local']}" ;
                                                   :Número_de_Registo "{planta['Número de Registo']}"^^xsd:int ;
                                                   :Número_de_intervenções "{planta['Número de intervenções']}"^^xsd:int ;
                                                   :Origem "{planta['Origem']}" ;
                                                   :Tutor "{planta['Tutor']}" .

###  http://rpcw.di.uminho.pt/2024/1/plantas/{planta['Espécie']}
:{planta['Espécie'].replace(" ","_")} rdf:type owl:NamedIndividual ,
                         :Espécie ;
                :Espécie "{planta['Espécie']}" ;
                :Nome_Científico "{planta['Nome Científico']}" .
"""
    
    print(registo)

