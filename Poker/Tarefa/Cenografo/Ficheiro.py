# -*- coding: cp1252 -*-
# Ficheiro e uma estrutura de dados logo seus atributos são publicos e suas funçoes são privadas 
import cv2
import numpy as np
import unittest
from lxml import etree
import Mural
import pyautogui

class Ficheiro(object):
    
    def __init__(self):
        self.molde_xml = 'null'
        self.imagem = 'null'
        self.nome = 'Ficheiro'
        self.largura = 0
        self.altura = 0
        self.site = 'null'
        self.estilo = 'null'
        self.jogo = 'null'
        self.valor = 'null'
        self.cadeiras = 'null'
        self.dicionario_de_murais = {}
        self.dicionario_das_respostas_dos_murais = {}

    def iniciar(self,molde_xml):
        self.molde_xml = molde_xml
        self.ler_molde(self.molde_xml)

    def adicionar_mural(self,nome_do_mural,cor):
        novo_mural = Mural.Mural()
        novo_mural.inicia(nome_do_mural,self.imagem,cor)
        self.dicionario_de_murais.setdefault(nome_do_mural,novo_mural)
        self.dicionario_das_respostas_dos_murais.setdefault(nome_do_mural,'null')

    def selecionar_mural(self,nome_do_mural):
        return self.dicionario_de_murais.get(nome_do_mural)

    def selecionar_resposta_do_mural(self,nome_do_mural):
        return self.dicionario_das_respostas_dos_murais.get(nome_do_mural)

    def remover_mural(self,nome_do_mural):
        self.dicionario_de_murais.pop(nome_do_mural)
        self.dicionario_das_respostas_dos_murais.pop(nome_do_mural)

    def salvar_molde(self,arquivo_xml):
        ficheiro = etree.parse(arquivo_xml)
        raiz = ficheiro.getroot()

        print raiz.find("".join(["mural[@nome='",'diler',"']"])).attrib

        raiz.attrib['nome'] = self.nome
        raiz.attrib['largura'] = str(2000)
        raiz.attrib['altura'] = str(3000)
        raiz.attrib['site'] = self.site
        raiz.attrib['jogo'] = self.jogo
        raiz.attrib['valor'] = str(self.valor)
        raiz.attrib['cadeiras'] = str(self.cadeiras)

        m = -1
        for  chave_m in self.dicionario_de_murais:
            m += 1
            r = 0
            mural = self.dicionario_de_murais[chave_m]
            atualizarMural = raiz.find("".join(["mural[@nome='",mural.nome,"']"]))
            if atualizarMural == None:
                novoMural = etree.SubElement(raiz, 'mural', nome = mural.nome)
                novoMural.set('cor_r', str(recorte.posicao_y_inicial))
                novoMural.set('cor_g', str(recorte.posicao_y_final))
                novoMural.set('cor_b', str(recorte.posicao_x_inicial))
                atualizarMural = novoMural
            else:
                atualizarMural.attrib['cor_r'] = str(mural.cor[0])
                atualizarMural.attrib['cor_g'] = str(mural.cor[1])
                atualizarMural.attrib['cor_b'] = str(mural.cor[2])
                
            for  chave_r in mural.dicionario_de_recortes:
                r += 1
                recorte = mural.dicionario_de_recortes[chave_r]
                atualizarRecorte = atualizarMural.find("".join(["recorte[@nome='",recorte.nome,"']"]))
                if atualizarRecorte == None:
                    novoElemento = etree.SubElement(atualizarMural, 'recorte', nome = recorte.nome)
                    novoElemento.set('posicao_y_inicial', str(recorte.posicao_y_inicial))
                    novoElemento.set('posicao_y_final', str(recorte.posicao_y_final))
                    novoElemento.set('posicao_x_inicial', str(recorte.posicao_x_inicial))
                    novoElemento.set('posicao_x_final', str(recorte.posicao_x_final))
                else:
                    atualizarRecorte.attrib['posicao_y_inicial'] = str(recorte.posicao_y_inicial)
                    atualizarRecorte.attrib['posicao_y_final'] = str(recorte.posicao_y_final)
                    atualizarRecorte.attrib['posicao_x_inicial'] = str(recorte.posicao_x_inicial)
                    atualizarRecorte.attrib['posicao_x_final'] = str(recorte.posicao_x_final)

            for x in range(len(self.dicionario_de_murais),len(raiz)):
                print x
                
        
        outFile = open(arquivo_xml,'w')
        ficheiro.write(outFile)

    def ler_molde(self,arquivo_xml):
        doc = etree.parse(arquivo_xml)
        ficheiro = doc.getroot()

        self.nome = ficheiro.attrib.get('nome')
        self.largura = int(ficheiro.attrib.get('largura'))
        self.altura = int(ficheiro.attrib.get('altura'))
        self.site = ficheiro.attrib.get('site')
        self.estilo = ficheiro.attrib.get('estilo')
        self.jogo = ficheiro.attrib.get('jogo')
        self.valor = ficheiro.attrib.get('valor')
        self.cadeiras = int(ficheiro.attrib.get('cadeiras'))
        
        if(self.imagem == 'null'):
            self.imagem = cv2.imread(ficheiro.attrib.get('imagem'))
        
        for  mural in ficheiro:
            nome_mural = mural.attrib.get('nome')
            cor_r = int(mural.attrib.get('cor_r'))
            cor_g = int(mural.attrib.get('cor_g'))
            cor_b = int(mural.attrib.get('cor_b'))
            self.adicionar_mural(nome_mural,(cor_r,cor_g,cor_b))
            for  recorte in mural:
                nome_recorte = recorte.attrib.get('nome')
                py_inicial = int(recorte.attrib.get('posicao_y_inicial'))
                py_final = int(recorte.attrib.get('posicao_y_final'))
                px_inicial = int(recorte.attrib.get('posicao_x_inicial'))
                px_final = int(recorte.attrib.get('posicao_x_final'))
                self.selecionar_mural(nome_mural).adicionar_recorte(nome_recorte,(py_inicial,py_final,px_inicial,px_final))        

    def marcar(self):
        for chave in self.dicionario_de_murais:
            self.dicionario_de_murais[chave].marcar()

    def cortar(self):
        for chave in self.dicionario_de_murais:
            self.dicionario_de_murais[chave].cortar()

    def set_imagem(self,imagem):
        self.imagem = imagem
        for chave in self.dicionario_de_murais:
            self.dicionario_de_murais[chave].set_imagem(imagem)

    def show(self):
        self.marcar()
        cv2.imshow(self.nome,self.imagem)
        cv2.waitKey(0)

    def resposta():
        print('resposta do ficheiro e')
        


