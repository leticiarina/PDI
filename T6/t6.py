# Nome: Letícia Rina Sakurai
# NUSP: 9278010
# SCC0251 - Processamento de Imagens
# 1º Semestre/2018
# Trabalho 6 - Restauração de Imagens

import numpy as np
import imageio
import math

# Restauração de imagens utilizando filtro adaptativo de redução de ruído local
def localNoise(inoisy, noisyDistr, N):

	# Matriz para armazenar a imagem dé saída
	iout = np.zeros(inoisy.shape) 

	# Quantidade de elementos em cada borda
	borders = int(N/2)

	# Criação da matriz circular
	inoisyWrapped = wrappedImg(inoisy, N, borders)

	# Variância do ruído da imagem
	noisyVar = math.pow(noisyDistr, 2)

	for i in range(borders, borders+inoisy.shape[0]):
		for j in range(borders, borders+inoisy.shape[1]):
			# Geração do filtro
			imgFilter = generateFilter (inoisyWrapped, i, j, N)
			# Cálculo da variância do filtro
			filterVar = np.var(imgFilter)
			# Média do filtro
			pixelsMean = np.mean(imgFilter)
			# Cálculo do pixel de saída
			iout[i-borders,j-borders] = inoisyWrapped[i,j]-((noisyVar/filterVar)*(inoisyWrapped[i,j]-pixelsMean))
	
	return iout

# Cria uma imagem em uma matriz circular.
def wrappedImg(img, N, borders):

	imgWrapped = np.zeros((img.shape[0]+N-1, img.shape[1]+N-1))
	
	for i in range(borders, borders+img.shape[0]):

		# Atribui a borda esquerda no meio da matriz
		for j in range(borders):
			imgWrapped[i,j] = img[i-borders, j-borders] 

		x = 0 # Itera sobre as colunas
	
		# Atribui a borda direita no meio da matriz
		for j in range(borders+img.shape[1], imgWrapped.shape[1]):
			imgWrapped[i,j] = img[i-borders, x] 
			x = x+1

	# Atribui a borda superior
	for i in range(borders):
		imgWrapped[i, :] = imgWrapped[i-borders, :]

	x = 0 # Itera sobre as linhas

	# Atribui a borda inferior
	for i in range(borders+img.shape[0], imgWrapped.shape[0]):
		imgWrapped[i, :] = imgWrapped[x, :]
		x = x+1

	# Atribui a imagem original em parte da matriz
	imgWrapped[borders:img.shape[0]+borders, borders:img.shape[1]+borders] = img
	
	return imgWrapped

# Utilizada principalmente com ruídos impulsivos, o processamento utiliza um filtro adaptativo de mediana
def median(inoisy, M, N):

	# Matriz para armazenar a imagem de saída
	iout = np.zeros(inoisy.shape) 

	for i in range(inoisy.shape[0]):
		for j in range(inoisy.shape[1]):
			# Etapa A
			iout[i, j] = medianStepA(inoisy, i, j, N, M)

	return iout

def medianStepA(inoisy, i, j, N, M):

	# Quantidade de elementos em cada borda
	borders = int(N/2)

	# Criação da matriz circular
	inoisyBorders = np.pad(inoisy, borders, mode='edge')

	# Geração do filtro
	imgFilter = generateFilter(inoisyBorders, i+borders, j+borders, N)

	# Ponto mínimo do filtro
	zmin = np.min(imgFilter)
	# Ponto máximo do filtro
	zmax = np.max(imgFilter)
	# Mediana do filtro
	zmed = np.median(imgFilter)

	# Calcula diferença entre a mediana e o ponto mínimo
	a1 = zmed-zmin
	# Calcula diferença entre a mediana e o ponto máximo
	a2 = zmed-zmax

	# Direciona para a etapa B se verificadas as condições
	if a1 > 0 and a2 < 0:
		
		# Etapa B
		# Diferença entre o pixel atual e o mínimo do filtro
		b1 = inoisy[i,j]-zmin
		# Diferença entre a mediana e o máximo do filtro
		b2 = zmed-zmax

		# Se verificadas as condições, retorna o pixel original
		if b1>0 and b2<0: return inoisy[i,j]
		# Caso contrário, retorna a mediana do filtro
		else: return zmed
	else:
		# Aumenta o tamanho do filtro
		N = N+1

		# Realiza mais uma passo se o tamanho máximo do filtro não foi atingido
		if(N<=M): return medianStepA(inoisy, i, j, N, M)
		# Caso contrário, retorna a mediana do filtro
		else: return zmed

# Remoção de ruídos impulsivos brancos (Q<0) ou pretos (Q>0)
def contraHarmonic(inoisy, N, Q):

	# Quantidade de pixels nos cantos
	borders = int(N/2)

	# Cria nova imagem com zero nas bordas
	inoisyMargin = np.pad(inoisy, borders, mode='constant', constant_values=(0))

	# Imagem final
	iout = np.zeros(inoisy.shape)

	# Itera sobre todos os pixels
	for i in range(inoisy.shape[0]):
		for j in range(inoisy.shape[1]):

			# Determina o filtro de acordo com o pixel atual
			g = generateFilter(inoisyMargin, i+borders, j+borders, N)

			# Aplica a equação do filtro da média contra-harmônica
			iout[i, j] = np.divide(np.sum(np.power(g[g!=0], Q+1)), np.sum(np.power(g[g!=0], Q)))

	return iout

# Gera um filtro baseado no pixel atual e sua vizinhaça.
def generateFilter(img, i, j, size):

	# Determina o corte da imagem original
	iMin = i-int(size/2)
	jMin = j-int(size/2)
	iMax = i+int(size/2)
	jMax = j+int(size/2)

	return img[iMin:iMax+1, jMin:jMax+1]

# Realiza o cálculo da raiz do erro médio quadrático para comparar a imagem
# original com a imagem restaurada
def getRmse(img1, img2):

	# Converte a imagem original e a imagem restaurada para uint8
	img1 = img1.astype(np.uint8)
	img2 = img2.astype(np.uint8)

	# Somatório do cálculo do RMSE
	rmse = np.sum(np.power(img1-img2, 2))

	# Multiplicação pelo inverso das dimensões e radiciação
	rmse = math.sqrt((1/(img1.shape[0]*img1.shape[1]*img2.shape[0]*img2.shape[1]))*rmse)
	
	# Impressão do resultado
	print('%.4f' %rmse)

if __name__ == "__main__":
	
	# Nome da imagem original
	icompFilename = str(input()).rstrip()
	# Nome da imagem ruidosa
	inoisyFilename = str(input()).rstrip()
	# Escolha do método 
	method = int(input())
	# Tamanho do filtro
	N = int(input())
	# Abertura da imagem ruidosa
	inoisy = imageio.imread(inoisyFilename)

	# Parâmetro e chamada específica de acordo com o método
	if method == 1:
		noisyDistr = float(input()) # Distribuição de ruído
		iout = localNoise(inoisy, noisyDistr, N)
	elif method == 2:
		M = int(input()) # Tamanho máximo do filtro
		iout = median(inoisy, M, N) 
	elif method == 3:
		Q = float(input()) # Ordem do filtro
		iout = contraHarmonic(inoisy, N, Q)

	# Abertura da imagem original
	icomp = imageio.imread(icompFilename)

	# Cálculo do RMSE entre a imagem original e a imagem restaurada
	getRmse(icomp, iout)

