# DIJK
Nome dado em homenagem ao cientista da computação holandês Edsger Dijkstra, o qual descreveu o algoritmo que serve como base para a resolução do problema proposto.

## Como executar a aplicação?
A partir do código fonte compartilhado em arquivo no formato'zip', é necessário, inicialmente, descompactá-lo e garantir que o interpretador de Python 3.8 está instalado.

Em seguida, navegue até o diretório bexs e execute a aplicação desejada entre as opções disponíveis:

- `python3.8 api/dijk_web.py` -> Inicia o servidor http em localhost:8080
- `python3.8 cli/dijk_cli.py` ->  Inicia a aplicação de linha de comando
- main/dijk.py
- `python3.8 test/test/test_dijk.py` -> Executa os testes definidos

## Estrutura dos arquivos

A estrutura a seguir foi discutida previamente em [postagem](https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/) do site Free Code Camp:

```
root
├── api
│   ├── dijk_web.py
│   └── __init__.py
├── cli
│   └── dijk_cli.py
├── data
│   └── input-routes.csv
├── __init__.py
├── main
│   ├── dijk.py
│   ├── __init__.py
├── README.md
└── test
    ├── __init__.py
    ├── samples
    │   └── samples.csv
    └── test_dijk.py

8 directories, 14 files
```

## Decisões de design

Do ponto de vista do algoritmo, esta implementação é baseada em tempo de execução da ordem de `O ((V + A) log A)`, onde 'V' é o número de vértices e 'A' é o número de arestas. Se o grafo for conectado - no sentido de um espaço topológico, ou seja, se há um caminho de qualquer ponto para qualquer outro ponto no grafo - então, o valor de 'V' prevalece sobre 'A', tornando o algoritmo `O (V log A)`.

Já em relação ao design do código, o grafo é representado através da classe `Graph`, que contém os métodos `add_node` e `add_edge`. Tendo em vista que o atributo `self.nodes`é um objeto do tipo `set`, o primeiro método insere um novo nó no grafo somente se ele ainda não estiver definido na estrutura. Já o segundo método, tem como base o atributo `self.edges`, do tipo `collections.defaultdict`. Esse tipo foi escolhido pois, através da definição do parâmetro `default_factory=list`, é possível construir um dicionário que mapeia chaves para listas de valores. Ou seja, ao tentar obter acesso a uma chave ausente, o dicionário executará as seguintes etapas, sem lançar `KeyError`:

- Chamar `list()` para criar uma nova lista vazia
- Inserir a lista vazia no dicionário usando a chave que falta como `key`
- Devolver uma referência a essa lista

Os cálculos efetuados nessa classe são baseados em um arquivo csv com o formato:

```csv
from,to,weight
GRU,BRC,10
BRC,SCL,5
GRU,CDG,75
GRU,SCL,20
GRU,ORL,56
ORL,CDG,5
SCL,ORL,20
```
De forma que, caso um arquivo não seja passado à classe `Graph` através do parâmetro `input_file_path`, então o arquivo padrão será o csv definido em 'data/input-routes.csv'.

Após o escopo da classe `Graph`, seguem as funções auxiliares `apply_dijkstra` e `find_shortest_path`. A primeira é a implementação do [Algoritmo de Dijkstra](https://www.ime.usp.br/~pf/algoritmos_para_grafos/aulas/dijkstra.html) e a segunda é a implementação de um filtro do grafo passado a partir de um nó de origem e de um nó de destino.

Por fim, as aplicações `dijk_cli` e `dijk_web` expõem a lógica do módulo anterior en diferentes interfaces. Na primeira aplicação, o controle da entrada do usuário é feito através da expressão regular: `^(?P<from>[A-Z]+)\s*\-\s*(?P<to>[A-Z]+)$` com o objetivo de capturar linha com definição do nome do nó de origem e do nó de destino, separados por espaço(s) e um traço.

Na segunda aplicação, um servidor HTTP é definido em `dijk_web.py` tendo em vista as limitações de se usar somente a biblioteca padrão do Python3.8. Nesse caso, optei por usar a biblioteca [http.server](https://docs.python.org/3/library/http.server.html), pela simplicidade da sua API e por atender o propósito de **escutar** requisições http em um endereço específico de socket TCP e por **lidar** com essas requisições e suas respostas.

Para tanto, dois endpoints foram definidos `\check` (GET) e `\insert` (POST). Para vê-los em ação, basta executar:

1. Em um janela do terminal ou prompt de comando -> `python3.8 api/dijk_web.py`
2. Em outra janela do terminal ou prompt de comando -> umas das opções a seguir:
2.1. `curl -X GET '127.0.0.1:8080/check?from=GRU&to=SCL`^1
2.2. `curl -X POST '127.0.0.1:8080/insert?from=FOO&to=BAR&weight=42'`


1: 
```
{"path": "GRU - BRC - SCL", "price": "$15", "error": false}
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.8.2
Date: Fri, 04 Sep 2020 03:12:00 GMT
Content-Type: application/json
```
