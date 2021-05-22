import requests
import json
import os
from bs4 import BeautifulSoup
import re
import datetime
from dateutil.relativedelta import relativedelta

url = 'https://quandovouservacinado.com/'
local_folder = os.path.dirname(os.path.abspath(__file__))
path = '' # path onde salvar o arquivo de dados

# cria o dicionário que representa uma pessoa
def pessoa(nome, idade, estado, prioritario=False):
    assert len(estado)==2, 'por favor insira apenas a sigla do estado'
    
    chaves = ('name', 'age', 'state', 'pni')
    valores = (nome, idade, estado.lower(), 'on' if prioritario else None)
    return dict(zip(chaves, valores))

# pessoas que quero acompanhar
with open(os.path.join(local_folder, 'perfis.json'),'r', encoding='utf-8') as perfis_json:
    perfis = [pessoa(**dados) for dados in json.loads(perfis_json.read())]

# obtém os dados e os processa
def vacinação(path=path, robô=False):
    for pf in perfis:
        req = requests.post(url, pf)
        soup = BeautifulSoup(req.content, 'lxml')
        raw_data = soup.body.h3
        
        def extrai(match): return int(match[1]) if match else 0
        
        dias = extrai(re.search(r'([0-9]+) dia(?:s)?', raw_data.text))
        meses = extrai(re.search(r'([0-9]{1,2}) (?:meses|mês)', raw_data.text))
        anos = extrai(re.search(r'([0-9]) ano', raw_data.text))
        
        hoje = datetime.date.today()
        vacina = hoje + relativedelta(days=dias, months=meses, years=anos)
        dias_totais = (vacina-hoje).days
    
        def mostra_data(dias, meses, anos):
            s_ano = f'{anos} anos' if anos else ''
            s_meses = f'{meses} meses' if meses else ''
            s_dias = f'{dias} dias' if dias else ''
            output = ', '.join(i for i in (s_ano, s_meses, s_dias) if i)
            return output
        
        if not robô:
            print(f'{pf["name"]} vai ser vacinado em '
                  f'{mostra_data(dias,meses,anos)}. ({dias_totais} dias)')
        
        arquivo = os.path.join(local_folder, path, pf['name'] + '.txt')
        with open(arquivo, 'a') as file:
            file.write(f'{dias_totais} {hoje}\n')