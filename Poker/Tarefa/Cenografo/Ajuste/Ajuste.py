import unittest

class Ajuste(object):

    def __init__(self):
        self.etapa = 'mural'
        pass

    def iniciar(self):
        pass

    def show(self):
        pass

    def menu(self, tecla):
        if self.etapa == 'mural':
            controle_do_mural(tecla)
        if self.etapa == 'recorte':
            controle_do_recorte(tecla)
        if self.etapa == 'mover':
            controle_do_mover(tecla)
        if self.etapa == 'dimencionar':
            controle_do_dimencionar(tecla)

    def controle_do_mural(self,tecla):
        if tecla == ord('w'):
            pass
        elif tecla == ord('s'):
            pass
        elif tecla == ord('u'):
            pass
        elif tecla == ord('j'):
            pass
        elif tecla == ord('h'):
            pass
        elif tecla == ord('k'):
            pass

    def controle_do_recorte(self,tecla):
        pass

    def controle_do_mover(self,tecla):
        pass

    def controle_do_dimencionar(self,tecla):
        pass

class AjusteTest(unittest.TestCase):

    def test_iniciar(self):
        pass

    def test_menu(self):
        pass

    def test_controle_do_mural(self):
        pass

if __name__ == "__main__":
    print('____Teste da classe Ajuste')
    unittest.main()
