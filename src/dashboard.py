import pandas as pd
import streamlit as st
import plotly.express as px

# Lê o arquivo bruto
df_raw = pd.read_csv("data/csv/vendas_2023_2024.csv")

# Tratamento simples
df_raw['sale_date'] = pd.to_datetime(df_raw['sale_date'], errors='coerce')
df_raw = df_raw.dropna(subset=['sale_date'])

df = df_raw

# Layout com abas
st.title("📊 LH Nauticals Data Challenge")
tab1, tab2, tab3 = st.tabs(["Questão 4", "Questão 5", "Questão 6"])

# Questão 4 – Prejuízos por Produto
with tab1:
    st.subheader("Produtos com maior prejuízo")
    if {'custo_unitario','qtd','total','name'}.issubset(df.columns):
        df['prejuizo'] = df['total'] - (df['qtd'] * df['custo_unitario'])
        ranking_prejuizo = df.groupby('name')['prejuizo'].sum().sort_values().head(10).reset_index()
        fig = px.bar(ranking_prejuizo, x="name", y="prejuizo", color="prejuizo",
                     color_continuous_scale="Reds", title="Top 10 Produtos com Prejuízo")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Produtos com maior prejuízo devem ser reavaliados em termos de preço ou custo.")
    else:
        st.warning("Colunas necessárias não encontradas no dataset.")

# Questão 5 – Clientes com maior lucro acumulado
with tab2:
    st.subheader("Clientes VIP")
    if {'id_client','total'}.issubset(df.columns):
        lucro_clientes = df.groupby('id_client')['total'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(lucro_clientes, x="id_client", y="total", color="total",
                     color_continuous_scale="Blues", title="Top 10 Clientes por Lucro")
        st.plotly_chart(fig, use_container_width=True)
        st.success("Clientes VIP concentram grande parte do faturamento. Estratégias de fidelização são recomendadas.")
    else:
        st.warning("Colunas necessárias não encontradas no dataset.")

# Questão 6 – Vendas médias por dia da semana
with tab3:
    st.subheader("Vendas médias por dia da semana")
    if 'qtd' in df.columns:
        dias = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        media_semana = df.groupby(df['sale_date'].dt.day_name())['qtd'].mean().reindex(dias, fill_value=0).reset_index()
        fig = px.bar(media_semana, x="sale_date", y="qtd", color="qtd",
                     color_continuous_scale="Greens", title="Média de Vendas por Dia da Semana")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Dias fracos podem ser alvo de campanhas promocionais.")
    else:
        st.warning("Colunas necessárias não encontradas no dataset.")
