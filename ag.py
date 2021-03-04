###########################################################################
#                             Apresentação                                #
###########################################################################
#
# Universidade Estadual de Montes Claros - Unimontes
#
# Programa de Pós Graduação em Modelagem Computacional e Sistemas (PPGMCS)
#
# Disciplina: Algoritmos Evolutivos
#
# Primeiro Trabalho Prático: Algoritmos Genéticos
#
# Parte 1: Módulo ag 
# 
# Autor: Cleidson dos Santos Souza 
# 
# Testado no Python 3.6
#
# Data: 20/09/2018

# Importação e renomeação do pacote numpy
import numpy as np

# Função que gera população binária aleatoriamente
def gerpopbin(tamPopulacao, tamIndividuo):	
	return np.random.randint(2, size=(tamPopulacao, tamIndividuo))	

# Função que gera população decimal aleatoriamente
def gerpopdec(tamPopulacao, tamIndividuo):
	return 2 * np.random.random_sample((tamPopulacao, tamIndividuo)) - 1

# Método que cria um array de inteiros (com permutação)
def gerpopint(tamPopulacao, tamIndividuo):
	pop =  np.zeros((tamPopulacao, tamIndividuo))
	for i in range(tamPopulacao):
		pop[i,:] = np.random.permutation(tamIndividuo)
	return pop

# Função que calcula o fitness
def fitness(arr, foper):
	return(foper(arr))

# Função de cálculo da seleção 
def selecao(pop, fitness, op, n):			
	popSelecao = np.zeros((n, pop.shape[1]))
	if op == 'roleta':			
		sumFitness = np.sum(fitness)					
		for i in range(n): # Ou até tamPopulacao			
			soma = 0
			numRand = np.random.uniform(0, sumFitness) 							
			for j in range(pop.shape[0]):				
				soma += fitness[j] 				
				if soma >= numRand:
					popSelecao[i,:] = pop[j,:]					
					break					
		return popSelecao

	elif op == 'torneio':			
		for i in range(n): # Ou até tamPopulacao		 			
			id1 = np.random.randint(pop.shape[0])			
			id2 = np.random.randint(pop.shape[0])			
			if fitness[id1] > fitness[id2]:
				popSelecao[i,:] = pop[id1,:]
			else: 
				popSelecao[i,:] = pop[id2,:]			
		return popSelecao