class FicheiroTest(unittest.TestCase):
    
    def test_adicionar_seleciona_remover_mural(self):
        print("____test_adicionar_seleciona_remover_mural(self): teste dos metodos ")
        ficheiro = Ficheiro()
        cor_verde = (0,255,0)
        ficheiro.adicionar_mural('nome_do_mural',cor_verde)
        self.assertTrue(ficheiro.dicionario_de_murais.get('nome_do_mural'))
        self.assertTrue(ficheiro.dicionario_das_respostas_dos_murais.get('nome_do_mural'))
        print("________Metodo adicionar_mural('nome_do_mural') >> sucesso")
        self.assertEqual(ficheiro.selecionar_mural('nome_do_mural').nome,'nome_do_mural')
        print("________Metodo selecionar_mural('nome_do_mural') >> sucesso")
        self.assertEqual(ficheiro.selecionar_resposta_do_mural('nome_do_mural'),'null')
        print("________Metodo selecionar_resposta_do_mural('nome_do_mural') >> sucesso")
        ficheiro.remover_mural('nome_do_mural')
        self.assertFalse(ficheiro.selecionar_mural('nome_do_mural'))
        self.assertFalse(ficheiro.selecionar_resposta_do_mural('nome_do_mural'))
        print("________Metodo remover_mural('nome_do_mural') >> sucesso")
            
    def test_show(self):
        ficheiro = Ficheiro()
        ficheiro.imagem = cv2.imread('entrada.jpg')
        cor_vilao = (0,0,255)
        ficheiro.adicionar_mural('vilao',cor_vilao)
        ficheiro.selecionar_mural('vilao').adicionar_recorte('A',(139,190,614,774))
        ficheiro.selecionar_mural('vilao').adicionar_recorte('B',(73,124,317,472))
        cor_vez = (0,255,0)
        ficheiro.adicionar_mural('vez',cor_vez)
        ficheiro.selecionar_mural('vez').adicionar_recorte('A',(190,200,634,734))
        ficheiro.selecionar_mural('vez').adicionar_recorte('B',(124,134,337,442))
        ficheiro.show()

    def test_salvar_molde(self):
        ficheiro = Ficheiro()
        ficheiro.ler_molde('MPSC6.xml')
        ficheiro.show()
        nome_do_ficheiro_original = ficheiro.nome
        posicao_x_final_original = ficheiro.selecionar_mural('vilao').selecionar_recorte('A').posicao_x_final
        ficheiro.nome = 'teste do salvar molde'
        ficheiro.selecionar_mural('vilao').selecionar_recorte('A').posicao_x_final = 400
        ficheiro.salvar_molde('MPSC6.xml')
        ficheiro.show()
        ficheiro.nome = nome_do_ficheiro_original
        ficheiro.selecionar_mural('vilao').selecionar_recorte('A').posicao_x_final = posicao_x_final_original
        ficheiro.salvar_molde('MPSC6.xml')
        ficheiro.show()
        ficheiro.selecionar_mural('vilao').adicionar_recorte('C',(139,190,614,774))
        cor_vez = (255,0,0)
        ficheiro.adicionar_mural('vez',cor_vez)
        ficheiro.selecionar_mural('vez').adicionar_recorte('A',(73,124,317,472))
        ficheiro.salvar_molde('MPSC6.xml')
        ficheiro.show()

    def test_ler_molde(self):
        ficheiro = Ficheiro()
        ficheiro.ler_molde('MPSC6.xml')
        ficheiro.show()

    def test_iniciar(self):
        ficheiro = Ficheiro()
        PILImage = pyautogui.screenshot(region = (0,0,400,400))
        imagem = cv2.cvtColor(np.array(PILImage), cv2.COLOR_RGB2BGR)
        ficheiro.iniciar('MPSC6.xml')
        ficheiro.set_imagem(imagem)
        ficheiro.show()

    def test_set_imagem(self):
        ficheiro = Ficheiro()
        PILImage = pyautogui.screenshot(region = (0,0,400,400))
        imagem = cv2.cvtColor(np.array(PILImage), cv2.COLOR_RGB2BGR)
        ficheiro.iniciar('MPSC6.xml')
        ficheiro.show()
        PILImage = pyautogui.screenshot(region = (0,0,400,400))
        imagem = cv2.cvtColor(np.array(PILImage), cv2.COLOR_RGB2BGR)
        ficheiro.set_imagem(imagem)
        ficheiro.show()
        

    def test_resposta(self):
        self.assertTrue(True)
    

if __name__ == "__main__":
    print('____Teste da classe Ficheiro')
    unittest.main()
