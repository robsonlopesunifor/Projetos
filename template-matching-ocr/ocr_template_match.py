# USAGE
# python ocr_template_match.py --image images/credit_card_01.png --reference ocr_a_reference.png

# import the necessary packages
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

#construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to input image")
#ap.add_argument("-r", "--reference", required=True, help="path to reference OCR-A image")
#args = vars(ap.parse_args())

# define a dictionary that maps the first digit of a credit card
# number to the credit card type
FIRST_NUMBER = {
	"3": "American Express",
	"4": "Visa",
	"5": "MasterCard",
	"6": "Discover Card"
}

# carregar a imagem OCR-A de referência do disco, convertê-la em escala de cinza,
# e limite-o, de modo que os dígitos aparecem como * branco * em um *fundo preto
# e inverte-o, de modo que os dígitos aparecem como * branco * em um * preto *
ref = cv2.imread("ocr_a_reference.png")
cv2.imshow("Carregar o OCR-A", ref)
cv2.waitKey(0)
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
cv2.imshow("Carregar o OCR-A aplicando o filtro cinza", ref)
cv2.waitKey(0)
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Carregar o OCR-A ", ref)
cv2.waitKey(0)

# encontrar contornos na imagem OCR-A (ou seja, os contornos dos dígitos)
# classifique-os da esquerda para a direita e inicialize um dicionário para mapa
# nome de dígitos para o ROI

refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
digits = {}

# loop over the OCR-A reference contours
for (i, c) in enumerate(refCnts):
        # calcular a caixa delimitadora para o dígito, extraí-lo e redimensionar
        # para um tamanho fixo
	(x, y, w, h) = cv2.boundingRect(c)
	roi = ref[y:y + h, x:x + w]
	roi = cv2.resize(roi, (57, 88))
	
        # atualize o dicionário dos dígitos, mapeando o nome do dígito para o ROI
	digits[i] = roi

# inicialize um retangular (mais largo que o alto) e quadrado
# kernel estruturante
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# carregar a imagem de entrada, redimensioná-la e convertê-la em escala de cinza
#image = cv2.imread (args ["imagem"])
image = cv2.imread('images/credit_card_01.png')
image = imutils.resize(image, width=300)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# aplique um operador morfológico tophat (whitehat) para encontrar luz
# regiões contra um fundo escuro (ou seja, os números do cartão de crédito)
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

cv2.imshow("To-Hat pegar parte mais claras", tophat)
cv2.waitKey(0)

# calcula o gradiente de Scharr da imagem tophat, então escala
# o resto de volta ao intervalo [0, 255]
gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
cv2.imshow("Sobel eixo X", gradX)
cv2.waitKey(0)
gradX = np.absolute(gradX)
cv2.imshow("Sobel eixo X", gradX)
cv2.waitKey(0)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
cv2.imshow("Sobel eixo X", gradX)
cv2.waitKey(0)
gradX = gradX.astype("uint8")
cv2.imshow("Sobel eixo X", gradX)
cv2.waitKey(0)

# aplique uma operação de fechamento usando o kernel retangular para ajudar
# cloes lacunas entre dígitos de número de cartão de crédito e, em seguida, aplique
# Método de thresholding do
# Otsu para binarizar a imagem
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)

cv2.imshow("Sobel eixo X", gradX)
cv2.waitKey(0)

thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

cv2.imshow("Sobel eixo X", thresh)
cv2.waitKey(0)

# aplica uma segunda operação de fechamento à imagem binária, novamente
# para ajudar a reduzir lacunas entre as regiões do número do cartão de crédito
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

cv2.imshow("2 operacao de fechamento ", thresh)
cv2.waitKey(0)

# encontre contornos na imagem limiar, então inicialize o
# lista de locais de dígitos
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
locs = []

# loop sobre os contornos
for (i, c) in enumerate(cnts):
	
        # calcula a caixa delimitadora do contorno, então use o
        # coordenadas da caixa delimitadora para derivar a proporção de aspecto
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h)

	#, já que os cartões de crédito usavam fontes de tamanho fixo com 4 grupos
        # de 4 dígitos, podemos podar contornos potenciais com base no
        # proporção da tela
	if ar > 2.5 and ar < 4.0:
                # contornos podem ainda ser podados na largura mínima / máxima
                # e altura
		if (w > 40 and w < 55) and (h > 10 and h < 20):	
                        # anexa a região da caixa delimitadora do grupo de dígitos
                        # para a nossa lista de locais
			locs.append((x, y, w, h))

# classifique os locais dos dígitos da esquerda para a direita e, em seguida, inicialize o
# lista de dígitos classificados
locs = sorted(locs, key=lambda x:x[0])
output = []

# loop sobre os 4 agrupamentos de 4 dígitos
for (i, (gX, gY, gW, gH)) in enumerate(locs):
	
        # inicialize a lista de dígitos de grupo
	groupOutput = []

        # extraia o ROI do grupo de 4 dígitos da imagem em escala de cinza, 
        # então aplique thresholding para segmentar os dígitos do 
        # background do cartão de crédito 
	group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
	group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	
        # detectar os contornos de cada dígito individual no grupo,
        # então classifique os contornos dos dígitos da esquerda para a direita
	digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
	digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

	
        # loop sobre os contornos dos dígitos
	for c in digitCnts:
		
                # calcular a caixa delimitadora do dígito individual, extrair
                # o dígito, e redimensioná-lo para ter o mesmo tamanho fixo que
                # as imagens OCR-A de referência
		(x, y, w, h) = cv2.boundingRect(c)
		roi = group[y:y + h, x:x + w]
		roi = cv2.resize(roi, (57, 88))

		# initialize a list of template matching scores	
		scores = []

                # loop sobre o nome do dígito de referência e o ROI do dígito
		for (digit, digitROI) in digits.items():
                        
			# aplique uma correspondência de modelo baseada em correlação,
                        # pontuação e atualize a lista de partituras
			result = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF)
			(_, score, _, _) = cv2.minMaxLoc(result)
			scores.append(score)
			#print digit, result, score

		# a classificação para o ROI dígito será a referência
                # nome de dígitos com o * maior * score de correspondência de modelo
		groupOutput.append(str(np.argmax(scores)))
		print np.argmax(scores)

	# desenhar as classificações de dígitos ao redor do grupo
	cv2.rectangle(image, (gX - 5, gY - 5),(gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)
	cv2.putText(image, "".join(groupOutput), (gX, gY - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

	# atualize a lista de dígitos de saída
	output.extend(groupOutput)
	print groupOutput, output

# display the output credit card information to the screen
print("Credit Card Type: {}".format(FIRST_NUMBER[output[0]]))
print("Credit Card #: {}".format("".join(output)))
cv2.imshow("Image", image)
cv2.waitKey(0)
