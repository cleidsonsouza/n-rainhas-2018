########################################################################################################################
#                                                       Apresentação                              					   #							
########################################################################################################################
#
# Universidade Estadual de Montes Claros - Unimontes
#
# Programa de Pós Graduação em Modelagem Computacional e Sistemas (PPGMCS)
#
# Disciplina: Algoritmos Evolutivos
#
# Segundo Trabalho Prático: Solução do problema das N-Rainhas utilizando representação inteira 
#
# Autor: Cleidson dos Santos Souza 
# 
# Testado no Python 3.6
#
# Data: 04/10/2018
# -------------------------------------------------------------------------------------------------------------------- #

# Importação de módulos
import ag
import pygame
import numpy as np
import matplotlib.pyplot as plt

# Definição da função objetivo
def func_custo(arr):
	erro = 0	
	for i in range(len(arr)):		
		for j in range(1, len(arr)-i):		
			if arr[i+j] == arr[i] + j:				
				erro += 1
		for k in range(1, (len(arr) - (len(arr)-i))+1):		
			if arr[i-k] == arr[i] + k:				
				erro += 1		
	return erro
	
# Criação e inicialização de variáveis - Parte 1
geracao = 0
elitismo = 0
numGeracoes = 30
numExecucoes = 50
tamPopulacao = 30
tamIndividuo = 8
probMutacao = 0.125
probCruzamento = 0.8
# Criação e inicialização de variáveis - Parte 2
melhorFitness = np.zeros(numGeracoes)
melhoresFitness = np.zeros((numExecucoes, numGeracoes))
mediaFitnessExecucao = np.zeros((numExecucoes, numGeracoes))
fitnessMelhorGeracao = np.zeros((numExecucoes, numGeracoes))
melhoresFitnessExecucao = np.zeros((numExecucoes, numGeracoes))
melhorIndividuoExecucao = np.zeros((numExecucoes, tamIndividuo))
melhorFitnessExecucao = np.zeros(numExecucoes)

# Algoritmo genético em si
def agint(tamPopulacao, tamIndividuo, probCruzamento, probMutacao, elitismo, numGeracoes):	
	
	# Criação e inicialização de variáveis
	sinal = 0
	geracao = 0	
	fitness = np.zeros(tamPopulacao)
	fitness2 = np.zeros((numGeracoes,tamPopulacao))
	mediaFitness = np.zeros(numGeracoes)	
	melhorIndividuo = np.zeros((numGeracoes, tamIndividuo))	
	
	# Criação da população inicial
	pop = ag.gerpopint(tamPopulacao, tamIndividuo)	
	
	# Avaliação
	for i in range(tamPopulacao):
		fitness[i] = ag.fitness(pop[i,:], func_custo)	
	
	# Loop principal
	while geracao < numGeracoes:	

		#print('\n','-'*28, 'Geração: ', geracao, '-'*28)
		
		# Teste #
		if np.min(fitness) == 0 and sinal == 0:
			print('Geração com fitness 0: ', geracao)
			sinal = 1
		
		# Seleção
		popSelecao = ag.selecao(pop, 1/(fitness+0.00000000000000001), 'torneio', tamPopulacao)	
		
		# Cruzamento
		popCruzamento = ag.cruzamento(popSelecao, probCruzamento, 'ox', tamPopulacao)		
		
		# Mutação
		popMutacao = ag.mutacao(popCruzamento, probMutacao, 'mutint', tamPopulacao)			
		
		# Avaliação	
		for i in range(tamPopulacao):
			fitness[i] = ag.fitness(popMutacao[i,:], func_custo)										
		
		# Cálculo do melhor fitness
		melhorFitness[geracao] = np.min(fitness)
		#print('melhorFitness', melhorFitness[geracao]) # Teste
		
		melhorIndividuo[geracao,:] = popMutacao[np.argmin(fitness),:] 		
		#print('melhorIndividuo: indivíduo {} => {}'.format(np.argmin(fitness), melhorIndividuo[geracao,:])) # Teste
					
		# Elitismo
		if elitismo:			
			if geracao>0:							
				if melhorFitness[geracao-1] < melhorFitness[geracao]:					
					popMutacao[1,:] = melhorIndividuo[geracao-1,:]
					melhorFitness[geracao] = melhorFitness[geracao-1]					
		
		# Cálculo da média dos fitness
		mediaFitness[geracao] = np.mean(fitness)			
		
		# Substituição da população
		pop = popMutacao
				
		# Incremento do número de gerações
		geracao += 1
		
	# Cálculo do índice da melhor geração
	indiceMelhorGeracao = np.argmin(melhorFitness)	
	#print('indiceMelhorGeracao', indiceMelhorGeracao)
	
	# Retorno da função		
	return mediaFitness, melhorIndividuo[indiceMelhorGeracao, :], melhorFitness[indiceMelhorGeracao], melhorFitness	

