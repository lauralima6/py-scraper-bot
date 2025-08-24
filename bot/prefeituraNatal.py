import re
import json
import time
import requests
from pathlib import Path
from datetime import date
from requests import session
from selenium import webdriver
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BotSelenium:
    def insert(self, url_publica, mes):
        url = "http://localhost:8000/apipublicacoes/"

        payload = json.dumps({
            "url_pdf": url_publica,
            "mes_publicacao": mes
        })

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response:
            print("URL inserida com sucesso")
        else:
            print(f"error:{response.text}")
        
    def download_diarios(self, url, nome_arquivo, pasta="pdfs"):

        Path(pasta).mkdir(parents=True, exist_ok=True)
        caminho_arquivo = Path(pasta) / f"{nome_arquivo}.pdf"

        r = self.session.get(url, stream=True, timeout=120)
        r.raise_for_status()
        
        with open(caminho_arquivo, "wb") as f:
            for chunk in r.iter_content(chunk_size=1<<15):
                if chunk: f.write(chunk)
        return caminho_arquivo

    def upload_diarios(self, caminho_arquivo, mes):
        url = "https://0x0.st"

        with open(caminho_arquivo, "rb") as f:
            files = {"file": f}
            headers = {
                "User-Agent": "curl/7.68.0"
            }

            r = requests.post(url, files=files, headers=headers)
            r.raise_for_status()
            url_publica = r.text.strip()

            if url_publica.startswith("http"):
                self.insert(url_publica=url_publica, mes=mes)
                return url_publica
            else:
                print("Upload falhou:", url_publica)
                return None

    def __init__(self):
        self.session = requests.Session()
        self.urls_publicas = []
        self.arquivos = []
        driver = None
        
        try:
            config = json.load(open(str(Path(__file__).parent.absolute()) + '\\config.json'))
            url = config['url_pesquisa']
        
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(url)

            today = date.today()
            subtract_month = today - relativedelta(months=1)
            current_month = subtract_month.month

            if current_month < 10: 
                current_month = str(current_month).zfill(2)
            else:
                current_month = str(current_month)

            options_month = driver.find_element(By.NAME, "mes")
            options_month.click()
            
            select_month = driver.find_element(By.XPATH, f'//*[@id="linha-conteudo"]/div[1]/div[1]/form/select[1]/option[{current_month}]')
            select_month.click()

            year = str(today.year)
            options_year = driver.find_element(By.NAME, "ano")
            options_year.click()

            select_year = driver.find_element(By.XPATH, '//*[@id="linha-conteudo"]/div[1]/div[1]/form/select[2]')
            select = Select(select_year)
            select.select_by_value(str(year)) 

            button_search = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.m-2")
            button_search.click()
            time.sleep(5)

            html = driver.page_source
            reg_pagination = re.search(r'(?P<pagination><ul\s+class="pagination">.*?</ul>)', html, flags=re.DOTALL)
            if reg_pagination is not None:
                pagination_group = reg_pagination.group('pagination')
                reg_num_pag = re.finditer(r'class="page-link">(?P<num>.*?)</a>', pagination_group, flags=re.DOTALL)
                for match in reg_num_pag:
                    num_page = match.group('num')
                    
                    button_pagination = driver.find_element(By.XPATH, f'//*[@id="example_paginate"]/ul/li[{num_page}]/a')
                    button_pagination.click()

                    html_pdfs = driver.page_source

                    reg_pdfs = re.search(r'(?P<links><div\s+class="col-sm-12">.*?</div></div>)', html_pdfs, flags=re.DOTALL)

                    if reg_pdfs is not None: 
                        pdfs_group = reg_pdfs.group('links')
                        reg_links = re.finditer(r'href="(?P<link>https://natal.rn.gov.br/storage/app/media/DOM/anexos/dom_(?P<codigo>.*?)\.pdf)"', pdfs_group, flags=re.DOTALL)
                        
                        print(f"Baixando arquivos da página {num_page}...")
                        for match in reg_links:
                            link = match.group('link')
                            codigo = match.group('codigo')
                            caminho_arquivo = self.download_diarios(url=link, nome_arquivo=f'diario_{codigo}')
                            self.arquivos.append(caminho_arquivo)
                            time.sleep(3)
                    else:
                        reg_pdfs = None
            else:
                num_page = None

            print("Fazendo upload de arquivos...")
            for arquivo in self.arquivos:
                url_publica = self.upload_diarios(arquivo, current_month)
                self.urls_publicas.append(url_publica)
                time.sleep(3)
            print(self.urls_publicas)
        except Exception as e:
            print("Erro:", e)
        finally:
            if driver: 
                driver.quit()
if __name__ == "__main__":
    bot = BotSelenium()
