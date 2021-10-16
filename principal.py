from time import sleep
import mysql.connector
from datetime import datetime
import os

connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '1234',
            database = 'mercado'
            )
cursor = connection.cursor()
    

def compra_vazia():
    if len(itens) == 0 or sum(total) == 0:
        return True
    else:
        return False


def insere_cadastro():
    global nome_cliente
    global cliente
    global cpf
    while True:
        print()
        print("------======      ======------")
        cliente = int(input("CLIENTE SUPERMECADOS PYTHON? (1- SIM / 0-NÃO): "))
        print()
        if cliente == 1:
            cpf = input("CPF: ")
            sql = "SELECT NOME FROM CLIENTE WHERE CPF = %s"
            cursor.execute(sql, (cpf, ))
            nome_cliente = cursor.fetchone()
            if nome_cliente:
                print(f"Bem-Vindo Cliente Supermercados PYTHON, {nome_cliente[0]}!")
                print("------======      ======------")
                print()
                break
            else:
                print("CLIENTE NÃO CADASTRADO!")
        else:
            break


def leitura_codigo():
    global product
    codigo = str(input("Código: ")).replace("x", " ").split() 
    sql = "SELECT preco_normal, preco_cliente, descricao FROM produto WHERE CODIGO = %s"
    if len(codigo) == 1: 
        if len(codigo[0]) > 4:
            cursor.execute(sql, (codigo[0], ))
            product = cursor.fetchone()
            if not product:
                print("[ERRO]: Código inválido")
            else:
                if cont == 0:
                    insere_cadastro()  
                if cliente == 1:
                    registra_produto_cliente(product[0], product[1], product[2])
                else:
                    registra_produto_normal(product[0], product[2])
        else:
            if codigo[0] == "m":
                return menu()
            else:
                print("[ERRO]: É necessário digitar o peso")
    elif len(codigo) == 0:
        print("[ERRO]: Código inválido")
    else: 
        cursor.execute(sql, (codigo[1], ))
        product = cursor.fetchone()
        if len(codigo[1]) > 4:
            if not product:
                print("[ERRO]: Código inválido")
            else:
                if cont == 0:
                    insere_cadastro()  
                if cliente == 1:
                    registra_produto_cliente(product[0], product[1], product[2], codigo[0])
                else:
                    registra_produto_normal(product[0], product[2], codigo[0])
        else:
            if not product:
                print("[ERRO]: Código inválido")
            else:
                if cont == 0:
                    insere_cadastro()
                if cliente == 1:
                    registra_flv_cliente(product[0], product[1], product[2], codigo[0])
                else:
                    registra_flv_normal(product[0], product[2], codigo[0])


def guarda_produto(nome, quant, preco):
    global cont
    itens.append([nome, preco, quant, total[cont]])
    cont += 1


def apresenta_produto(nome, quant, preco):
    print(f"{cont + 1} - {nome}  Preço/Kg R${preco}")
    print(f"    {quant} x R${preco} = R${total[cont]:.2f} \n")
    print(f"Total R${sum(total):.2f}")
    guarda_produto(nome, quant, preco)
    

def registra_flv_normal(p_normal, nome, quant):
    peso = float(quant)
    calcula_preco(peso, p_normal)
    return apresenta_produto(nome, peso, p_normal)


def registra_produto_normal(p_normal, nome, quant=0):
    if quant == 1 or quant == 0:
        calcula_preco(1, p_normal)
        return apresenta_produto(nome, 1, p_normal)
    else:
        calcula_preco(quant, p_normal)
        return apresenta_produto(nome, quant, p_normal)


def registra_flv_cliente(p_normal, p_cliente, nome, quant):
    peso = float(quant)
    if p_cliente:
        calcula_preco(peso, p_cliente)
        calcula_desconto(p_normal, p_cliente, peso)
        return apresenta_produto(nome, peso, p_cliente)
    else:
        calcula_preco(peso, p_normal)
        return apresenta_produto(nome, peso, p_normal)


