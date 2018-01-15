import unittest
import pyautogui
import Fotografo
import Cenografo
import cv2
import numpy as np
from copy import copy

class Tarefa(object):

    def __init__(self):
        self.mesa = 'null'
        self.molde = 'null'
        self.imagem = 'null'
        self.molde = 'null'
        self.fotografo = Fotografo.Fotografo.Fotografo()
        self.ficheiro = Cenografo.Ficheiro.Ficheiro()

    def iniciar(self,molde,mesa):
        self.molde = molde
        self.mesa = mesa
        self.fotografo.iniciar(2)
        self.ficheiro.iniciar(self.molde,self.imagem)

    def executar(self):
        self.imagem = self.fotografo.fotografar_mesa(self.mesa)
        self.ficheiro.set_imagem(self.imagem)

    def show(self):
        self.ficheiro.marcar()
        self.ficheiro.show()

    def show_dinamico(self):

        cv2.namedWindow('image')
        while(1):
            self.executar()
            self.ficheiro.marcar()
            cv2.imshow('image',self.ficheiro.imagem)
            k = cv2.waitKey(33)
            print k
            if k == 27:
                break
        cv2.destroyAllWindows()


class TarefaTest(unittest.TestCase):

    def test_iniciar(self):
        fotografo = Fotografo.Fotografo.Fotografo()
        fotografo.registrar_lista_de_mesas()
        dicionario_de_mesas = fotografo.dicionario_de_mesas
        for chave in dicionario_de_mesas:
            print chave
            if input(' 1 / 0 : ') == 1:
                tarefa = Tarefa()
                tarefa.iniciar('MPSC6.xml',chave)
                for x in range(0,1):
                    tarefa.executar()
                    tarefa.show()

    def test_show_dinamico(self):
        fotografo = Fotografo.Fotografo.Fotografo()
        fotografo.registrar_lista_de_mesas()
        dicionario_de_mesas = fotografo.dicionario_de_mesas
        for chave in dicionario_de_mesas:
            if input(' 1 / 0 : ') == 1:
                tarefa = Tarefa()
                tarefa.iniciar('MPSC6.xml',chave)
                for x in range(0,1):
                    tarefa.show_dinamico()
        

if __name__ == "__main__":
    print('____Teste da classe Tarefa')
    unittest.main()
