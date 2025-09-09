from search import search_prompt

def main():
    print("==== Chat com Base de Cnnhecimento ====")
    print("Digite 'sair' para encerrar o chat")
    print("Perguntas serão respondidas com base no PDF disponível")   
    
    while True:
       try:
          pergunta = input("Faça sua pergunta: ").strip()

          if pergunta.lower() in ["sair", "exit", "quit"]:
                print("Encerrando chat. Até logo!")
                break
                
          print("Processando...")

          resposta = search_prompt(pergunta)

          print(f"RESPOSTA: {resposta}")

          print("=" * 60 + "\\n")

       except KeyboardInterrupt:
                print("\n\nChat interrompido pelo usuário. Até logo!")
                break
       except Exception as e:
                print(f"Erro ao processar pergunta: {e}")
                print("Tente novamente.\\n")
                
if __name__ == "__main__":
    main()