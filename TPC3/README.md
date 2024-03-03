# Ontologia Mapa Virtual

## Autor
Vasco Manuel Araújo Andrade de Oliveira

## Data
03/03/2024

## UC
RPCW

### Resumo

Para criar a Ontologia do Mapa Virtual criei duas classes, a classe Cidade (com as DPs "id", "nome", "população", "descrição", "distrito"), e a classe Ligação
com duas OPs (a Cidade da "origem" e a Cidade do "distino" da Ligação) e duas DPs ("id" e "distância" da Ligação). A Ontologia foi povoada através da script
`geraMapa.py` e posteriormente carregada no GraphDB, para poder responder às queries propostas, onde as respostas estão guardadas no ficheiro `Queries.txt`.

### Ficheiros

- [`mapa-virtual.json`](mapa-virtual.json): Arquivo *JSON*, fornecido pelo professor, contendo dados sobre as cidades de Portugal, e as ligações entre elas. 

- [`example.ttl`](example.ttl): Arquivo *Turtle*, criado através do programa *Protege*, com a Estrutura da Ontologia e a construção de um indivíduo exemplar para cada classe distinta.

- [`geraMapa.py`](geraMapa.py): *Script* em *Python* usado para popular a Ontologia com indivíduos através dos dados do ficheiro `mapa-virtual.json`.

- [`output.ttl`](output.ttl): Arquivo *Turtle* de saída gerado pelo script `geraMapa.py`, através do comando "python3 geraMapa.py > output.ttl", sendo o resultado final da Ontologia.

- [`Queries.txt`](Queries.txt): Arquivo *TextFile* que guarda as respostas das queries, propostas pelo professor, resolvidas no programa *GraphDB*, depois de ter carregado a topologia "output.ttl" nesse programa.
