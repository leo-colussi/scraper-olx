# Scraper de OLX - Desafio Seazone

Projeto desenvolvido para desafio da empresa Seazone. O objetivo do projeto é obter informações de anúncios da OLX para terrenos na localização de Florianópolis e região em Santa Catarina. Em cada anúncio serão o tipo, o título, a descrição, o tamanho, a localização do imóvel e o nome do vendedor. O módulo de scraping utilizado para a coleta desses dados é "Beautiful Soup 4".
***

## Instalação 

Para o bom funcionamento do script é necessária a instalação de módulos específicos que são todos catalogados no arquivo "requirements.txt". Antes de instalá-los é aconselhável a criação de um "Virtual Environment" com Python na diretoria desejada.

```bash
py -m venv venv
```
Dessa forma será criada uma pasta chamada venv no diretório requerido.

Após isso poderá ser realizado a instalação das bíbliotecas.

```bash
pip install requirements.txt
```

Caso não funcione:

```bash
pip install - r requirements.txt
```
Feito isso, o script está pronto para ser utilizado.

***

## Modo de uso
No começo do script, existem algumas variáveis que podem ser modificadas para obter os resultados desejados. Por padrão no script são utilizadas essas configurações de pesquisa.

```python
PREFIXO = 'sc'
REGIAO = 'florianopolis-e-regiao'
CATEGORIA = 'imoveis'
SUBCATEGORIA = 'terrenos'
PAGINAS = 1
```
Após configurar corretamente a região, é necessário inicializar o script.


```bash
py scraper_seazone.py
```

No mesmo resultado onde estará o script será criado um arquivo chamado "terrenos.csv" onde contém todas as informações coletadas de cada anúncio analisado.

Exemplo de conteúdo do arquivo:
```csv
Título_1,preço_1,vendedor_1,tamanho_1,localização_1,descrição_1
Título_2,preço_2,vendedor_2,tamanho_2,localização_2,descrição_2
Título_3,preço_3,vendedor_3,tamanho_3,localização_3,descrição_3
Título_4,preço_4,vendedor_4,tamanho_4,localização_4,descrição_4
Título_5,preço_5,vendedor_5,tamanho_5,localização_5,descrição_5
```
Após a finalização da coleta de informações, serão exibidos no terminal todas as análises realizadas com os dados coletados, sendo eles:
* Quantidade de imovéis por município;
* Número médio, mínimo e máximo dos terrenos em metros quadrados;
* Número médio, mínimo e máximo dos preços dos terrenos.

Exemplo de conteúdo no terminal:
```bash
Número de anúncios por região:
Local_1: número
Local_2: número
local_3: número

 Tamanho terreno:
        Médio: número
        Mínimo: número
        Máximo: número
 Preço:
        Médio: número
        Mínimo: número
        Máximo: número
```
***
## Contribuições
Pull requests são sempre bem vindos. O código é público e está aberto a melhorias contínuas.
