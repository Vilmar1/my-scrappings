from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--headless')

### YOUR DATA FOR DOWNLOADING EOG_DATAMINES
email= ''
password= ''

## PATH TO CHROMEDRIVER
path_c='your/path/to/chromedriver.exe'

def download_imgs(dia_ini,dia_fim,ano,mes,qtde_navs):
    navs=[]
    for i in range(0,qtde_navs):
        navs.append(webdriver.Chrome(executable_path=rf'{path_c}'))

    for k in range(dia_ini,dia_fim+1):    
        if k<10:
            navs[k%qtde_navs].get(fr'https://eogdata.mines.edu/nighttime_light/nightly/rade9d/SVDNB_npp_d{ano}{mes}0{k}.rade9d.tif')        
        else:
            navs[k%qtde_navs].get(fr'https://eogdata.mines.edu/nighttime_light/nightly/rade9d/SVDNB_npp_d{ano}{mes}{k}.rade9d.tif')
        navs[k%qtde_navs].implicitly_wait(20)
        elem = navs[k%qtde_navs].find_element_by_name('username')
        elem.clear()
        elem.send_keys(email)
        elem2 = navs[k%qtde_navs].find_element_by_name('password')
        elem2.clear()
        elem2.send_keys(password)
        navs[k%qtde_navs].find_element_by_name('login').click()
        if (k-dia_ini+1)%qtde_navs==0 or k==dia_fim:
            sleep(3600)
            for i in range(0,qtde_navs):
                navs[i].quit()
            navs=[]
            if k!=dia_fim:
                for i in range(0,qtde_navs):
                    navs.append(webdriver.Chrome(executable_path=rf'{path_c}'))
        print('baixando ', ano, ' ' , mes ,' ', k)
    return True


def download_mask(dia_ini,dia_fim,ano,mes,qtde_navs):
    navs=[]
    for i in range(0,qtde_navs):
        navs.append(webdriver.Chrome(executable_path=rf'{path_c}'))

    for k in range(dia_ini,dia_fim+1):    
        if k<10:
            navs[k%qtde_navs].get(fr'https://eogdata.mines.edu/nighttime_light/nightly/cloud_cover/SVDNB_npp_d{ano}{mes}0{k}.vcld.tif')  
        else:
            navs[k%qtde_navs].get(fr'https://eogdata.mines.edu/nighttime_light/nightly/cloud_cover/SVDNB_npp_d{ano}{mes}{k}.vcld.tif')
        navs[k%qtde_navs].implicitly_wait(20)
        elem = navs[k%qtde_navs].find_element_by_name('username')
        elem.clear()
        elem.send_keys(email)
        elem2 = navs[k%qtde_navs].find_element_by_name('password')
        elem2.clear()
        elem2.send_keys(password)
        navs[k%qtde_navs].find_element_by_name('login').click()
        if (k-dia_ini+1)%qtde_navs==0 or k==dia_fim:
            sleep(300)
            for i in range(0,qtde_navs):
                navs[i].quit()
            navs=[]
            if k!=dia_fim:
                for i in range(0,qtde_navs):
                    navs.append(webdriver.Chrome(executable_path=rf'{path_c}'))
        print('baixando ', ano, ' ' , mes ,' ', k)
    return True


dowmload_imgs(30,30,'2020','11',3)

download_mask(1,31,'2019','01',4)

for i in range(0,qtde_navs):
    navs[i].quit()
