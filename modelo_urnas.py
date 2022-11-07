import requests
import json
import os
import py7zr
import pandas as pd

data_folder = 'arquivos_urna'

eleicao_id = 545
eleicao_str = 'ele2022'

data = {}

# # exemplo:
# # https://resultados.tse.jus.br/oficial/ele2022/545/config/mun-e000545-cm.json
# uf_mun_zon_LINK = f"https://resultados.tse.jus.br/oficial/{eleicao_str}/{eleicao_id}/config/mun-e000{eleicao_id}-cm.json"


# uf = 'ac'
# # exemplo:
# # https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/config/ac/ac-p000407-cs.json
# mun_zon_sec_LINK = f"https://resultados.tse.jus.br/oficial/{eleicao_str}/arquivo-urna/407/config/{uf}/{uf}-p000407-cs.json"

# mun_id = '01120'
# zon_id = '0008'
# sec_id = '0009'
# # exemplo:
# # https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/ac/01120/0008/0009/p000407-ac-m01120-z0008-s0009-aux.json
# hash_arquivos_LINK = f"https://resultados.tse.jus.br/oficial/{eleicao_str}/arquivo-urna/407/dados/{uf}/{mun_id}/{zon_id}/{sec_id}/p000407-{uf}-m{mun_id}-z{zon_id}-s{sec_id}-aux.json"


def download(link,filename,directory=''):
    dir_and_file = os.path.join(directory, filename)
    r = requests.get(link) # create HTTP response object
    with open(dir_and_file,'wb') as f:
        f.write(r.content)
        f.close()
    # print('d')
    return dir_and_file

def json_link_to_var(link,directory=''):
    filename = link.split('/')[-1]
    dir_and_file = os.path.join(directory, filename)
    if not os.path.exists(dir_and_file):
        # print(filename)
        dir_and_file = download(link, filename, directory)
    
    f = open(dir_and_file, encoding='utf-8')
    v = json.load(f)
    f.close()
    return v

def mount_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
        
def read_logjez(directory, filename):
    dir_and_file_logjez = os.path.join(directory, filename)
    dir_and_file_dat = os.path.join(directory, 'logd.dat')
    if not os.path.exists(dir_and_file_dat):
        py7zr.SevenZipFile(dir_and_file_logjez).extractall(path=directory)

    with open(dir_and_file_dat, 'r', encoding='cp1252') as f:
        s = f.read()
        f.close()
    
    a = s.index('Modelo de Urna:')
    s = s[a+16:a+22]
    modelo = s.strip()
    
    os.remove(dir_and_file_dat)
    
    return modelo

#def download_urna(uf,mun_id,zon_id,sec_id):
def do(uf_list=[], readonly=False):
    global data
    
    uf_mun_zon_LINK = f"https://resultados.tse.jus.br/oficial/{eleicao_str}/{eleicao_id}/config/mun-e000{eleicao_id}-cm.json"
    mount_folder(data_folder)
    j1 = json_link_to_var(uf_mun_zon_LINK, data_folder)

    if len(uf_list) == 0:
        for i in range(len(j1["abr"])):
            uf_list.append(j1["abr"][i]["cd"].lower())
    
    for uf in uf_list:
        data = {}
        data["uf"] = []
        data["municipio"] = []
        data["cod_municipio"] = []
        data["zona"] = []
        data["secao"] = []
        data["modelo_urna"] = []
        
        print(f"montando diretório: {uf}")
        
        uf_folder = f"{data_folder}/{uf}"
        mount_folder(uf_folder)
        
        mun_zon_sec_LINK = f"https://resultados.tse.jus.br/oficial/{eleicao_str}/arquivo-urna/407/config/{uf}/{uf}-p000407-cs.json"
        j2 = json_link_to_var(mun_zon_sec_LINK, uf_folder)
        
        
        
        i = 0
        total_mun = len(j2["abr"][0]["mu"])
        for mun_item in j2["abr"][0]["mu"]:
            i += 1
            mun_nome = mun_item["nm"]
            mun_id = mun_item["cd"]
            mun_folder_name = f"{mun_nome} ({mun_id})"
            mount_folder(f"{data_folder}/{uf}/{mun_folder_name}")    
           
            j=0
            total_zon = len(mun_item["zon"])
            for zon_item in mun_item["zon"]:
                j+=1
                zon_id = zon_item["cd"]
                mount_folder(f"{data_folder}/{uf}/{mun_folder_name}/{zon_id}")
                
                k=0
                total_sec = len(zon_item["sec"])
                for sec_item in zon_item["sec"]:
                    k+=1
                    sec_id = sec_item["ns"]
                    mount_folder(f"{data_folder}/{uf}/{mun_folder_name}/{zon_id}/{sec_id}")
                    
                    hash_arquivos_LINK = f"https://resultados.tse.jus.br/oficial/{eleicao_str}/arquivo-urna/407/dados/{uf}/{mun_id}/{zon_id}/{sec_id}/p000407-{uf}-m{mun_id}-z{zon_id}-s{sec_id}-aux.json"
                    j3 = json_link_to_var(hash_arquivos_LINK, f"{data_folder}/{uf}/{mun_folder_name}/{zon_id}/{sec_id}")
                    
                    for urna_item in j3["hashes"]:
                        urna_hash = urna_item["hash"]
                        mount_folder(f"{data_folder}/{uf}/{mun_folder_name}/{zon_id}/{sec_id}/{urna_hash}")
                        
                        urna_arqs = urna_item["nmarq"]
                        for arq in urna_arqs:
                            if arq.split('.')[-1] == 'logjez':
                                
                                # exemplo:
                                # https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/407/dados/ac/01120/0008/0009/77624b3969784a5a4e5276684942614f674779796a424b645a464d6a32795550684f683472785a494479733d/o00407-0112000080009.rdv
                                link = f"https://resultados.tse.jus.br/oficial/{eleicao_str}/arquivo-urna/407/dados/{uf}/{mun_id}/{zon_id}/{sec_id}/{urna_hash}/{arq}"
                                file_folder = f"{data_folder}/{uf}/{mun_folder_name}/{zon_id}/{sec_id}/{urna_hash}"
                                
                                dir_and_file = os.path.join(file_folder,arq)
                                if not os.path.exists(dir_and_file):
                                    download(link, arq, file_folder)
                                
                                modelo = read_logjez(file_folder,arq)
                                
                                if readonly:
                                    os.remove(dir_and_file)
                                
                                data["uf"].append(uf)
                                data["municipio"].append(mun_nome)
                                data["cod_municipio"].append(mun_id)
                                data["zona"].append(zon_id)
                                data["secao"].append(sec_id)
                                data["modelo_urna"].append(modelo)
                                
                                print(f"{uf}: {i}/{total_mun} {j}/{total_zon} {k}/{total_sec}: {modelo}")
                            
                            
                            
        print(' ok!')
        df = pd.DataFrame(data) 
        df.to_csv(f"{uf}.csv") 

do([],True)
