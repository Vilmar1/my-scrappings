from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

### SET THE CONFIGURATIONS FOR SELENIUM CHROMEDRIVE
options = Options()
options.add_argument('--headless')
path_c= 'chromedrive/path/chromedriver.exe' # your chromedrive path


# =============================================================================
# Coletar os contadores de cada estado na variável n_mun
# =============================================================================
path_o = 'your/output/path/to/counters.xlsx' #your output path to the counters

num_mun={}
for i in range(2,29):
    nav = webdriver.Chrome(executable_path=fr'{path_c}'
                            , options=options)
    
    nav.get('http://www2.aneel.gov.br/relatoriosrig/(S(cf2kkjn2boyd4mt2knmkvmct))/relatorio.aspx?folder=sfe&report=PainelMunicipio')
    nav.implicitly_wait(20)
    # o numero dentro de option é o estado
    nav.find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}]').click()
    nav.implicitly_wait(20)
    # o numero dentro de option é o municipio
    nav.find_element_by_xpath('//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[2]').click()
    nav.implicitly_wait(20)
    # o numero dentro de option é o estado
    state=nav.find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}-1]').text
        
    site = BeautifulSoup(nav.page_source,'html.parser')
    # Find select tag
    select_tag = site.find_all("select")[1]
    # find all option tag inside select tag
    option = select_tag.find_all("option")
    num_mun[state]=len(option)
    print(state, '   ', num_mun[state])
    
nav.close()    
n_mun=pd.DataFrame()
n_mun=n_mun.append(num_mun,ignore_index=True).transpose()
n_mun.reset_index(inplace=True)

with pd.ExcelWriter(rf'{path_o}') as writer:
    n_mun.to_excel(writer,sheet_name='n_mun',index=False)

# =============================================================================
# SCRAPING COM 11 NAVEGADORES 
# =============================================================================
# coleta os últimos 11 anos de dados (o scraping vai coletar a quantidade 
# de anos igual a quantidade de navegadores)

path_df = 'your/output/path/to/df/scraping.xlsx' # your output path to the scraping
ano_atual= 2022     # INPUT THE CURRENT YEAR / COLOQUE O ANO ATUAL

nav=[]
nao_visitados=[]
for k in range(0,11):
    nav.append(webdriver.Chrome(executable_path=fr'{path_c}', options=options))

for k in range(0,len(nav)):
   nav[k].get('http://www2.aneel.gov.br/relatoriosrig/(S(cf2kkjn2boyd4mt2knmkvmct))/relatorio.aspx?folder=sfe&report=PainelMunicipio')
   nav[k].implicitly_wait(20)
sleep(4)

for i in range(1,28):
    #### driblando o <select a value> do estado
    for k in range(0,len(nav)):
         # o numero dentro de option é o estado
        WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[2]')))
        nav[k].find_element_by_xpath('//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[2]').click()
    
   #### driblando o <select a value> do municipio
    for k in range(0,len(nav)):
        try:
            WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}]')))
        except Exception:
            sleep(4)
            WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}]')))            
        nav[k].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}]').click()
    for k in range(0,len(nav)):
        try:
            WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[2]')))
        except Exception:
            sleep(4)
            WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[2]')))
        nav[k].find_element_by_xpath('//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[2]').click()
        
    # Colocando o período de referência
    for k in range(0,len(nav)):             
        try:
            WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]')))
        except Exception:
            sleep(4)
            WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]')))
        nav[k].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]').click()

    for j in range(1,int(n_mun.iloc[i-1,1])+1): 
        # CONDIÇÃO PARA NAO SUPERLOTAR A MEMÓRIA DO CHROME, descomente se 
        # estiver sobrecarregando a RAM do pc
        
        # if j%40 == 0:
            # for k in range(0,len(nav)):
            #     nav[k].quit()
             
        #     count=0
        #     nav=[]
        #     for k in range(0,11):
        #         nav.append(webdriver.Chrome(executable_path=r'C:\Users\Vilmar\Desktop\Public Data\Dados\chromedriver.exe', options=options))

        #     for k in range(0,len(nav)):
        #        nav[k].get('http://www2.aneel.gov.br/relatoriosrig/(S(cf2kkjn2boyd4mt2knmkvmct))/relatorio.aspx?folder=sfe&report=PainelMunicipio')
        #        nav[k].implicitly_wait(20)
        #     sleep(4)
            
        #     for k in range(0,len(nav)):
        #          # o numero dentro de option é o estado
        #         WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[2]')))
        #         nav[k].find_element_by_xpath('//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[2]').click()
        #     count+=1
            
        #    #### driblando o <select a value> do municipio
        #     for k in range(0,len(nav)):
        #         try:
        #             WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}]')))
        #         except Exception:
        #             sleep(4)
        #             WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}]')))            
        #         nav[k].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}]').click()
        #     for k in range(0,len(nav)):
        #         try:
        #             WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[2]')))
        #         except Exception:
        #             sleep(4)
        #             WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[2]')))
        #         nav[k].find_element_by_xpath('//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[2]').click()
                
        #     # Colocando o período de referência
        #     for k in range(0,len(nav)):             
        #         try:
        #             WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]')))
        #         except Exception:
        #             sleep(4)
        #             WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]')))
        #         nav[k].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]').click()
        #     print('....... TROCANDO O NAVEGADOR ..........')
        
        for k in range(0,len(nav)):            
            # o numero dentro de option é o municipio
            try:
                WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[{j}]')))
            except Exception:
                sleep(4)
                WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[{j}]')))
            nav[k].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[{j}]').click()

            
        # for k in range(0,1):             
        #     try:
        #         WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]')))
        #     except Exception:
        #         sleep(4)
        #         WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]')))
        # ano_inicial= nav[1].find_element_by_xpath('//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[1]').text
        # if ano_inicial not in [str(ano_atual)]:
        #     nao_visitados.append(nav[1].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[{j}]').text)
        #     continue
        
        # Colocando o período de referência
        for k in range(0,len(nav)):             
            try:
                WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]')))
            except Exception:
                sleep(4)
                WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]')))
            nav[k].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl07_ddValue"]/option[{k+1}]').click()
        
        # clica em view report        
        for k in range(0,len(nav)):
            try:
                WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ReportViewer1_ctl04_ctl00"]')))
            except Exception:
                sleep(4)
                WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ReportViewer1_ctl04_ctl00"]')))                
            nav[k].find_element_by_xpath('//*[@id="ReportViewer1_ctl04_ctl00"]').click()
            # nav[k].implicitly_wait(50)
                        
        for k in range(0,len(nav)):
            try:
                WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[{j}]')))
            except Exception:
                sleep(2)
                WebDriverWait(nav[k], 40).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[{j}]')))
            state=nav[0].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl03_ddValue"]/option[{i}]').text
            mun=nav[0].find_element_by_xpath(f'//*[@id="ReportViewer1_ctl04_ctl05_ddValue"]/option[{j}]').text
            soup = BeautifulSoup(nav[k].page_source,'html.parser')
            a=soup.text
            valor=a[(a.find('TOTAL'))+7:(a.find('TOTAL')+7)+9]
            year = int(ano_inicial)-k

            
            print('valor: ',valor,'estado: ', state,'municipio: ',mun, 'ano: ',year)
        
            dic={'state':state,'city':mun,'year':int(year),'value':valor}
            df2=df2.append(dic,ignore_index=True)
with pd.ExcelWriter(rf'{path_df}') as writer:
    df2.to_excel(writer,sheet_name='scraping',index=False)

for k in range(0,len(nav)):
    nav[k].quit()