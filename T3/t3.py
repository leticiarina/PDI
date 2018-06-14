# Nome: Letícia Rina Sakurai
# NUSP: 9278010
# SCC0251 - Processamento de Imagens
# 1º Semestre/2018
# Trabalho 3 - Filtragem 1D

import numpy as np 
import imageio
import math

# Calcula a posição central do filtro
def centerPos(n):

	if n%2 == 0:
		return int(n/2-1)
	else:
		return math.floor(n/2)

# Cria o filtro gaussiano utilizando o desvio padrão da distribuição gaussiana
def gaussianFilter(weight, center, n):

	unidFilter = np.zeros(n, dtype=float)

	# Define o primeiro peso do filtro
	actualWeight = 0-center

	# Preenche o filtro com todos os pesos
	for x in range(n):
		unidFilter[x] = actualWeight
		actualWeight = actualWeight+1

	# Aplica a equação para gerar o filtro
	unidFilter = (1/((math.sqrt(2*math.pi))*weight))*np.exp(-(np.power(unidFilter,2))/2*(math.pow(weight, 2)))

	# Normaliza para que a soma seja unitária
	unidFilter = (unidFilter-np.min(unidFilter))/(np.max(unidFilter)-np.min(unidFilter))
	unidFilter = unidFilter/np.sum(unidFilter)

	return unidFilter

# Aplicação da transformada discreta de Fourier
def DFT1D(A):
    
    F = np.zeros(np.size(A), dtype=np.complex64)
    n = np.size(A)

    # criamos os indices para x
    x = np.arange(n)
    # para cada frequencia, computamos de forma vetorial para x e somamos em 'u'
    for u in np.arange(n):
        F[u] = np.sum(A*np.exp( (-1j * 2 * np.pi * u*x) / n ))
            
    return F

# Aplicação da inversa da transformada discreta de Fourier
def inverseDFT1D(A):
    
    F = np.zeros(np.size(A), dtype=np.complex64)
    n = np.size(A)

    # criamos os indices para x
    x = np.arange(n)
    # para cada frequencia, computamos de forma vetorial para x e somamos em 'u', multiplicando pelo inverso do tamanho
    for u in np.arange(n):
        F[u] = 1/n*(np.sum(A*np.exp( (+1j * 2 * np.pi * u*x) / n )))

    return F

# Realiza convolução do domínio espacial com deslocamento do filtro sobre a imagem
def spacialDomain(img, n, center, unidFilter):

	convolution = np.zeros(img.size, dtype=float)

	# Primeiro pixel a ser utilizado na convolução
	firstPixel = 0-center

	# x serve para iterar sobre cada pixel da imagem
	for x in range(img.size):

		# Recebe a posição pixel em que irá iniciar a convolução
		actualPixel = firstPixel

		# y serve para iterar sobre cada posição do filtro
		for y in range(n):
		
			# Retona às posições iniciais se ultrapassar o tamanho do vetor	
			if actualPixel >= img.size:
				actualPixel = actualPixel-(img.size)

			# Realiza a multiplicação 
			convolution[x] = convolution[x]+(unidFilter[y]*img[actualPixel])
			
			# Troca o pixel atual
			actualPixel = actualPixel+1

		# Aumenta o pixel de início da operação
		firstPixel = firstPixel+1

	return convolution

# Calcula domínio de filtragem da frequência
def frequencyDomain(i, unidFilter):

	unidFilter = np.resize(unidFilter, np.size(i))

	# Completa o filtro com zeros
	for x in range(n, np.size(i)):
		unidFilter[x] = 0

	# Aplicação da transformada de Fourier no filtro e na imagem
	fourierFilter = DFT1D(unidFilter)
	fourierImg = DFT1D(i)

	# Multiplica os vetores e aplica a transformada inversa de Fourier
	return inverseDFT1D(fourierFilter*fourierImg)

# Realiza o cálculo da raiz do erro médio quadrático para comparar a imagem
# gerada com a imagem base fornecida
def compareImages(generatedImg, imgFile):

	# Carrega imagem base para comparação
	imgBase = imageio.imread(imgFile)

	# Retorna vetor ao formato de array de duas dimensões
	generatedImg = np.reshape(generatedImg, (imgBase.shape[0], imgBase.shape[1]))

	# Valor máximo da imagem
	imageMax = np.max(generatedImg)

	# Valor mínimo da imagem
	imageMin = np.min(generatedImg)

	# Normalização da imagem e conversão para int
	generatedImg = (generatedImg - imageMin)/(imageMax-imageMin)
	generatedImg = (np.real(generatedImg)*255).astype(np.int)

	# Variável que armazenará o cálculo da diferença entre as imagens
	rmse = 0

	# Somatório do cálculo do RMSE
	for i in range(generatedImg.shape[0]):
		for j in range(generatedImg.shape[1]):
			rmse = rmse + math.pow((imgBase[i,j]-generatedImg[i,j]),2)

	# Multiplicação pelo inverso das dimensões e radiciação
	rmse = math.sqrt((1/(generatedImg.shape[0]*generatedImg.shape[1]))*rmse)
	
	# Impressão do resultado
	print('%.4f' %rmse)

if __name__ == "__main__":

	# Nome da imagem para filtragem
	imgFile = str(input()).rstrip()
	# Escolha do filtro - 1: arbitrário; 2: função Gaussiana
	filterOpt = int(input())
	# Tamanho do filtro N
	n = int(input())

	# Parâmetro(s) definindo pesos do filtro
	if filterOpt == 1:
		weight = str(input())
		weight = weight.split()

		for x in range(n):
			weight[x] = int(weight[x])

	elif filterOpt == 2:
		weight = float(input())

	# Domínio da filtragem
	filterDomain = int(input())

	# Transforma a imagem em um vetor unidimensional
	i = imageio.imread(imgFile).flatten()

	# Posição central do filtro
	center = centerPos(n)

	# Escolha do filtro
	if filterOpt == 1:
		unidFilter = weight
	elif filterOpt == 2:
		unidFilter = gaussianFilter(weight, center, n)

	# Aplicação do domínio de filtragem
	if filterDomain == 1:
		generatedImg = spacialDomain(i, n, center, unidFilter)
	elif filterDomain == 2:
		generatedImg = frequencyDomain(i, unidFilter)

	# Compara a imagem gerada com a imagem base fornecida
	compareImages(generatedImg, imgFile)
