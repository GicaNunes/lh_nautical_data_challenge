import pandas as pd
import streamlit as st
import plotly.express as px
from collections import Counter
import networkx as nx
import plotly.graph_objects as go

# --- Dados principais ---
df_raw = pd.read_csv("data/csv/vendas_2023_2024.csv")
df_raw['sale_date'] = pd.to_datetime(df_raw['sale_date'], errors='coerce')
df_raw = df_raw.dropna(subset=['sale_date'])
df = df_raw

# --- Menu lateral ---
page = st.sidebar.radio("Selecione o dashboard:", ["Executivo", "Explorações Adicionais"])

# --- Dashboard Executivo ---
if page == "Executivo":
    st.title("📊 LH Nauticals Data Challenge")

    tab1, tab2, tab3 = st.tabs(["Questão 4", "Questão 5", "Questão 6"])

    # Questão 4 – Ranking de Produtos
    with tab1:
        st.subheader("Produtos com maior valor e quantidade de vendas")
        if {'id_product','qtd','total'}.issubset(df.columns):
            ranking_valor = df.groupby('id_product')['total'].sum().sort_values(ascending=False).head(10).reset_index()
            fig1 = px.bar(ranking_valor, x="id_product", y="total", color="total",
                          color_continuous_scale="Reds", title="Top 10 Produtos por Valor Total de Vendas")
            st.plotly_chart(fig1, use_container_width=True)

            ranking_qtd = df.groupby('id_product')['qtd'].sum().sort_values(ascending=False).head(10).reset_index()
            fig2 = px.bar(ranking_qtd, x="id_product", y="qtd", color="qtd",
                          color_continuous_scale="Oranges", title="Top 10 Produtos por Quantidade Vendida")
            st.plotly_chart(fig2, use_container_width=True)

            st.info("Produtos mais vendidos em quantidade refletem alta demanda, enquanto os de maior valor indicam maior impacto no faturamento.")
        else:
            st.warning("Colunas necessárias não encontradas no dataset.")

    # Questão 5 – Clientes VIP
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
            st.info("Dias com menor média de vendas podem ser alvo de campanhas promocionais.")
        else:
            st.warning("Colunas necessárias não encontradas no dataset.")

# --- Dashboard de Explorações Adicionais ---
else:
    st.title("🔎 Explorações Adicionais")

    vendas = pd.read_csv("data/csv/vendas_2023_2024.csv")
    produtos = pd.read_csv("data/csv/produtos_raw.csv")
    clientes = pd.read_json("data/json/clientes_crm.json")

    vendas['sale_date'] = pd.to_datetime(vendas['sale_date'], errors='coerce')

    # Sazonalidade (corrigido para string)
    vendas['mes'] = vendas['sale_date'].dt.to_period('M').astype(str)
    mensal = vendas.groupby('mes')['qtd'].sum().reset_index()
    fig_mensal = px.line(mensal, x="mes", y="qtd", title="Vendas Mensais")
    st.plotly_chart(fig_mensal, use_container_width=True)

    # Vendas por dia da semana
    vendas['dia_semana'] = vendas['sale_date'].dt.day_name()
    semana = vendas.groupby('dia_semana')['qtd'].sum().reset_index()
    fig_semana = px.bar(semana, x="dia_semana", y="qtd", title="Vendas por Dia da Semana")
    st.plotly_chart(fig_semana, use_container_width=True)

    # Segmentação de clientes
    df_seg = vendas.merge(clientes, left_on='id_client', right_on='code', how='left')
    df_seg['ticket_medio'] = df_seg['total'] / df_seg['qtd']
    ticket_clientes = df_seg.groupby('full_name')['ticket_medio'].mean().sort_values(ascending=False).head(5).reset_index()
    fig_ticket = px.bar(ticket_clientes, x="full_name", y="ticket_medio", title="Top 5 Clientes VIP (Ticket Médio)")
    st.plotly_chart(fig_ticket, use_container_width=True)

    # Ranking de categorias
    df_cat = vendas.merge(produtos, left_on='id_product', right_on='code', how='left')
    ranking = df_cat.groupby('actual_category')['qtd'].sum().sort_values(ascending=False).reset_index()
    fig_cat = px.bar(ranking, x="actual_category", y="qtd", title="Ranking de Categorias")
    st.plotly_chart(fig_cat, use_container_width=True)

    # Top produtos
    top_produtos = df_cat.groupby('name')['qtd'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_top = px.bar(top_produtos, x="name", y="qtd", title="Top 10 Produtos")
    st.plotly_chart(fig_top, use_container_width=True)

    # Co-ocorrência de produtos
    coocorrencia = df_cat.groupby(['id_client','sale_date'])['name'].apply(list)
    pares = Counter()
    for lista in coocorrencia:
        for i in range(len(lista)):
            for j in range(i+1, len(lista)):
                pares[(lista[i], lista[j])] += 1
    
    # Selecionar os 10 pares mais comuns
    pares_top = pares.most_common(10)
    
    # Criar grafo
    G = nx.Graph()
    for (p1, p2), count in pares_top:
        G.add_edge(p1, p2, weight=count)
    
    pos = nx.spring_layout(G, seed=42)
    
    # Arestas
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='lightblue'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Nós
    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(size=20, color='orange')
    )
    
    fig_network = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Produtos comprados em conjunto",
            showlegend=False,
            hovermode='closest'
        )
    )
    
    st.plotly_chart(fig_network, use_container_width=True)
    
    
       
