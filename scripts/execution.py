#!/usr/bin/python3

from brownie import accounts, network, SMC
import json
import os
import random

# Função que recebe uma tabela verdade em forma de matriz e retorna uma lista com todos os elementos da matriz em ordem linear

# Função para implantar o contrato SMC
def deploy_and_interact_with_SMC(TT, TT_A, TT_B, A_rows, B_rows, b3_A, b3_B):
    # Muda para a rede de desenvolvimento local
    network.connect("development")

    # Implanta o contrato SMC
    smartContract = SMC.deploy(getLinearTable(TT), getLinearTable(TT_A), {'from': accounts[0]})

    # Envia a tabela TT_B para o contrato inteligente
    smartContract.receiveTableFromB(TT_B, {'from': accounts[1]})

    # Envia as linhas para o contrato inteligente
    smartContract.receiveLinesFromA(A_rows[0], A_rows[1], {'from': accounts[0]})
    smartContract.receiveLinesFromB(B_rows[0], B_rows[1], {'from': accounts[1]})

    # Envia a inversão para o contrato inteligente
    smartContract.receiveInversionFromA(b3_A, {'from': accounts[0]})
    smartContract.receiveInversionFromB(b3_B, {'from': accounts[1]})

    # Obtenha o resultado final
    A_result = smartContract.getValue.call({'from': accounts[0]})
    B_result = smartContract.getValue.call({'from': accounts[1]})

    return A_result == B_result


def getLinearTable(TT):
    linearTable = []
    for row in TT:
        linearTable.extend(row)
    return linearTable

# Função que retorna a operação lógica de "E" entre dois booleanos a e b


def function_and(a, b):
    return a and b

# Função que retorna a operação lógica de "OU" entre dois booleanos a e b


def function_or(a, b):
    return a or b

# Função que retorna "True" se o primeiro valor é maior que o segundo valor e "False" caso contrário


def function_greater(a, b):
    return (a == 1) and (b == 0)

# Função que embaralha as linhas de uma matriz


def shuffle(T):
    rows_position = [0, 1, 2, 3]
    random.shuffle(rows_position)
    shuffleT = []
    for position in rows_position:
        shuffleT.append([_ for _ in T[position]])
    return (shuffleT, rows_position)

# Função que inverte aleatoriamente os valores de uma coluna de uma tabela verdade


def inversion(T, column):
    inversion_bit = bool(random.getrandbits(1))
    for row in T:
        row[column] = row[column] ^ inversion_bit
    return inversion_bit

# Função que retorna uma escolha aleatória entre True e False


def getChoice():
    choice = bool(random.getrandbits(1))
    return choice

# Função que gera uma tabela verdade aleatória a partir de uma tabela verdade dada


def randomPermutation(TT):
    (TT_permuted, rows_position) = shuffle(TT)
    return TT_permuted

# Função que inverte aleatoriamente os valores de duas colunas de uma tabela verdade


def inversionOfColumns(TT, firstColumn, secondColumn):
    firstInversionBit = inversion(TT, firstColumn)
    secondInversionBit = inversion(TT, secondColumn)
    return (firstInversionBit, secondInversionBit, TT)

# Função que retorna as linhas de uma tabela verdade que têm o valor de uma determinada coluna igual a uma escolha aleatória


def getRows(TT, inversionBit, choice):
    rows = [0, 0]
    index = 0

    for i in range(len(TT)):
        if (TT[i][1] ^ inversionBit) == choice:
            rows[index] = i
            index = index + 1

    return rows

# Função que imprime uma tabela verdade na saída padrão


def showTruthTable(TT):
    for row in TT:
        print(row)

# Função principal que executa o protocolo


def main():
    # Tabela verdade inicial
    TruthTable = [[False, False, False],
                  [False, True, False],
                  [True, False, False],
                  [True, True, False]
                  ]

# Ampliação do tamanho da tabela verdade, fazendo um por vez e criando compromissos hipotéticos

TT_A = TruthTable.copy()  # TT_A recebe a tabela verdade original

# Adiciona uma nova linha na tabela verdade A
TT_A.append([False, False, False])

# Atribui um valor aleatório para o último elemento da linha adicionada
TT_A[-1][-1] = bool(random.getrandbits(1))
print('\n\n>>>FINAL TT_A<<<')
showTruthTable(TT_A)

# Envio da TT_A para o contrato inteligente
smartContract = SMC.deploy(getLinearTable(
    TruthTable), getLinearTable(TT_A), {'from': accounts[0]})

# Obtenção da TT_A enviada para o contrato inteligente
TT_A_from_SMC = smartContract.getTTA.call({'from': accounts[1]})

# Ampliação do tamanho da tabela verdade, fazendo um por vez e criando compromissos hipotéticos
TT_B = TT_A_from_SMC.copy()  # TT_B recebe a TT_A enviada para o contrato inteligente
# Adiciona uma nova linha na tabela verdade B
TT_B.append([False, False, False])
# Atribui um valor aleatório para o último elemento da linha adicionada
TT_B[-1][-1] = bool(random.getrandbits(1))
print('\n\n>>>FINAL TT_B<<<')
showTruthTable(TT_B)

# Envio da TT_B para o contrato inteligente
smartContract.receiveTableFromB(TT_B, {'from': accounts[1]})

# Escolha aleatória das linhas e envio para o contrato inteligente
read_TTA = smartContract.getTTB.call({'from': accounts[0]})
read_TTB = TT_B
A_choice = getChoice()
B_choice = getChoice()

A_rows = getRows(read_TTA, b1_A, A_choice)
B_rows = getRows(read_TTB, b2_B, B_choice)

print('\n\n>>>Envia Linhas para o contrato inteligente<<<')
smartContract.receiveLinesFromA(A_rows[0], A_rows[1], {'from': accounts[0]})
smartContract.receiveLinesFromB(B_rows[0], B_rows[1], {'from': accounts[1]})

# Inversão aleatória das colunas e envio para o contrato inteligente
(b1_A, b3_A, TT_A) = inversionOfColumns(TT_A, 0, 2)
(b2_B, b3_B, TT_B) = inversionOfColumns(TT_B, 1, 2)

print('\n\n>>>Envia a inverção para o contrato inteligente<<<')
smartContract.receiveInversionFromA(b3_A, {'from': accounts[0]})
smartContract.receiveInversionFromB(b3_B, {'from': accounts[1]})

# Avaliação final dos resultados
A_result = smartContract.getValue.call({'from': accounts[0]})
B_result = smartContract.getValue.call({'from': accounts[1]})
print('>>>>>>Resultado final: {result} <<<<<<'.format(
    result=A_result == function(A_choice, B_choice)))

if __name__ == "__main__":
    result = deploy_and_interact_with_SMC()
    print('>>>>>>FINAL RESULT: {result} <<<<<<'.format(result=result))
