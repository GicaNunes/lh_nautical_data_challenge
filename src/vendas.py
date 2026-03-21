import pandas as pd
import matplotlib.pyplot as plt


def run():
    print("=== Análise de Vendas rodando ===")

    vendas = pd.read_csv("data/csv/vendas_2023_2024.csv")
    vendas['sale_date'] = pd.to_datetime(vendas['sale_date'], errors='coerce')
    vendas['dia_semana'] = vendas['sale_date'].dt.day_name()

    # Vendas médias por dia da semana
    media_dia = vendas.groupby('dia_semana')['qtd'].mean()

    # Ordenar dias
    dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    media_dia = media_dia.reindex(dias, fill_value=0)

    print(media_dia)

    # Exportar gráfico
    plt.figure(figsize=(8, 5))
    media_dia.plot(kind='bar', color='skyblue')
    plt.title("Vendas médias por dia da semana")
    plt.ylabel("Quantidade média")
    plt.savefig("visuals/vendas_por_dia.png")
    plt.close()


    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("\n=== Vendas ===\n")
        f.write("Gráficos salvos em visuals/vendas_por_dia.png e visuals/vendas_mensais.png\n")
        f.write("Resumo: Vendas totais = " + str(vendas['qtd'].sum()) + "\n")
        f.write("Média por mês = " + str(vendas.groupby(vendas['sale_date'].dt.to_period('M'))['qtd'].mean().mean()) + "\n")

if __name__ == "__main__":
    run()
