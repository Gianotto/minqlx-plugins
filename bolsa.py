import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from flask import Flask, render_template
import io
import base64

app = Flask(__name__)

# Define o código da empresa a ser buscada
empresa = 'BBAS3.SA'
# Busca os dados financeiros da empresa
empr = yf.Ticker(empresa)
dados = empr.history(period='1mo')
info = empr.info
title = '{} - {}'.format(info['symbol'], info['longName'])
#print(dados)
fig, ax = plt.subplots()

@app.route('/')
def index(): 
    ax.plot(dados) #, type="candle", mav=(10, 20), volume=True, title=title)
    # Salva o gráfico em um buffer de memória
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Converte o buffer em uma string base64 para exibir na página da web
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Renderiza a página da web com o gráfico
    return render_template('index.html', graphic=graphic)

if __name__ == '__main__':
    app.run()