# Nome: Letícia Rina Sakurai
# NUSP: 9278010
# SCC0251 - Processamento de Imagens
# 1º Semestre/2018
# Trabalho 1 - Gerador de Imagens

import numpy as np
import math
import random
import sys

def functionOne(cLateral):
	
	# Numpy Array que irá armazenar a imagem da cena
	sceneImg = np.zeros((cLateral, cLateral), dtype = float)

	# Realiza a função de geração da imagem f(x,y) = x+y
	for x in range(cLateral):
		for y in range(cLateral):
			sceneImg[x,y] = float(x)+float(y)

	# Valor máximo da imagem
	imageMax = np.max(sceneImg)

	# Normalização da imagem
	sceneImg = sceneImg*65535/imageMax

	return sceneImg

def functionTwo(cLateral, q):

	# Numpy Array que irá armazenar a imagem da cena
	sceneImg = np.zeros((cLateral, cLateral), dtype = float)

	# Realiza a função de geração da imagem f(x,y) = |sin(x/Q)+sin(y/Q)|
	for x in range(cLateral):
		for y in range(cLateral):
			sceneImg[x,y] = abs(math.sin(x/q)+math.sin(y/q))

	# Valor máximo da imagem
	imageMax = np.max(sceneImg)

	# Normalização da imagem
	sceneImg = sceneImg*65535/imageMax

	return sceneImg	

def functionThree(cLateral, q):

	# Numpy Array que irá armazenar a imagem da cena
	sceneImg = np.zeros((cLateral, cLateral), dtype = float)

	# Realiza a função de geração da imagem f(x,y) = |(x/Q)-sqrt(y/Q)|
	for x in range(cLateral):
		for y in range(cLateral):
			sceneImg[x,y] = abs((x/q)-math.sqrt(y/q))

	# Valor máximo da imagem
	imageMax = np.max(sceneImg)

	# Normalização da imagem
	sceneImg = sceneImg*65535/imageMax

	return sceneImg	

def functionFour(cLateral, seed):

	# Numpy Array que irá armazenar a imagem da cena
	sceneImg = np.zeros((cLateral, cLateral), dtype = float)

	# Inicializa a função aleatória uma única vez
	random.seed(seed)

	# Realiza a função de geração da imagem f(x,y) = rand
	for x in range(cLateral):
		for y in range(cLateral):
			sceneImg[x,y] = random.random()

	# Valor máximo da imagem
	imageMax = np.max(sceneImg)

	# Normalização da imagem
	sceneImg = sceneImg*65535/imageMax

	return sceneImg	

def functionFive(cLateral, seed):

	# Numpy Array que irá armazenar a imagem da cena, atribuindo 0 para todo f(x,y)
	sceneImg = np.zeros((cLateral, cLateral), dtype = float)

	# Inicializa a semente uma única vez
	random.seed(seed)

	# Define f(0,0) = 1 
	sceneImg[0,0] = 1

	# Inicializa x e y como o ponto inicial
	x = 0
	y = 0

	# Cálculo dos valores aleatórios de x e y e atribuição de f(x,y) = 1
	for i in range(int(1+(cLateral*cLateral)/2)):
		x = (x+random.randint(-1, 1))%cLateral
		sceneImg[x,y] = 1

		y = (y+random.randint(-1, 1))%cLateral
		sceneImg[x,y] = 1

	# Valor máximo da imagem
	imageMax = np.max(sceneImg)

	# Normalização da imagem
	sceneImg = sceneImg*65535/imageMax

	return sceneImg	

def generateDigitalImg(sceneImg, nLateral, bits, d):

	# Numpy Array que irá armazenar a imagem digital
	digitalImg = np.zeros((nLateral, nLateral), dtype = float)

	# Geração da imagem digital
	for x in range(nLateral):
		for y in range(nLateral):

			# Cálculo do intervalo de pixels a serem considerados na maximização
			x1 = x*d
			x2 = (x*d)+d-1

			y1 = y*d
			y2 = (y*d)+d-1

			# Retorna o valor máximo do array considerado
			digitalImg[x,y] = float(sceneImg[x1:x2+1,y1:y2+1].max())

	# Valor máximo da imagem
	imageMax = np.max(digitalImg)

	# Quantização da imagem
	digitalImg = digitalImg*255/imageMax

	# Conversão para inteiro de 8 bits
	digitalImg = digitalImg.astype(np.uint8)

	# Deslocamento de bits
	digitalImg = np.right_shift(digitalImg, 8-bits)

	return digitalImg

def compareImages(digitalImg, filename):

	# Carregamento da imagem referência
	refImg = np.load(filename).astype(np.uint8)

	# Variável que armazenará o cálculo da diferença entre as imagens
	rmse = 0

	# Somatório do cálculo do RMSE
	for x in range(nLateral):
		for y in range(nLateral):
			rmse = rmse + math.pow((digitalImg[x,y]-refImg[x,y]),2)

	# Tira a raiz quadrada para obter o RMSE final
	rmse = math.sqrt(rmse)

	# Impressão do resultado
	print('%.4f' %rmse)

if __name__ == "__main__":

	# Nome do arquivo que contém a imagem referência
	filename = str(input()).rstrip()
	# Dimensões da imagem cena a ser gerada
	cLateral = int(input())
	# Função escolhida para geração da imagem cena
	function = int(input())
	# Parâmetro Q utilizado em cálculos das funções 2 e 3
	q = int(input())
	# Dimensões da imagem digital a ser gerada
	nLateral = int(input())
	# Quantidade de bits a considerar na quantização
	bits = int(input())
	# Semente para funções aleatórias
	seed = int(input())
	
	# Cálculo da quantidade relativa de pixels entre imagem cena e imagem digital
	d = int(cLateral/nLateral)

	# Chamada da função para geração da imagem cena
	if function == 1:
		sceneImg = functionOne(cLateral)
	elif function == 2:
		sceneImg = functionTwo(cLateral, q)
	elif function == 3:
		sceneImg = functionThree(cLateral, q)
	elif function == 4:
		sceneImg = functionFour(cLateral, seed)
	elif function == 5:
		sceneImg = functionFive(cLateral, seed)

	# Chamada da função para gerar a imagem digital
	digitalImg = generateDigitalImg(sceneImg, nLateral, bits, d)
	
	# Chamada da função para comparar a imagem gerada e a referência
	compareImages(digitalImg, filename)