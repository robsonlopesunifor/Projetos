import numpy
import cv2
import pyautogui
import unittest
import sys

class Fotografo(object):

    def __init__(self):
        self.dicionario_de_mesas = {}
        self.imagem = 'null'

    def iniciar(self,divisoes):
        self.registrar_lista_de_mesas()
        self.organizar_mesas(2)

    def registrar_lista_de_mesas(self):
        dicionario_de_telas = pyautogui.getWindows()
        for chave in dicionario_de_telas:
            if chave.find("No Limit Hold'em") != -1:
                self.dicionario_de_mesas.setdefault(chave,None)

    def organizar_mesas(self,divisoes):
        tamanho_da_tela = pyautogui.size()
        altura = int((tamanho_da_tela[1] - 20)/divisoes)
        largura = int(altura * (1.35))
        i = 0
        for chave in self.dicionario_de_mesas:
            janela = pyautogui.getWindow(chave)
            posicao_x = (largura - 20)* int( i / divisoes) - 10
            posicao_y = (altura - 10)* int( i % divisoes)
            dupla = (posicao_x + 10,posicao_y,largura - 20,altura - 10)
            self.dicionario_de_mesas[chave] = dupla
            janela.resize( largura, altura)
            janela.move(posicao_x,posicao_y)
            i += 1
        
    def fotografar_mesa(self,janela):
        dupla = self.dicionario_de_mesas.get(janela)
        PILImage = pyautogui.screenshot(region = dupla)
        self.imagem = cv2.cvtColor(numpy.array(PILImage), cv2.COLOR_RGB2BGR)
        return  self.imagem
        

    def show(self):
        if self.imagem != 'null':
            cv2.imshow('Show',self.imagem)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

class FotografoTest(unittest.TestCase):

    def test_lista_de_mesas(self):
        print '------------test_lista_de_mesas---------------'
        fotografo = Fotografo()
        fotografo.registrar_lista_de_mesas()
        print fotografo.dicionario_de_mesas

    def test_organizar_mesas(self):
        print '------------test_organizar_mesas---------------'
        fotografo = Fotografo()
        fotografo.registrar_lista_de_mesas()
        fotografo.organizar_mesas(2)

    def test_fotografar_mesa(self):
        print '------------test_fotografar_mesa---------------'
        fotografo = Fotografo()
        fotografo.registrar_lista_de_mesas()
        fotografo.organizar_mesas(2)
        for chave in fotografo.dicionario_de_mesas:
            print chave, fotografo.dicionario_de_mesas[chave]
            fotografo.fotografar_mesa(chave)

    def test_show(self):
        print '------------test_show---------------'
        fotografo = Fotografo()
        fotografo.registrar_lista_de_mesas()
        fotografo.organizar_mesas(2)
        for chave in fotografo.dicionario_de_mesas:
            print chave, fotografo.dicionario_de_mesas[chave]
            if input('1 / 0 : ') == 1:
                fotografo.fotografar_mesa(chave)
                fotografo.show()

    def test_iniciar(self):
        print '------------test_iniciar---------------'
        fotografo = Fotografo()
        fotografo.registrar_lista_de_mesas()
        for chave in fotografo.dicionario_de_mesas:
            print chave
            if input('1 / 0 : ') == 1:
                fotografo.iniciar(2)
                fotografo.fotografar_mesa(chave)
                fotografo.show()
        
        
        

if __name__ == "__main__":
    print('____Teste da classe Fotografo')
    unittest.main()

