import numpy as np
import requests, bs4

precios = open("Precios.txt", "w", encoding="utf-8")
descripcion = open("Descripcion.txt", "w", encoding="utf-8")
reglas = open("atilusDecicion.py", "w", encoding="utf-8")
casas = []
localizacionCasas = []
areaCasas = []
pisoCasas = []
habitacionesCasas = []
bathroomsCasas = []
parqueaderoCasas = []
incluyeCasas = []
precioCasas = []


def pathBusqueda(int):
    return "https://www.lahaus.com/venta/casas/bogota"


def descomponerPagina(path, selector):
    res = requests.get(path)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    linkElems = soup.select(selector)
    return linkElems


def buscadorDeApartamentos(lista, titulo, dat):
    dat.write(titulo.center(60) + "\n")
    for elem in lista:
        if "text-14" in str(elem) and "mt-lh-12" in str(elem):
            escribir("Ubicacion: ", elem)
        if "text-14" in str(elem) and "mt-lh-12" in str(elem) and "font-semibold" in str(elem):
            escribir("-", elem)
        if "text-18" in str(elem) and "COP" in str(elem):
            escribir("Precio ", elem)
        if "text-14 pt-lh-8" in str(elem):
            escribir("Descripcion ", elem)


def buscadorCasas(lista, titulo, dat, flag):
    dat.write(titulo.center(60) + "\n")
    cont = 0
    for elem in lista:
        if "fa-pin-location" in str(elem) and "Datos" in titulo:
            cont += 1
            if cont > 2 and flag == True:
                if cont > 3:
                    valoresPorDefecto()
                tamaño(cont)
                localizacionCasas.append(elem.getText())
                escribir("Localizacion: ", elem, dat)
            if flag == False:
                valoresPorDefecto()
                tamaño(cont)
                # valoresPorDefecto(cont)
                localizacionCasas.append(elem.getText())
                escribir("Localizacion: ", elem, dat)
        if 'aria-hidden="true"' in str(elem) and "Área" in str(elem) and "Datos" in titulo:
            if cont > 2 and flag == True:
                areaCasas.append(elem.getText())
                escribir("Area: ", elem, dat)
            if flag == False:
                areaCasas.append(elem.getText())
                escribir("Area: ", elem, dat)
        if "Piso" in str(elem) and "Datos" in titulo:
            if cont > 2 and flag == True:
                pisoCasas.append(elem.getText())
                escribir("Piso:", elem, dat)
            if flag == False:
                pisoCasas.append(elem.getText())
                escribir("Piso:", elem, dat)
        if "Habitaciones" in str(elem) and "Datos" in titulo:
            if cont > 2 and flag == True:
                habitacionesCasas.append(elem.getText())
                escribir("Habitaciones: ", elem, dat)
            if flag == False:
                habitacionesCasas.append(elem.getText())
                escribir("Habitaciones: ", elem, dat)
        if "Baños" in str(elem) and "Datos" in titulo:
            if cont > 2 and flag == True:
                bathroomsCasas.append(elem.getText())
                escribir("Baños: ", elem, dat)
            if flag == False:
                bathroomsCasas.append(elem.getText())
                escribir("Baños: ", elem, dat)
        if "Parqueaderos" in str(elem) and "Datos" in titulo:
            if cont > 2 and flag == True:
                parqueaderoCasas.append(elem.getText())
                escribir("Par: ", elem, dat)
            if flag == False:
                parqueaderoCasas.append(elem.getText())
                escribir("Par: ", elem, dat)
        if "Incluye" in str(elem) and "Datos" in titulo:
            if cont > 2 and flag == True:
                incluyeCasas.append(elem.getText())
                escribir("", elem, dat)
            if flag == False:
                incluyeCasas.append(elem.getText())
                escribir("", elem, dat)

        if "millones" in str(elem) and "text-14" in str(elem) and "Precios" in titulo:
            escribir(" \n- ", elem, dat)
            precioCasas.append(elem.getText())
    if "Precios" in titulo:
        llenarPrecio()
    return cont


def llenarPrecio():
    if len(precioCasas) != len(localizacionCasas):
        for cont in range(len(localizacionCasas) - len(precioCasas)):
            precioCasas.append(0)


