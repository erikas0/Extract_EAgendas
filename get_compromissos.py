# bibliotecas

import pandas as pd 
import requests
import json
import os
import re
from config.properties import BEARER_API_CGU 
from config.logger import logger




class AgendasAutoridades():
    def __init__(self):
        bearer = f"Bearer {BEARER_API_CGU}"
        self.headers = {
            'Authorization': bearer
        }

    # colhendo orgaos
    def orgaos(self):
            #acessando api - cgu
        url = 'https://eagendas.cgu.gov.br/api/v2/orgaos'
        response = requests.get(url,headers=self.headers)
        if response.status_code == 503:
            logger.info("Site passando por instabilidade. Tente daqui alguns minutos!")
            raise 
        response.raise_for_status()
        json_orgaos = response.json()
        siglas,codigo_sigla = [],[]
        try:
            if 'resposta' in json_orgaos.keys():
                json_orgaos = json_orgaos['resposta']
                if 'orgaos' in json_orgaos.keys():
                    for i in json_orgaos['orgaos']:
                        siglas.append(i['sigla'])
                        codigo_sigla.append(i['id'])
        except Exception as e:
            logger.info('Erro no processamento do JSON de siglas.')
        return siglas, codigo_sigla

    def identifica_orgaos(self, sigla):
        try:
            siglas, codigo_sigla = self.orgaos()
            orgao_id = codigo_sigla[siglas.index(sigla)]
        except Exception as e:
            logger.info('Erro na ao identificar orgãos!')
            raise
        return orgao_id

    def inserir_compromissos(self, json_compromisso, df, apo_id):
        try:
            for i in json_compromisso['resposta']['compromissos']:
                i['objetivos_compromisso'] = r"\n".join(map(str,i['objetivos_compromisso']))
                part = ''
                if i['participantes_publicos'] != "":
                    for p in i['participantes_publicos']:
                        part = part + f"{p['apo_nome']} - {p['cargo']} ({p['orgao']}) \n"
                    
                i['participantes_publicos'] = [part]
                i['participantes_privados'] = r"\n".join(map(str,i['participantes_privados']))
                i['representantes'] = r"\n".join(map(str,i['representantes']))
                df_temporario = pd.DataFrame(i)
                df_temporario['apo_id'] = apo_id
                df = pd.concat([df,df_temporario])
                return df
        except Exception as e:
            logger.info("Erro ao inserir compromisso!")
            raise

    def busca_agentes_publicos(self, orgao_id):
        apo_list, cargo_comissao_list, cargo_efetivo_list = [], [], []
        try:
            url = f'https://eagendas.cgu.gov.br/api/v2/agentes-publicos-obrigados?orgao_id={orgao_id}'

            response = requests.get(url,headers=self.headers)
            if response.status_code == 503:
                logger.info("Site passando por instabilidade. Tente daqui alguns minutos!")
                raise 
            response.raise_for_status()
            
            json_agentes = response.json()
            if 'resposta' in json_agentes.keys():
                json_agentes = json_agentes['resposta']
                if 'agentes_publicos_obrigados' in json_agentes.keys():
                    df_agentes_publicos = pd.DataFrame(json_agentes['agentes_publicos_obrigados'])
                    df_agentes_publicos = df_agentes_publicos[df_agentes_publicos.data_termino.isna()]
                    
                    return df_agentes_publicos

        except Exception as e:
            logger.info('Erro no processamento do JSON de agente públicos obrigados.')
            raise
        


    def busca_compromissos_api(self, data_inicio,data_fim,sigla='MEC'):
        logger.info("Iniciando...")
        logger.info("Identificando Id do órgão")
        if sigla != 'MEC':
            orgao_id = self.identifica_orgaos(sigla)
        else:
            orgao_id = 549
        logger.info(f"Finalizou a identificação do Id do órgão. Id Órgão: {orgao_id}")
        
        logger.info('Buscando agentes públicos...')
        df_agente_publicos =  self.busca_agentes_publicos(orgao_id)
        apo_list = df_agente_publicos['apo_id'].tolist()
        logger.info('Finalizou busca de agentes públicos...')
        
        logger.info(f"Buscando compromissos dos {len(apo_list)} agentes públicos para o dia {data_inicio} até o dia {data_fim}...")
        df_compromissos = pd.DataFrame()
        for apo_id in apo_list:
            url = f'https://eagendas.cgu.gov.br/api/v2/compromissos?data_inicio={data_inicio}&data_termino={data_fim}&apo_id={apo_id}&orgao_id={orgao_id}'

            response = requests.get(url, headers=self.headers)
            if response.status_code == 503:
                logger.info("Site passando por instabilidade. Tente daqui alguns minutos!")
                raise 
            if response.json()['sucesso']:
                df_compromissos = self.inserir_compromissos(response.json(),df_compromissos,apo_id)
            
        df_compromissos = df_compromissos.merge(df_agente_publicos, 
                                                    how='left', 
                                                    on='apo_id', 
                                                    suffixes=("_compromissos",'_agentes')
            )
        logger.info("Finalizou busca de compromissos!")
        logger.info(f'Encontrado compromissos de {df_compromissos["apo_id"].nunique(dropna=True)} agentes!')
        
        logger.info('Salvando no excel...')
        if not os.path.isdir('./temp'):
            os.mkdir('./temp')
        
        df_compromissos.to_excel(f'./temp/AgendaCompromissos_{sigla}_{data_inicio}_{data_fim}.xlsx',index=False,engine='openpyxl')
        logger.info("Excel salvo no Docker com sucesso! Transferir para máquina local.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        logger.info("Por favor, disponibilize sigla, data inicial e data final!")
        sys.exit(1)

    #sigla = 'MEC'
    #data_inicio = '28-07-2025'
    #data_fim = '28-07-2025'
    
    sigla = sys.argv[1]
    data_inicio = sys.argv[2]
    data_fim = sys.argv[3]
    
    get_compromissos = AgendasAutoridades()
    get_compromissos.busca_compromissos_api(data_inicio,data_fim,sigla)