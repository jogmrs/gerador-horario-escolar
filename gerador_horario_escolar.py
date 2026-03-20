# Projeto de geração de horários escolares 
# Data: 30/10/2025
# Constrói um horário escolar usando uma heurística muito simples baseada
# na estrutura de dados conjunto. Os dados de entrada são as disciplinas
# a serem oferecidas e as matrículas dos alunos que farão algumas das
# disciplinas oferecidas.

import sys

def main():
    # Define os nomes dos arquivos de entrada; usa os defaults, se não houver
    # argumentos com os nomes na linha de comando.
    nomeArqDisc = 'disciplinas.txt'
    nomeArqMatric = 'matriculas.txt'
    if len(sys.argv) > 1:
        nomeArqDisc = sys.argv[1]
    if len(sys.argv) > 2:
        nomeArqMatric = sys.argv[2]
    
    discs = leia_arq_disciplinas(nomeArqDisc)
    matrics = leia_arq_matriculas(nomeArqMatric)

    confs = calcule_conflitos(discs, matrics)
    hor = faz_horario_escolar(discs, confs)
    
    # Imprime as sessões não conflitantes do horário.
    print('\nSessões:')
    for i in range(len(hor)):
        print('{:3d}: '.format(i), sorted(hor[i]))


# Lê uma disciplina por linha do arquivo cujo nome externo é 'nomearq'.
# Retorna a lista de disciplinas lidas.
def leia_arq_disciplinas(nomearq):
    disciplinas = []
    try:
        arqDiscs = open(nomearq, 'r', encoding='utf-8')
        for linha in arqDiscs.readlines():
            disciplinas.append(linha.rstrip('\n'))
        arqDiscs.close()
    except FileNotFoundError:
        print('***ERRO: o arquivo \'{}\' não existe ou está corrompido.'.\
              format(nomearq))
    return disciplinas


# Lê, por linha, o nome de um aluno e as disciplinas em que ele se matriculou.
# Os dados em cada linha são separados por uma vírgula. O nome externo do
# arquivo é passado como parâmetro. Retorna um dicionário em que a chave é o
# nome de um aluno e o valor associado é o conjunto de disciplinas em que o
# aluno se matriculou.
def leia_arq_matriculas(nomearq):
    matriculas = {}
    try:
        arqMatrics = open(nomearq, 'r', encoding='utf-8')
        for linha in arqMatrics.readlines():
            dados = linha.rstrip('\n').split(',')
            nome = dados[0]
            matrics = set(dados[1:])
            matriculas[nome] = matrics
        arqMatrics.close()
    except FileNotFoundError:
        print('***ERRO: o arquivo \'{}\' não existe ou está corrompido.'.\
              format(nomearq))
    return matriculas


def calcule_conflitos(disciplinas, matriculas):
    emptySet = set()  # conjunto vazio
    
    # Determina os conjuntos de disciplinas conflitantes a partir das
    # matrículas individuais dos alunos nas disciplinas.
    conflitos = [ emptySet for d in disciplinas ]
    for a in matriculas.keys():
        for d in range(len(disciplinas)):
            if disciplinas[d] in matriculas[a]:
                conflitos[d] = conflitos[d] | matriculas[a]
    return conflitos


####                                                                        ####
# COLOQUE AQUI A IMPLEMENTAÇÃO DA FUNÇÃO: faz_horario_escolar(disciplinas,     #
#                                                             conflitos)       #
####                                                                        ####
def faz_horario_escolar (disciplinas, conflitos):
    horario = []
    for i in range(len(disciplinas)):
        disc_colocada = False  
        disc_atual = disciplinas[i]
        conflito_disciplina = conflitos[i]
        for sessao in horario:
            if sessao.isdisjoint(conflito_disciplina):
                sessao.add(disc_atual)
                disc_colocada = True
                break
        if not disc_colocada:
            horario.append({disc_atual})
            
    return horario


if __name__ == '__main__':
    main()