def valoresPorDefecto():
    # print("complementado...")
    if len(areaCasas) != len(localizacionCasas):
        # print("complementando areaCasas")
        areaCasas.append(0)
    if len(pisoCasas) != len(localizacionCasas):
        # print("complementando pisoCasas")
        pisoCasas.append("Piso 0")
    if len(habitacionesCasas) != len(localizacionCasas):
        # print("complementando habitacionesCasas")
        habitacionesCasas.append(1)
    if len(bathroomsCasas) != len(localizacionCasas):
        # print("complementando bathroomsCasas")
        bathroomsCasas.append(1)
    if len(parqueaderoCasas) != len(localizacionCasas):
        # print("complementando parqueaderoCasas")
        parqueaderoCasas.append(0)
    if len(incluyeCasas) != len(localizacionCasas):
        # print("complementando incluyeCasas")
        incluyeCasas.append("no incluye")


def valorMinimo(lista):
    lista.sort()
    return lista[0]


def valorMaximo(lista):
    lista.sort()
    return lista[len(lista) - 1]


def inventarioUbicacion(lista):
    inventario = dict()
    for cont in range(0, len(lista), 1):
        inventario[lista[cont]] = inventario.get(lista[cont], 0) + 1
    return inventario


def valorRecmendadoMax(lista, tipo):
    if tipo == "float":
        valorMax = 0.0
        valorMax = float(valorMaximo(lista))
        valorMax -= valorMax * 0.20
        return str(valorMax)
    if tipo == "int":
        valorMax = 0
        valorMax = int(valorMaximo(lista))
        valorMax -= int(valorMax * 0.20)
        return str(valorMax)
    return valorMinimo(lista)


def valorRecmendadoMin(lista, tipo):
    if tipo == "float":
        valorMin = 0.0
        valorMin = float(valorMinimo(lista))
        valorMin += valorMin * 0.20
        return str(valorMin)
    if tipo == "int":
        valorMin = 0
        valorMin = int(valorMinimo(lista))
        valorMin += int(valorMin * 0.20)
        return str(valorMin)
    return str(valorMinimo(lista))


def llenarDatos(url, flag, contadorPagina):
    print("lleno %i" % contadorPagina)
    contadorPagina += 1
    buscadorCasas(descomponerPagina(url, "span"), "links Datos %i" % contadorPagina, descripcion, flag)
    buscadorCasas(descomponerPagina(url, "p"), "links Precios %i" % contadorPagina, precios, flag)
    if siguiente(url) != "/venta/casas/bogota?pagina=3":
        llenarDatos("https://www.lahaus.com" + siguiente(url), False, contadorPagina)
        # buscadorCasas(descomponerPagina("https://www.lahaus.com"+siguiente(url),"Span"),"links 2",bogota,False)
    # buscadorCasas(descomponerPagina(url,"p"),"P",precios,False)


def siguiente(url):
    linkELements = descomponerPagina(url, "a")
    for elem in linkELements:
        if "Next" in str(elem):
            return str(elem.get('href'))
    return ""


def limpiarDatos(lista):
    datosLimpios = []
    for casa in lista:
        print("tipo de casa %s" % str(type(casa)))
        vec = []
        if "\n" in casa[0]:
            vec.append(casa[0].split("\n")[1])
        if str(type(casa[1])) == str(type(1)):
            vec.append(float(casa[1]))
        if str(type(casa[1])) != str(type(1)):
            if "\n" in casa[1]:
                if "," in casa[1]:
                    casa[1] = casa[1].replace(",", ".")
                vec.append(float(casa[1].split("\n")[2].strip().split(" ")[0]))
        vec.append(casa[2].strip())
        vec.append(int(casa[3].split("\n")[2].strip()))
        if casa[4] != "no incluye":
            if len(casa[4].split("\n")[1].split("Incluye:")[1]) > 1:
                vec.append(casa[4].split("\n")[1].split("Incluye:")[1].split("·"))
            if len(casa[4].split("\n")[1].split("Incluye:")[1]) <= 1:
                vec.append(casa[4].split("\n")[1].split("Incluye:")[1])
        if casa[4] == "no incluye":
            vec.append(["no incluye"])
        vec.append(int(casa[5].split("\n")[2].strip()))
        if str(type(casa[6])) == str(type(1)):
            vec.append(float(casa[6]))
        if str(type(casa[6])) != str(type(1)):
            if "\n" in casa[6]:
                if "," in casa[6]:
                    casa[6] = casa[6].replace(",", ".")
                if "." in casa[6]:
                    vec.append(
                        float(retornarPrecio(casa[6].split("\n")[1].strip().split(" ")[0].split("$")[1].split("."))))
                if "." not in casa[6] and "," not in casa[6]:
                    vec.append(float(casa[6].split("\n")[1].strip().split(" ")[0].split("$")[1]))
            if "\n" not in casa[6]:
                vec.append(float(casa[6].split(" ")[0][1:]))
        datosLimpios.append(vec)
    return datosLimpios


