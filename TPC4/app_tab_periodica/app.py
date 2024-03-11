from flask import Flask, render_template, url_for
from datetime import datetime
import requests

app = Flask(__name__)

#dat do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

#GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/tabelaPeriodica"

@app.route('/')
def index():
    return render_template('index.html',data = {"data": data_iso_formatada})

@app.route('/elementos')
def elementos():
    sparql_query = """
prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
select * where{
    ?s a tp:Element ;
       tp:name ?nome ;
       tp:symbol ?simb ;
       tp:atomicNumber ?n ;
       tp:group ?group_uri .

       BIND(REPLACE(STR(?group_uri), STR(tp:), "") AS ?groupFragment)
       BIND(STRAFTER(?groupFragment, "_") AS ?groupNumeric)
}
order by ?n
"""

    resposta = requests.get(graphdb_endpoint, 
                            params = {"query": sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('elementos.html', data = dados)
    else:
        return render_template('empty.html', data = data_iso_formatada)

def treat_groups_data(data):

    for value in data:
        if "name" not in value.keys():
            value["name"] = {'type': 'literal', 'value': ''}
        if "number" not in value.keys():
            value["number"] = {'datatype': 'http://www.w3.org/2001/XMLSchema#integer', 'type': 'literal', 'value': ''}

@app.route('/<int:n>')
def elementoN(n):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select * where {{
        ?s a tp:Element ;
           tp:name ?nome ;
           tp:symbol ?simb ;
           tp:atomicNumber {n} ;
           tp:group ?group_uri .

        BIND(REPLACE(STR(?group_uri), STR(tp:), "") AS ?groupFragment)
        BIND(STRAFTER(?groupFragment, "_") AS ?groupNumeric)
    }}
    """

    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        if dados:
            dados[0]['n'] = {'type': 'literal', 'value': str(n)}
        entry_data = dados[0] if dados else {}
        return render_template('elemento.html', entry=entry_data, tempo=data_iso_formatada)
    else:
        return render_template('empty.html', data={"data": data_iso_formatada})
    
@app.route('/<string:nome>')
def elementoNome(nome):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select * where {{
        ?s a tp:Element ;
           tp:name "{nome}" ;
           tp:symbol ?simb ;
           tp:atomicNumber ?n ;
           tp:group ?group_uri .

        BIND(REPLACE(STR(?group_uri), STR(tp:), "") AS ?groupFragment)
        BIND(STRAFTER(?groupFragment, "_") AS ?groupNumeric)
    }}
    """

    resposta = requests.get(graphdb_endpoint,
                            params={"query": sparql_query},
                            headers={'Accept': 'application/sparql-results+json'})

    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        if dados:
            dados[0]['nome'] = {'type': 'literal', 'value': str(nome)}
        entry_data = dados[0] if dados else {}
        return render_template('elemento.html', entry=entry_data, tempo=data_iso_formatada)
    else:
        return render_template('empty.html', data={"data": data_iso_formatada})

@app.route('/grupos')
def grupos():
    sparql_query = """
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?number ?name WHERE {
    ?s rdf:type :Group .
    Optional{ ?s :number ?number .}
    Optional{ ?s :name ?name .}
}
Order by ?number
"""

    resposta = requests.get(graphdb_endpoint, 
                            params = {"query": sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        treat_groups_data(dados)
        return render_template('grupos.html', data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = {"data": data_iso_formatada})

@app.route('/grupos/<string:grupo>')
def grupo(grupo):
    sparql_query = f"""
    PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?n ?gname ?simb ?name ?na WHERE {{
        :{grupo} rdf:type :Group ;
                 :number ?n ;
                 :name ?gname .

        ?el :group :{grupo} ;
		    :symbol ?simb ;
            :name ?name ;
            :atomicNumber ?na .
    
    }}
    Order by ?na
    """

    resposta = requests.get(graphdb_endpoint, 
                            params = {"query": sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        print(dados)
        return render_template('grupo.html', data = dados)
    else:
        return render_template('empty.html', data = data_iso_formatada)

if __name__ == '__main__':
    app.run(debug=True)