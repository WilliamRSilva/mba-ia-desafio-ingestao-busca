from search import search_prompt

def main():
    #PEDE A PERGUNTA DO USUÁRIO
    pergunta = input("O que deseja buscar no documento? ").strip()

    if not pergunta:
        print("Você não digitou nada. Tente novamente.")
    else:
        busca = search_prompt(pergunta)
        print(busca)

    if not busca:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
if __name__ == "__main__":
    main()