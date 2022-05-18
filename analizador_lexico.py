import re

#Errores
class Error_Lexico(Exception):
    def __init__(self,msg):
        super().__init__(msg)
class Error_Sintactico(Exception):
    def __init__(self,msg):
        super().__init__(msg)
class Error_Semantico(Exception):
    def __init__(self,msg):
        super().__init__(msg)

#Manejador de errores
def manejadorErrores(linea,tipo,error):
    if tipo == "Error léxico":
        raise Error_Lexico("Error lexico en la línea " + str(linea) + " el error es: " + error)

    if tipo == "Error sintáctico":
        raise Error_Sintactico("Error sintactico en la línea " + str(linea) + " el  error es: " + error)

    if tipo == "Error semántico":
        raise Error_Semantico("Error semántico en la línea " + str(linea) + " el error es: " + error)

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
            manejadorErrores(self.linea[0],"Error léxico",error)
        

def crearAutomata(ubicacion_archivo):
    automata = Automata()

    archivo = open(ubicacion_archivo)
    lineas = archivo.readlines()
    archivo.close()
    for linea in lineas:
        linea = linea.replace("\n","")##Linea nueva
        if linea.__contains__("***"):
            continue
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
