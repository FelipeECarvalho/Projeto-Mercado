import mysql.connector
import os
clear = lambda: os.system('cls')

def insere_nascimento():
    nasc = input('Nascimento (DD/MM/AAAA): ').replace('/', ' ').replace('-', ' ').split(" ")
    while len(nasc) > 3 or len(nasc) < 3:
        print('[ERRO], As datas precisam ser separadas por "/" ')
        nasc = input('Nascimento (DD/MM/AAAA): ').replace('/', ' ').replace('-', ' ').split(" ")
    dia = int(nasc[0])
    mes = int(nasc[1])
    ano = int(nasc[2])
    while (dia > 31 or dia < 1) or (mes > 12 or mes < 1) or (ano > 2021 or ano < 1900):
        print('[ERRO], Digite o nascimento corretamente!')
        nasc = input('Nascimento (DD/MM/AAAA): ').replace('/', ' ').replace('-', ' ').split()
        dia = int(nasc[0])
        mes = int(nasc[1])
        ano = int(nasc[2])
    nasc = str(ano) + str(mes) + str(dia)  
    return nasc
 

def insere_cpf():
    while True:
        try:
            cpf = int(input('CPF: '))
            cpf = str(cpf).replace('.', '').replace('-', '').replace('/', '')
            while len(cpf) != 11:
                print("[ERRO], Digite um CPF válido!")
                cpf = input('Cpf: ').replace('.', '').replace('-', '').replace('/', '')
            break
        except ValueError:
            print("[ERRO], Digite um CPF válido!")
    return cpf

def insere_email():
    while True:
        email = input("E-mail: ")
        if verifica_com(email) and verifica_arr(email):
            break
    return email


def verifica_com(mail):
    try:
        um = mail.index('.com')
        return True
    except (ValueError, IndexError):
        print("[ERRO], Digite um e-mail válido(necessário @, .com)")
        return False

def verifica_arr(mail):
    try:
        um = mail.index('@')
        return True
    except (ValueError, IndexError):
        print("[ERRO], Digite um e-mail válido(necessário @, .com)")
        return False

connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    database = 'mercado'
)

cursor = connection.cursor()
if connection.is_connected():
    print("----==== CADASTRO DE CLIENTE PYTHON SUPERMERCADOS ====----")
    print('----==== INFORMAÇÕES PESSOAIS ====----')
    print()
    nome = input("Nome: ").capitalize()
    sobrenome = input('Sobrenome: ').capitalize()
    cpf = insere_cpf()
    email = insere_email()
    sexo = input('Sexo (M/F): ')
    while sexo.upper() != 'M' and sexo.upper() != 'F':
        print('[ERRO], Digite um sexo válido.')
        sexo = input('Sexo (M/F): ')
    nascimento = insere_nascimento()
    clear()
    print("----==== CADASTRO DE CLIENTE PYTHON SUPERMERCADOS ====----")
    print('----==== CADASTRO DO ENDERECO ====----')
    print()
    rua = input('Rua: ').capitalize()
    bairro = input('Bairro: ').capitalize()
    cidade = input('Cidade: ').capitalize()

    while True:
        try:
            numero = int(input("Número: "))
            break
        except ValueError:
            print("[ERRO], Digite um número válido")

    while True:
        try:
            cep = input('CEP: ').replace('.', '').replace('-', '').replace('/', '')
            cep = int(cep)
            cep = str(cep)
            break
        except ValueError:
            print("[ERRO], Digite um número válido")
    clear()
    print("----==== CADASTRO DE CLIENTE PYTHON SUPERMERCADOS ====----")
    print()
    print()
    print()
    print('----==== CADASTRO CONCLUIDO COM SUCESSO! ====----')

    try:
        id = cursor.lastrowid
        add_cliente = "INSERT INTO CLIENTE(CPF, NOME, SOBRENOME, EMAIL, SEXO, NASCIMENTO) VALUES(%s, %s, %s, %s, %s, %s)"
        dados_cliente = cpf, nome, sobrenome, email, sexo, nascimento
        cursor.execute(add_cliente, dados_cliente)

        add_endereco = "INSERT INTO ENDERECO(IDENDERECO, RUA, BAIRRO, CIDADE, NUMERO, CEP, CPF_CLIENTE) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        dados_endereco = id, rua, bairro, cidade, numero, cep, cpf
        cursor.execute(add_endereco, dados_endereco)
        connection.commit()
    finally:
        cursor.close()
        connection.close()
else:
    print("[ERRO], Falha ao conectar a Base de dados, reinicie o programa!")

