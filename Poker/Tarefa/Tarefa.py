import unittest
import pyautogui
import Fotografo
import Cenografo

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
        self.ficheiro.iniciar(self.molde,self.imagem)

    def executar(self):
        self.imagem = self.fotografo.iniciar(self.mesa,2)
        self.ficheiro.set_imagem(self.imagem)

    def show(self):
        self.ficheiro.marcar()
        self.ficheiro.show()
        pass


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
        

if __name__ == "__main__":
    print('____Teste da classe Tarefa')
    unittest.main()
