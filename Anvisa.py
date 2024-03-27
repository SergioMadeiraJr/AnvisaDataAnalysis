# %%

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%

chunk_size = 10000  # Experimente com tamanhos diferentes para encontrar o melhor para sua situação
chunks = pd.read_csv("C:/Users/Sergio Notebook/Downloads/Anvisa_dc/DB-Anvisa2.csv", chunksize=chunk_size)

#for chunk in chunks:
    # Processe cada parte aqui
    # print(chunk.head())  
# %%
dados_PI = pd.DataFrame()  # DataFrame vazio para acumular os resultados

for chunk in chunks:
    filtrado = chunk[chunk['UF_VENDA'] == 'PI']
    dados_PI = pd.concat([dados_PI, filtrado])

# %%
print(dados_PI.shape)


# %%
 dados_PI.head()
 dados_PI.nunique()
 dados_PI['QTD_UNIDADE_FARMACOTECNICA'].value_counts()
 tipos_unicos = dados_PI['QTD_UNIDADE_FARMACOTECNICA'].apply(type).unique()

print(tipos_unicos)

filtro_str = dados_PI['QTD_UNIDADE_FARMACOTECNICA'].apply(lambda x: isinstance(x, str))
df_str = dados_PI[filtro_str]

print(df_str)
# %%

dados_PI['QTD_UNIDADE_FARMACOTECNICA'] = pd.to_numeric(dados_PI['QTD_UNIDADE_FARMACOTECNICA'], errors='coerce')

# Substituir NaNs por 0
dados_PI['QTD_UNIDADE_FARMACOTECNICA'].fillna(0, inplace=True)

dados_PI['ANO_MES'] = dados_PI['ANO_VENDA'].astype(str) + '-' + dados_PI['MES_VENDA'].astype(str).str.zfill(2)

# Agrupando os dados por 'ANO_MES' e somar a 'QTD_UNIDADE_FARMACOTECNICA'
vendas_mensais = dados_PI.groupby('ANO_MES')['QTD_UNIDADE_FARMACOTECNICA'].sum().reset_index()

# Convertendo 'ANO_MES' para tipo datetime para ordenação correta no gráfico
vendas_mensais['ANO_MES'] = pd.to_datetime(vendas_mensais['ANO_MES'])

# Ordenando os dados por 'ANO_MES'
vendas_mensais = vendas_mensais.sort_values('ANO_MES')

