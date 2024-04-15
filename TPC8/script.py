import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, RDF, OWL, Literal

g = Graph()
g.parse("familia-base.ttl")

familia = Namespace("http://rpcw.di.uminho.pt/2024/familia/")

tree = ET.parse('biblia.xml')
root = tree.getroot()

for entrada in root.iter('person'):
    id = entrada.find('id').text
    person_uri = familia[id]

    g.add((person_uri, RDF.type, OWL.NamedIndividual))
    g.add((person_uri, RDF.type, familia.Pessoa))
    g.add((person_uri, familia.nome, Literal(entrada.find('name').text)))

    for pai in entrada.iter('parent'):
        parent_id = pai.get('ref')
        parent = root.find(f'.//person[id="{parent_id}"]')
        parent_sex = parent.find('sex').text

        if parent_sex == 'F':
            g.add((person_uri, familia.temMae, familia[parent_id]))
        elif parent_sex == 'M':
            g.add((person_uri, familia.temPai, familia[parent_id]))
        else:
            print('OUTLIER')
            exit()

g.serialize(destination="biblia.ttl", format="turtle")
