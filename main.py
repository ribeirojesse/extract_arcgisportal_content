import os
from pathlib import Path
from configparser import ConfigParser
from src.search_content import LayersInfo


def main():
    if not Path('config.cfg').exists():
        print('Arquivo config.cfg não encontrado')

    config = ConfigParser()
    config.read('config.cfg')

    token = config.get('ambiente', 'TOKEN')
    if not token:
        print('Token inválido')
        return

    url_portal = config.get('ambiente', 'PORTAL_URL')
    if not url_portal:
        print('URL do Portal inválido')
        return

    result_xlsx = config.get('path', 'RESULT_XLSX')
     
    params = {
        'token': token,
        'url_portal': url_portal,
        'result_xlsx': result_xlsx
    }

    LayersInfo.parameters(params=params)

    LayersInfo.run()



if __name__ == '__main__':
    main()
