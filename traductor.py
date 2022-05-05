import re

class Error_Lexico(Exception):
    def __init__(self,msg):
        super().__init__(msg)


def manejadorErrores(linea,tipo,error):

    if tipo == "Error lexico":
        raise Error_Lexico("Error lexico en la linea " + str(linea) + " el error es: " + error)

class Automata:
    
    def __init__(self):
        self.tabla_transciciones = {}
        self.estados_finales = []
        self.estado_inicial = ''
        self.dic_retrocesos = {}
        self.dic_tokens = {}
        self.codigo=None
        self.linea=[]
        self.token=''
        self.palabras_reservadas = {}

    def guardar_codigo(self,ubicacion_archivo):
        archivo = open(ubicacion_archivo)
        self.codigo = []
        pattern = re.compile(r'(?P<lexema>[^\s]+)')

        i = 1
        for linea in archivo.readlines():
            aux = re.findall(pattern,linea)
            if aux != []:
                self.codigo.append(aux)
                self.linea.append(i)
            i += 1
        archivo.close()

    def guardar_reservadas(self,ubucacion_palabras):
        archivo = open(ubucacion_palabras)
        lineas = archivo.readlines()
        archivo.close()
        for linea in lineas:
            linea = linea.replace("\n","",1)
            linea = linea.replace("reservada[","",1)
            linea = linea.replace("]","",1)
            tipo, valor = linea.split(",")
            self.palabras_reservadas[valor]=tipo

    def analex(self):
        if self.codigo == []:
            self.token = 'EOF'
            return
        
        lexema = ''
        estado = self.estado_inicial
        error  = ''

        for letra in self.codigo[0][0]:
            bandera = False
            
            for dic in self.tabla_transciciones[estado].items():
                if letra in dic[1]:
                    estado = dic[0]
                    lexema += letra
                    bandera = True
                    break
            
            error += letra
            if not(bandera):
                break
            
        if estado in self.estados_finales:
            retroceso = int(self.dic_retrocesos[estado])
            if retroceso > 0:
                retroceso -= 1
            if retroceso != 0:
                lexema = lexema[:-retroceso]
            
            if lexema in self.palabras_reservadas.keys():
                tipo = self.palabras_reservadas[lexema]
            else:
                tipo = self.dic_tokens[estado]
            
            self.token = tipo + "," + lexema
            self.codigo[0][0] = self.codigo[0][0].replace(lexema,"",1)

            if self.codigo[0][0] == '':
                self.codigo[0].pop(0)
            if self.codigo[0] == []:
                self.codigo.pop(0)
                self.linea.pop(0)
        else:
             manejadorErrores(self.linea[0],"Error lexico",error)

def crearAutomata(ubicacion_archivo):
    automata = Automata()

    archivo = open(ubicacion_archivo)
    lineas = archivo.readlines()
    archivo.close()
    for linea in lineas:
        
        if linea.__contains__("***"):
            continue
        linea = linea.replace("\n","")
        #1...2...abcdefghijklmnopkr
        if linea.__contains__("..."):
            inicio,destino,valores = linea.split("...")
            automata.tabla_transciciones[inicio][destino] = valores
            continue

        if linea.__contains__("estados=("):
            estados = linea.replace("estados=(","",1)
            estados = estados.replace(")","",1)
            estados = estados.split(",")
            for estado in estados:
                automata.tabla_transciciones[estado] = {}
            continue


        if linea.__contains__("estados_finales={"):
            estados = linea.replace("estados_finales={","",1)
            estados = estados.replace("}","",1)
            estados = estados.split(",")
            for estado_retroceso in estados:
                estado, retroceso = estado_retroceso.split(":")
                automata.dic_retrocesos.update({estado:retroceso})
                automata.estados_finales.append(estado)
            continue
        
        if linea.__contains__("estado_inicial=("):
            estado = linea.replace("estado_inicial=(","",1)
            estado = estado.replace(")","",1)
            automata.estado_inicial = estado
            continue

        if linea.__contains__("token("):
            token = linea.replace("token(","",1)
            token = token.replace(")","",1)
            estado, tipo = token.split(",")
            automata.dic_tokens.update({estado:tipo})

    return automata

