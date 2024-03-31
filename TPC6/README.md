# Construção da Ontologia de Cinema

## Autor
Vasco Manuel Araújo Andrade de Oliveira

## Data
31/03/2024

## UC
RPCW

### Resumo

Antes de começar este TPC foi adaptado o TPC anterior para o dataset ter mais informação sobre os filmes. Na aula já tinhamos criado uma ontologia `cinema.ttl` 
para usar com o dataset do tpc anterior `cinema2.json`, mas agora populamos a topologia com esse dataset `cinema_populated.ttl`. Por fim foi-se criado uma aplicação
web para se poder visualizar os dados dessa topologia já populada.

### Ficheiros

Aqui apresentam-se os ficheiros acrescentados ou modificados ao trabalho já feito na aula:

- [`cinema2.json`](cinema2.json): Arquivo JSON, criado no TPC anterior, com a informação sobre cinema, usado para popular a ontologia.

- [`parseTTL.py`](parseTTL.py): Arquivo Python usado para popular a ontologia `cinema.ttl` com a informação do dataset `cinema2.json`. 

- [`cinema.ttl`](cinema.ttl): Arquivo *Turtle*, realizado na aula, com a estrutura da ontologia do cinema.

- [`cinema_populated.ttl`](cinema_populated.ttl): Arquivo *Turtle* de saída gerado pelo script `parseTTL.py`, através do comando "python3 parseTTL.py", sendo o resultado final da Ontologia.

- [`app.py`](app.py):  Arquivo Python que contém um aplicativo Flask para criar o servidor web, com o objetivo de criar uma página web para os dados da topologia do Cinema.
