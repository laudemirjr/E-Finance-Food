import csv
import json
import os

usuarios = {}

def clean_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_dados():
    try:
        with open('usuarios.json', 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

def salvar_dados():
    with open('usuarios.json', 'w') as arquivo:
        json.dump(usuarios, arquivo)

def criar_usuario():
    username = input("Digite o novo nome de usuário: ")

    if username not in usuarios:
        password = input("Digite a senha: ")
        meta = float(input(f"Digite a meta de gastos mensais (R$): "))
        usuarios[username] = {'senha': password, 'meta': meta, 'despesas': []}
        clean_terminal()
        print(f"Usuário {username} criado com sucesso!")
        salvar_dados()
    else:
        clean_terminal()
        print("Nome de usuário já existe. Tente outro.")

def fazer_login():
    username = input("Digite o nome de usuário: ")

    if username in usuarios:
        password = input("Digite a senha: ")

        if usuarios[username]['senha'] == password:
            clean_terminal()
            print("Login bem-sucedido!")
            return username
        else:
            clean_terminal()
            print("Senha incorreta. Tente novamente.")
    else:
        clean_terminal()
        print("Nome de usuário não encontrado. Tente novamente.")
    return None

def menu_inicial():
    print("\nBem-vindo ao E-FINANCE FOOD")
    print('\nSeu aplicativo de gerenciamento de orçamento pessoal')
    print("\nMenu Inicial:")
    print("1. Fazer Login")
    print("2. Criar Usuário")
    print("3. Sair")

    escolha = input("Escolha uma opção: ")
    return escolha

def cadastrar_despesa(usuario):
    if usuario:
        data = input("Digite a data (ex. Dia/Mês/Ano): ")
        descricao = input("Digite a descrição da despesa: ")

        valor_input = input("Digite o valor da despesa (R$): ")
        valor = float(valor_input.replace(',', '.'))

        if valor > usuarios[usuario]['meta']:
            print("Aviso: A despesa é maior que a meta mensal!")

        despesa = {'data': data, 'descricao': descricao, 'valor': valor}
        usuarios[usuario]['despesas'].append(despesa)
        usuarios[usuario]['meta'] -= valor

        if usuarios[usuario]['meta'] < 0:
            print("A sua meta foi Ultrapassada!")

        salvar_dados()
        clean_terminal()
        print("Despesa cadastrada com sucesso!")
    else:
        clean_terminal()
        print("Usuário não logado.")

def listar_despesas(usuario):
    if usuario:
        despesas_usuario = usuarios[usuario]['despesas']
        clean_terminal()
        for i, despesa in enumerate(despesas_usuario, 1):
            print(f"{i}. Data: {despesa['data']}, Descrição: {despesa['descricao']}, Valor: R${despesa['valor']}")
        print(f"Restante para bater a Meta: R${usuarios[usuario]['meta']:.2f}")
    else:
        clean_terminal()
        print("Usuário não logado.")

def deletar_despesa(usuario):
    if usuario:
        listar_despesas(usuario)

        try:
            indice = int(input("Digite o número da despesa a ser excluída: ")) - 1

            if 0 <= indice < len(usuarios[usuario]['despesas']):
                despesa_excluida = usuarios[usuario]['despesas'].pop(indice)
                usuarios[usuario]['meta'] += despesa_excluida['valor']
                salvar_dados()
                clean_terminal()
                print(f"Despesa na data {despesa_excluida['data']}, descrição '{despesa_excluida['descricao']}' excluída com sucesso!")
            else:
                clean_terminal()
                print("Número de despesa inválido.")
        except ValueError:
            clean_terminal()
            print("Entrada inválida. Por favor, digite um número de despesa válido.")
    else:
        clean_terminal()
        print("Usuário não logado.")

def deletar_usuario(usuario):
    if usuario:
        del usuarios[usuario]
        salvar_dados()
        clean_terminal()
        print(f"Usuário {usuario} excluído com sucesso!")
    else:
        clean_terminal()
        print("Usuário não logado.")

usuarios = carregar_dados()

while True:
    escolha_inicial = menu_inicial()

    if escolha_inicial == '1':
        usuario_atual = fazer_login()
        if usuario_atual is None:
            continue
        else:
            while True:
                print('\nBem-vindo ao Menu do E-FINANCE FOOD')
                print("\nMenu:")
                print("1. Cadastrar Despesa")
                print("2. Listar Despesas")
                print("3. Deletar Despesa")
                print("4. Deletar Usuário")
                print("5. Sair")

                escolha = input("Escolha uma opção: ")

                if escolha == '1':
                    cadastrar_despesa(usuario_atual)
                elif escolha == '2':
                    listar_despesas(usuario_atual)
                elif escolha == '3':
                    deletar_despesa(usuario_atual)
                elif escolha == '4':
                    deletar_usuario(usuario_atual)
                    usuario_atual = None
                    break
                elif escolha == '5':
                    print("Encerrando o programa. Até logo!")
                    exit()
                else:
                    print("Opção inválida. Por favor, tente novamente.")

    elif escolha_inicial == '2':
        criar_usuario()
    elif escolha_inicial == '3':
        print("Encerrando o programa. Até logo!")
        break
    else:
        print("Opção inválida. Por favor, tente novamente.")