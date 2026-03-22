import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Lê o arquivo bruto
df_raw = pd.read_csv("data/csv/vendas_2023_2024.csv")

# Tratamento simples
df_raw['sale_date'] = pd.to_datetime(df_raw['sale_date'], errors='coerce')
df_raw = df_raw.dropna(subset=['sale_date'])
df = df_raw

# Título principal
st.title("📊 LH Nauticals Data Challenge")

# Layout com abas
tab1, tab2, tab3 = st.tabs(["Questão 4", "Questão 5", "Questão 6"])

# Questão 4 – Ranking de Produtos por Vendas
st.header("Questão 4 – Ranking de Produtos por Vendas")

if {'id_product','qtd','total'}.issubset(df.columns):
    # Ranking por valor total
    ranking_produtos = df.groupby('id_product')['total'].sum().sort_values(ascending=False).head(10).reset_index()

    fig = px.bar(ranking_produtos, x="id_product", y="total", color="total",
                 color_continuous_scale="Reds", title="Top 10 Produtos por Valor Total de Vendas")
    st.plotly_chart(fig, use_container_width=True)

    st.info("Produtos com maior valor de vendas podem ser analisados para estratégias de estoque e marketing.")

    # Ranking por quantidade vendida (opcional)
    ranking_qtd = df.groupby('id_product')['qtd'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(ranking_qtd, x="id_product", y="qtd", color="qtd",
                  color_continuous_scale="Oranges", title="Top 10 Produtos por Quantidade Vendida")
    st.plotly_chart(fig2, use_container_width=True)

    st.info("Produtos mais vendidos em quantidade podem indicar popularidade e demanda.")
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
