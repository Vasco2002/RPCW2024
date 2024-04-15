# Transformação de ficheiro .xml em .ttl

## Autor
Vasco Manuel Araújo Andrade de Oliveira

## Data
15/04/2024

## UC
RPCW

### Resumo

Neste TPC foi pedido converter um dataset de XML para TTL, sendo que na ontologia deverão existir apenas duas relações entre os indivíduos: temPai e temMae.
Como tal escolhi o ficheiro `biblia.xml` para o converter através da script `script.py`, esta script usa o módulo `xml.etree.ElementTree` para analisar o arquivo XML 
e o módulo `rdflib` para manipular e serializar o grafo RDF no formato Turtle.

### Ficheiros

Aqui apresentam-se os ficheiros acrescentados ou modificados ao trabalho já feito na aula:

- [`script.py`](script.py): Arquivo *Python* que transforma o ficheiro `biblia.xml` na ontologia `biblia.ttl`, com base na ontologia `familia-base`.

- [`familia-base.ttl`](familia-base.ttl): Arquivo *Turtle* com a estrutura base da ontologia pronta para ser populada.

- [`biblia.xml`](biblia.xml): Arquivo *XML* que contém informações genealógicas de personagens bíblicas.

- [`biblia.ttl`](biblia.ttl): Arquivo *Turtle* de saída gerado pelo script `script.py`, sendo este o resultado final.