# Visualizando com um gráfico de linha
plt.figure(figsize=(, 6))
plt.plot(vendas_mensais['ANO_MES'], vendas_mensais['QTD_UNIDADE_FARMACOTECNICA'], marker='o', linestyle='-')
plt.title('Evolução da Quantidade de Medicamentos Vendidos ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Quantidade de Unidades Vendidas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# Agrupando por princípio ativo e ANO_MES, e somando a quantidade de unidades vendidas
vendas_por_grupo = dados_PI.groupby(['PRINCIPIO_ATIVO', 'ANO_MES'])['QTD_UNIDADE_FARMACOTECNICA'].sum().reset_index()

# Convertendo 'ANO_MES' para datetime para ordenação e visualização adequadas
vendas_por_grupo['ANO_MES'] = pd.to_datetime(vendas_por_grupo['ANO_MES'])
vendas_por_grupo.sort_values(by=['PRINCIPIO_ATIVO', 'ANO_MES'], inplace=True)

# %%


# Exemplo: Visualizando os dados para os 5 princípios ativos mais vendidos
top_principios = vendas_por_grupo.groupby('PRINCIPIO_ATIVO')['QTD_UNIDADE_FARMACOTECNICA'].sum().nlargest(5).index

dados_top_principios = vendas_por_grupo[vendas_por_grupo['PRINCIPIO_ATIVO'].isin(top_principios)]

plt.figure(figsize=(12, 6))
sns.lineplot(data=dados_top_principios, x='ANO_MES', y='QTD_UNIDADE_FARMACOTECNICA', hue='PRINCIPIO_ATIVO', marker='o')
plt.title('Evolução das Vendas dos 5 Princípios Ativos Mais Vendidos')
plt.xlabel('Data')
plt.ylabel('Quantidade de Unidades Vendidas')
plt.xticks(rotation=45)
plt.legend(title='Princípio Ativo')
plt.tight_layout()
plt.show()

# %%
print(top_principios)

# %%


# Calculando a variação percentual de mês para mês
vendas_mensais['VARIAÇÃO_MENSAL'] = vendas_mensais['QTD_UNIDADE_FARMACOTECNICA'].pct_change() * 100

# Calculando a variação anual
# Primeiro, extrair o ano do 'ANO_MES'
vendas_mensais['ANO'] = vendas_mensais['ANO_MES'].dt.year

# Agora, agrupar por 'ANO' e somar antes de calcular a variação percentual
vendas_anuais = vendas_mensais.groupby('ANO')['QTD_UNIDADE_FARMACOTECNICA'].sum().pct_change() * 100

# Mostrando os resultados
print(vendas_mensais[['ANO_MES', 'VARIAÇÃO_MENSAL']])
print(vendas_anuais)


# %%

# Configurando o estilo do gráfico
sns.set(style="whitegrid")

# Criando o gráfico de linha para a variação mensal
plt.figure(figsize=(14, 7))
plt.plot(vendas_mensais['ANO_MES'], vendas_mensais['VARIAÇÃO_MENSAL'], marker='o', linestyle='-', color='blue')
plt.title('Variação Mensal na Quantidade de Unidades Farmacotécnicas Vendidas')
plt.xlabel('Mês/Ano')
plt.ylabel('Variação Percentual')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# Resetando o índice para facilitar a plotagem
vendas_anuais = vendas_anuais.reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='ANO', y='QTD_UNIDADE_FARMACOTECNICA', data=vendas_anuais, palette='coolwarm')
plt.title('Variação Anual na Quantidade de Unidades Farmacotécnicas Vendidas')
plt.xlabel('Ano')
plt.ylabel('Variação Percentual')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# Agrupando os dados por princípio ativo e ANO_MES, e somando a QTD_UNIDADE_FARMACOTECNICA
vendas_top_mensais = dados_top_principios.groupby(['PRINCIPIO_ATIVO', 'ANO_MES'])['QTD_UNIDADE_FARMACOTECNICA'].sum().reset_index()

# Calculando a variação percentual mensal para cada princípio ativo
vendas_top_mensais['VARIAÇÃO_MENSAL'] = vendas_top_mensais.groupby('PRINCIPIO_ATIVO')['QTD_UNIDADE_FARMACOTECNICA'].pct_change() * 100

plt.figure(figsize=(14, 7))
sns.lineplot(data=vendas_top_mensais, x='ANO_MES', y='VARIAÇÃO_MENSAL', hue='PRINCIPIO_ATIVO', marker='o', linestyle='-')
plt.title('Variação Mensal na Quantidade de Unidades Farmacotécnicas Vendidas (Top Princípios Ativos)')
plt.xlabel('Mês/Ano')
plt.ylabel('Variação Percentual (%)')
plt.xticks(rotation=45)
plt.legend(title='Princípio Ativo')
plt.tight_layout()
plt.show()

# %%

sns.set(style="whitegrid")

# Criando a figura e os eixos para os subplots
fig, axs = plt.subplots(2, 1, figsize=(14, 14), sharex=True)

# Plotando a variação mensal total no primeiro subplot
sns.lineplot(ax=axs[0], x=vendas_mensais['ANO_MES'], y=vendas_mensais['VARIAÇÃO_MENSAL'], color='blue', marker='o', linestyle='-')
axs[0].set_title('Variação Mensal Total na Quantidade de Unidades Farmacotécnicas Vendidas')
axs[0].set_ylabel('Variação Percentual (%)')
axs[0].tick_params(axis='x', rotation=45)

