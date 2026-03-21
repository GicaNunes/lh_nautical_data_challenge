from src import eda, tratamento, vendas, clientes, previsao, recomendacao, exploracao_extra, questoes


def run_pipeline():
    print("=== Iniciando pipeline completo ===\n")

    print("\n--- EDA ---")
    eda.run()

    print("\n--- Tratamento ---")
    df = tratamento.run()

    print("\n--- Vendas ---")
    vendas.run()

    print("\n--- Clientes ---")
    clientes.run()

    print("\n--- Previsão ---")
    previsao.run()

    print("\n--- Recomendação ---")
    recomendacao.run()

    print("\n--- Exploração Extra ---")
    exploracao_extra.run()

    print("\n--- Questões ---")
    questoes.run()

    print("\n=== Pipeline finalizado ===")

if __name__ == "__main__":
    run_pipeline()



