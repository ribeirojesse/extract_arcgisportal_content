from arcgis.gis import GIS
from arcgis.mapping import WebMap
from src.logs import send_message_info, send_message_error
from src.lists import webmap_list_id
import requests
import pandas as pd

class LayersInfo:
    token: str = ''
    url_portal: str = ''
    result_xlsx: str = ''
    

    def parameters(self, params: dict = None) -> None:
        """Configurar os parâmetros da aplicação

        :param params: Dicionário contendo os parâmetros
        :return:
        """
        self.token = params['token']
        self.url_portal = params['url_portal']
        self.result_xlsx = params['result_xlsx']

    @staticmethod
    def list_content(content):
        '''
        Cria uma lista contendo o link de cada conteúdo

        param content: Lista de conteúdo
        '''
        url_list = []
        try:
            for webmap_item in content:
                webmap_obj = WebMap(webmap_item)

                for layer in webmap_obj.layers:
                    my_string = str(layer.url)
                    url_list.append({"url":my_string,
                                    "webmap":str(webmap_item.title)})
            return url_list
        except Exception as e:
            send_message_error(f'Erro: {e}')
            return []    

    def get_layers_info(self, token, url_list):
        '''
        Cria uma lista contendo o link de cada conteúdo

        param token: Token de acesso
        param url_list: Lista de URLs
        '''
        layers_info = []
        try:
            for service in url_list:
                url = ''
                if service["url"]:
                    url = service["url"]
                site = f'{url}?f=pjson&token={self.token}'
                send_message_info('Acessando URL...')  
                
                try:
                    send_message_info("Acessando URL...")
                    response = requests.get(site)
                    response.raise_for_status() 
                    send_message_info('Requisição bem-sucedida.')
                    
                    send_message_info('Decodificando resposta JSON...')
                    data = response.json()
                    send_message_info('Decodificada com sucesso.')
        
                    send_message_info('Obtendo informações...')
                    name = data.get('name', 'N/A')
                    webmap = service["webmap"]
                    # print(f'Nome extraído: {name}') 
                    layers_info.append({"WebMap": webmap,
                                        "name": name,
                                        "url": url})
                    send_message_info('Informações obtidas com sucesso.')                     
                except requests.exceptions.RequestException as e:
                    send_message_error(f'Erro ao acessar o serviço: {e}')
                except ValueError:
                    send_message_error('Erro ao decodificar a resposta JSON.')
            send_message_info(layers_info)
            return layers_info

        except Exception as e:
            send_message_error(f'Erro ao obter o conteúdo: {e}')


    def run(self):
        gis = GIS(self.url_portal)
        send_message_info(gis)
        all_layers_info = []
        for webmap_id in webmap_list_id:
            contents = gis.content.search(query=webmap_id['id'], item_type="Web Map")
            if not contents:
                send_message_info(f"contents: Nenhum conteúdo em: {webmap_id['id']}")
                continue

            url_list = self.list_content(contents)
            if not url_list:
                send_message_info(f"url_list: Nenhum conteúdo encontrado para o ID: {webmap_id['id']}")
                continue
            
            layers_info = self.get_layers_info(url_list)
            if not layers_info:
                send_message_info(f"layers_info: Nenhuma informação de camada encontrada para o ID: {webmap_id['id']}")
                continue

            all_layers_info.extend(layers_info)
            if not all_layers_info:
                send_message_info(f"all_layers_info: Nenhuma camada encontrada para o ID: {webmap_id['id']}")
                continue

        if all_layers_info:
            df = pd.DataFrame(all_layers_info)
            df.to_excel(self.result_xlsx, index=False)
            send_message_info(f"Dados salvos em {self.result_xlsx}")
        else:
            send_message_info("Nenhuma informação de camada foi extraída.")

LayersInfo = LayersInfo()
