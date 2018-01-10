# tutoriais: https://docs.python.org/2/library/xml.etree.elementtree.html
# tutoriais: http://infohost.nmt.edu/tcc/help/pubs/pylxml/web/index.html

# lxml e baseado no ElementTree uma arvore que ajuda a manipular xml

from lxml import etree  

doc = etree.parse('test.xml')
ficheiro = doc.getroot()


print ficheiro.tail, ficheiro.attrib.get('estilo')
for mural in ficheiro:
    print mural.tag, mural.attrib
    for recorte in mural:
        print recorte.tag, recorte.attrib
    

print doc.getroot().tag # retorna o elemento raiz
print doc.find('mural').tab # retorna o primeiro elemento que encontrar 
print doc.getroot().find('mural').tab # retorna o primeiro elemento que encontrar 
print doc.findtext()

