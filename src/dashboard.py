import streamlit as st
import pandas as pd

# Carregar dados tratados
df = pd.read_csv("data/df_tratado.csv")
df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')

st.title("📊 Dashboard LH Nauticals")

# Questão 4 – Prejuízos por Produto
st.header("Questão 4 – Prejuízos por Produto")
if 'custo_unitario' in df.columns:
    df['prejuizo'] = df['total'] - (df['qtd'] * df['custo_unitario'])
    ranking_prejuizo = df.groupby('name')['prejuizo'].sum().sort_values()
    st.bar_chart(ranking_prejuizo.head(10))
    st.write("Produtos com maior prejuízo devem ser reavaliados em termos de preço ou custo.")

# Questão 5 – Clientes com maior lucro acumulado
st.header("Questão 5 – Clientes com maior lucro acumulado")
lucro_clientes = df.groupby('id_client')['total'].sum().sort_values(ascending=False).head(10)
st.bar_chart(lucro_clientes)
st.write("Clientes VIP concentram grande parte do faturamento. Estratégias de fidelização são recomendadas.")

# Questão 6 – Vendas médias por dia da semana
st.header("Questão 6 – Vendas médias por dia da semana")
dias = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
media_semana = df.groupby(df['sale_date'].dt.day_name())['qtd'].mean().reindex(dias, fill_value=0)
st.bar_chart(media_semana)
st.write("Dias fracos podem ser alvo de campanhas promocionais.")
