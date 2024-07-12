
# SEARCH CONTENT PORTAL

Script criado para extrair as camadas de cada webmap existente no ArcGIS Portal Enterprise. A busca pode ser alterada facilmente para buscar outros tipos de conteú dentro do portal.

## Estrutura necessária para o código:

```path
search_content_portal/
│
├── logs/         
│   └── arquivo.txt   
│
├── src/    
│   ├── list.py
│   ├── logs.py
│   └── search_content.py
│        
├── .gitignore
├── config-example.cfg
├── main.py
└── README.md
```

## Arquivo de configuração:

No arquivo config-example.cfg contém o necessário para que o código possa ser executado, tendo isso, altere o nome desse arquivo para "config.cfg" e preencha as configurações como indicado.

```
[ambiente]
TOKEN = SEU TOKEN DE ACESSO AO SERVIÇO REST
PORTAL_URL = URL DO SEU PORTAL

[path]
RESULT_XLSX = CAMINHO ONDE SERÁ O OUTPUT DO RESULTADO

```

## Alteração do tipo buscado:
Para alterar o tipo de contúdo buscado pelo script dentro do seu portal, basta alterar o tipo no trecho que está no arquivo **search_content.py**, dentro da função **def run():**.

Lemabrando que ao alterar o tipo do item buscado, é necessário reavaliar a query que será realizada.

Segue exemplo da alteração:

```py
def run(self):
        gis = GIS(self.url_portal)
        send_message_info(gis)
        all_layers_info = []
        for webmap_id in webmap_list_id:
            contents = gis.content.search(query=webmap_id['id'], item_type="Web Map") <--- Alterar o item_type e a query se necessário
```


## Execução do código:

A execução do código é realizada através do arquivo **main.py**. 

No *cmd*, basta acessar a pasta do projeto e executar o comando exibido abaixo e o script será executado.

Comando:

```cmd
python main.py
```

## Logs 

A cada execução será criado um arquivo de log dentro da pasta *logs*, o que é util para o acompnahmento do processo e também na correção de bug's.