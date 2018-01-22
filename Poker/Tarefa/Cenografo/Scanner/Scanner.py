import unittest
import cv2
import numpy as np
from matplotlib import pyplot as plt

class Scanner(object):

    def __init__(self):
        self.imagem_base = None
        self.imagem_topo = None
        self.imagem_diferenca = None
        self.histograma_base = None
        self.histograma_topo = None
        self.histograma_diferenca = None
        

    def iniciar(self):
        self.imagem_base = cv2.imread("diler_base.jpg")
        self.imagem_base = cv2.cvtColor(self.imagem_base, cv2.COLOR_RGB2BGR)
        self.imagem_topo = cv2.imread("diler_topo.jpg")
        self.imagem_topo = cv2.cvtColor(self.imagem_topo, cv2.COLOR_RGB2BGR)
        self.imagem_diferenca = self.imagem_topo - self.imagem_base

    def gera_histograma(self):
        self.histograma_base = cv2.calcHist([self.imagem_base], [0], None, [256], [0, 256])
        self.histograma_topo = cv2.calcHist([self.imagem_topo], [0], None, [256], [0, 256])
        self.histograma_diferenca = cv2.calcHist([self.imagem_diferenca], [0], None, [256], [0, 256])

    def show(self):
        plt.subplot(2,3,1),plt.imshow(self.imagem_base,cmap = 'gray')
        plt.title('Imagem base'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,3,2),plt.imshow(self.imagem_topo,cmap = 'gray')
        plt.title('Imagem topo'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,3,3),plt.imshow(self.imagem_diferenca,cmap = 'gray')
        plt.title('Imagem diferenca'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,3,4),plt.plot(self.histograma_base),
        plt.title('Hist base'), plt.xlim([0,256]),plt.ylim([0,100])
        plt.subplot(2,3,5),plt.plot(self.histograma_topo)
        plt.title('Hist topo'), plt.xlim([0,256]),plt.ylim([0,100])
        plt.subplot(2,3,6),plt.plot(self.histograma_diferenca)
        plt.title('Hist diferenca'), plt.xlim([0,256]),plt.ylim([0,100])
        plt.show()


class ScannerTest(unittest.TestCase):

    def test_iniciar(self):
        scanner = Scanner()
        scanner.iniciar()
        scanner.gera_histograma()
        scanner.show()
        print scanner.histograma_diferenca



if __name__ == "__main__":
    print('____Teste da classe Scanner')
    unittest.main()
    
