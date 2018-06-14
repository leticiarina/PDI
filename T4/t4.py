# Nome: Letícia Rina Sakurai
# NUSP: 9278010
# SCC0251 - Processamento de Imagens
# 1º Semestre/2018
# Trabalho 4 - Filtragem 2D

import numpy as np 
import imageio
import math
np.seterr(over='ignore')

# Aplicação de convolução a partir de um filtro
def convolution(img, filterWeight):

	# Recria o filtro com zeros nas demais posições
	filterRes = np.zeros(img.shape, dtype=float)
	filterRes[:filterWeight.shape[0], :filterWeight.shape[1]] = filterWeight

	# Aplicação da transformada de Fourier no filtro e na imagem
	img = np.fft.fft2(img)
	filterRes = np.fft.fft2(filterRes)

	return img*filterRes

# Realiza convolução em duas imagens e gera a imagem a partir delas
def sobelOperator(img):

	ix = np.zeros(img.shape, dtype=int)
	iy = np.zeros(img.shape, dtype=int)

	# Percorre todos os pontos da imagem
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):

			# Zera variáveis e altera somente se estão dentro da matriz
			a = b = c = d = f = g = h = i = 0

			# Considere p o ponto atual, a matriz a ser usada no ponto é:
			# [a b c]
			# [d p f]
			# [g h i]
			if x != 0 and y != 0: a = img[x-1][y-1]
			if x != 0: b = img[x-1][y]
			if x != 0 and y != img.shape[1]-1: c = img[x-1][y+1]
			if y != 0: d = img[x][y-1]
			if y != img.shape[1]-1: f = img[x][y+1]
			if x != img.shape[0]-1 and y != 0: g = img[x+1][y-1]
			if x != img.shape[0]-1: h = img[x+1][y]
			if x != img.shape[0]-1 and y != img.shape[1]-1: i = img[x+1][y+1]

			# Efetua a convolução no ponto atual usando as matrizes
			ix[x][y] = a-c+(2*d)-(2*f)+g-i
			iy[x][y] = a+(2*b)+c-g-(2*h)-i

	# Aplica a equação e retorna a imagem final
	return np.sqrt(np.power(ix,2)+np.power(iy,2))

# Cria o filtro Laplaciana da Gaussiana 
def laplacianOfGaussian(n, sigma):	

	# Cria o array que armazenará o filtro
	f = np.zeros((n, n), dtype=float)

	# Variável para armazenar soma de valores positivos para a normalização
	pos = 0
	# Variável para armazenar soma de valores negativos para a normalização
	neg = 0

	# Cálculo do valor que deve ser somado para manter a linearidade dos pontos
	value = 10/(n-1)

	# Percorre cada posição do filtro
	for i in range(n):

		# Atribui os valores a serem utilizados em y
		if i == 0: y = 5
		elif i == n-1: y = -5
		else: y = y-value

		for j in range(n):

			# Atribui os valores a serem utilizados em x
			if j == 0: x = -5
			elif j == n-1: x = 5
			else: x = x+value

			# Calcula o valor de acordo com a função dada e utilizando x, y e sigma do ponto
			f[i][j] = -(1/(math.pi*math.pow(sigma,4)))*(1-((math.pow(x,2)+math.pow(y,2))/(2*math.pow(sigma,2))))*math.exp(-((math.pow(x,2)+math.pow(y,2))/(2*math.pow(sigma,2))))

			# Soma o valor na variável correspondente
			if f[i][j] >= 0: pos = pos+f[i][j]
			else: neg = neg+f[i][j] 

	# Normalização
	for i in range(n):
		for j in range(n):

			if f[i][j] < 0:
				f[i][j] = f[i][j]*(-pos/neg)

	return f

# Calcula as distâncias euclidianas entre os exemplos do dataset e retorna  
# o índice do vetor com a menor distância
def KNN(icut2, datasetFilename):

	# Transforma o corte em um array unidimensional
	vout = icut2.flatten()

	# Carrega o dataset do arquivo .npy
	dataset = np.load(datasetFilename)

	# Calcula a distância euclidiana entre todas as amostras do dataset e do corte
	for x in range(dataset.shape[0]):
		dist = np.linalg.norm(vout-dataset[x])

		# Se é a primeira iteração, armazena a primeira distância
		if x == 0:
			minDist = dist
			index = x
		
		# Nas demais, armazena somente se a distância atual é menor do que a armazenada
		else:
			if minDist > dist:
				minDist = dist
				index = x

	return index

if __name__ == "__main__":

	# Nome da imagem pra filtragem
	imgFile = str(input()).rstrip()
	# Método escolhido
	method = int(input())
	
	# Parâmetros para pesos do filtro
	if method == 1:

		# Altura e largura do filtro
		filterShape = input().rstrip().split(" ")
		filterShape = [int(shape) for shape in filterShape]
		h, w = filterShape

		filterWeight = []

		# Leitura dos pesos do filtro
		for i in range(h):
			filterWeight.append(input().rstrip())
			filterWeight[i] = filterWeight[i].split(" ")
			filterWeight[i] = [float(weight) for weight in filterWeight[i]]

		# Conversão para numpy
		filterWeight = np.array(filterWeight)

	elif method == 2:
		n = int(input()) # Tamanho do filtro
		sigma = float(input()) # Desvio padrão da distribuição

	# Posições de corte
	cut = input().rstrip().split(" ")
	cut = [float(c) for c in cut]
	hlb, hub, wlb, wub = cut

	# Arquivo com o dataset
	datasetFilename = str(input()).rstrip()
	# Arquivo com as labels do dataset
	labelsFilename = str(input()).rstrip()

	# Abre a imagem a ser filtrada
	img = imageio.imread(imgFile)

	# Aplicação da filtragem escolhida
	if method == 1: iout = convolution(img, filterWeight)
	elif method == 2: iout = convolution(img, laplacianOfGaussian(n, sigma))
	elif method == 3: iout = np.fft.fft2(sobelOperator(img))

	# Realização do corte de simetria
	icut1 = iout[0:int(iout.shape[0]/2), 0:int(iout.shape[1]/2)]

	# Limites do corte
	limits = [int(icut1.shape[0]*hlb), int(icut1.shape[0]*hub), int(icut1.shape[1]*wlb), int(icut1.shape[1]*wub)]
	
	# Corte de acordo com os limites definidos 
	icut2 = icut1[limits[0]:limits[1], limits[2]:limits[3]]	

	# Obtém o índice do dataset com menor distância euclidiana
	index = KNN(icut2, datasetFilename)

	# Abre o conteúdo de labels
	labels = np.load(labelsFilename)

	# Imprime o conteúdo referente ao índice obtido e o próprio índice
	print(labels[index])
	print(index)