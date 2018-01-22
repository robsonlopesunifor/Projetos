import unittest
import cv2
import numpy as np
from copy import copy

class Filtro(object):

    def __init__(self):
        self.lista_de_filtros = []
        self.lista_de_imagens = []

    def iniciar(self,imagem):
        self.lista_de_imagens.append(imagem)

    def aplicar_filtros(self):
        pass

    def filtro_cor(self,r,g,b):
        imagem = copy(self.lista_de_imagens[-1])
        if r == 0:
            imagem[:,:,2] = 0    #elimina o vermelho
        if g == 0:
            imagem[:,:,1] = 0    #elimina o verde
        if b == 0:
            imagem[:,:,0] = 0    #elimina o azul
        self.lista_de_imagens.append(imagem)

    def filtro_canal(self,canal):
        imagem = copy(self.lista_de_imagens[-1])
        if canal == 'gray':
            imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        elif canal == 'hsv':
            imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
        elif canal == 'lab':
            imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2LAB)
        self.lista_de_imagens.append(imagem)
        
    def filtro_binario(self,imagem):
        self.lista_de_imagens.append(imagem)
        pass

    def show(self):
        cv2.imshow('Filtro',self.lista_de_imagens[-1])
        cv2.waitKey(0)

class FiltroTest(unittest.TestCase):

    def test_iniciar(self):
        pass

    def test_aplicar_filtros(self):
        pass

    def test_filtro_cor(self):
        print '-------test_filtro_cor-------'
        imagem = cv2.imread("entrada.jpg")
        filtro = Filtro()
        filtro.iniciar(imagem)
        filtro.filtro_cor(0,1,1)
        filtro.show()
        filtro.filtro_cor(0,0,1)
        filtro.show()

    def test_filtro_canal(self):
        print '-------test_filtro_canal-------'
        imagem = cv2.imread("entrada.jpg")
        filtro = Filtro()
        filtro.iniciar(imagem)
        filtro.filtro_canal('lab')
        filtro.show()

    def test_filtro_binario(self):
        pass

    def test_show(self):
        print '-------test_show---------'
        imagem = cv2.imread("entrada.jpg")
        filtro = Filtro()
        filtro.iniciar(imagem)
        filtro.filtro_cor(1,0,0)
        filtro.show()


if __name__ == "__main__":
    print('____Teste da classe Filtro')
    unittest.main()
