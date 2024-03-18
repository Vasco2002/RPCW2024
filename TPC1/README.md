# Script para Ontologia de Plantas

## Autor
Vasco Manuel Araújo Andrade de Oliveira

## Data
19/02/2024

## UC
RPCW

### Resumo

Este trabalho teve como objetivo criar uma Ontologia a partir dos dados do ficheiro `plantas.json`. Como tal, comecei por identificar quais seriam as classes
da Ontologia e de seguida atribui os atributos às respetivas classes e as ligações entre as classes. Foram criadas as classes "Plantas" (sendo a classe principal desta Ontologia, contendo OPs com as outras classes e os restantes DPs), "Rua" 
(contendo uma OP com a classe Planta, e as DPs relacionadas com ruas) e "Espécie" (Contendo as DPs "Espécie" e "Nome Científico").
Para o atributo "Rua", existiam casos onde havia uma " a mais, sendo esta removida com a função *replace*. Também haviam casos onde não existia "Código de rua", onde passaram a
ficar guardados no indivíduo "Sem_Código_de_rua". Nos casos onde a "Espécie" não é identificada, igualei os valores "a identificar" e
"A identificar", pois têm o mesmo significado.

### Ficheiros

- [`plantas.json`](plantas.json): Arquivo *JSON*, fornecido pelo professor, contendo dados sobre plantas. 

- [`exemplo.ttl`](exemplo.ttl): Arquivo *Turtle*, criado através do programa *Protege*, com a Estrutura da Ontologia e a construção de um indivíduo para cada classe distinta.

- [`geraPlanta.py`](geraPlanta.py): *Script* em *Python* usado para popular a Ontologia com indivíduos através dos dados do ficheiro `plantas.json`.

- [`output.ttl`](output.ttl): Arquivo *Turtle* de saída gerado pelo script `geraPlanta.py`, através do comando "python3 geraPlanta.py > output.ttl", sendo o resultado final da Ontologia.


