# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Criado por  : Leonarodo Colussi
# Data de criação: 20/02/2022
# versão = '1.0'
# ---------------------------------------------------------------------------
""" Scraper de OLX para coleta de informações em anúncios """

import csv
import json
import os.path
import numpy as np
from lxml import html
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36'
}

PREFIXO = 'sc'
REGIAO = 'florianopolis-e-regiao'
CATEGORIA = 'imoveis'
SUBCATEGORIA = 'terrenos'
PAGINAS = 1


class Scraper():
    """
    Classe para definição do Scraper e seus métodos
    """

    def __init__(self):
        self.sessao = HTMLSession()
        self.precos = []
        self.tamanhos = []
        self.regioes = []

        if not os.path.isfile('terrenos.csv'):
            with open('terrenos.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'tipo', 'título', 'preço',
                    'vendedor', 'tamanho',
                    'localização', 'descrição'
                    ])

    def pagina_principal(self):
        """
        Realiza o request da página principal com os links dos anúncios.

        :param None

        :return bs4 object :
        """
        lista_paginas = []
        for pagina in range(1, PAGINAS + 1):
            url = f'https://{PREFIXO}.olx.com.br/{REGIAO}/{CATEGORIA}/{SUBCATEGORIA}?o={pagina}'
            result = self.sessao.get(url, headers=HEADERS)

            doc = bs(result.content, "lxml")
            div = doc.find(class_='h3us20-6 dQYDAH')
            itens = div.find_all('li')

            for item in itens:
                try:
                    tag_a = item.find('a')
                    link = tag_a['href']
                except TypeError:
                    continue

                lista_paginas.append(link)

        return lista_paginas

    def pagina_anuncio(self, link):
        """
        Realiza o request da página do anúncio individual.

        :param link: string

        :return bs4 object html:
        """
        req_an = self.sessao.get(link, headers=HEADERS)
        print(link)
        return bs(req_an.content, 'html.parser'), req_an


    def tipo(self, anuncio):
        """
        Retorna um dict com todas as informações dos locais

        :param anuncio: bs4 object

        :return float principal_amount * (1 + rate)**time:
        """
        tipo = anuncio.find('div', class_='h3us20-6 bcHOOp')
        tipo = tipo.find_all('div', class_='duvuxf-0 h3us20-0 jyICCp')[1]
        tipo = tipo.find(
            'dd', class_='sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ').text
        return tipo[0:len(tipo) - 1]

    def titulo(self, anuncio):
        """
        Coleta o título do anúncio do terreno.

        :param anuncio: bs4 object

        :return titulo: string
        """
        titulo = anuncio.find(class_='h3us20-6 gFNxVM')
        return titulo.find(class_='sc-45jt43-0 eCghYu sc-ifAKCX cmFKIN').string

    def preco(self, anuncio):
        """
        Coleta o valor do preço do terreno.

        :param anuncio: bs4 object

        :return preco: int
        """
        preco_card = anuncio.find('div', class_='h3us20-6 iYWWXj').h2.text
        preco = preco_card.replace('R$ ', '').replace(
            '.', '').replace(',', '.')

        if preco != '':
            self.precos.append(int(preco))
        return preco

    def descricao(self, anuncio):
        """
        Coleta a descrição do anúncio do terreno.

        :param anuncio: bs4 object

        :return descricao: string
        """
        descricao_card = anuncio.find('div', class_='h3us20-6 jtENip')
        descricao = descricao_card.find(
            class_='sc-1sj3nln-1 eOSweo sc-ifAKCX cmFKIN').text
        return descricao.replace('\n', '')

    def vendedor(self, anuncio):
        """
        Coleta o nome do vendedor/empresa do terreno.

        :param anuncio: bs4 object

        :return vendedor: string
        """
        root = html.fromstring(anuncio.content)
        tag = root.xpath('/html/body/script[1]/@data-json')
        resultado = tag[0].replace("'","/")
        res_dict = json.loads(resultado)
        return res_dict['ad']['user']['name']


    def tamanho(self, anuncio):
        """
        Coleta o valor do tamanho do terreno.

        :param anuncio: bs4 object

        :return tamanho: int
        """
        tamanho_card = anuncio.find('div', class_='h3us20-6 bcHOOp')
        tamanho_card = tamanho_card.find_all(
            'div', class_='duvuxf-0 h3us20-0 jyICCp')[-1]
        tamanho_card = tamanho_card.find(
            'dd', class_='sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ').text
        tamanho = ''
        if 'm²' in tamanho_card:
            tamanho = int(tamanho_card.replace('m²', ''))
            self.tamanhos.append(int(tamanho))
        return tamanho

    def localizacao(self, anuncio):
        """
        Retorna um dict com todas as informações dos locais

        :param anuncio: bs4 object

        :return info_local: dict
        """
        info_local = {}
        localizacao = anuncio.find('div', class_='h3us20-6 fiikIi')
        localizacao = localizacao.find_all(
            class_='sc-hmzhuo sc-1f2ug0x-3 ONRJp sc-jTzLTM iwtnNi')

        for card in localizacao:
            nome = card.find(
                class_='sc-1f2ug0x-0 cLGFbW sc-ifAKCX cmFKIN').text
            atributo = card.find(
                class_='sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ').text
            info_local[nome] = atributo

        self.regioes.append(info_local['Município'])
        return info_local

    def csv(self, titulo, preco, vendedor,
            tamanho, localizacao, descricao):
        """
        Cria um arquivo csv e escreve os dados coletado em um
        arquivo chamado terrenos.csv

        :param tipo: string
        :param titulo: string
        :param preco: int
        :param vendedor: string
        :param tamanho: int
        :param localizacao: dict
        :param descricao: string

        :return None:
        """
        with open('terrenos.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                titulo, preco,vendedor, tamanho,
                localizacao, descricao
            ])
            return

    def encerrar_sessao(self):
        """
        Encerra a sessão do request_html.

        :param None:

        :return None:
        """
        self.sessao.close()

    def analise_local(self):
        """
        Realiza a análise de quantidade de anúncio por local.

        :param None:

        :return string: string
        """
        string = 'Número de anúncios por região:\n'
        for regiao in set(self.regioes):
            contador = 0
            for item in self.regioes:
                if item == regiao:
                    contador += 1
            string += f'{regiao}: {contador}\n'
        return string


    def analise_tamanho(self):
        """
        Realiza a análise do tamanho dos terrenos dos anúncios.

        :param None:

        :return string: string
        """
        self.tamanhos = [i for i in self.tamanhos if i != 0]
        min_tam = np.min(self.tamanhos)
        max_tam = np.max(self.tamanhos)
        med_tam = np.mean(self.tamanhos)
        return f'''Tamanho terreno:\n\t
                    Médio: {med_tam:.2f}\n\t
                    Mínimo: {min_tam:.2f}\n\t
                    Máximo: {max_tam:.2f}\n\n'''

    def analise_preco(self):
        """
        Realiza a análise do preço dos terrenos dos anúncios.

        :param None:

        :return string: string
        """
        min_preco = np.min(self.precos)
        max_preco = np.max(self.precos)
        med_preco = np.mean(self.precos)
        return f'''Preço:\n\t
                    Médio: {med_preco:.2f}\n\t
                    Mínimo: {min_preco:.2f}\n\t
                    Máximo: {max_preco:.2f}\n'''


def main():
    """
    Função principal para o funcionamento do script
    """
    scraper = Scraper()
    lista_pag = scraper.pagina_principal()
    print(len(lista_pag))

    for link in lista_pag:
        anuncio, request = scraper.pagina_anuncio(link)
        if scraper.tipo(anuncio) != 'Terreno':
            continue
        titulo = scraper.titulo(anuncio)
        preco = scraper.preco(anuncio)
        descricao = scraper.descricao(anuncio)
        vendedor = scraper.vendedor(request)
        tamanho = scraper.tamanho(anuncio)
        localizacao = scraper.localizacao(anuncio)
        scraper.csv(titulo, preco, vendedor,
                    tamanho, localizacao, descricao)

    scraper.encerrar_sessao()
    analise_local = scraper.analise_local()
    analise_tamanho = scraper.analise_tamanho()
    analise_preco = scraper.analise_preco()

    print(analise_local, analise_tamanho, analise_preco)


if "__main__" == __name__:
    main()