auto = crearAutomata("proyecto/automataProyecto.txt")
#
#Informacion de automata
print(auto.tabla_transciciones)
print(auto.dic_retrocesos)
print(auto.estados_finales)
print(auto.dic_tokens)
print(auto.estado_inicial)
#
#palabras reservadas
auto.guardar_reservadas("proyecto/palabras_reservadasProyecto.txt")
print(auto.palabras_reservadas)
#
#codigo
auto.guardar_codigo("proyecto/codigoProyecto1.txt")
for linea in auto.codigo:
    print(linea)
#
#analizador_lexico
auto.analex()
while auto.token != "EOF":
    print(auto.token)
    auto.analex()
#
#

def X(automata):
    I(automata)

def I(automata):
    automata.analex()
    if(automata.token == "pgr"):
        automata.analex()
        if(automata.token == "id"):
            automata.analex()
            if(automata.token == "ini"):
                automata.analex()
                Z(automata,automata.token)
                if(automata.token is "fn"):
                    ...
                else:
                    #sintax error
            else:
                #sintax error
        else:
            #sintax error
    else:
        #sintax error

def Z(automata,token):
    if token in {"fn","fc","fns","sino"}:
        return
    elif token in {"cc","bc","cn","ceb","ceo"}:
        automata.analex()
        F(automata,automata.token)
        Z(automata,automata.token)
        return
    elif token is "si":
        automata.analex()
        ES(automata,automata.token)
        Z(automata,automata.token)
        return
    elif token is "cl":
        automata.analex()
        EC(automata,automata.token)
        Z(automata,automata.token)
        return
    else:
        #Sintax error

def F(automata,token):
    if token in {"cc","bc","cn","ceb"}:
        F1(automata,token)
        return
    elif token is "ceo":
        F2(automata,token)
        return
    else:
        #sintax error

def F1(automata,token):
    if token is "cc":
        automata.analex()
        if automata.token is "(":
            automata.analex()
            if automata.token is "id":
                automata.analex()
                if automata.token is ",":
                    automata.analex()
                    if automata.token is "numero":
                        automata.analex()
                        if automata.token is ",":
                            automata.analex()
                            if automata.token is "numero":
                                automata.analex()
                                if automata.token is ")":
                                    ...
                                else:
                                    #sintax error
                            else:
                                #sintax error
                        else:
                            #sintax error
                    else:
                        #sintax error
                else:
                    #sintax error
            else:
                #sintax error
        else:
            #sintax error
    elif token is "bc":
        automata.analex()
        if automata.token is "(":
            automata.analex()
            if automata.token is "id":
                automata.analex()
                if automata.token is ")":
                    ...
                else:
                    #sintax error
            else:
                #sintax error
        else:
            #sintax error
    elif token is "cn":
        automata.analex()
        if automata.token is "(":
            automata.analex()
            if automata.token is "id":
                automata.analex()
                if automata.token is ",":
                    automata.analex()
                    if automata.token is "id":
                        automata.analex()
                        if automata.token is ")":
                            ...
                        else:
                            #sintax error
                    else:
                        #sintax error
                else:
                    #sintax error
            else:
                #sintax error
        else:
            #sintax error
    elif token is "ceb":
        automata.analex()
        if automata.token is "(":
            automata.analex()
            if automata.token is "id":
                automata.analex()
                if automata.token is ",":
                    automata.analex()
                    F1_prima(automata,automata.token)
                else:
                    #sintax error
            else:
                #sintax error
        else:
            #sintax error
    else:
        #sintax error

def F1_prima(automata,token):
    if token in {"abierto","cerrado"}:
        E1(automata,token)
        automata.analex()
        if automata.token is ")":
            ...
        else:
            #sintax error
    elif token in {"sonriente","enojado","triste"}:
        E2(automata,token)
        automata.analex()
        if automata.token is ")":
            ...
        else:
            #sintax error
    else:
        #sintax error

#################

def E1(automata,token):
    if token is "abierto":
        ...
    elif token is "cerrado":
        ...
    else:
        #sintax error

def E2(automata,token):
    if token is "sonriente":
        ...
    elif token is "enojado":
        ...
    elif token is "triste":
        ...
    else:
        #sintax error

def OJO(automata,token):
    if token is "derecho":
        ...
    elif token is "izquierdo":
        ...
    else:
        #sintax error


