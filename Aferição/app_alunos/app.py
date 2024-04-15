from flask import Flask, jsonify, request
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

# Endpoint do GraphDB
graphdb_endpoint = "http://localhost:7200/repositories/Alunos"

# Namespace do grafo RDF
ontologia = Namespace("http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/")

# Função para executar consultas SPARQL no GraphDB
def executar_query_sparql(query):
    sparql = SPARQLWrapper(graphdb_endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

# Rota para obter a lista de todos os alunos ou filtrar por curso
@app.route('/api/alunos', methods=['GET'])
def get_alunos():
    curso = request.args.get('curso')
    group_by = request.args.get('groupBy')

    if group_by == 'curso':
        query = """
            PREFIX : <http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?curso (COUNT(?aluno) AS ?num_alunos)
            WHERE {
              ?aluno rdf:type :Aluno ;
                     :curso ?curso .
            }
            GROUP BY ?curso
            ORDER BY ASC(?curso)
        """
        resultados = executar_query_sparql(query)
        result = [{"curso": r["curso"]["value"], "num_alunos": int(r["num_alunos"]["value"])} for r in resultados]
        return jsonify(result)
    elif group_by == 'projeto':
        # Consulta para agrupar por nota do projeto
        query = """
            PREFIX : <http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?nota_projeto (COUNT(?aluno) AS ?num_alunos)
            WHERE {
              ?aluno rdf:type :Aluno ;
                     :nota_projeto ?nota_projeto .
            }
            GROUP BY ?nota_projeto
            ORDER BY ASC(?nota_projeto)
        """
        resultados = executar_query_sparql(query)
        result = [{"nota_projeto": r["nota_projeto"]["value"], "num_alunos": int(r["num_alunos"]["value"])} for r in resultados]
        return jsonify(result)
    elif group_by == 'recurso':
        # Consulta para obter alunos que realizaram o exame de recurso
        query = """
            PREFIX : <http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?idAluno ?nome ?curso ?recurso
            WHERE {
	            ?aluno rdf:type :Aluno ;
	                   :idAluno ?idAluno ;
	                   :nome ?nome ;
	                   :curso ?curso ;
                       :fezExame ?exame .
                       ?exame :nota_exame ?recurso .
                       FILTER(contains(str(?exame), "_R"))
            }
            ORDER BY ASC(?nome)
        """
        resultados = executar_query_sparql(query)
        result = [{"idAluno": r["idAluno"]["value"], "nome": r["nome"]["value"], "curso": r["curso"]["value"], "recurso": r["recurso"]["value"]} for r in resultados]
        return jsonify(result)
    else:
        if curso:
            query = f"""
                PREFIX : <http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                SELECT ?idAluno ?nome ?curso
                WHERE {{
                  ?aluno rdf:type :Aluno ;
                         :idAluno ?idAluno ;
                         :nome ?nome ;
                         :curso ?curso .
                  FILTER(?curso = "{curso}")
                }}
                ORDER BY ASC(?nome)
            """
        else:
            query = """
                PREFIX : <http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                SELECT ?idAluno ?nome ?curso
                WHERE {
                  ?aluno rdf:type :Aluno ;
                         :idAluno ?idAluno ;
                         :nome ?nome ;
                         :curso ?curso .
                }
                ORDER BY ASC(?nome)
            """

        resultados = executar_query_sparql(query)
        result = [{"idAluno": r["idAluno"]["value"], "nome": r["nome"]["value"], "curso": r["curso"]["value"]} for r in resultados]
    return jsonify(result)

# Rota para obter informações de um aluno específico
@app.route('/api/alunos/<id>', methods=['GET'])
def get_aluno(id):
    query = f"""
        PREFIX : <http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?nome ?curso ?nota_projeto
        WHERE {{
          :{id} rdf:type :Aluno .
          :{id} :nome ?nome .
          :{id} :curso ?curso .
          :{id} :nota_projeto ?nota_projeto .
        }}
    """
    resultados = executar_query_sparql(query)
    aluno = {"idAluno": id, "nome": resultados[0]["nome"]["value"], "curso": resultados[0]["curso"]["value"], "nota_projeto": resultados[0]["nota_projeto"]["value"]}
    return jsonify(aluno)

# Rota para obter a lista de alunos com o número de TPCs realizados
@app.route('/api/alunos/tpc', methods=['GET'])
def get_alunos_com_tpc():
    query = """
        PREFIX : <http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?idAluno ?nome ?curso (COUNT(?tpc) AS ?num_tpc)
        WHERE {
          ?aluno rdf:type :Aluno .
          ?aluno :idAluno ?idAluno .
          ?aluno :nome ?nome .
          ?aluno :curso ?curso .
          ?aluno :fezTPC ?tpc .
        }
        GROUP BY ?idAluno ?nome ?curso
        ORDER BY ASC(?nome)
    """
    resultados = executar_query_sparql(query)
    alunos = [{"idAluno": r["idAluno"]["value"], "nome": r["nome"]["value"], "curso": r["curso"]["value"], "num_tpc": int(r["num_tpc"]["value"])} for r in resultados]
    return jsonify(alunos)

# Rota para obter a lista de alunos avaliados
@app.route('/api/alunos/avaliados', methods=['GET'])
def get_alunos_avaliados():
    # Consulta SPARQL para obter os dados necessários
    query = """
        PREFIX : <http://www.semanticweb.org/vasco/ontologies/2024/3/alunos/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?idAluno ?nome ?curso ?nota_projeto (MAX(?nota_exame) AS ?max_nota_exame) (SUM(?nota_tpc) AS ?total_tpc)
        WHERE {
          ?aluno rdf:type :Aluno ;
                 :idAluno ?idAluno ;
                 :nome ?nome ;
                 :curso ?curso ;
                 :nota_projeto ?nota_projeto .
          OPTIONAL {
            ?aluno :fezExame ?exame .
            ?exame :nota_exame ?nota_exame .
          }
          OPTIONAL {
            ?aluno :fezTPC ?tpc .
            ?tpc :nota_tpc ?nota_tpc .
          }
        }
        GROUP BY ?idAluno ?nome ?curso ?nota_projeto
        ORDER BY ASC(?nome)
    """

    resultados = executar_query_sparql(query)
    alunos_avaliados = []

    # Calcular a nota final para cada aluno
    for resultado in resultados:
        id_aluno = resultado["idAluno"]["value"]
        nome = resultado["nome"]["value"]
        curso = resultado["curso"]["value"]
        nota_projeto = float(resultado["nota_projeto"]["value"])

        # Verificar se a nota do projeto é inferior a 10
        if nota_projeto < 10:
            nota_final = "R"
        else:
            # Calcular a nota final
            max_nota_exame = float(resultado["max_nota_exame"]["value"]) if resultado.get("max_nota_exame") else 0
            total_tpc = float(resultado["total_tpc"]["value"]) if resultado.get("total_tpc") else 0

            total_tpc *= 0.2  # Ponderação dos TPCs (20%)
            
            nota_final = (total_tpc + (nota_projeto * 0.4) + (max_nota_exame * 0.4))

            if nota_final < 10:
                nota_final = "R"

        aluno_avaliado = {
            "idAluno": id_aluno,
            "nome": nome,
            "curso": curso,
            "notaFinal": nota_final
        }
        alunos_avaliados.append(aluno_avaliado)

    return jsonify(alunos_avaliados)

if __name__ == '__main__':
    app.run(debug=True)