# Chamada da função executa o AG	
for i in range(numExecucoes):
	print("******************************", "EXECUÇÃO ", i, "*********************************")	
	mediaFitnessExecucao[i,:], melhorIndividuoExecucao[i,:], melhorFitnessExecucao[i], melhoresFitnessExecucao[i,:] = agint(tamPopulacao, tamIndividuo, probCruzamento, probMutacao, elitismo, numGeracoes)	

# 
cont = 0	
for i in range(numExecucoes):
	if melhorFitnessExecucao[i]	== 0:
		cont+=1
print('O número de sucesso foi: ', cont)
	
#Plotagem dos resultados
indiceMelhorExecucao = int(np.argmin(melhorFitnessExecucao))
print('indiceMelhorExecucao', indiceMelhorExecucao)
print('melhorFitnessExecucao', melhorFitnessExecucao)
#print('melhorIndividuoExecucao', melhorIndividuoExecucao)
print("Melhor fitness: ", np.min(melhorFitnessExecucao))
print("Melhor solução: ", melhorIndividuoExecucao[indiceMelhorExecucao,:])
print("Média de execução: ", np.mean(mediaFitnessExecucao))
	
# Plotagem dos gráficos
fig, ax = plt.subplots()
ax.plot(mediaFitnessExecucao[indiceMelhorExecucao,:], 'g--', label='Média do Fitness')
ax.plot(melhoresFitnessExecucao[indiceMelhorExecucao,:], 'b-', label='Melhor Fitness')
ax.legend()
ax.set(xlabel='Gerações', ylabel='Fitness', title='Evolução do Fitness - Melhor Geração')
ax.grid()

fig, ax = plt.subplots()
ax.plot(melhorFitnessExecucao, 'g--', label='Melhor Fitness Execucao')
ax.legend()
ax.set(xlabel='Execuções', ylabel='Fitness', title='Execução do Fitness')
ax.grid()

# --------------- Plotagem do tabuleiro --------------- # 

mi = melhorIndividuoExecucao[indiceMelhorExecucao,:]

# Inicializa todos os módulos pygame importados
pygame.init()   

# Define a altura e largura da tela do jogo
alturaTela = 626
larguraTela = 626

# Define as dimensões da tela do jogo
tela = pygame.display.set_mode((larguraTela,alturaTela))

# Define o texto que aparecerá na janela do jogo
pygame.display.set_caption('Problema das N-Rainhas')

# Carrega imagens de fundo 
imagemFundo = pygame.image.load('planoFundo.jpg') 
imagemRainha = pygame.image.load('rainhas.png')

# Imprime a imagens de fundo da tela
tela.blit(imagemFundo, (0,0))  

# Imprime as rainhas no tabuleiro
for i in range(8):	
		tela.blit(imagemRainha, ((i*78)+15,(78*mi[i])+15))
	
# Atualiza a tela do jogo
pygame.display.update()	
while True:
     pass