def registra_produto_cliente(p_normal, p_cliente, nome, quant=0):
    quant = float(quant)
    if quant == 1 or quant == 0:
        if p_cliente:
            calcula_preco(1, p_cliente)
            calcula_desconto(p_normal, p_cliente, quant)
            return apresenta_produto(nome, 1, p_cliente)
        else:
            calcula_preco(1, p_normal)
            return apresenta_produto(nome, 1, p_normal)
    else:
        if p_cliente:
            calcula_preco(quant, p_cliente)
            calcula_desconto(p_normal, p_cliente, quant)
            return apresenta_produto(nome, quant, p_cliente)
        else:
            calcula_preco(quant, p_normal)
            return apresenta_produto(nome, quant, p_normal)


def calcula_desconto(p_normal, p_cliente, quant):
    global desconto
    desconto += (p_normal * quant) - (p_cliente * quant)


def calcula_preco(quant, preco):
    valor = quant * preco
    return total.append(valor)


def menu():
    print("-----------------------------")
    print("[1] - Para exclusão de item ")
    print("[2] - Para finalizar a venda")
    print("[3] - Para cancelar compra")
    print("[4] - Para fechar o caixa")
    print("[0] - Para voltar           ")
    print("-----------------------------")
    try:
        opcao = int(input("Sua opção: "))
    except ValueError:
        print("[ERRO]: Opção inválida")
    else:
        if opcao == 1: 
            if compra_vazia():
                print("[ERRO]: Não foi possivel excluir - Compra vazia")
            else:
                return exclusao()
        elif opcao == 2:
            if compra_vazia():
                print("[ERRO]: Não foi possivel finalizar - Compra vazia")
            else:
                lista_pagamento = list()
                total_compra = sum(total)
                total_pago = 0
                valor_pago = 0
                valor_a_pagar = total_compra
                return encerra_compra(total_compra, valor_pago, valor_a_pagar, lista_pagamento, total_pago)
        elif opcao == 3:
            if compra_vazia():
                print("[ERRO]: Não foi possivel cancelar - Compra vazia")
            else:
                return cancela_compra()
        elif opcao == 4:
            if not compra_vazia():
                print("[ERRO]: Encerre a compra para fechar o caixa")
            else:
                return fecha_caixa()
        elif opcao == 0:
            return leitura_codigo()
        else:
            print("[ERRO]: Opção inválida")
            return menu()
    

def exclusao():
    try:
        excluir = int(input("Digite o indice do produto: "))
        excluir -= 1
        if not (itens[excluir] != []):
            print("[ERRO]: índice já excluido")
            return leitura_codigo()
    except (ValueError, IndexError):
        print("[ERRO]: Índice não encontrado")
    else:
        print(f"ITEM  REMOVIDO == {excluir + 1}")
        print(f"    {itens[excluir][2]} x {itens[excluir][1]} = -{total[excluir]:.2f}\n")
        total[excluir] = 0
        itens[excluir] = []
        print(f"Total R${sum(total):.2f}")


def encerra_compra(total, pago, pagar, lista_pagamento, total_pago):
    print("-----------------------------")
    print("[1] - Para dinheiro          ")
    print("[4] - Para crédito a vista   ")
    print("[5] - Para crédito parcelado ")
    print("[7] - Para débito            ")
    print("[0] - Para cancelar          ")
    print("-----------------------------")
    print()
    total_pago += pago
    pago = 0
    print(f"VALOR PAGO: R${total_pago:.2f}   TOTAL A PAGAR: R${pagar:.2f}    TOTAL: R${total:.2f}")
    print(f"VOCÊ ENCOMINZOU R${desconto:.2f}!")
    print()
    try:
        pagamento = int(input("Forma de pagamento: "))
    except ValueError:
        print("[ERRO]: Opção inválida")
        return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)
    else:
        if pagamento == 1:
            dinheiro(total, pago, pagar, lista_pagamento, total_pago)
        elif pagamento == 4:
            credito(total, pago, pagar, lista_pagamento, total_pago)
        elif pagamento == 5:
            credito_parcelado(total, pago, pagar, lista_pagamento, total_pago)
        elif pagamento == 7:
            debito(total, pago, pagar, lista_pagamento, total_pago)
        elif pagamento == 0:
            return leitura_codigo()
        else:
            print("[ERRO]: Opção inválida")
            return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)