# Plotando a variação mensal dos princípios ativos mais vendidos no segundo subplot
sns.lineplot(ax=axs[1], data=vendas_top_mensais, x='ANO_MES', y='VARIAÇÃO_MENSAL', hue='PRINCIPIO_ATIVO', marker='o', linestyle='-')
axs[1].set_title('Variação Mensal para Top Princípios Ativos')
axs[1].set_xlabel('Mês/Ano')
axs[1].set_ylabel('Variação Percentual (%)')
axs[1].tick_params(axis='x', rotation=45)
axs[1].legend(title='Princípio Ativo')

plt.tight_layout()
plt.show()


# %%

sns.set(style="whitegrid")

# Criando a figura
plt.figure(figsize=(14, 8))

# Plotando a variação mensal total
sns.lineplot(x=vendas_mensais['ANO_MES'], y=vendas_mensais['VARIAÇÃO_MENSAL'], label='Variação Mensal Total', color='gray', linestyle='--')

# Plotando a variação mensal para cada um dos top princípios ativos
for principio in top_principios:
    subset = vendas_top_mensais[vendas_top_mensais['PRINCIPIO_ATIVO'] == principio]
    sns.lineplot(x=subset['ANO_MES'], y=subset['VARIAÇÃO_MENSAL'], label=principio)

# Configurando títulos e etiquetas
plt.title('Variação Mensal na Quantidade de Unidades Farmacotécnicas Vendidas')
plt.xlabel('Mês/Ano')
plt.ylabel('Variação Percentual (%)')
plt.xticks(rotation=45)
plt.legend(title='Princípio Ativo / Total', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# %%

# Agrupando os dados por princípio ativo e ANO_MES, e somando a QTD_UNIDADE_FARMACOTECNICA
vendas_por_principio_mensal = dados_PI.groupby(['PRINCIPIO_ATIVO', 'ANO_MES'])['QTD_UNIDADE_FARMACOTECNICA'].sum().reset_index()

# Calculando a variação percentual mensal para cada princípio ativo
vendas_por_principio_mensal['VARIAÇÃO_MENSAL'] = vendas_por_principio_mensal.groupby('PRINCIPIO_ATIVO')['QTD_UNIDADE_FARMACOTECNICA'].pct_change() * 100

# Identificando os medicamentos com as maiores variações mensais
# Podemos usar o valor absoluto da variação para considerar tanto aumentos quanto diminuições
vendas_por_principio_mensal['VARIAÇÃO_ABS'] = vendas_por_principio_mensal['VARIAÇÃO_MENSAL'].abs()

# Ordenando os medicamentos pela variação absoluta e pegando os top N
top_variações = vendas_por_principio_mensal.sort_values(by='VARIAÇÃO_ABS', ascending=False).head(10)

print(top_variações[['PRINCIPIO_ATIVO', 'ANO_MES', 'VARIAÇÃO_MENSAL']])

# %%


plt.figure(figsize=(24, 6))
sns.lineplot(data=dados_PI, x='ANO_MES', y='QTD_UNIDADE_FARMACOTECNICA', marker='o', label='NANDROLONA')
plt.title(f'Evolução das Vendas de NANDROLONA')
plt.xlabel('Data')
plt.ylabel('Quantidade de Unidades Vendidas')
plt.xticks(rotation=45)
plt.legend(title='Princípio Ativo')
plt.tight_layout()
plt.show()

# %%
# Filtrando para o princípio ativo de interesse e os meses específicos
filtro_nandrolona = vendas_por_principio_mensal['PRINCIPIO_ATIVO'] == 'NANDROLONA'
filtro_meses = vendas_por_principio_mensal['ANO_MES'].isin(['2021-02', '2021-03'])
dados_nandrolona = vendas_por_principio_mensal[filtro_nandrolona & filtro_meses]

print(dados_nandrolona[['PRINCIPIO_ATIVO', 'ANO_MES', 'QTD_UNIDADE_FARMACOTECNICA']])

# %%
# Aplicando filtro para o princípio ativo 'NANDROLONA'
filtro_principio_ativo = dados_PI['PRINCIPIO_ATIVO'] == 'MALEATO DE MIDAZOLAM'
dados_analise = dados_PI[filtro_principio_ativo]
dados_PI['ANO_MES'] = pd.to_datetime(dados_PI['ANO_MES'])


plt.figure(figsize=(24, 6))
sns.lineplot(data=dados_PI, x='ANO_MES', y='QTD_UNIDADE_FARMACOTECNICA', marker='o', label='NANDROLONA')
plt.title('Evolução das Vendas de NANDROLONA')
plt.xlabel('Data')
plt.ylabel('Quantidade de Unidades Vendidas')
plt.xticks(rotation=45)
plt.legend(title='Princípio Ativo')
plt.tight_layout()
plt.show()


# %%
# Analise de vendas por municipio

vendas_por_municipio = dados_PI.groupby('MUNICIPIO_VENDA')['QTD_UNIDADE_FARMACOTECNICA'].sum().reset_index()

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(14, 8))
sns.barplot(data=vendas_por_municipio, x='QTD_UNIDADE_FARMACOTECNICA', y='MUNICIPIO_VENDA')
plt.title('Distribuição das Vendas de Medicamentos por Município no PI')
plt.xlabel('Quantidade de Unidades Vendidas')
plt.ylabel('Município')
plt.tight_layout()
plt.show()

