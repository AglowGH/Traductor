#cadena = "abcde"

#for letra in cadena:
#    print(letra)
#    cadena = cadena[1:]
#    print(cadena)

#import re

#cadena = "  como        HDGD(*6445--++-- c  ++//???       45\n"
#pattern = re.compile(r'(?P<lexema>[^\s]+)')
#pattern ='              '
#resultado = re.findall(pattern,cadena)
#print(resultado)

#print([5,1] == [1,5])

#cadena = "hola mundo"
#cadena = cadena[:-2]
#print(cadena)

#dicc = {'2':'a','3':'b'}
#r = dicc.keys()
#print(('3' in r))

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
                
        if estado in self.estados_finales:
            if int(self.dic_retrocesos[estado]) == 0:
                break
            if not(bandera):
                retroceso = int(self.dic_retrocesos[estado])
                lexema = lexema[:-retroceso]
                break
            
        error += letra
            
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
        #manejadorErrores(self.linea[0],"Error lexico",error)
        ...

#copy
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
            
            self.token = [tipo , lexema , self.linea[0]]
            self.codigo[0][0] = self.codigo[0][0].replace(lexema,"",1)

            if self.codigo[0][0] == '':
                self.codigo[0].pop(0)
            if self.codigo[0] == []:
                self.codigo.pop(0)
                self.linea.pop(0)
        else:
             manejadorErrores(self.linea[0],"Error lexico",error)