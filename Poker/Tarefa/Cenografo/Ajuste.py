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
        self.etapa = 'inicil'
        self.pausar = False
        self.posicao_da_mesa = 1
        self.mesa = None
        self.posicao_do_mural = 1
        self.mural = None
        self.recorte = None
        self.cor = (0,0,0)
        self.posicao_do_recorte = 1
        self.abilitar_marcar = True
        self.ficheiro = Ficheiro.Ficheiro()
        self.fotografo = Fotografo.Fotografo.Fotografo()

    def iniciar(self,molde,divisao):
        self.fotografo.iniciar(divisao)
        self.ficheiro.iniciar(molde)
        self.definir_mesa()

    def menu(self, tecla):
        self.pausar_imagem(tecla)
        self.controle_da_mesa(tecla)
        if self.etapa == 'inicil':
            self.controle_do_inicil(tecla)
        elif self.etapa == 'mural':
            self.controle_do_mural(tecla)
        elif self.etapa == 'recorte':
            self.controle_do_recorte(tecla)
        elif self.etapa == 'mover':
            self.controle_do_mover(tecla)
        elif self.etapa == 'dimencionar':
            self.controle_do_dimencionar(tecla)
        elif self.etapa == 'base':
            self.controle_da_base(tecla)

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

    def controle_do_inicil(self,tecla):
        if tecla == 44:
            pass
        elif tecla == 46:
            self.etapa = 'mural'
            self.entrar_no_mural()
            self.info(self.etapa)

    def controle_do_mural(self,tecla):
        if tecla == 44:
            self.etapa = 'inicil'
        elif tecla == 46:
            self.sair_do_mural()
            self.etapa = 'recorte'
            self.entrar_no_recorte()
            self.info(self.etapa)
        elif tecla == 2555904:
            self.sair_do_mural()
            self.posicao_do_mural += 1
            tamanho = len(self.ficheiro.dicionario_de_murais)
            if self.posicao_do_mural >= tamanho:
                self.posicao_do_mural = tamanho
            self.entrar_no_recorte()
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
            self.info(self.etapa)
            self.posicao_do_recorte = 1 
        elif tecla == 46:
            self.etapa = 'mover'
            self.info(self.etapa)
        elif tecla == 2555904:
            self.sair_do_recorte()
            self.posicao_do_recorte += 1
            tamanho = len(self.mural.dicionario_de_recortes)
            if self.posicao_do_recorte >= tamanho:
                self.posicao_do_recorte = tamanho
            self.entrar_no_recorte()
        elif tecla == 2424832:
            self.sair_do_recorte()
            self.posicao_do_recorte -= 1
            if self.posicao_do_recorte <= 1:
                self.posicao_do_recorte = 1
            self.entrar_no_recorte()

    def controle_do_mover(self,tecla):
        self.recorte.marcar()
        if tecla == 44:
            self.sair_do_recorte()
            self.entrar_no_recorte()
            self.etapa = 'recorte'
            self.info(self.etapa)
        elif tecla == 46:
            self.etapa = 'dimencionar'
            self.info(self.etapa)
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
        self.recorte.marcar()
        if tecla == 44:
            self.etapa = 'mover'
            self.info(self.etapa)
        elif tecla == 46:
            self.etapa = 'base'
            self.info(self.etapa)
        elif tecla == 2555904:
            self.recorte.posicao_x_final += 1
        elif tecla == 2424832:
            self.recorte.posicao_x_final -= 1
        elif tecla == 2490368:
            self.recorte.posicao_y_final -= 1
        elif tecla == 2621440:
            self.recorte.posicao_y_final += 1

    def controle_da_base(self,tecla):
        if tecla == 44:
            self.etapa = 'dimencionar'
            self.info(self.etapa)
        elif tecla == 46:
            self.etapa = 'base'
            self.info(self.etapa)
        elif tecla == 98:
            self.recorte.salvar_base()
        elif tecla == 118:
            self.recorte.comparar(1000)

    def info(self,etapa):

        if etapa == 'mural':
            print '------------mural------------'
            print '<'
            print '>'
            print 'Esquerda:    Mudar de Mural'
            print 'Direita:     Mudar de Mural'
            print '-----------------------------'
        elif etapa == 'recorte':
            print '------------recorte------------'
            print '<'
            print '>'
            print 'Esquerda:    Mudar de recorte'
            print 'Direita:     Mudar de recorte'
            print '-----------------------------'
        if etapa == 'mover':
            print '------------Mover------------'
            print '<'
            print '>'
            print 'Cima:        Mover Para Cima'
            print 'Baixo:       Mover Para Baixo'
            print 'Esquerda:    Mover Para Esquerda'
            print 'Direita:     Mover para direita'
            print '-----------------------------'
        elif etapa == 'dimencionar':
            print '------------dimencionar------------'
            print '<'
            print '>'
            print 'Cima:        Diminuir a Altura'
            print 'Baixo:       Aumentar a Altura'
            print 'Esquerda:    Diminuir a Largura'
            print 'Direita:     Aumentar a Largura'
            print '-----------------------------'
        elif etapa == 'base':
            print '------------base------------'
            print '<'
            print '>'
            print 'C:           Apagar macacao'
            print 'B:           Salvar a Base'
            print 'V:           Coparar imagem'
            print '-----------------------------'

    def entrar_no_mural(self):
        i = 1
        for chave in self.ficheiro.dicionario_de_murais:
            if i == self.posicao_do_mural:
                print chave
                self.mural = self.ficheiro.dicionario_de_murais[chave]
                self.cor = self.mural.cor
                self.mural.set_cor((255,255,255))
                self.mural.marcar()
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
                self.recorte.marcar()
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

    def marcar(self):
            if self.etapa == 'inicil':
                self.ficheiro.marcar()
            elif self.etapa == 'mural':
                self.mural.marcar()
            elif self.etapa == 'recorte':
                self.recorte.marcar()
            elif self.etapa == 'mover':
                self.recorte.marcar()
            elif self.etapa == 'dimencionar':
                self.recorte.marcar()
            elif self.etapa == 'base':
                self.recorte.marcar()
            

    def show(self):

        cv2.namedWindow('Ajuste')
        while(1):
            if self.pausar == False:
                self.imagem = self.fotografo.fotografar_mesa(self.mesa)
            img = copy(self.imagem)
            self.ficheiro.set_imagem(img)
            self.marcar()
            cv2.imshow('Ajuste',img)
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
        ajuste.iniciar('Moldes/MPSC6',1)
        ajuste.show()

if __name__ == "__main__":
    print('____Teste da classe Ajuste')
    unittest.main()
