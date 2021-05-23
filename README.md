# vacina
Um script em python para acompanhar sua data estimada de vacinação puxando dados do site [Quando vou ser vacinado](https://quandovouservacinado.com/).

## Dependências
O pacote necessita das seguintes bibliotecas: `bs4 dateutil matplotlib`

## Instruções

- Inclua sua própria lista de pessoas a acompanhar criando um arquivo perfis.json da seguinte maneira:
```json
[
    {
        "nome":"Romeu",
        "idade":17,
        "estado":"SP",
        "prioritario":false
    },
    {
        "nome":"Julieta",
        "idade":13,
        "estado":"RJ",
        "prioritario":false
    },
    ...
]
```
- Se for usar o Windows Task Scheduler, edite também o `vacinação.bat`, inserindo seu usuário, ou o path correto de sua instalação python (o `.bat` assume anaconda). Assegure-se de que o arquivo `.bat` está salvo em formato ANSI; caso contrário, salve-o como tal.

## Plot (GUI)

Basta rodar `python gui.py`!

## Plot (Linha de comando)

Para plotar o número de dias estimados até a vacinação para cada data de acesso de várias pessoas, é só usar `python plot.py pessoa1 pessoa2 ...`. Mais informações em `python plot.py -h`.
