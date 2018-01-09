import numpy
import cv2
import pyautogui
import unittest

class Fotografo(object):

    def __init__(self):
        self.dicionario_de_mesas = {}
        self.laudo = None
        pass

    def inicia(self):
        pass

    def lista_de_mesas(self):
        lista_de_telas = pyautogui.getWindows()
        for chave in lista_de_telas:
            if chave.find('Bloco de notas') != -1:
                self.dicionario_de_mesas.setdefault(chave,lista_de_telas[chave])

    def organizar_mesas(self):
        janena = pyautogui.getWindow('caminho - Bloco de notas')
        print janena
        tamanho_da_tela = pyautogui.size()

        #proporcao = (tamanho_da_tela[1]/)
        
        pass

    def fotografar_mesa(self):
        pass

class FotografoTest(unittest.TestCase):

    def test_lista_de_mesas(self):
        fotogrado = Fotografo()
        fotogrado.lista_de_mesas()
        print fotogrado.dicionario_de_mesas

    def test_organizar_mesas(self):
        fotogrado = Fotografo()
        fotogrado.organizar_mesas()
        pass

    def test_fotografar_mesa(self):
        pass

if __name__ == "__main__":
    print('____Teste da classe Fotografo')
    unittest.main()

