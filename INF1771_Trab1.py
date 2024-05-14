import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

# Heuristica escolhida, distância em linha reta. h(x)
def distanciaManhattan(atual, destino):
    return abs((destino[0] - atual[0])) + abs((destino[1] - destino[1]))

def ordena_pelo_custo():
    global listaVizNaoVisitado
    listaVizNaoVisitado_aux = []
    
    for chave in listaVizNaoVisitado:
        listaVizNaoVisitado_aux.append(dicCustos[chave])

    listaVizNaoVisitado_aux = sorted(listaVizNaoVisitado_aux , key=lambda t: (t[1]+t[2]))

    listaVizNaoVisitado = []

    for elemento in listaVizNaoVisitado_aux:
        listaVizNaoVisitado.append(elemento[0])
    return

def desenhar(lista_coordenadas):
    global matrix_aux
    
    for pos in range(1, len(lista_coordenadas)):  # 0 1 2 ... 17
        x = lista_coordenadas[pos][0]
        y = lista_coordenadas[pos][1]
        matrix_aux[x][y] += 1
    sns.heatmap(matrix_aux, cmap="flare", annot=mapa2d, fmt= '', linewidths=.5, annot_kws={"size": 6})
    plt.show()
    matrix_aux = np.zeros_like(matrix_aux)
    return

def recuperar_caminho(atual, partida):
    global dicCustos
    global percurso
    percurso_aux = []
    if atual != partida:
        pontoOrigem = dicCustos[atual][3]
    else:
        pontoOrigem = partida

    percurso_aux.append(atual)
    while pontoOrigem != partida:
        percurso_aux.append(pontoOrigem)
        pontoOrigem = dicCustos[pontoOrigem][3]
    if partida not in percurso_aux:
        percurso_aux.append(partida)
    
    percurso_aux.reverse()
    
    for i in range(len(percurso_aux)):
        percurso.append(percurso_aux[i])
    
    return percurso_aux

def calcula_custos(pai, vizinhos, destino):
    global dicCustos

    for vizinho in vizinhos:
        heuristica = distanciaManhattan(vizinho, destino)
        coord_x = vizinho[0]
        coord_y = vizinho[1]
        try:
            if (mapa[coord_x][coord_y] == 'R'):
                custo = dicCustos[pai][1] + 5  # Custo = Custo do Pai + Rochoso
            elif (mapa[coord_x][coord_y] == 'F'):
                custo = dicCustos[pai][1] + 15  # Custo = Custo do Pai + Floresta
            elif (mapa[coord_x][coord_y] == 'A'):
                custo = dicCustos[pai][1] + 30  # Custo = Custo do Pai + Água
            elif (mapa[coord_x][coord_y] == 'M'):
                custo = dicCustos[pai][1] + 200  # Custo = Custo do Pai + Montanha
            else:
                custo = dicCustos[pai][1] + 1  # Custo = Custo do Pai + Montanha
        except:
            custo = 1  # No caso do Pai ser o Ponto Inicial

        try:
            if (dicCustos[vizinho][1] > custo):
                dicCustos[vizinho] = (vizinho, custo, heuristica, pai)
        except:
            dicCustos[vizinho] = (vizinho, custo, heuristica, pai)

    return dicCustos