def retornarPrecio(lista):
    valor = ""
    for item in lista:
        if item == ".":
            continue
        valor += item
    print(valor)
    return valor


def guardarCasa():
    datosSucios = []
    for cont in range(0, len(localizacionCasas), 1):
        vec = []
        vec.append(localizacionCasas[cont][:])
        vec.append(areaCasas[cont])
        vec.append(pisoCasas[cont][:])
        vec.append(habitacionesCasas[cont][:])
        vec.append(incluyeCasas[cont][:])
        vec.append(bathroomsCasas[cont][:])
        vec.append(precioCasas[cont])
        datosSucios.append(vec)
    # print(datosSucios[1])
    return datosSucios

    # casas.append(vec)


def escribir(name, elem, dat):
    if name == "Localizacion: ":
        dat.write("________________________________________________________\n")
    palabra = name + str(elem.getText()).lstrip()
    palabra.lstrip()
    dat.write(palabra)


# buscadorDeApartamentos(descomponerPagina(pathBusqueda(3)),"Lanzamientos")
# ----------------------------------
# data2=open("enlaces.txt","w",encoding="utf-8")
# 
def tamaño(cont):
    print("index: %i" % cont)
    print("Tamaño localizacionCasas: %i" % len(localizacionCasas))
    print("Tamaño areaCasas: %i" % len(areaCasas))
    print("Tamaño pisoCasas: %i" % len(pisoCasas))
    print("Tamaño habitacionesCasas: %i" % len(habitacionesCasas))
    print("Tamaño bathroomsCasas: %i" % len(bathroomsCasas))
    print("Tamaño parqueaderoCasas: %i" % len(parqueaderoCasas))
    print("Tamaño incluyeCasas: %i" % len(incluyeCasas))
    print("Tamaño precioCasas: %i" % len(precioCasas))


def run():
    llenarDatos(pathBusqueda(4), True, 0)
    parqueaderoCasas.append(0)
    incluyeCasas.append("no incluye")
    tamaño(99)
    guardarCasa()
    escribirMuestra()


def mostrarInventario():
    vec = []
    for i in limpiarDatos(guardarCasa()):
        vec.append(i[0])
    print(inventarioUbicacion(vec))
    return vec


def recolectarMuestra():
    filtros = set(mostrarInventario())
    muestras = []
    for filtro in filtros:
        muestra = []
        for casa in limpiarDatos(guardarCasa()):
            vec = []
            if casa[0] == filtro and casa[6] != 0:
                vec.append(casa[0])
                vec.append(casa[1])
                vec.append(casa[2])
                vec.append(casa[3])
                vec.append(casa[4])
                vec.append(casa[5])
                vec.append(casa[6])
                muestra.append(vec)
        muestras.append(muestra)
    return muestras


def retornarlista(lista, nombre):
    vec = []
    for item in lista:
        if "Nombre" == nombre:
            vec.append(item[0])
        if "Area" == nombre:
            vec.append(item[1])
        if "Piso" == nombre:
            vec.append(item[2])
        if "Habitaciones" == nombre:
            vec.append(item[3])
        if "Incluye" == nombre:
            vec.append(item[4])
        if "Numero de baños" == nombre:
            vec.append(item[5])
        if "Precio" == nombre:
            vec.append(item[6])
    return vec