# Função que executa o cruzamento
def cruzamento(popSelecao, pc, op, n):
	[tamPopulacao, tamIndividuo] = popSelecao.shape	
	popCruzamento = np.zeros((n, tamIndividuo))
	if op == '1pc':
		for i in range(n):
			pontoCorte = np.random.randint(tamIndividuo)			
			id1 = np.random.randint(tamPopulacao)			
			id2 = np.random.randint(tamPopulacao)		
			tc = np.random.random()			
			if tc < pc:			
				popCruzamento[i,:pontoCorte] = popSelecao[id1,:pontoCorte]				
				popCruzamento[i,pontoCorte:] = popSelecao[id2,pontoCorte:]	
				filho1 = popCruzamento[i,:]				
			else:
				popCruzamento[i,:pontoCorte] = popSelecao[id2,:pontoCorte]
				popCruzamento[i,pontoCorte:] = popSelecao[id1,pontoCorte:]	
				filho1 = popCruzamento[i,:]													
		return popCruzamento

	if op == '2pc':		
		for i in range(n): # Ou até tamPopulacao
			pc1 = np.random.randint(tamIndividuo-1) 					
			pc2 = np.random.randint(pc1+1, tamIndividuo) 					
			id1 = np.random.randint(tamPopulacao)			
			id2 = np.random.randint(tamPopulacao) 
			tc = np.random.random()			
			if tc < pc:				
				popCruzamento[i,:pc1] = popSelecao[id1,:pc1]				
				popCruzamento[i,pc1:pc2] = popSelecao[id2,pc1:pc2]
				popCruzamento[i,pc2:] = popSelecao[id1,pc2:]				
			else:
				popCruzamento[i,:pc1] = popSelecao[id2,:pc1]
				popCruzamento[i,pc1:pc2] = popSelecao[id1,pc1:pc2]
				popCruzamento[i,pc2:] = popSelecao[id2,pc2:]		
		return popCruzamento

	if op == 'mascbit':		
		for i in range(0,n,2): # Ou até tamPopulacao				
			id1 = np.random.randint(tamPopulacao)			
			id2 = np.random.randint(tamPopulacao) 
			mascara = np.random.randint(2, size=(tamIndividuo))				
			tc = np.random.random()			
			if tc < pc:
				for j in range(tamIndividuo):
					if mascara[j] == 0:
						popCruzamento[i,j] = popSelecao[id1,j]	
						popCruzamento[i+1,j] = popSelecao[id2,j]	
					else:
						popCruzamento[i,j] = popSelecao[id2,j]
						popCruzamento[i+1,j] = popSelecao[id1,j]
			else:
				popCruzamento[i,:] = popSelecao[id1,:]
				popCruzamento[i+1,:] = popSelecao[id2,:]			
		return popCruzamento

	# Método 'ox' que realiza cruzamento utilizando representação inteira
	if op == 'ox':
		for i in range(0, n, 2): 				
			filho1 = np.zeros(tamIndividuo) - 1
			filho2 = np.zeros(tamIndividuo) - 1			
			pai1 = popSelecao[np.random.randint(tamPopulacao), :]
			pai2 = popSelecao[np.random.randint(tamPopulacao), :] 			
			pontoCorte1 = np.random.randint(tamIndividuo-1)			
			pontoCorte2 = np.random.randint(pontoCorte1+1, tamIndividuo)

			if np.random.random() < pc:						
				filho1[pontoCorte1:pontoCorte2] = pai1[pontoCorte1:pontoCorte2]	
				filho2[pontoCorte1:pontoCorte2] = pai2[pontoCorte1:pontoCorte2]

				# Quantidade de genes a serem preenchidos nos filhos	
				genesRestantes = tamIndividuo - (pontoCorte2 - pontoCorte1)				

				indiceCorrentePai1 = pontoCorte2
				indiceCorrentePai2 = pontoCorte2
				indiceCorrenteFilho1 = pontoCorte2
				indiceCorrenteFilho2 = pontoCorte2
				for j in range(genesRestantes):						
					# Preenche o cromossomo do filho1 com genes do pai2
					while any(gene == pai2[indiceCorrentePai2] for gene in filho1[pontoCorte1:]):
						indiceCorrentePai2 += 1
						if indiceCorrentePai2 >= tamIndividuo:
							indiceCorrentePai2 = 0
							pontoCorte1 = 0
					filho1[indiceCorrenteFilho1] = pai2[indiceCorrentePai2]
					# Atualiza o índice corrente do filho1
					indiceCorrenteFilho1 += 1
					if indiceCorrenteFilho1 >= tamIndividuo:
						indiceCorrenteFilho1 = 0	
					# Preenche o cromossomo do filho2 com genes do pai1
					while any(gene == pai1[indiceCorrentePai1] for gene in filho2[pontoCorte1:]):
						indiceCorrentePai1 += 1
						if indiceCorrentePai1 >= tamIndividuo:
							indiceCorrentePai1 = 0
							pontoCorte1 = 0					
					filho2[indiceCorrenteFilho2] = pai1[indiceCorrentePai1]
					# Atualiza o índice corrente do filho2
					indiceCorrenteFilho2 += 1
					if indiceCorrenteFilho2 >= tamIndividuo:
						indiceCorrenteFilho2 = 0	
					# Atualiza o índice corrente do pai2
					indiceCorrentePai2 += 1
					if indiceCorrentePai2 >= tamIndividuo:
						indiceCorrentePai2 = 0					
					# Copia os filhos 1 e 2 para a nova população
					popCruzamento[i,:] = filho1
					popCruzamento[i+1,:] = filho2
			else:
				popCruzamento[i,:] = pai1
				popCruzamento[i+1,:] = pai2
		return popCruzamento

# Função que realiza a mutação
def mutacao(popCruzamento, pm, op, n):
	[tamPopulacao, tamIndividuo] = popCruzamento.shape
	popMutacao = popCruzamento
	if op == 'bit':
		for i in range(n): # Ou até tamPopulacao
			tm = np.random.random()			
			if tm < pm:
				bit =  np.random.randint(tamIndividuo)											
				if popMutacao[i,bit] == 0:
					popMutacao[i,bit] = 1
				else:
					popMutacao[i,bit] = 0
		return popMutacao	

	if op == 'bitbit':
		for i in range(n): # Ou até tamPopulacao
			for bit in range(tamIndividuo):
				tm = np.random.random()
				if tm < pm:	
					if(popMutacao[i,bit] == 0):
						popMutacao[i,bit] = 1
					else:
						popMutacao[i,bit] = 0
		return popMutacao
	
	if op == 'mutint':
		for i in range(n):
			geneAleatorio1 = np.random.randint(tamIndividuo-1) 
			geneAleatorio2 = np.random.randint(tamIndividuo-1)
			if np.random.randint(tamPopulacao) < pm:
				aux = popCruzamento[i, geneAleatorio1]
				popCruzamento[i, geneAleatorio1] = popCruzamento[i, geneAleatorio2]
				popCruzamento[i, geneAleatorio2] = aux
		return popCruzamento

