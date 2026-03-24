import pandas as pd

# -----------------------------
# Parte 1 — Carregar vendas
# -----------------------------
vendas = pd.read_csv("../data/csv/vendas_2023_2024.csv")

# Converter coluna de data (formatos mistos)
vendas["sale_date"] = pd.to_datetime(vendas["sale_date"], format="mixed", dayfirst=True)

# -----------------------------
# Parte 2 — Criar calendário completo
# -----------------------------
data_min = vendas["sale_date"].min()
data_max = vendas["sale_date"].max()

calendario = pd.DataFrame({"data": pd.date_range(data_min, data_max, freq="D")})

# -----------------------------
# Parte 3 — Vendas diárias
# -----------------------------
vendas_diarias = vendas.groupby("sale_date")["total"].sum().reset_index()

# -----------------------------
# Parte 4 — Cruzar calendário com vendas
# -----------------------------
df = calendario.merge(vendas_diarias, left_on="data", right_on="sale_date", how="left")
df["valor_venda"] = df["total"].fillna(0)

# -----------------------------
# Parte 5 — Dia da semana em português
# -----------------------------
dias_semana = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}
df["dia_semana"] = df["data"].dt.dayofweek.map(dias_semana)

# -----------------------------
# Parte 6 — Média de vendas por dia da semana
# -----------------------------
media_por_dia = df.groupby("dia_semana")["valor_venda"].mean().reset_index()
media_por_dia["media_vendas"] = media_por_dia["valor_venda"].round(2)

# -----------------------------
# Parte 7 — Identificar pior dia
# -----------------------------
pior_dia = media_por_dia.sort_values("media_vendas").head(1)

print("\n=== Questão 6.2 — Validação ===")
print(f"O pior dia da semana é {pior_dia['dia_semana'].values[0]}, "
      f"com média de vendas de R$ {pior_dia['media_vendas'].values[0]:,.2f}")