def nombreMuestraUnida(nombre):
    nombresincoma = ""
    nombreUnido = ""
    for palabra in nombre.split(","):
        if palabra != ",":
            nombresincoma += palabra
    for palabra in nombresincoma.split(" "):
        if palabra != " ":
            nombreUnido += palabra
    return nombreUnido.strip()


def escribirMuestra():
    muestras = recolectarMuestra()
    reglas.write("\nfrom experta import *\n")
    reglas.write("\nfrom tkinter import *\n")
    reglas.write("\nclass Casa(Fact):")
    reglas.write("\n    ubicacion=Field(str)")
    reglas.write("\n    area=Field(float)")
    reglas.write("\n    numeroBaños=Field(int)\n\n")
    reglas.write("\n    precio=Field(float)")
    reglas.write("\nclass SugerenciaCasa(KnowledgeEngine):\n")
    print('MUESTRA')
    print(muestras)
    for muestra in muestras:
        # Reglas de excelente compra #1 (precio menor, resto dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <=%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >=1),')
        reglas.write(
            '\n    TEST(lambda area: area >=%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write(
            '\n    TEST(lambda area: area <=%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <%s))' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeExcelente1%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#49FF33",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una excelente compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de excelente compra #2 (area mayor, resto dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <=%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >=1),')
        reglas.write(
            '\n    TEST(lambda area: area >%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >=%s),' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <=%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeExcelente2%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#49FF33",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una excelente compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de excelente compra #3 (baños mayor, resto dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write(
            '\n    TEST(lambda area: area >=%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write(
            '\n    TEST(lambda area: area <=%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >=%s),' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <=%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeExcelente3%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#49FF33",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una excelente compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de excelente compra #4 (baños mayor, area mayor, precio dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write(
            '\n    TEST(lambda area: area >%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >=%s),' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <=%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeExcelente4%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#49FF33",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una excelente compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de excelente compra #5 (baños mayor, area mayor, precio menor)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write(
            '\n    TEST(lambda area: area >%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <%s))' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeExcelente5%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#49FF33",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una excelente compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de excelente compra #6 (baños mayor, area dentro del rango, precio menor)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write(
            '\n    TEST(lambda area: area <=%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write(
            '\n    TEST(lambda area: area >=%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <%s))' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeExcelente6%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#49FF33",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una excelente compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')



        # Regla compra normal (todo dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <=%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >=1),')
        reglas.write(
            '\n    TEST(lambda area: area <=%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write(
            '\n    TEST(lambda area: area >=%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >=%s),' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <=%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeNormal%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#aba7b4",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una compra NORMAL",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')



        # Reglas de mala compra #1 (precio mayor, resto dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <=%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >=1),')
        reglas.write(
            '\n    TEST(lambda area: area >=%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write(
            '\n    TEST(lambda area: area <=%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeMala1%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#FF4633",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una mala compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de mala compra #2 (area menor, resto dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <=%s),' % str(
            valorMaximo(retornarlista(muestra, "Numero de baños"))))
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >=1),')
        reglas.write(
            '\n    TEST(lambda area: area <%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >=%s),' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <=%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeMala2%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#FF4633",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una mala compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de mala compra #3 (baños menor, resto dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <1),')
        reglas.write(
            '\n    TEST(lambda area: area >=%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write(
            '\n    TEST(lambda area: area <=%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >=%s),' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <=%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeMala3%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#FF4633",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una mala compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de mala compra #4 (baños menor, area menor, precio dentro del rango)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <1),')
        reglas.write(
            '\n    TEST(lambda area: area <%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >=%s),' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <=%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeMala4%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#FF4633",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una mala compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de mala compra #5 (baños menor, area menor, precio mayor)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <1),')
        reglas.write(
            '\n    TEST(lambda area: area <%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeMala5%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#FF4633",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una mala compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')


        # Reglas de mala compra #6 (baños menor, area dentro del rango, precio mayor)
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños <1),')
        reglas.write(
            '\n    TEST(lambda area: area <=%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write(
            '\n    TEST(lambda area: area >=%s),' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    TEST(lambda precio: precio >%s))' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    def mensajeMala6%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#FF4633",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una mala compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')

        """
        # Regla de mala compra
        reglas.write('\n\n    @Rule(Casa(ubicacion="%s",' % muestra[0][0].strip())
        reglas.write('\n    area=MATCH.area,')
        reglas.write('\n    numeroBaños=MATCH.numeroBaños,')
        reglas.write('\n    precio=MATCH.precio),')
        reglas.write('\n    TEST(lambda precio: precio >=%s),' % str(
            valorRecmendadoMax(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda precio: precio <%s),' % str(
            valorRecmendadoMin(retornarlista(muestra, "Precio"), "float")))
        reglas.write('\n    TEST(lambda numeroBaños: numeroBaños >=%s),' % str(
            valorMinimo(retornarlista(muestra, "Numero de baños"))))
        reglas.write(
            '\n    TEST(lambda area: area >=%s),' % str(valorRecmendadoMax(retornarlista(muestra, "Area"), "float")))
        reglas.write(
            '\n    TEST(lambda area: area <%s))' % str(valorRecmendadoMin(retornarlista(muestra, "Area"), "float")))
        reglas.write('\n    def mensajeRechazado%s(self):' % nombreMuestraUnida(muestra[0][0]))
        reglas.write(
            '\n        resultado="\\nUbicacion: " +str(list(self.facts.get(1).values())[0])+ "\\nArea mt2: "+str('
            'list(self.facts.get(1).values())[1])+"\\nnumero Baños: "+str(list(self.facts.get(1).values())[2])+ '
            '"\\nPrecio: "+str(list(self.facts.get(1).values())[3])')
        reglas.write(
            '\n        respuesta_label=Label(text=resultado,bg="#FF4633",width="36",heigh="14",font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=300,y=70)')
        reglas.write(
            '\n        respuesta_label=Label(text="Es una mala compra",bg="#FDFCFB",width="66",heigh="3", '
            'font=("Cambria",12))')
        reglas.write('\n        respuesta_label.place(x=22,y=430)')
        """

    escribirGraficadora()
    # reglas.write("\n\nNombre muestra: %s".center(60) %muestra[0][0])
    # reglas.write("muestra: \n" )
    # reglas.write("Area \n" )
    # reglas.write("valor minimo de Area  %s \n" %str( valorMinimo(retornarlista(muestra,"Area"))))
    # reglas.write("valor maximo de Area  %s \n" %str( valorMaximo(retornarlista(muestra,"Area"))))
    # reglas.write("Piso \n" )
    # reglas.write("valor minimo de Piso  %s \n" %str( valorMinimo(retornarlista(muestra,"Piso"))))
    # reglas.write("valor maximo de Piso  %s \n" %str( valorMaximo(retornarlista(muestra,"Piso"))))
    # reglas.write("Habitaciones \n" )
    # reglas.write("valor minimo de Habitaciones  %s \n" %str( valorMinimo(retornarlista(muestra,"Habitaciones"))))
    # reglas.write("valor maximo de Habitaciones  %s \n" %str( valorMaximo(retornarlista(muestra,"Habitaciones"))))
    # reglas.write("Incluye \n"  )
    # reglas.write("valor minimo de Incluye  %s \n" %str( valorMinimo(retornarlista(muestra,"Incluye"))))
    # reglas.write("valor maximo de Incluye  %s \n" %str( valorMaximo(retornarlista(muestra,"Incluye"))))
    # reglas.write("Numero de baños \n" )
    # reglas.write("valor minimo de Numero de baños  %s \n" %str( valorMinimo(retornarlista(muestra,"Numero de baños"))))
    # reglas.write("valor maximo de Numero de baños  %s \n" %str( valorMaximo(retornarlista(muestra,"Numero de baños"))))
    # reglas.write("Precio \n" )
    # reglas.write("valor minimo de Precio  %s \n" %str( valorMinimo(retornarlista(muestra,"Precio"))))
    # reglas.write("valor maximo de Precio  %s \n" %str( valorMaximo(retornarlista(muestra,"Precio"))))


def escribirGraficadora():
    reglas.write('\ndef send_data():')
    reglas.write('\n    ubicacionD= str(ubicacion_entry.get())')
    reglas.write('\n    areaD= str(area_entry.get())')
    reglas.write('\n    areaD= float(areaD)')
    reglas.write('\n    numeroBañosD= str(numeroBaños_entry.get())')
    reglas.write('\n    numeroBañosD= int(numeroBañosD)')
    reglas.write('\n    precioD= str(precio_entry.get())')
    reglas.write('\n    precioD= float(precioD)')
    reglas.write('\n    print(ubicacionD, areaD, numeroBañosD, precioD)')
    reglas.write('\n    sugerencia=SugerenciaCasa()')
    reglas.write('\n    sugerencia.reset()')
    reglas.write(
        '\n    sugerencia.declare(Casa(ubicacion=ubicacionD, area=areaD, numeroBaños=numeroBañosD, precio=precioD))')
    reglas.write('\n    sugerencia.run()')
    # print("\n ubicacionData\t : %s \nareaData\t : %s \nnumeroBañosData\t : %s \nprecioData\t : %s" %ubicacionData %areaData %numeroBañosData %precioData)  

    reglas.write('\nmyWindows=Tk()')
    reglas.write('\nmyWindows.geometry("650x650")')
    reglas.write('\nmyWindows.title("Atilus Desicion")')
    reglas.write('\nmyWindows.resizable(False,False)')
    reglas.write('\nmyWindows.config(background ="#121726")')
    reglas.write(
        '\nmain_title=Label(text="Ingrese los datos",font=("Cambria",13),bg="#146a87",fg="white",width="50",heigh="2")')
    reglas.write('\nmain_title.pack()')
    reglas.write('\n')
    reglas.write(
        '\nubicacion_label=Label(text="Ubicacion            ",bg="#1da2c8",fg="white", width=14,font=("Cambria",12))')
    reglas.write('\nubicacion_label.place(x=22,y=70)')
    reglas.write(
        '\narea_label=Label(text="Area (m2)               ",bg="#1da2c8",fg="white", width=14,font=("Cambria",12))')
    reglas.write('\narea_label.place(x=22,y=130)')
    reglas.write(
        '\nnumeroBaños_label=Label(text="Numero de baños",bg="#1da2c8",fg="white", width=14,font=("Cambria",12))')
    reglas.write('\nnumeroBaños_label.place(x=22,y=190)')
    reglas.write('\nprecio_label=Label(text="Precio (Millones)",bg="#1da2c8",fg="white", width=14,font=("Cambria",12))')
    reglas.write('\nprecio_label.place(x=22,y=250)')
    reglas.write('\n')
    reglas.write('\n')
    reglas.write('\nubicacion_Input= StringVar()')
    reglas.write('\narea_Input= StringVar()')
    reglas.write('\nnumeroBaños_Input= StringVar()')
    reglas.write('\nprecio_Input= StringVar()')
    reglas.write('\n')
    reglas.write('\nubicacion_entry=Entry(textvariable=ubicacion_Input,width="40")')
    reglas.write('\narea_entry=Entry(textvariable=area_Input,width="40")')
    reglas.write('\nnumeroBaños_entry=Entry(textvariable=numeroBaños_Input,width="40")')
    reglas.write('\nprecio_entry=Entry(textvariable=precio_Input,width="40")')
    reglas.write('\n')
    reglas.write('\nubicacion_entry.place(x=22,y=100)')
    reglas.write('\narea_entry.place(x=22,y=160)')
    reglas.write('\nnumeroBaños_entry.place(x=22,y=220)')
    reglas.write('\nprecio_entry.place(x=22,y=280)')
    reglas.write('\n')
    reglas.write(
        '\nsubmit_btn =Button(myWindows, text="PROBAR", command=send_data, widt="30", heigh="2", bg= "#20dbd8")')
    reglas.write('\nsubmit_btn.place(x=22 , y =320)')
    reglas.write('\n')
    reglas.write('\nmyWindows.mainloop()')


run()
# TODO filtrar valores aplicar min y max
# TODO 
# for link in descomponerPagina(pathBusqueda(4),"span"):
#     reglas.write(reglask)
