import unittest
import cv2
import pyautogui
import numpy as np
import Recorte
from PIL import Image
from matplotlib import pyplot as plt
import sys
sys.path.insert(0,"../")
import Fotografo

class Binario(object):

    def __init__(self):
        self.imagem_base = None
        self.imagem_topo = None
        self.caminho = None

    def iniciar(self):
        pass
    
    def carregar_base(self):
        self.imagem_base = cv2.imread(self.caminho)
        if self.imagem_base is None and self.imagem_topo is not None:
            self.salvar_base()
            self.imagem_base = cv2.imread(self.caminho)

    def salvar_base(self):
        imagem = cv2.cvtColor(self.imagem_topo, cv2.COLOR_RGB2BGR) 
        Image.fromarray(imagem).save(self.caminho)
        
    def comparar(self,tolerancia):
        imageA = cv2.cvtColor(self.imagem_base, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(self.imagem_topo, cv2.COLOR_BGR2GRAY)
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        #print err
        if err < tolerancia:
            return True
        else:
            return False 

    def show(self):
        imageA = cv2.cvtColor(self.imagem_base, cv2.COLOR_BGR2GRAY)
        plt.subplot(1,2,1),plt.imshow(imageA,cmap = 'gray')
        plt.title('Imagem base'), plt.xticks([]), plt.yticks([])
        imageB = cv2.cvtColor(self.imagem_topo, cv2.COLOR_BGR2GRAY)
        plt.subplot(1,2,2),plt.imshow(imageB,cmap = 'gray')
        plt.title('Imagem topo'), plt.xticks([]), plt.yticks([])
        plt.show()


class SemaforoTest(unittest.TestCase):

    def test_carregar_base(self):
        print '-------test_carregar_base--------'
        binario = Binario()
        binario.caminho = "Moldes/MPSC6/Bases/teste/teste.png"
        binario.carregar_base()
        binario.caminho = "Moldes/MPSC6/Bases/teste/testee.png"
        binario.carregar_base()
        binario.caminho = "Moldes/MPSC6/Bases/teste/testee.png"
        binario.imagem_topo = cv2.imread("teste.png")
        binario.carregar_base()

    def test_salvar_base(self):
        print '-------test_salvar_base--------'
        fotografo = Fotografo.Fotografo.Fotografo()
        fotografo.iniciar(2)
        for chave in fotografo.dicionario_de_mesas:
            print chave, fotografo.dicionario_de_mesas[chave]
            fotografo.fotografar_mesa(chave)
            fotografo.show()
            break
        recorte = Recorte.Recorte()
        recorte.inicia('A','null',fotografo.imagem,(255,255,255),(100,300,100,300))
        recorte.cortar()
        recorte.show()
        binario = Binario()
        binario.imagem_topo = recorte.subimagem
        binario.caminho = "Moldes/MPSC6/Bases/teste/teste.png"
        binario.salvar_base()
        binario.carregar_base()
        binario.imagem_topo = recorte.subimagem
        binario.show()
        print binario.comparar(1000)
        

    def test_comparar(self):
        print '-------test_comparar--------'
        binario = Binario()
        binario.imagem_base = cv2.imread("vez_topo.jpg")
        binario.imagem_topo = cv2.imread("vez_topo.jpg")
        print binario.comparar(100)
        binario.imagem_base = cv2.imread("vez_base.jpg")
        binario.imagem_topo = cv2.imread("vez_topo.jpg")
        print binario.comparar(1000)

    def test_show(self):
        pass

if __name__ == "__main__":
    print('____Teste da classe binario')
    unittest.main()
