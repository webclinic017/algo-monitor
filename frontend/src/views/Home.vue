<template>
	<div class="home">
		<p>
			Este sistema de monitoramento tem com finalidade facilitar a utilização de tecnicas complexas de Algo Trading através de uma interface amigavel, tanto para desenvolvedores quanto para usuários. Através dessa ferramenta, é possível utilizar algoritmos complexos através de uma parametrização simplificada, definindo valores de entrada pré-definidos para a execução, e visualizando seus resultados de forma organizada e centralizada.
		</p>
		<p>
			Após o inicio da execução, é possível monitorar o andamento do algoritmo, desde sua adição na fila de execução, enquanto aguarda outros processos, até o momento em que há a apresentação dos resultados, seguida pelo fim da atividade.
		</p>

		<br>
		<h4 class="subtitle">
			Criação
		</h4>
		<p>
			Inicialmente, o desenvolvedor deve registrar um novo algoritmo no sistema, através da <router-link :to="{name:'strat-create'}">página de criação</router-link>.
		</p>
		<p>
			Cabe à ele preecher os campos:
		</p>
		<dl>
			<dt>Nome da Estratégia</dt>
			<dd>Nome do algoritmo criado</dd>
			
			<dt>Arquivo de Entrada</dt>
			<dd>
				Caminho do arquivo de entrada do algoritmo.
				<br><br>
				Exemplo:
				<ul>
					<li>
						files
						<ul>
							<li>main.py</li>
							<li>
								dependencies
								<ul>
									<li>example.py</li>
									<li>config.json</li>
								</ul>
							</li>
						</ul>
					</li>
					<li>README.md</li>
					<li>.gitignore</li>
				</ul>
				No caso acima, o arquivo de entrada seria "files/main.py".
			</dd>
			
			<dt>Parâmetros</dt>
			<dd>
				Parâmetros de entrada da estratégia, definidos no formato JSON.
				<br>
				Deve seguir o padrão "chave": "valor", em que o valor será utilizado para prezumir o tipo do dado em questão.
				<br>
				<small>Obs: os parâmetros seram enviados em forma de lista, visto que os usuários podem enviar múltiplos parâmetros simultaneamente.</small>
				<br><br>
				Exemplo de esquema:
<pre>
{
  "param1": "parametro exemplo",	# string
  "param2": 123,			# number
  "param3": [1,2,3],			# list : number (número de elementos não é considerado)
  "param4": {				# dictionary
    "param4_child1": "filho1"		# dictionary property | string
    "param4_child2": 999,		# dictionary property | number
    "param4_child3": ["a","b"],		# dictionary property | list : string
    "param4_child4": {			# dictionary property | dictionary
      "param4_child4_gchild1": "neto1"	# dictionary property | dictionary property | string
    }
  },
  "param5": [				# list : dict
    {
      "param5_child1": 1		# list element (NÃO tipado, lista de dicts aceita quaisquer propriedades)
    },
    {
      "param5_child2": 2
    }
  ]
}
</pre>
				Exemplo válido de entrada:
<pre>
{
  "param1": "PETR4",
  "param2": 199.5,
  "param3": [10,20,30],
  "param4": {
    "param4_child1": "Pré-sal"
    "param4_child2": 1520,
    "param4_child3": ["c"],
    "param4_child4": {
      "param4_child4_gchild1": "petróleo"
    },
  },
  "param5": [
    {
      "macd": [12,26]
    }
  ]
}
</pre>
			</dd>

			<dt>Arquivo (zip) da Estratégia</dt>
			<dd>Todos arquivos utilizados pelo algoritmo, zipados em um único arquivo.</dd>
		</dl>

		<br>
		<h5>
			Template de Código
		</h5>
		<p>
			Para utilizar os parâmetros enviados para o algoritmo durante sua execução, o código cadastrado deve carregar-los da seguinte maneira:
		</p>
<pre>
import json
import sys

config_id = sys.argv[1]
with open(f'config_{config_id}.json') as file:
	config_list = json.loads(file.read())
	# config_list representa uma lista composta por N conjuntos de parâmetros,
	# em que cada um dos conjuntos segue o esquema definido no cadastro do algoritmo
</pre>
		<p>
			Já para salvar os resultados do algoritmo, o seguinte processo deve ser utilizado:
		</p>
<pre>
import uuid
import json

result_id = str(uuid.uuid4())
with open(f'result_{result_id}.json', 'w') as file:
	result = {
		"id": result_id,			# id do resultado
		"config": config_list,			# configurações utilizadas pelo algoritmo
		"result": {				# resultados do algoritmo, composto por "real", "pred" e "metrics"
			"real": [1,2,3],		# array com os valores reais (Ex.: para um algoritmo que prevê a abertura do dia seguinte, na lista pode constar o preço real da abertura, para comparação)
			"pred": [4,5,6],		# array com os valores da previsão
			"metrics": {			# campo livre para salvar as métricas do algoritmo (Ex. MAE, MAPE, Accuracy...)
				"param1": 1,
				"param2": "2",
				"param3": [3],
			}
		}
	}
	file.write(json.dumps(result))
</pre>

		<br>
		<h4 class="subtitle">
			Execução
		</h4>
		<p>
			Após o cadastro do algoritmo no sistema, o usuário poderá executa-lo, através da <router-link :to="{name:'strat-run'}">página de execução</router-link>.
		</p>
		<p>
			Nesta página, o usuário deve configurar os seguintes campos:
		</p>
		<dl>
			<dt>Estratégia</dt>
			<dd>Seleção da estratégia à ser executada.</dd>
			
			<dt>Label</dt>
			<dd>
				Categoria à qual a execução pertence. Por exemplo, um mesmo algoritmo executado multiplas vezes para o mesmo ativo e mesma estratégia, mas prevendo dias distintos (D+1, D+2, D+3, ...), pode ser agrupado como "PETR4 LONG-SHORT fev/2019".
				<br>
				Essa funcionalidade facilita a organização dos resultados e também possibilita a visualização gráfica do conjunto de execuções.
			</dd>

			<dt>Parâmetros</dt>
			<dd>
				Determinação dos parâmetros de entrada do algoritmo, seguindo o esquema definido em sua criação.
				<br>
				<small>Obs: múltiplos parâmetros podem ser enviados simultaneamente.</small>
			</dd>
		</dl>

		<br>
		<h4 class="subtitle">
			Processos
		</h4>
		<p>
			Após o ínicio da execução, esta pode ser acompanhada na <router-link :to="{name:'process'}">página de processos</router-link>.
		</p>

		<br>
		<h4 class="subtitle">
			Resultados
		</h4>
		<p>
			Após o fim da execução do algoritmo, é possível visualizar seus resultados através da <router-link :to="{name:'results'}">página de resultados</router-link>.
		</p>
		<p>
			Para uma análise melhor, é possível filtrar os resultados por suas labels, habilitando a visualização gráfica, ou através pelo ID do resultado.
		</p>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';

	@Component({})
	export default class Home extends Vue { }
</script>

<style lang="scss" scoped>
	pre {
		white-space: pre-wrap;
	}
</style>
