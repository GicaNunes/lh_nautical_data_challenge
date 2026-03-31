import pandas as pd
import streamlit as st
import plotly.express as px
from collections import Counter
import unidecode
import re

# --- Carregar dados ---
df = pd.read_csv("data/csv/vendas_2023_2024.csv")
df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
df = df.dropna(subset=['sale_date'])
df["id_client"] = df["id_client"].astype(str)
df["total"] = pd.to_numeric(df["total"], errors="coerce")

produtos = pd.read_csv("data/csv/produtos_raw.csv")
clientes = pd.read_json("data/json/clientes_crm.json")

# --- Limpeza de categorias ---
def limpar_categoria(cat):
    if pd.isna(cat):
        return None
    cat = unidecode.unidecode(cat).lower().strip()
    cat = re.sub(r"\s+", "", cat)
    return cat

produtos["actual_category"] = produtos["actual_category"].apply(limpar_categoria)

mapa_categorias = {
    "ancoragem":"ancoragem","ancorajem":"ancoragem","ancora":"ancoragem",
    "eletronicos":"eletronicos","eletronico":"eletronicos",
    "propulsao":"propulsao","propulcao":"propulsao","propulsor":"propulsao"
}
produtos["actual_category"] = produtos["actual_category"].replace(mapa_categorias)
produtos["actual_category"] = produtos["actual_category"].fillna("Outros")

# --- Menu lateral ---
page = st.sidebar.radio("Selecione o dashboard:", ["Executivo", "Explorações Adicionais"])

# --- Filtros globais ---
st.sidebar.subheader("Filtros")
data_ini = st.sidebar.date_input("Data inicial", df['sale_date'].min())
data_fim = st.sidebar.date_input("Data final", df['sale_date'].max())
df = df[(df['sale_date'] >= pd.to_datetime(data_ini)) & (df['sale_date'] <= pd.to_datetime(data_fim))]

# --- Dashboard Executivo ---
if page == "Executivo":
    st.title("📊 Dashboard Executivo - Questões 2, 3 e 8")

    # Questão 2 - Estatísticas
    st.subheader("Questão 2 - Estatísticas de Vendas")
    stats = {
        "Linhas": df.shape[0],
        "Colunas": df.shape[1],
        "Data mínima": str(df['sale_date'].min().date()),
        "Data máxima": str(df['sale_date'].max().date()),
        "Valor mínimo": df['total'].min(),
        "Valor máximo": df['total'].max(),
        "Valor médio": round(df['total'].mean(), 2)
    }
    st.table(pd.DataFrame(stats.items(), columns=["Métrica", "Valor"]))

    # Questão 3 - Lucro acumulado por cliente
    st.subheader("Questão 3 - Lucro por Cliente")
    lucro_clientes = df.groupby('id_client')['total'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_clientes = px.bar(lucro_clientes, x="id_client", y="total",
                          color="id_client", color_discrete_sequence=px.colors.qualitative.Set2,
                          title="Top 10 Clientes por Lucro")
    st.plotly_chart(fig_clientes, use_container_width=True)
    st.dataframe(lucro_clientes)

    # Questão 8 - Distribuição de categorias
    st.subheader("Questão 8 - Distribuição de Categorias")
    df_cat = df.merge(produtos, left_on='id_product', right_on='code', how='left')
    ranking = df_cat.groupby('actual_category')['qtd'].sum().sort_values(ascending=False).reset_index()

    fig_cat = px.bar(ranking, x="actual_category", y="qtd",
                     color="actual_category", color_discrete_sequence=px.colors.qualitative.Dark2,
                     title="Ranking de Categorias (limpas)")
    st.plotly_chart(fig_cat, use_container_width=True)

    fig_donut = px.pie(ranking, names="actual_category", values="qtd", hole=0.4,
                       color="actual_category", color_discrete_sequence=px.colors.qualitative.Set3,
                       title="Distribuição de Vendas por Categoria (limpas)")
    st.plotly_chart(fig_donut, use_container_width=True)

    st.dataframe(ranking)

# --- Dashboard Explorações Adicionais ---
else:
    st.title("🔎 Explorações Adicionais")

    # Vendas mensais
    df['mes'] = df['sale_date'].dt.to_period('M').astype(str)
    mensal = df.groupby('mes')['qtd'].sum().reset_index()
    fig_mensal = px.line(mensal, x="mes", y="qtd", markers=True,
                         title="Vendas Mensais")
    st.plotly_chart(fig_mensal, use_container_width=True)

    # Vendas por dia da semana
    df['dia_semana'] = df['sale_date'].dt.day_name().astype(str)
    semana = df.groupby('dia_semana')['qtd'].sum().reset_index()
    fig_semana = px.bar(semana, x="dia_semana", y="qtd",
                        color="dia_semana", color_discrete_sequence=px.colors.qualitative.Set2,
                        title="Vendas por Dia da Semana")
    st.plotly_chart(fig_semana, use_container_width=True)

    # Top produtos
    df_cat = df.merge(produtos, left_on='id_product', right_on='code', how='left')
    top_produtos = df_cat.groupby('name')['qtd'].sum().sort_values(ascending=False).head(10).reset_index()
    top_produtos['name'] = top_produtos['name'].astype(str)
    fig_top = px.bar(top_produtos, x="name", y="qtd",
                     color="name", color_discrete_sequence=px.colors.qualitative.Pastel,
                     title="Top 10 Produtos")
    st.plotly_chart(fig_top, use_container_width=True)

    # Pares de produtos
    coocorrencia = df_cat.groupby(['id_client','sale_date'])['name'].apply(list)
    pares = Counter()
    for lista in coocorrencia:
        for i in range(len(lista)):
            for j in range(i+1, len(lista)):
                pares[(lista[i], lista[j])] += 1
    pares_top = pares.most_common(10)
    df_pares = pd.DataFrame(pares_top, columns=["Par de Produtos", "Frequência"])
    df_pares['Par de Produtos'] = df_pares['Par de Produtos'].apply(lambda x: f"{x[0]} + {x[1]}")
    fig_pares = px.bar(df_pares, x="Par de Produtos", y="Frequência",
                       color="Par de Produtos", color_discrete_sequence=px.colors.qualitative.Set2,
                       title="Top 10 Pares de Produtos Comprados Juntos")
    st.plotly_chart(fig_pares, use_container_width=True)
    st.dataframe(df_pares)
