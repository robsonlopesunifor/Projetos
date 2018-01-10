import numpy
import cv2
import pyautogui
import unittest
import sys

class Fotografo(object):

    def __init__(self):
        self.dicionario_de_mesas = {}
        self.imagem = 'null'
        self.laudo = None
        pass

    def inicia(self):
        pass

    def registrar_lista_de_mesas(self):
        dicionario_de_telas = pyautogui.getWindows()
        for chave in dicionario_de_telas:
            if chave.find("No Limit Hold'em") != -1:
                self.dicionario_de_mesas.setdefault(chave,None)

    def organizar_mesas(self,divisoes):
        tamanho_da_tela = pyautogui.size()
        altura = int(tamanho_da_tela[1]/divisoes)
        largura = int(altura * (1.3714))
        i = 0
        for chave in self.dicionario_de_mesas:
            janela = pyautogui.getWindow(chave)
            posicao_x = (largura - 25)* int( i / divisoes) - 10
            posicao_y = (altura - 10)* int( i % divisoes)
            dupla = (posicao_x,posicao_y,largura,altura)
            self.dicionario_de_mesas[chave] = dupla
            print self.dicionario_de_mesas.get(chave)
            janela.resize( largura, altura)
            janela.move(posicao_x,posicao_y)
            i += 1
        
    def fotografar_mesa(self,titulo):
        dupla = self.dicionario_de_mesas.get(titulo)
        print dupla
        PILImage = pyautogui.screenshot(region = dupla)
        self.imagem = cv2.cvtColor(numpy.array(PILImage), cv2.COLOR_RGB2BGR)

    def show(self):
        if self.imagem != 'null':
            cv2.imshow('Show',self.imagem)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

class FotografoTest(unittest.TestCase):

    def test_lista_de_mesas(self):
        fotogrado = Fotografo()
        fotogrado.registrar_lista_de_mesas()
        print fotogrado.dicionario_de_mesas

    def test_organizar_mesas(self):
        fotogrado = Fotografo()
        fotogrado.registrar_lista_de_mesas()
        fotogrado.organizar_mesas(2)

    def test_fotografar_mesa(self):
        fotogrado = Fotografo()
        fotogrado.registrar_lista_de_mesas()
        fotogrado.organizar_mesas(2)
        for chave in fotogrado.dicionario_de_mesas:
            print chave, fotogrado.dicionario_de_mesas[chave]
            fotogrado.fotografar_mesa(chave)

    def test_show(self):
        fotogrado = Fotografo()
        fotogrado.registrar_lista_de_mesas()
        fotogrado.organizar_mesas(2)
        for chave in fotogrado.dicionario_de_mesas:
            print chave, fotogrado.dicionario_de_mesas[chave]
            if input('1 / 0 : ') == 1:
                fotogrado.fotografar_mesa(chave)
                fotogrado.show()
        

if __name__ == "__main__":
    print('____Teste da classe Fotografo')
    unittest.main()

