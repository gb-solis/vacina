from vacinação import perfis, load_dados, melhor_estimativa
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import matplotlib.units as munits
import sys
import datetime

# converte datas no matplotlib para formato mais legível
converter = mdates.ConciseDateConverter(show_offset=False)
munits.registry[datetime.date] = converter

def plota(pessoas, linhas = False):
    for nome in pessoas:
        x, y = load_dados(nome)
        p = plt.plot_date(x, y, 'o:', xdate=True, label = str(nome))
        estim = melhor_estimativa(nome)
        if linhas:
            plt.axline((mdates.date2num(x[0]), (estim - x[0]).days), slope=-1, color = p[0].get_color(), linestyle = '--', label = estim)
        
    plt.title('Tempo estimado para a vacinação')
    plt.xlabel('Data de acesso')
    plt.ylabel('Dias estimados até a vacinação')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    ajudamsg = 'Uso: plot.py [-l] pessoa1 pessoa2... (-l para linhas de estimativa) \nou   plot.py -p [--perfis] (para ver perfis) \nou   plot.py -h [--help] (para ver esta ajuda)'
    pessoas = sys.argv[1:]
    nomes = [perfil['name'] for perfil in perfis]
    linhas = False
    if pessoas == ['-h'] or pessoas == ['-help']:
        print(ajudamsg)
    elif pessoas == ['-p'] or pessoas == ['-perfis']:
        print('Os perfis em perfis.json são:')
        map(print, nomes)
    else: 
        if pessoas[0] == '-l':
            linhas = True
            del(pessoas[0])
        for pessoa in pessoas:
            if pessoa not in nomes:
                raise Exception(f'Pessoa {pessoa} não é um dos perfis de perfis.json')
        plota(pessoas, linhas)