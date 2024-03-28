# %%
## separando os dados por UF em um data frame

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

chunk_size = 10000  
chunks = pd.read_csv("C:/Users/Sergio Notebook/Downloads/Anvisa_dc/DB-Anvisa2.csv", chunksize=chunk_size)

dados_PI = pd.DataFrame()  # DataFrame vazio para acumular os resultados

for chunk in chunks:
    filtrado = chunk[chunk['UF_VENDA'] == 'PI']
    dados_PI = pd.concat([dados_PI, filtrado])
# %%
print(dados_PI.shape)
dados_PI.head()

# %%
print(dados_PI.columns)

# %%
colunas = dados_PI.columns

for nome in colunas:
    print( dados_PI[nome].value_counts())
