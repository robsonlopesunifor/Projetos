import unittest
import cv2
import numpy as np
from copy import copy
import Ficheiro
import sys
sys.path.insert(0, "../")
import Fotografo

class Ajuste(object):

    def __init__(self):
        self.imagem = None
        self.etapa = 'mural'
        self.pausar = False
        self.posicao_da_mesa = 1
        self.mesa = None
        self.posicao_do_mural = 1
        self.mural = None
        self.recorte = None
        self.cor = (0,0,0)
        self.posicao_do_recorte = 1
        self.ficheiro = Ficheiro.Ficheiro()
        self.fotografo = Fotografo.Fotografo.Fotografo()

    def iniciar(self,molde,divisao):
        self.fotografo.iniciar(divisao)
        self.ficheiro.iniciar(molde)
        self.definir_mesa()

    def menu(self, tecla):
        self.pausar_imagem(tecla)
        self.controle_da_mesa(tecla)
        if self.etapa == 'mural':
            self.controle_do_mural(tecla)
        elif self.etapa == 'recorte':
            self.controle_do_recorte(tecla)
        elif self.etapa == 'mover':
            self.controle_do_mover(tecla)
        elif self.etapa == 'dimencionar':
            self.controle_do_dimencionar(tecla)

    def pausar_imagem(self,tecla):
        if tecla == 112:
            if self.pausar == False:
                self.pausar = True
            else:
                self.pausar = False

    def controle_da_mesa(self,tecla):
        if tecla == 109:
            self.posicao_da_mesa += 1
            self.definir_mesa()
        elif tecla == 110:
            self.posicao_da_mesa -= 1
            if self.posicao_da_mesa <= 1:
                self.posicao_da_mesa = 1
            self.definir_mesa()

    def controle_do_mural(self,tecla):
        if tecla == 44:
            pass
        elif tecla == 46:
            self.sair_do_mural()
            self.etapa = 'recorte'
        elif tecla == 2555904:
            self.sair_do_mural()
            self.posicao_do_mural += 1
            self.entrar_no_mural()
        elif tecla == 2424832:
            self.sair_do_mural()
            self.posicao_do_mural -= 1
            if self.posicao_do_mural <= 1:
                self.posicao_do_mural = 1
            self.entrar_no_mural()

    def controle_do_recorte(self,tecla):
        if tecla == 44:
            self.entrar_no_mural()
            self.sair_do_recorte()
            self.etapa = 'mural'
            self.posicao_do_recorte = 1 
        elif tecla == 46:
            self.etapa = 'mover'
        elif tecla == 2555904:
            print 'direita'
            self.sair_do_recorte()
            self.posicao_do_recorte += 1
            if self.posicao_do_recorte >= 5:
                self.posicao_do_recorte = 5
            self.entrar_no_recorte()
        elif tecla == 2424832:
            print 'esquerda'
            self.sair_do_recorte()
            self.posicao_do_recorte -= 1
            if self.posicao_do_recorte <= 1:
                self.posicao_do_recorte = 1
            self.entrar_no_recorte()

    def controle_do_mover(self,tecla):
        if tecla == 44:
            self.sair_do_recorte()
            self.entrar_no_recorte()
            self.etapa = 'recorte'
        elif tecla == 46:
            self.etapa = 'dimencionar'
        elif tecla == 2555904:
            self.recorte.posicao_x_inicial += 1
            self.recorte.posicao_x_final += 1       
        elif tecla == 2424832:
            self.recorte.posicao_x_inicial -= 1
            self.recorte.posicao_x_final -= 1    
        elif tecla == 2490368:
            self.recorte.posicao_y_inicial -= 1
            self.recorte.posicao_y_final -= 1    
        elif tecla == 2621440:
            self.recorte.posicao_y_inicial += 1
            self.recorte.posicao_y_final += 1    
            

    def controle_do_dimencionar(self,tecla):
        if tecla == 44:
            self.etapa = 'mover'
        elif tecla == 46:
            self.etapa = 'dimencionar'
        elif tecla == 2555904:
            self.recorte.posicao_x_final += 1             
        elif tecla == 2424832:
            self.recorte.posicao_x_final -= 1
        elif tecla == 2490368:
            self.recorte.posicao_y_final -= 1
        elif tecla == 2621440:
            self.recorte.posicao_y_final += 1

    def entrar_no_mural(self):
        i = 1
        for chave in self.ficheiro.dicionario_de_murais:
            if i == self.posicao_do_mural:
                print chave
                self.mural = self.ficheiro.dicionario_de_murais[chave]
                self.cor = self.mural.cor
                self.mural.set_cor((255,255,255))
            i += 1

    def sair_do_mural(self):
        if self.mural != None:
            self.mural.set_cor(self.cor)

    def entrar_no_recorte(self):
        i = 1
        for chave in self.mural.dicionario_de_recortes:
            if i == self.posicao_do_recorte:
                print chave
                self.recorte = self.mural.dicionario_de_recortes[chave]
                self.cor = self.recorte.cor
                self.recorte.cor = (255,255,255)
            i += 1   

    def sair_do_recorte(self):
        if self.recorte != None:
            self.recorte.cor = self.cor

    def definir_mesa(self):
        i = 1
        for chave in self.fotografo.dicionario_de_mesas:
            if i == self.posicao_da_mesa:
                self.mesa = chave       
            i += 1


    def show(self):

        cv2.namedWindow('image')
        while(1):
            if self.pausar == False:
                self.imagem = self.fotografo.fotografar_mesa(self.mesa)
            img = copy(self.imagem)
            self.ficheiro.set_imagem(img)
            self.ficheiro.marcar()
            cv2.imshow('image',img)
            key = cv2.waitKey(33)
            self.menu(key)
            if key == 27:
                break
        cv2.destroyAllWindows()

class AjusteTest(unittest.TestCase):

    def test_iniciar(self):
        pass

    def test_menu(self):
        pass

    def test_controle_do_mural(self):
        pass

    def test_show(self):
        ajuste = Ajuste()
        ajuste.iniciar('MPSC6.xml',2)
        ajuste.show()

if __name__ == "__main__":
    print('____Teste da classe Ajuste')
    unittest.main()
