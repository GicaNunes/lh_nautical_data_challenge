# --- Depois de aplicar filtros de data no df ---
df_cat = df.merge(produtos, left_on='id_product', right_on='code', how='left')

# Função para encurtar nomes longos
def encurtar_nome(nome):
    if len(nome) > 30:
        return nome[:27] + "..."
    return nome

# Adicionar coluna com nomes encurtados
df_cat['name_curto'] = df_cat['name'].apply(encurtar_nome)

# --- Questão 8: Ranking de categorias ---
ranking = df_cat.groupby('actual_category')['qtd'].sum().sort_values(ascending=False).reset_index()
fig_cat_bar = px.bar(ranking, x="actual_category", y="qtd", title="📦 Ranking de Categorias")
fig_cat_donut = px.pie(ranking, names="actual_category", values="qtd", hole=0.4,
                       title="📦 Distribuição de Vendas por Categoria")

# --- Top produtos ---
top_produtos = df_cat.groupby('name_curto')['qtd'].sum().sort_values(ascending=False).head(10).reset_index()
fig_top = px.bar(top_produtos, x="name_curto", y="qtd", title="🏆 Top 10 Produtos")

# --- Pares de produtos ---
coocorrencia = df_cat.groupby(['id_client','sale_date'])['name_curto'].apply(list)
from collections import Counter
pares = Counter()
for lista in coocorrencia:
    for i in range(len(lista)):
        for j in range(i+1, len(lista)):
            pares[(lista[i], lista[j])] += 1
pares_top = pares.most_common(10)
df_pares = pd.DataFrame(pares_top, columns=["Par de Produtos", "Frequência"])
df_pares['Par de Produtos'] = df_pares['Par de Produtos'].apply(lambda x: f"{x[0]} + {x[1]}")
fig_pares = px.bar(df_pares, x="Par de Produtos", y="Frequência",
                   title="🤝 Top 10 Pares de Produtos Comprados Juntos",
                   color="Frequência", color_continuous_scale="Blues")