# Função que realiza o elitismo
def elitismo(popMutacao, fitness, melhorFitnessGeracao, geracao):
	if np.max(fitness) > melhorFitnessGeracao[geracao-1]:	
		indiceMelhorIndividuo = np.argmax(fitness)				
		popMutacao[0,:] = popMutacao[indiceMelhorIndividuo,:]							
		melhorFitnessGeracao[geracao] = np.max(fitness)			
	else:
		melhorFitnessGeracao[geracao] = melhorFitnessGeracao[geracao-1]
	return popMutacao

# Função que realiza o elitismo
def elitismo2(popMutacao, fitness, melhorFitnessGeracao, geracao):
	if np.min(fitness) > melhorFitnessGeracao[geracao-1]:	
		indiceMelhorIndividuo = np.argmin(fitness)				
		popMutacao[0,:] = popMutacao[indiceMelhorIndividuo,:]							
		melhorFitnessGeracao[geracao] = np.min(fitness)			
	else:
		melhorFitnessGeracao[geracao] = melhorFitnessGeracao[geracao-1]
	return popMutacao

####################################################################################
#		 	        OPERADORES GENÉTICOS PARA REPRESENTAÇÃO REAL     		       #
####################################################################################

# Função que realiza a mutação
def mutacao_real(popCruzamento, pm, op, n):
	[tamPopulacao, tamIndividuo] = popCruzamento.shape
	popMutacao = popCruzamento
	if op == 'subaleat':
		for i in range(n): # Ou até tamPopulacao
			tm = np.random.random()			
			if tm < pm:
				bit =  np.random.randint(tamIndividuo)															
				popMutacao[i,bit] = (2 * np.random.random_sample()) - 1				
		return popMutacao	

	if op == 'creep':
		for i in range(n): # Ou até tamPopulacao
			tm = np.random.random()			
			if tm < pm:
				bit =  np.random.randint(tamIndividuo)															
				popMutacao[i,bit] -= (np.random.random() - 0.5)**9				
		return popMutacao

	if op == 'geometrico':
		for i in range(n): # Ou até tamPopulacao
			tm = np.random.random()			
			if tm < pm:
				bit =  np.random.randint(tamIndividuo)															
				popMutacao[i,bit] = popMutacao[i,bit] * ((0.995 - 1.001) * np.random.random_sample() + 1.001)				
		return popMutacao	

def bin4dec2(pop, numBits):	
	[tamPopulacao, tamIndividuo] = pop.shape	
	pop = np.flip(pop, 1)	
	exp = 0	
	cont = 0
	numReal = 0
	pop2 = np.zeros((tamPopulacao, int(tamIndividuo/numBits)))		
	for i in range(tamPopulacao):		
		for j in range(int(tamIndividuo/numBits)):			
			for k in range(j*numBits, (j+1)*numBits):												
				numReal += pop[i,k] * (2**exp)
				exp+=1
			exp = 0
			numReal = (numReal/(2**numBits)) * (1 + 1) - 1							
			pop2[i,cont] = numReal
			numReal = 0
			cont+=1			
		cont=0			
	return pop2


# Conversão de binário para real
def bin4dec(pop, numBits):	
	[tamPopulacao, tamIndividuo] = pop.shape
	cont = 0
	numBin = ''
	pop2 = np.zeros((tamPopulacao, int(tamIndividuo/numBits)))	
	for i in range(tamPopulacao):		
		for j in range(int(tamIndividuo/numBits)):			
			for k in range(j*numBits, (j+1)*numBits):								
				numBin += str(int(pop[i,k]))				
			pop2[i, cont] = float(int(numBin, 2))
			numBin = ''
			cont+=1			
		cont=0	
	return pop2

####################################################################################
#  	 	          OPERADORES GENÉTICOS PARA REPRESENTAÇÃO INTEIRA    		       #
####################################################################################

# Método que realiza o cruzamento utilizando representação inteira
