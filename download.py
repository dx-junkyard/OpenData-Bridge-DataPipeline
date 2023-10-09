import re, os, requests, yaml
from datetime import datetime

GHPAGE_FOLDER = 'docs'
DATA_FOLDER = 'source'
OUTPUT_FOLDER = 'fixed'

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return e

def create_filename(name, url):
    # 現在の時間をもとにファイル名を作成
    file_name = f'{ datetime.now().strftime("%Y%m%d-%H:%M:%S") }-'

    # Curl形式の様々な引き数のついたURLに対応したファイル名抽出
    pattern = r'/([^/]+?\.[a-zA-Z0-9]{1,8})$'
    file_org = re.search(pattern, url)
    file_name += name if file_org is None else file_org.group(1)

    return file_name
    
def main():
    with open('opendata.yml', 'r') as yml:
        config = yaml.safe_load(yml)
        od_links = config['link']

    html = '# Open Data 整形済み最新データ  \n'

    for od_link in od_links:
        obj_data = fetch_data(od_link['url'])
        # 200 OK 以外ならErrorをMarkdownに出力して処理継続
        if type(obj_data) is not str:
            html += '// ' + od_link['title'] + ': Error - ' + str(obj_data) + '  \n'
            continue
   
        # ファイルに取得したDataを保存
        file_name = create_filename(od_link['name'], od_link['url'])
        with open(GHPAGE_FOLDER + '/' + DATA_FOLDER + '/' + file_name, 'w') as f:
            f.write(obj_data)

        ### TODO: 保存したファイルにConverter処理を行う
        
        # Markdown出力
        html += '[' + od_link['title'] + '](' + DATA_FOLDER + '/' + file_name + ') \('
        html += '[source](' + od_link['url'] + ')\)  \n'
        
    # GitHub Pagesで公開するトップページを作成
    html += f'last update: { datetime.now().strftime("%Y%m%d-%H:%M:%S") }  '
    with open(GHPAGE_FOLDER + '/index.md', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    main()
