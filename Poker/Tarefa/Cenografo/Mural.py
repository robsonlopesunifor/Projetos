import cv2
import numpy as np
import unittest
import Recorte

class Mural:
    
    def __init__(self):
        self.nome = 'Mural'
        self.imagem = 'null'
        self.largura = 0
        self.altura = 0
        self.cor = (0,0,0)
        self.caminho = ''
        self.dicionario_de_recortes = {}
        self.dicionario_das_respostas_dos_recortes = {}
        self.resultado = 'null'

    def inicia(self,nome,caminho,imagem,cor):
        self.nome = nome
        self.imagem = imagem
        self.cor = cor
        self.caminho = "".join([caminho,nome,'/'])
        print self.caminho

    def adicionar_recorte(self,nome_do_recorte,retangulo):
        novo_recorte = Recorte.Recorte()
        novo_recorte.inicia(nome_do_recorte,self.caminho,self.imagem,self.cor,retangulo)
        self.dicionario_de_recortes.setdefault(nome_do_recorte,novo_recorte)
        self.dicionario_das_respostas_dos_recortes.setdefault(nome_do_recorte,'null')

    def selecionar_recorte(self,nome_do_recorte):
        return self.dicionario_de_recortes.get(nome_do_recorte)

    def selecionar_resposta_do_recorte(self,nome_do_recorte):
        return self.dicionario_das_respostas_dos_recortes.get(nome_do_recorte)

    def remover_recorte(self,nome_do_recorte):
        self.dicionario_de_recortes.pop(nome_do_recorte)
        self.dicionario_das_respostas_dos_recortes.pop(nome_do_recorte)

    def marcar(self):
        for chave in self.dicionario_de_recortes:
            self.dicionario_de_recortes[chave].marcar()

    def cortar(self):
        for chave in self.dicionario_de_recortes:
            self.dicionario_de_recortes[chave].cortar()

    def set_imagem(self,imagem):
        self.imagem = imagem
        for chave in self.dicionario_de_recortes:
            self.dicionario_de_recortes[chave].imagem = imagem

    def set_cor(self,cor):
        self.cor = cor
        for chave in self.dicionario_de_recortes:
            self.dicionario_de_recortes[chave].cor = cor

    def comparar(self,erro):
        for chave in self.dicionario_de_recortes:
            resposta = self.dicionario_de_recortes[chave].comparar(erro)
            self.dicionario_das_respostas_dos_recortes[chave] = resposta
        print self.nome, self.dicionario_das_respostas_dos_recortes
        return self.dicionario_das_respostas_dos_recortes

    def show(self):
        self.marcar()
        cv2.imshow(self.nome,self.imagem)
        cv2.waitKey(0)


    def show_informacoes():
        pass

class MuralTest(unittest.TestCase):

    def test_inicia(self):
        mural = Mural()
        nome = 'nomedo mural'
        imagem = cv2.imread('entrada.jpg')
        cor = (0, 255, 0)
        mural.inicia(nome,'null/',imagem,cor)

    def test_adicionar_seleciona_remover_recorte(self):
        print("____test_adicionar_seleciona_remover_recorte(self)")
        mural = Mural()
        nome = 'nomedo mural'
        imagem = cv2.imread('entrada.jpg')
        cor = (0, 255, 0)
        mural.inicia(nome,'null/',imagem,cor)
        mural.adicionar_recorte('A',(0,100,0,100))
        self.assertTrue(mural.dicionario_de_recortes.get('A'))
        self.assertTrue(mural.dicionario_das_respostas_dos_recortes.get('A'))
        print("________Metodo adicionar_mural('A') >> sucesso")
        self.assertEqual(mural.selecionar_recorte('A').nome,'A')
        print("________Metodo selecionar_mural('A') >> sucesso")
        self.assertEqual(mural.selecionar_resposta_do_recorte('A'),'null')
        print("________Metodo selecionar_resposta_do_recorte('A') >> sucesso")
        mural.remover_recorte('A')
        self.assertFalse(mural.selecionar_recorte('A'))
        self.assertFalse(mural.selecionar_resposta_do_recorte('A'))
        print("________Metodo remover_mural('A') >> sucesso")

    def test_show(self):
        mural = Mural()
        nome = 'nomedo mural'
        imagem = cv2.imread('Teste/mesa_2.jpg')
        cor = (0, 255, 0)
        mural.inicia(nome,'null/',imagem,cor)
        mural.adicionar_recorte('A',(131,149,373,392))
        mural.adicionar_recorte('B',(209,227,352,371))
        mural.adicionar_recorte('C',(231,249,275,294))
        mural.adicionar_recorte('D',(209,227,115,134))
        mural.adicionar_recorte('E',(128,146,100,119))
        mural.adicionar_recorte('F',(95,113,197,216))        
        mural.show()

    def test_marcar(self):
        pass

    def test_cortar(self):
        pass

    def test_set_imagem(self):
        mural = Mural()
        nome = 'nomedo mural'
        imagem = cv2.imread('Teste/mesa_1.jpg')
        cor = (0, 255, 0)
        mural.inicia(nome,'null/',imagem,cor)
        mural.adicionar_recorte('A',(131,149,373,392))
        mural.adicionar_recorte('B',(209,227,352,371))
        mural.adicionar_recorte('C',(231,249,275,294))
        mural.adicionar_recorte('D',(209,227,115,134))
        mural.adicionar_recorte('E',(128,146,100,119))
        mural.adicionar_recorte('F',(95,113,197,216))
        mural.show()
        imagem = cv2.imread('Teste/mesa_2.jpg')
        mural.set_imagem(imagem)
        mural.show()

    def test_set_cor(self):
        print 'teste set_cor'
        mural = Mural()
        nome = 'nomedo mural'
        imagem = cv2.imread('Teste/mesa_3.jpg')
        cor = (0, 255, 0)
        mural.inicia(nome,'null/',imagem,cor)
        mural.adicionar_recorte('A',(131,149,373,392))
        mural.adicionar_recorte('B',(209,227,352,371))
        mural.adicionar_recorte('C',(231,249,275,294))
        mural.adicionar_recorte('D',(209,227,115,134))
        mural.adicionar_recorte('E',(128,146,100,119))
        mural.adicionar_recorte('F',(95,113,197,216))
        mural.show()
        imagem = cv2.imread('Teste/mesa_4.jpg')
        mural.set_cor((255,255,255))
        mural.show()
        pass

    def test_comparar(self):
        mural = Mural()
        nome = 'diler'
        imagem = cv2.imread('Teste/mesa_3.jpg')
        cor = (0, 255, 0)
        mural.inicia(nome,'Moldes/MPSC6/Bases/',imagem,cor)
        mural.adicionar_recorte('A',(131,149,373,392))
        mural.adicionar_recorte('B',(209,227,352,371))
        mural.adicionar_recorte('C',(231,249,275,294))
        mural.adicionar_recorte('D',(209,227,115,134))
        mural.adicionar_recorte('E',(128,146,100,119))
        mural.adicionar_recorte('F',(95,113,197,216))  
        mural.show()
        mural.comparar(1000)
        imagem = cv2.imread('Teste/mesa_2.jpg')
        mural.set_imagem(imagem)
        mural.show()
        mural.comparar(1000)
        imagem = cv2.imread('Teste/mesa_1.jpg')
        mural.set_imagem(imagem)
        mural.show()
        mural.comparar(1000)
        

    def test_show_informacoes(self):
        self.assertTrue(True)

if __name__ == "__main__":
    print('Teste da classe Mural')
    unittest.main()
    
