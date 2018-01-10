import cv2
import numpy as np
import unittest

class Recorte:

    def __init__(self):
        self.imagem = 'null'
        self.nome = 'null'
        self.cor = (255,255,255)
        self.posicao_y_inicial = 0
        self.posicao_y_final = 0
        self.posicao_x_inicial = 0
        self.posicao_x_final = 0
        self.subimagem = 'null'
    
    def inicia(self,nome,imagem,cor,retangulo):
        self.nome = nome
        self.imagem = imagem
        self.cor = cor
        self.posicao_y_inicial = retangulo[0]
        self.posicao_y_final = retangulo[1]
        self.posicao_x_inicial = retangulo[2]
        self.posicao_x_final = retangulo[3]

    def cortar(self):
        self.subimagem = self.imagem[self.posicao_y_inicial:self.posicao_y_final,self.posicao_x_inicial:self.posicao_x_final]

    def marcar(self):
        cv2.rectangle(self.imagem,(self.posicao_x_inicial,self.posicao_y_inicial), (self.posicao_x_final, self.posicao_y_final), self.cor, 1)

    def show(self):
        cv2.imshow('subimagem',self.subimagem)
        cv2.waitKey(0)
        cv2.imshow('imagem',self.imagem)
        cv2.waitKey(0)


class RecorteTest(unittest.TestCase):


    def test_cortar(self):
        recorte = Recorte()
        recorte.imagem = cv2.imread('entrada.jpg')
        recorte.posicao_x_inicial = 0
        recorte.posicao_x_final = 100
        recorte.posicao_y_inicial = 0
        recorte.posicao_y_final = 100
        recorte.cortar()
        self.assertEqual(recorte.subimagem.shape[0],100)
        cv2.imshow('teste do metodo cortar',recorte.subimagem)
        cv2.waitKey(0)

    def test_marcar(self):
        recorte = Recorte()
        recorte.imagem = cv2.imread('entrada.jpg')
        recorte.posicao_x_inicial = 0
        recorte.posicao_x_final = 100
        recorte.posicao_y_inicial = 0
        recorte.posicao_y_final = 100
        recorte.marcar()
        cv2.imshow('teste do metodo marca',recorte.imagem)
        cv2.waitKey(0)

    def test_inicia(self):
        nome = 'A'
        imagem = cv2.imread('entrada.jpg')
        cor = (255,255,0)
        retangulo = (614,774,139,190)
        recorte = Recorte()
        recorte.inicia('A',imagem,cor,retangulo)

    def test_show(self):
        nome = 'A'
        imagem = cv2.imread('entrada.jpg')
        cor = (0,255,0)
        retangulo = (139,190,614,774)
        recorte = Recorte()
        recorte.inicia(nome,imagem,cor,retangulo)
        recorte.marcar()
        recorte.cortar()
        recorte.show()

if __name__ == "__main__":
    print('Teste da classe Recorte')
    unittest.main()
