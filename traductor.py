import re

#Errores
class Error_Lexico(Exception):
    def __init__(self,msg):
        super().__init__(msg)
class Error_Sintactico(Exception):
    def __init__(self,msg):
        super().__init__(msg)

#Manejador de errores
def manejadorErrores(linea,tipo,error):

    if tipo == "Error lexico":
        raise Error_Lexico("Error lexico en la linea " + str(linea) + " el error es: " + error)

    if tipo == "Error sintáctico":
        raise Error_Sintactico("Error sintactico en la linea " + str(linea) + " error: " + error)

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
            error += letra
            lexema += letra
            
            for dic in self.tabla_transciciones[estado].items():
                if letra in dic[1]:
                    estado = dic[0]
                    bandera = True
                
            if estado in self.estados_finales:
                if int(self.dic_retrocesos[estado]) == 0:
                    break
                if not(bandera):
                    retroceso = int(self.dic_retrocesos[estado])
                    lexema = lexema[:-retroceso]
                    break
            elif not(bandera):
                break
            
            
            
        if estado in self.estados_finales:
            
            if lexema in self.palabras_reservadas.keys():
                tipo = self.palabras_reservadas[lexema]
            else:
                tipo = self.dic_tokens[estado]
            
            self.token = [tipo , lexema , self.linea[0]]
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

auto = crearAutomata("automataProyecto.txt")
#
#Informacion de automata
print(auto.tabla_transciciones)
print(auto.dic_retrocesos)
print(auto.estados_finales)
print(auto.dic_tokens)
print(auto.estado_inicial)
#
#palabras reservadas
auto.guardar_reservadas("palabras_reservadasProyecto.txt")
print(auto.palabras_reservadas)
#
#codigo
auto.guardar_codigo("codigoProyecto1.txt")
for linea in auto.codigo:
    print(linea)


#analizador_lexico
#auto.analex()
#while auto.token != "EOF":
#    print(auto.token)
#    auto.analex()
#
#
#Analizador sintactico LL1 ASDR
#
#
def E2(automata,token):
    if token[0] == "snr":
        ...
    elif token[0] == "enj":
        ...
    elif token[0] == "trt":
        ...
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def OJO(automata,token):
    if token[0] == "dr":
        ...
    elif token[0] == "izq":
        ...
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def CP(automata,token):
    if token[0] == "igualdad":
        ...
    elif token[0] == "desigualdad":
        ...
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def E1(automata,token):
    if token[0] == "abr":
        ...
    elif token[0] == "crr":
        ...
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def PR(automata,token):
    if token[0] == "eoi":
        ...
    elif token[0] == "eod":
        ...
    elif token[0] == "eb":
        ...
    elif token[0] in ["dr","izq"]:
        ...
    elif token[0] in ["abr","crr"]:
        ...
    elif token[0] in ["snr","enj","trt"]:
        ...
    elif token[0] == "numero":
        ...
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def ES_prima(automata,token):
    if token[0] == "fns":
        ...
    elif token[0] == "sino":
        automata.analex()
        token = Z(automata,automata.token)
        if token[0] == "fns":
            ...
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def ES(automata,token):
    if token[0] == "si":
        automata.analex()
        PR(automata,automata.token)
        automata.analex()
        CP(automata,automata.token)
        automata.analex()
        PR(automata,automata.token)
        automata.analex()
        if automata.token[0] == "ents":
            automata.analex()
            token = Z(automata,automata.token)
            ES_prima(automata,token)
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def EC(automata,token):
    if token[0] == "cl":
        automata.analex()
        if automata.token[0] == "numero":
            automata.analex()
            token = Z(automata,automata.token)
            if token[0] == "fc":
                ...
            else:
                manejadorErrores(token[2],"Error sintáctico",automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])