def mapeia_vizinhos(atual):
    global mapa
    global listaVizVisitado
    
    vizinhos = [] # Lista de vizinhos
    coord_x = atual[0] # Indice da Linha na Matriz
    coord_y = atual[1] # Indice da Coluna na Matriz

    # Checando a existencia de cada vizinho , se a célula não é barreira , se o vizinho não está na Lista Fechada 
    if( ((coord_x-1) >= 0) and (mapa[coord_x-1][coord_y] != 1) ):  # Em cima
        vizinho_cima = (coord_x-1,coord_y)
        if ( (vizinho_cima not in listaVizVisitado) ):
            vizinhos.append(vizinho_cima)
    
    if( ((coord_x+1) <= len(mapa)-1) and (mapa[coord_x+1][coord_y] != 1) ):   # Em baixo
        vizinho_baixo = (coord_x+1,coord_y)
        if ( (vizinho_baixo not in listaVizVisitado) ):
            vizinhos.append(vizinho_baixo)

    if( ((coord_y-1) >= 0) and (mapa[coord_x][coord_y-1] != 1) ):  # Esquerda
        vizinho_esquerda = (coord_x,coord_y-1)
        if ( (vizinho_esquerda not in listaVizVisitado)):
            vizinhos.append(vizinho_esquerda)

    if( ((coord_y+1) <= len(mapa[0])-1) and (mapa[coord_x][coord_y+1] != 1) ):  # Direita
        vizinho_direita = (coord_x,coord_y+1)
        if ( (vizinho_direita not in listaVizVisitado)):
            vizinhos.append(vizinho_direita)

    return vizinhos

def buscar(partida, destino):
    global custoTotal
    
    listaVizNaoVisitado.append(partida)
    chegou = False

    while listaVizNaoVisitado != [] and not chegou:        
        # Primeiro elemento da lista já ordenada
        atual = listaVizNaoVisitado[0]

        # Pesquisa pelos elementos vizinhos elegiveis (nao é barreira) e não presentes na lista fechada
        vizinhos = mapeia_vizinhos(atual)
        
        calcula_custos(atual, vizinhos, destino)  # Calculo de custo de cada vizinho

        # Verificando de um vizinho do atual ja nao esta presente na lista aberta
        for vizinho in vizinhos:
            if (vizinho not in listaVizNaoVisitado):
                listaVizNaoVisitado.append(vizinho)            
        
        # Remocao do primeiro elemento da lista aberta
        listaVizNaoVisitado.remove(atual)
        
        # Adicionando o elemento processado na lista fechada
        listaVizVisitado.append(atual)

        # Ordenação dos elementos em ordem de custo crescente
        ordena_pelo_custo() 

        if(destino in listaVizVisitado): # Achou o objetivo se o vizinho for coordenada de destino
            chegou = True
            fatiaPercurso = recuperar_caminho(atual, partida) # Lista com as posicoes percorridas até o destino
            custoTotal += dicCustos[destino][1]
            print("Custo do percurso de", ordemGin[ondeEstou], "para", ordemGin[ondeEstou+1], ":", dicCustos[destino][1])
            if(umPorUm):
                desenhar(fatiaPercurso) 
            
    return

def read_file(filename, partida, destino):

    global x, y
    lines = None    
    start = (0,0)
    end = (0,0)

    with open(filename) as file:
        lines = file.readlines()

        j = 0
        for line in lines:
            lines[j] = line.strip('\n')
            
            if line.find(partida) > -1:
                start = (j, line.find(partida))
            if line.find(destino) > -1:
                end = (j, line.find(destino))
            
            j += 1

    x = len(lines[0])
    y = len(lines)

    return lines, start, end


mapa, inicio, final = read_file("mapa_dbz.txt", 'I', 'E')
matrix_aux = np.zeros((57,200), dtype=np.uint16)
matrix_aux[inicio] += 1
mapa2d = np.zeros((57,200), dtype='U1')
for i in range(57):
    for j in range(200):
        mapa2d[i][j] = mapa[i][j]

percurso = []
ondeEstou = 0
custoTotal = 0
ordemGin = ['I', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'B', 'C', 'D', 'E']

listaVizNaoVisitado = []
listaVizVisitado = []
dicCustos = {}

# Opcao para mostrar um caminho de cada vez
umPorUm = False


for ondeEstou in range(len(ordemGin)-1):
    listaVizNaoVisitado = []
    listaVizVisitado = []
    dicCustos = {}
    mapa, partida, destino = read_file("mapa_dbz.txt", ordemGin[ondeEstou], ordemGin[ondeEstou+1])
    buscar(partida, destino)

print("\nO custo total da aventura foi", custoTotal)

desenhar(percurso)