def dinheiro(total, pago, pagar, lista_pagamento, total_pago):
    try:
        pago = float(input("Digite a quantidade: R$"))
        pago = round(pago, 2)
        pagar = round(pagar, 2)
    except ValueError:
        print("[ERRO]: Digite apenas valores numéricos")
        return dinheiro(total, pago, pagar, lista_pagamento, total_pago)
    else:
        if pago < pagar:
            pagar -= pago
            pagar = round(pagar, 2)
            lista_pagamento.append(["DINHEIRO", pago])
            return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)
        else:
            total_pago += pago
            troco = total_pago - total
            print(f"Troco: R${troco:.2f}")
            input("Pressione Entra caso o troco for realizado:")
            lista_pagamento.append(["DINHEIRO", pago])
            imprime_nota(total, troco, lista_pagamento)


def credito(total, pago, pagar, lista_pagamento, total_pago):
    try:
        pago = float(input("Digite a quantidade: R$"))
        pago = round(pago, 2)
        pagar = round(pagar, 2)
    except ValueError:
        print("[ERRO]: Digite valores numéricos")
        return credito(total, pago, pagar, lista_pagamento, total_pago)
    else:
        if pago < pagar:
            pagar -= pago
            pagar = round(pagar, 2)
            lista_pagamento.append(["CREDITO A VISTA", pago])
            return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)
        elif pago > pagar:
            print("[ERRO]: Forma de pagamento não aceita troco")
            pago = 0
            return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)
        else:
            troco = 0
            total_pago += pago
            lista_pagamento.append(["CREDITO A VISTA", pago])
            imprime_nota(total, troco, lista_pagamento)


def credito_parcelado(total, pago, pagar, lista_pagamento, total_pago):
    try:
        pago = float(input("Digite a quantidade: R$"))
        pago = round(pago, 2)
        pagar = round(pagar, 2)
        vezes = int(input("Parcelas: "))
    except ValueError:
        print("[ERRO]: Digite valores numéricos")
        return credito_parcelado(total, pago, pagar, lista_pagamento, total_pago)
    else:
        if pago < pagar:
            pagar -= pago
            pagar = round(pagar, 2)
            lista_pagamento.append([f"CREDITO PARCELADO {vezes}", pago])
            return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)
        elif pago > pagar:
            print("[ERRO]: Forma de pagamento não aceita troco")
            pago = 0
            return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)
        else:
            troco = 0
            total_pago += pago
            lista_pagamento.append(["CREDITO PARCELADO", vezes, pago])
            imprime_nota(total, troco, lista_pagamento)


def debito(total, pago, pagar, lista_pagamento, total_pago):
    try:
        pago = float(input("Digite a quantidade: R$"))
        pago = round(pago, 2)
        pagar = round(pagar, 2)
    except ValueError:
        print("[ERRO]: Digite valores numéricos")
        return debito(total, pago, pagar, lista_pagamento, total_pago)
    else:
        if pago < pagar:
            pagar -= pago
            pagar = round(pagar, 2)
            lista_pagamento.append(["DEBITO", pago])
            return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)
        elif pago > pagar:
            print("[ERRO]: Forma de pagamento não aceita troco")
            pago = 0
            return encerra_compra(total, pago, pagar, lista_pagamento, total_pago)
        else:
            troco = 0
            total_pago += pago
            lista_pagamento.append(["DEBITO", pago])
            imprime_nota(total, troco, lista_pagamento)


def formata_lista(lista):
    lista_formatada = []
    for elemento in lista:
        if not (elemento == []):
            lista_formatada.append(elemento)
    return lista_formatada