# %%
#quantidade de vendas por municipio
print(vendas_por_municipio)

# %%
# encontrando o top 3 para cada um deles

vendas_municipio_principio = dados_PI.groupby(['MUNICIPIO_VENDA', 'PRINCIPIO_ATIVO'])['QTD_UNIDADE_FARMACOTECNICA'].sum().reset_index()

top_3_por_municipio = vendas_municipio_principio.groupby('MUNICIPIO_VENDA').apply(lambda x: x.nlargest(3, 'QTD_UNIDADE_FARMACOTECNICA')).reset_index(drop=True)

# Exibindo os resultados para inspeção
print(top_3_por_municipio)

# %%


# Top 3 de alguns municipios 
municipios_de_interesse = ['TERESINA', 'PICOS', 'PARNAÍBA']  

for municipio in municipios_de_interesse:
    # Filtrando dados para o município atual
    dados_municipio = top_3_por_municipio[top_3_por_municipio['MUNICIPIO_VENDA'] == municipio]
    
    # Criando o gráfico de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dados_municipio, x='PRINCIPIO_ATIVO', y='QTD_UNIDADE_FARMACOTECNICA')
    plt.title(f'Top 3 Medicamentos Mais Vendidos em {municipio}')
    plt.xlabel('Princípio Ativo')
    plt.ylabel('Quantidade de Unidades Vendidas')
    plt.xticks(rotation=45)
    plt.show()

# %%


# Supondo que 'dados_PI' seja o DataFrame original com todos os dados
# E que 'top_3_por_municipio' contém os top 3 medicamentos para cada município

municipios_de_interesse = ['TERESINA', 'PICOS', 'PARNAÍBA']

for municipio in municipios_de_interesse:
    # Identificando os top 3 medicamentos para o município atual
    top_medicamentos = top_3_por_municipio[top_3_por_municipio['MUNICIPIO_VENDA'] == municipio]['PRINCIPIO_ATIVO'].unique()
    
    # Filtrando os dados originais para incluir apenas os top 3 medicamentos desse município
    dados_filtrados = dados_PI[(dados_PI['MUNICIPIO_VENDA'] == municipio) & (dados_PI['PRINCIPIO_ATIVO'].isin(top_medicamentos))]
    
    # Convertendo 'ANO_MES' para datetime para facilitar a plotagem
    dados_filtrados['ANO_MES'] = pd.to_datetime(dados_filtrados['ANO_MES'])
    
    # Criando o gráfico
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=dados_filtrados, x='ANO_MES', y='QTD_UNIDADE_FARMACOTECNICA', hue='PRINCIPIO_ATIVO', marker='o', style='PRINCIPIO_ATIVO')
    plt.title(f'Variação Mensal das Vendas dos Top 3 Medicamentos em {municipio}')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Unidades Vendidas')
    plt.xticks(rotation=45)
    plt.legend(title='Princípio Ativo')
    plt.tight_layout()
    plt.show()
