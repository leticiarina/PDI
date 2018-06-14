# Nome: Letícia Rina Sakurai
# NUSP: 9278010
# SCC0251 - Processamento de Imagens
# 1º Semestre/2018
# Trabalho 2 - Realce e superresolução

import numpy as np 
import imageio
import math

# Gera a imagem de alta resolução utilizando as imagens base de baixa resolução
def generateHighImgRes(l1, l2, l3, l4):

	# Numpy Array que irá armazenar a imagem de alta resolução gerada
	imgHigh = np.zeros((2*l1.shape[0], 2*l1.shape[1]), dtype=float)

	# i e j servem para iterar sobre as dimensões da imagem de alta resolução
	i = 0
	j = 0

	# x e y servem para iterar sobre as dimensões da imagem de baixa resolução
	for x in range(l1.shape[0]):
		for y in range(l1.shape[1]):

			# Popula 4 pixels da imagem de alta resolução
			imgHigh[i,j] = l1[x,y]
			imgHigh[i+1,j] = l3[x,y]
			imgHigh[i,j+1] = l2[x,y]
			imgHigh[i+1,j+1] = l4[x,y]

			# Troca para a coluna seguinte a ser populada
			j = j+2

		# Troca a linha da imagem de alta resolução
		i = i+2
		j = 0

	return imgHigh

# Implementa o ajuste gama na imagem
def gammaAdjustment(img, param):

	return np.floor(255*(np.power(img/255.0, 1/param)))

# Aplica a função de transferência para equalizar uma imagem
def transferFunction(img, histogram):

	# Função de transferência
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			img[x,y] = (255/(img.shape[0]*img.shape[1]))*histogram[img[x,y]]

	return img

# Calcula a média dos histogramas de todas as imagens
def uniqueHistogram(l1, l2, l3, l4):

	return (calculateHistogram(l1)+calculateHistogram(l2)+calculateHistogram(l3)+calculateHistogram(l4))/4

# Realiza o cálculo do histograma acumulado de uma determinada imagem
def calculateHistogram(img):

	# Array para armazenar o histograma acumulado
	cumulativeHist = np.zeros(256)

	# Armazena a ocorrência de cada pixel
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			cumulativeHist[img[x,y]] = cumulativeHist[img[x,y]]+1

	# Calcula o histograma cumulativo 
	for i in range(1, len(cumulativeHist)):
		cumulativeHist[i] = cumulativeHist[i]+cumulativeHist[i-1]

	return cumulativeHist

# Realiza o cálculo da raiz do erro médio quadrático para comparar a imagem
# gerada com a imagem base fornecida
def compareImages(imgHigh, imgHighFilename):

	# Carrega imagem base para comparação
	imgBase = imageio.imread(imgHighFilename)

	# Variável que armazenará o cálculo da diferença entre as imagens
	rmse = 0

	# Somatório do cálculo do RMSE
	for i in range(imgHigh.shape[0]):
		for j in range(imgHigh.shape[1]):
			rmse = rmse + math.pow((imgBase[i,j]-imgHigh[i,j]),2)

	# Multiplicação pelo inverso das dimensões e radiciação
	rmse = math.sqrt((1/(imgHigh.shape[0]*imgHigh.shape[1]))*rmse)
	
	# Impressão do resultado
	print('%.4f' %rmse)

if __name__ == "__main__":

	# Arquivo base para imagens de baixa resolução
	imgLow = str(input()).rstrip()
	# Arquivo com imagem de alta resolução 
	imgHighFilename = str(input()).rstrip()
	# Método de realce escolhido
	enhancementOpt = int(input())
	# Parâmetro a ser utilizado no método 3 de realce
	param = float(input())

	# Gera as strings com os nomes das imagens de baixa resolução
	imgLowFilename = [imgLow, imgLow, imgLow, imgLow]

	for i in range(len(imgLowFilename)):
		imgLowFilename[i] += str(i+1)+'.png'

	# Abre as imagens base 
	l1 = imageio.imread(imgLowFilename[0])
	l2 = imageio.imread(imgLowFilename[1])
	l3 = imageio.imread(imgLowFilename[2])
	l4 = imageio.imread(imgLowFilename[3])

	# Chama a função de realce escolhida pelo usuário
	if enhancementOpt == 1:
		l1 = transferFunction(l1, calculateHistogram(l1))
		l2 = transferFunction(l2, calculateHistogram(l2))
		l3 = transferFunction(l3, calculateHistogram(l3))
		l4 = transferFunction(l4, calculateHistogram(l4))
	elif enhancementOpt == 2:
		histogram = uniqueHistogram(l1, l2, l3, l4)
		l1 = transferFunction(l1, histogram)
		l2 = transferFunction(l2, histogram)
		l3 = transferFunction(l3, histogram)
		l4 = transferFunction(l4, histogram)
	elif enhancementOpt == 3:
		l1 = gammaAdjustment(l1, param)
		l2 = gammaAdjustment(l2, param)
		l3 = gammaAdjustment(l3, param)
		l4 = gammaAdjustment(l4, param)

	# Gera a imagem de alta resolução
	imgHigh = generateHighImgRes(l1, l2, l3, l4)

	# Compara a imagem gerada com a imagem base fornecida
	compareImages(imgHigh, imgHighFilename+'.png')

