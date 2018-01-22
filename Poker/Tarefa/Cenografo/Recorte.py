import cv2
import numpy as np
import unittest
import Binario
from copy import copy

class Recorte:

    def __init__(self):
        self.imagem = 'null'
        self.imagem_para_corte = 'null'
        self.nome = 'null'
        self.cor = (255,255,255)
        self.posicao_y_inicial = 0
        self.posicao_y_final = 0
        self.posicao_x_inicial = 0
        self.posicao_x_final = 0
        self.subimagem = None
        self.caminho = ''
        self.binario = Binario.Binario()
        
    
    def inicia(self,nome,caminho,imagem,cor,retangulo):
        self.nome = nome
        self.imagem = imagem
        self.cor = cor
        self.posicao_y_inicial = retangulo[0]
        self.posicao_y_final = retangulo[1]
        self.posicao_x_inicial = retangulo[2]
        self.posicao_x_final = retangulo[3]
        self.binario.caminho = "".join([caminho,nome,".png"])
        self.base_carregada = False

    def cortar(self):
        proporcao = self.imagem.shape[0] / 364.0
        x_inicial = int(self.posicao_x_inicial * proporcao)
        y_inicial = int(self.posicao_y_inicial * proporcao)
        x_final = int(self.posicao_x_final * proporcao)
        y_final = int(self.posicao_y_final * proporcao)
        self.subimagem = self.imagem[y_inicial:y_final,x_inicial:x_final]

    def marcar(self):
        proporcao = self.imagem.shape[0] / 364.0
        x_inicial = int(self.posicao_x_inicial * proporcao) - 1
        y_inicial = int(self.posicao_y_inicial * proporcao) - 1
        x_final = int(self.posicao_x_final * proporcao)
        y_final = int(self.posicao_y_final * proporcao)
        cv2.rectangle(self.imagem,(x_inicial,y_inicial), (x_final, y_final), self.cor, 1)

    def salvar_base(self):
        self.cortar()
        self.binario.imagem_topo = self.subimagem
        self.binario.salvar_base()
        self.binario.carregar_base()
        self.binario.show()

    def comparar(self,erro):
        largura = self.posicao_x_final - self.posicao_x_inicial 
        altura = self.posicao_y_final - self.posicao_y_inicial 
        self.cortar()
        self.subimagem = cv2.resize(self.subimagem,(largura, altura),interpolation = cv2.INTER_AREA)
        if self.base_carregada == False:
            self.binario.imagem_topo = self.subimagem
            self.binario.carregar_base()
            self.base_carregada = True
            return self.binario.comparar(erro)
        else:
            self.binario.imagem_topo = self.subimagem
            return self.binario.comparar(erro)
        

    def show(self):
        cv2.imshow('subimagem',self.subimagem)
        cv2.waitKey(0)
        cv2.imshow('imagem',self.imagem)
        cv2.waitKey(0)


class RecorteTest(unittest.TestCase):

    def test_cortar(self):
        print '--------------test_cortar--------------'
        recorte = Recorte()
        recorte.imagem = cv2.imread('entrada.jpg')
        recorte.posicao_x_inicial = 0
        recorte.posicao_x_final = 100
        recorte.posicao_y_inicial = 0
        recorte.posicao_y_final = 100
        recorte.cortar()
        cv2.imshow('teste do metodo cortar',recorte.subimagem)
        cv2.waitKey(0)

    def test_marcar(self):
        print '--------------test_marcar--------------'
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
        print '--------------test_inicia--------------'
        nome = 'A'
        imagem = cv2.imread('entrada.jpg')
        cor = (255,255,0)
        retangulo = (209,227,352,371)
        recorte = Recorte()
        recorte.inicia('A','null',imagem,cor,retangulo)

    def test_show(self):
        print '--------------test_show--------------'
        nome = 'A'
        imagem = cv2.imread('entrada.jpg')
        cor = (0,255,0)
        retangulo = (209,227,352,371) 
        recorte = Recorte()
        recorte.inicia(nome,'null',imagem,cor,retangulo)
        recorte.marcar()
        recorte.cortar()
        recorte.show()

    def test_comparar(self):
        print '--------------test_comparar--------------'
        nome = 'B'
        imagem = cv2.imread('entrada.jpg')
        cor = (255,255,0)
        retangulo = (209,226,352,370)
        recorte = Recorte()
        recorte.inicia(nome,'Moldes/MPSC6/Bases/teste/',imagem,cor,retangulo)
        print recorte.comparar(1000)
        recorte.show()
        
        
        

if __name__ == "__main__":
    print('Teste da classe Recorte')
    unittest.main()
