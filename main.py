import streamlit as st 
import yfinance as yf
import pandas as pd
from datetime import timedelta, date


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