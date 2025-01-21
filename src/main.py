import streamlit as st 
import yfinance as yf
import pandas as pd
import os
from datetime import timedelta, date
import logging
import logfire
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logging import basicConfig, getLogger


# ------------------------------------------------------
# Configuração Logfire
logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()

# ------------------------------------------------------
# Importar Base e BitcoinPreco do database.py
from database import Base, ticket_price

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Lê as variáveis separadas do arquivo .env
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Monta a URL de conexão ao banco PostgreSQL (sem SSL)
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Cria o engine e a sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def criar_tabela():
    """Cria a tabela no banco de dados, se não existir."""
    Base.metadata.create_all(engine)
    logger.info("Tabela criada/verificada com sucesso!")
#cria as funcoes de carregaento de dados


final_date = "2025-1-21"
def carrega_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao =  yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start="2020-1-1", end= final_date )
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

#acoes = ["JPM", "COST", "DIS", "AMZN", "DE"]
acoes = ["JPM"]
dados = carrega_dados(acoes)
print(dados)

def tratar_dados(dados):
    valor = float(dados['close'],['Valor'])
    timestamp = datetime.now()

    dados_tratados = {
        "valor": valor,
        "Data": timestamp
       
    }

    return dados_tratados

def salvar_dados_postgres(dados):
    """Salva os dados no banco PostgreSQL."""
    session = Session()
    try:
        novo_registro = ticket_price(**dados)
        session.add(novo_registro)
        session.commit()
        logger.info(f"[{dados['timestamp']}] Dados salvos no PostgreSQL!")
    except Exception as ex:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {ex}")
        session.rollback()
    finally:
        session.close()