def imprime_nota(total, troco, lista_pagamento):
    print("Imprimindo Cupom Fiscal...")
    print()
    sleep(2)
    soma = 0
    nova_lista = formata_lista(itens)
    for i, elemento in enumerate(nova_lista):
        print(f"{i + 1} - {nova_lista[i][0]}  Preço/Kg R${nova_lista[i][1]}")
        print(f"   {nova_lista[i][2]} x R${nova_lista[i][1]:.2f} = R${nova_lista[i][3]:.2f} \n")
    print("TOTAL:", end="                                   ")
    print(f"{total:<1.2f}")
    for elemento in lista_pagamento:
        if len(elemento) == 3:
            print(f"     {elemento[0]} {elemento[1]:<4}", end="")
            print(f"{elemento[2]:>20.2f}")
            soma += elemento[2]
            transacoes_finalizadas.append([elemento[0], elemento[2]])
        else:
            print(f"     {elemento[0]:<16}", end="")
            print(f"{elemento[1]:>26.2f}")
            soma += elemento[1]
            transacoes_finalizadas.append([elemento[0], elemento[1]])
    print("SOMA:", end="                                    ")
    print(f"{soma:<1.2f}")
    print("TROCO:", end="                                   ")
    print(f"{troco:<1.2f}")
    print(f"PARABÉNS CLIENTE SUPERMERCADOS PYTHON!, VOCÊ ECONOMINZOU R${desconto:.2f}!")
    input("Pressione Entra para encerrar")
    if cliente == 1:
        insere_pagamento_banco_cliente(lista_pagamento, total)
    else:
        insere_pagamento_banco_normal(lista_pagamento, total)
    nova_compra()
    

def insere_pagamento_banco_normal(pagamentos, tot):
    data_e_hora_atuais = datetime.now()
    dados = (tot, data_e_hora_atuais)
    sql = "INSERT INTO VENDA VALUES(NULL, %s, %s, NULL, NULL)"
    cursor.execute(sql, dados)
    connection.commit()
    sql = "SELECT MAX(IDVENDA) FROM VENDA"
    cursor.execute(sql)
    idvenda = cursor.fetchone()
    idvenda = idvenda[0]
    for forma in pagamentos:
        quant = forma[1]
        tipo = forma[0]
        dados = (quant, tipo, idvenda)
        print(quant, tipo, id)
        sql = "INSERT INTO OPCAO VALUES(NULL, %s, %s, %s)"
        cursor.execute(sql, dados)
        connection.commit()

def insere_pagamento_banco_cliente(pagamentos, tot):
    data_e_hora_atuais = datetime.now()
    dados = (tot, data_e_hora_atuais, desconto, cpf)
    sql = "INSERT INTO VENDA VALUES(NULL, %s, %s, %s, %s)"
    cursor.execute(sql, dados)
    connection.commit()
    sql = "SELECT MAX(IDVENDA) FROM VENDA"
    cursor.execute(sql)
    idvenda = cursor.fetchone()
    idvenda = idvenda[0]
    for forma in pagamentos:
        quant = forma[1]
        tipo = forma[0]
        dados = (quant, tipo, idvenda)
        print(quant, tipo, id)
        sql = "INSERT INTO OPCAO VALUES(NULL, %s, %s, %s)"
        cursor.execute(sql, dados)
        connection.commit()


def nova_compra():
    global itens
    global total
    global cont
    global cliente
    itens = list()
    total = list()
    cont = 0
    cliente = 0
    os.system('cls')


def cancela_compra():
    global itens
    global total
    global cont
    global cliente
    itens = list()
    total = list()
    cont = 0
    cliente = 0
    print("---- COMPRA CANCELADA ----")
    sleep(1)
    os.system('cls')


def fecha_caixa():
    global aberto
    tot = 0
    for elemento in transacoes_finalizadas:
        tot += elemento[1]
    print(f"TOTAL DE VENDAS R${tot:.2f}")
    print()
    while len(transacoes_finalizadas) != 0:
        print("ELIMINE AS TRANSAÇÕES FINALIZADAS:")
        for i, elemento in enumerate(transacoes_finalizadas):
            print(f"{i:<1}", end="|    ")
            print(f"{elemento[0]:<17}", end="|")
            print(f"{elemento[1]:>5.2f}")
        try:
            aux = int(input(""))
            tot -= transacoes_finalizadas[aux][1]
            tot = round(tot, 2)
            transacoes_finalizadas.pop(aux)
        except ValueError:
            print("[ERRO]: Digite valores válidos")
            return fecha_caixa()
        except IndexError:
            print(f" Indice <= {len(transacoes_finalizadas)}")
    print(f"TRANSAÇÕES ELIMINADAS TOTAL: R${tot}")
    print("CAIXA FECHADO COM SUCESSO!")
    aberto = False

            


itens = list()
total = list()
transacoes_finalizadas = list()
cont = 0
cliente = 0
desconto = 0.0
nome_cliente = ''
cpf = ''
aberto = True
while aberto:
    leitura_codigo() 

    
