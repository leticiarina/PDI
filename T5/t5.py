# Nome: Letícia Rina Sakurai
# NUSP: 9278010
# SCC0251 - Processamento de Imagens
# 1º Semestre/2018
# Trabalho 5 - Inpainting usando FFTs

import numpy as np 
import imageio
import math

# Geração de uma imagem restaurada utilizando o algoritmo de Gerchberg-Papoulis
def gerchbergPapoulis(imgi, imgm, t):

	# Primeira imagem a ser restaurada 
	imgr = imgi

	# Transformada de Fourier da máscara
	M = np.fft.fft2(imgm)

	# Magnitude máxima da máscara M
	magM = np.max(M)

	# Gera T iterações
	for x in range(t):

		# Transformada de Fourier da imagem
		Gk = np.fft.fft2(imgr)

		# Magnitude máxima da imagem
		magGk = np.max(Gk)

		# Filtragem de Gk
		for i, j in np.ndindex(Gk.shape):
			if Gk[i,j]>= 0.9*magM and Gk[i,j]<=0.01*magGk:
				Gk[i,j] = 0

		# Transformada inversa da imagem
		imgr = np.fft.ifft2(Gk)

		# Convolução
		imgr = convolution(imgr)

		# Normalização
		imgr = np.real(imgr) # Extração da parte real
		imgMax = np.max(imgr) # Valor máximo da imagem
		imgMin = np.min(imgr) # Valor mínimo da imagem
		imgr = ((imgr - imgMin)/(imgMax-imgMin))*255 # Garantia do intervalo [0,255]

		# Insere os pixels conhecidos na imagem
		imgr = ((1-(imgm/255))*imgi)+((imgm/255)*imgr)

	return imgr

# Realiza a convolução na imagem 
def convolution(i):

	# Cria o filtro 7x7 com elementos 1/49 e o restante sendo zero
	ftr = np.zeros(i.shape, dtype='complex64')
	ftr[0:7, 0:7] = np.full((7,7),(1/49.0))

	# Aplicação da transformada de Fourier no filtro e na imagem
	fourierFilter = np.fft.fft2(ftr)
	fourierImg = np.fft.fft2(i)

	# Multiplica os vetores e aplica a transformada inversa de Fourier
	return np.fft.ifft2(fourierFilter*fourierImg)

# Realiza o cálculo da raiz do erro médio quadrático para comparar a imagem
# original com a imagem restaurada
def getRmse(imgo, imgr):

	# Converte a imagem original e a imagem restaurada para uint8
	imgo = imgo.astype(np.uint8)
	imgr = imgr.astype(np.uint8)

	# Somatório do cálculo do RMSE
	rmse = np.sum(np.power(imgo-imgr, 2))

	# Multiplicação pelo inverso das dimensões e radiciação
	rmse = math.sqrt((1/(imgo.shape[0]*imgo.shape[1]))*rmse)
	
	# Impressão do resultado
	print('%.5f' %rmse)

if __name__ == "__main__":

	# Nome do arquivo da imagem original
	imgoF = str(input()).rstrip()
	# Nome do arquivo da imagem deteriorada
	imgiF = str(input()).rstrip()
	# Nome do arquivo com a máscara
	imgmF = str(input()).rstrip()
	# Número de iterações
	t = int(input())

	# Abertura dos arquivos
	imgo = imageio.imread(imgoF)
	imgi = imageio.imread(imgiF)
	imgm = imageio.imread(imgmF)

	# Gera a imagem restaurada
	imgr = gerchbergPapoulis(imgi, imgm, t)

	# Cálculo do RMSE entre a imagem original e a imagem restaurada
	getRmse(imgo, imgr)