def F2_prima(automata,token):
    if token[0] in ["dr","izq"]:
        OJO(automata,token)
        automata.analex()
        if automata.token[0] == "coma":
            automata.analex()
            if automata.token[0] in ["abr","crr"]:
                E1(automata,automata.token)
                automata.analex()
                if automata.token[0] == "parentesisCierra":
                    ...
                else:
                    manejadorErrores(token[2],"Error sintáctico",automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",automata.token[1])
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    elif token[0] in ["abr","crr"]:
        E1(automata,token)
        automata.analex()
        if automata.token[0] == "parentesisCierra":
            ...
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    else:
       manejadorErrores(token[2],"Error sintáctico",token[1])

def F2(automata,token):
    if token[0] == "ceo":
        automata.analex()
        if automata.token[0] == "parentesisAbre":
            automata.analex()
            if automata.token[0] == "id":
                automata.analex()
                if automata.token[0] == "coma":
                    automata.analex()
                    F2_prima(automata,automata.token)
                else:
                    manejadorErrores(token[2],"Error sintáctico",automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def F1_prima(automata,token):
    if token[0] in {"abr","crr"}:
        E1(automata,token)
        automata.analex()
        if automata.token[0] == "parentesisCierra":
            ...
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    elif token[0] in {"snr","enj","trt"}:
        E2(automata,token)
        automata.analex()
        if automata.token[0] == "parentesisCierra":
            ...
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def F1(automata,token):
    if token[0] == "cc":
        automata.analex()
        if automata.token[0] == "parentesisAbre":
            automata.analex()
            if automata.token[0] == "id":
                automata.analex()
                if automata.token[0] == "coma":
                    automata.analex()
                    if automata.token[0] == "numero":
                        automata.analex()
                        if automata.token[0] == "coma":
                            automata.analex()
                            if automata.token[0] == "numero":
                                automata.analex()
                                if automata.token[0] == "parentesisCierra":
                                    ...
                                else:
                                    manejadorErrores(token[2],"Error sintáctico",automata.token[0])
                            else:
                                manejadorErrores(token[2],"Error sintáctico",automata.token[0])
                        else:
                            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
                    else:
                        manejadorErrores(token[2],"Error sintáctico",automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    elif token[0] == "bc":
        automata.analex()
        if automata.token[0] == "parentesisAbre":
            automata.analex()
            if automata.token[0] == "id":
                automata.analex()
                if automata.token[0] == "parentesisCierra":
                    ...
                else:
                    manejadorErrores(token[2],"Error sintáctico",automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    elif token[0] == "cn":
        automata.analex()
        if automata.token[0] == "parentesisAbre":
            automata.analex()
            if automata.token[0] == "id":
                automata.analex()
                if automata.token[0] == "coma":
                    automata.analex()
                    if automata.token[0] == "id":
                        automata.analex()
                        if automata.token[0] == "parentesisCierra":
                            ...
                        else:
                           manejadorErrores(token[2],"Error sintáctico",automata.token[0])
                    else:
                       manejadorErrores(token[2],"Error sintáctico",automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    elif token[0] == "ceb":
        automata.analex()
        if automata.token[0] == "parentesisAbre":
            automata.analex()
            if automata.token[0] == "id":
                automata.analex()
                if automata.token[0] == "coma":
                    automata.analex()
                    F1_prima(automata,automata.token)
                else:
                    manejadorErrores(token[2],"Error sintáctico",automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def F(automata,token):
    if token[0] in {"cc","bc","cn","ceb"}:
        F1(automata,token)
        return
    elif token[0] == "ceo":
        F2(automata,token)
        return
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def Z(automata,token):
    if token[0] in {"fn","fc","fns","sino"}:
        return token
    elif token[0] in {"cc","bc","cn","ceb","ceo"}:
        F(automata,automata.token)
        automata.analex()
        token = Z(automata,automata.token)
        return token
    elif token[0] == "si":
        ES(automata,automata.token)
        automata.analex()
        token = Z(automata,automata.token)
        return token
    elif token[0] == "cl":
        EC(automata,automata.token)
        automata.analex()
        token = Z(automata,automata.token)
        return token
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])


def I(automata,token):
    if(token[0] == "prg"):
        automata.analex()
        if(automata.token[0] == "id"):
            automata.analex()
            if(automata.token[0] == "ini"):
                automata.analex()
                token = Z(automata,automata.token)
                if token[0] == "fn":
                    ...
                else:
                    manejadorErrores(token[2],"Error sintáctico",automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",automata.token[0])
    else:
        manejadorErrores(token[2],"Error sintáctico",token[0])

def X(automata):
    automata.analex()
    I(automata,automata.token)

X(auto)