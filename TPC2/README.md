# Ontologia Escola de Música

## Autor
Vasco Manuel Araújo Andrade de Oliveira

## Data
19/02/2023

## UC
RPCW

### Resumo

Foram cridas três classes:

- A classe Aluno, contendo duas OPs com as classes Curso (ao qual pertence) e Instrumento (que possui) e quatro DPs ("id", "nome", "anoCurso", "dataNasc").

- A classe Instrumento, que contem uma subclasse Tipo, e a subclasse Tipo contem três subclasses Sopro, Cordas, Outro. É indicado que a classe Instrumento só
poderá ter um Tipo, e as diferentes subclasses de Tipo são disjuntas. A classe tem duas DPs ("id_instrumento", "instrumento"). O tipo de um instrumento é classificado
através da função `tipo_instrumento` que contem as listas dos nomes dos instrumentos de sopros e de cordas e compara com o nome do instrumento que se pretende classificar.

- A classe Curso, que contem duas subclasses disjuntas Básico e Supletivo. Um curso é considerado Básico quando o seu nome começa com "CB" e Supletivo quando começa com
"CS", sendo esta classificação feita através da função `tipo_curso`. A classe tem uma OP com a classe Instrumento (o instrumento que o curso ensina) e as OPs de todos os 
Alunos que o Curso tenha, e três DPs ("curso","designacao","duracao")

O dataset `db.json` tinha alguns erros ao identificar o curso dos alunos, mais particularmente dar a grande parte dos cursos supletivos o mesmo número que os cursos básicos
que ensinavam o mesmo instrumento.

### Ficheiros

- [`db.json`](db.json): Arquivo *JSON*, fornecido pelo professor, contendo dados sobre a escola de música. 

- [`musica.ttl`](musica.ttl): Arquivo *Turtle*, criado através do programa *Protege*, com a Estrutura da Ontologia e a construção de um indivíduo para cada classe distinta.

- [`geraEscolaMusica.py`](geraEscolaMusica.py): *Script* em *Python* usado para popular a Ontologia com indivíduos através dos dados do ficheiro `db.json`.

- [`output.ttl`](output.ttl): Arquivo *Turtle* de saída gerado pelo script `geraEscolaMusica.py`, através do comando "python3 geraEscolaMusica.py > output.ttl", sendo o resultado final da Ontologia.


