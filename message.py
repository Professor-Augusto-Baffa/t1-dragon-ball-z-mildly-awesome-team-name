

# Heuristica escolhida, distância em linha reta. h(x)
def distanciaManhattan(atual, final):
    return abs((final[0] - atual[0])) + abs((final[1] - atual[1]))

def ordena_pelo_custo():
    global listaVizNaoVisitado
    listaVizNaoVisitado_aux = []
    
    for chave in listaVizNaoVisitado:
        listaVizNaoVisitado_aux.append(dicCustos[chave])

    sorted(listaVizNaoVisitado_aux , key=lambda t: (t[1]+t[2]))

    listaVizNaoVisitado = []

    for elemento in listaVizNaoVisitado_aux:
        listaVizNaoVisitado.append(elemento[0])
    return

def desenhar(lista_coordenadas):
    #print(f"### PERCURSO de {inicio} ate {final} ###")
    #print(lista_coordenadas)
    #print()

    '''
    delta = [[-1, 0],   # Para cima
             [1, 0],    # Para baixo
             [0, -1],   # Para esquerda
             [0, 1]]    # Para direita
    '''

    simbolo_cima = '^'
    simbolo_baixo = 'v'
    simbolo_esquerda = '<'
    simbolo_direita = '>'


    resultado = []

    for i in mapa:
        resultado.append(i)

    atual = inicio
    simbolo = ''

    for pos in range(1, len(lista_coordenadas)):  # 0 1 2 ... 17        
        #print('%s ? %s' % (atual, lista_coordenadas[pos]))
        
        if (lista_coordenadas[pos] != inicio):
            if atual[0] > lista_coordenadas[pos][0]:    # Para cima
                simbolo = simbolo_cima  
            elif atual[0] < lista_coordenadas[pos][0]:  # Para baixo
                simbolo = simbolo_baixo
            elif atual[1] > lista_coordenadas[pos][1]:  # Para esquerda
                simbolo = simbolo_esquerda
            elif atual[1] < lista_coordenadas[pos][1]:  # Para direita
                simbolo = simbolo_direita
            
            if lista_coordenadas[pos] == final:     # Verifica se o próximo passo é a chegada
                x = lista_coordenadas[pos-1][0]
                y = lista_coordenadas[pos-1][1]
            else:
                x = lista_coordenadas[pos][0]
                y = lista_coordenadas[pos][1]
            aux = list(resultado[x][y])
            aux[0] = simbolo
            straux = resultado[x][:y+1]+ aux[0] + resultado[x][y+1:]
            resultado[x] = straux
            atual = lista_coordenadas[pos]

    print(resultado)
    '''
    for x in range(len(resultado)):
        for y in range(len(resultado[x])):
            if resultado[x][y] == 1:
                resultado[x][y] = simbolo_obstaculo
            elif resultado[x][y] == 0:
                resultado[x][y] = simbolo_livre
    '''
    
    '''
    print()
    print(resultado)
    '''
    return resultado

def recuperar_caminho(atual):
    global dicCustos

    percurso = []
    if atual != inicio:
        pontoOrigem = dicCustos[atual][3]
    else:
        pontoOrigem = inicio

    percurso.append(atual)
    while pontoOrigem != inicio:
        percurso.append(pontoOrigem)
        pontoOrigem = dicCustos[pontoOrigem][3]
    if inicio not in percurso:
        percurso.append(inicio)
    
    percurso.reverse()
    return percurso

def calcula_custos(pai, vizinhos):
    global dicCustos

    for vizinho in vizinhos:
        heuristica = distanciaManhattan(vizinho, final)
        coord_x = vizinho[0]
        coord_y = vizinho[1]
        try:
            if (mapa[coord_x][coord_y] == '.') or (mapa[coord_x][coord_y] == 'E') or (mapa[coord_x][coord_y] == 'I'):
                custo = dicCustos[pai][1] + 1  # Custo = Custo do Pai + Livre
            elif (mapa[coord_x][coord_y] == 'R'):
                custo = dicCustos[pai][1] + 5  # Custo = Custo do Pai + Rochoso
            elif (mapa[coord_x][coord_y] == 'F'):
                custo = dicCustos[pai][1] + 15  # Custo = Custo do Pai + Floresta
            elif (mapa[coord_x][coord_y] == 'A'):
                custo = dicCustos[pai][1] + 30  # Custo = Custo do Pai + Água
            else:
                custo = dicCustos[pai][1] + 200  # Custo = Custo do Pai + Montanha
        except:
            custo = 1  # No caso do Pai ser o Ponto Inicial

        try:
            if (dicCustos[vizinho][1] > custo):
                dicCustos[vizinho] = (vizinho, custo, heuristica, pai)
        except:
            dicCustos[vizinho] = (vizinho, custo, heuristica, pai)

    return dicCustos

def mapeia_vizinhos(atual):
    '''
        # Vizinhos (linha , coluna)
        (atual[0]-1) , (atual[1])   # Em cima
        (atual[0]+1) , (atual[1])   # Em baixo
        (atual[0]) , (atual[1]-1)   # Esquerda
        (atual[0]) , (atual[1]+1)   # Direita
    '''
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

def buscar():
    listaVizNaoVisitado.append(inicio)
    chegou = False

    while listaVizNaoVisitado != [] and not chegou:        
        # Primeiro elemento da lista já ordenada
        atual = listaVizNaoVisitado[0]

        # Pesquisa pelos elementos vizinhos elegiveis (nao é barreira) e não presentes na lista fechada
        vizinhos = mapeia_vizinhos(atual)
        
        calcula_custos(atual, vizinhos)  # Calculo de custo de cada vizinho

        # Verificando de um vizinho do atual ja nao esta presente na lista aberta
        for vizinho in vizinhos:
            if (vizinho not in listaVizNaoVisitado):
                listaVizNaoVisitado.append(vizinho)            
        
        # Remocao do primeiro elemento da lista aberta
        listaVizNaoVisitado.remove(atual)
        
        # Adicionando o elemento processado na lista fechada
        listaVizVisitado.append(atual)

        ordena_pelo_custo() 

        if(final in listaVizVisitado): # Achou o objetivo se o vizinho for coordenada final
            chegou = True
            caminho = recuperar_caminho(atual) # Lista com as posicoes percorridas até o destino      
            resultado = desenhar(caminho)

        # Ordenação dos elementos em ordem de custo crescente
        #ordena_pelo_custo() 
    
    return resultado

def read_file(filename):

    global x, y
    lines = None    
    start = (0,0)
    end = (0,0)

    with open(filename) as file:
        lines = file.readlines()

        j = 0
        for line in lines:
            lines[j] = line.strip('\n')
            
            if line.find('I') > -1:
                start = (j, line.find('I'))
            if line.find('E') > -1:
                end = (j, line.find('E'))
            j += 1

    x = len(lines[0])
    y = len(lines)

    return lines, start, end


mapa, inicio, final = read_file("mapa_dbz.txt")
listaVizNaoVisitado = []
listaVizVisitado = []
dicCustos = {}
solucao = buscar()
#print(solucao)
