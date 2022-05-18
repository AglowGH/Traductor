from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.ttk import Labelframe
from analizador_lexico import *
import copy
class Face():

    def create_circle(self,xc,yc,r,color):
        return self.canvas.create_oval(xc-r,yc-r,xc+r,yc+r,fill=color,width=2)   

    def create_semi_circle(self,xc,yc,r,starting_point):
        return self.canvas.create_arc(xc-r,yc-r,xc+r,yc+r,fill="black",width=2,start=starting_point,extent=180)

    def __init__(self,name,xc,yc,canvas):
        self.canvas = canvas
        self.xc = xc
        self.yc = yc
        self.face = self.create_circle(xc,yc,100,"yellow")
        self.name = self.canvas.create_text(xc-30,yc-60,text=name)
        self.left_eye = self.create_circle(xc-50,yc-20,20,"black")
        self.right_eye = self.create_circle(xc+50,yc-20,20,"black")
        self.mouth = self.canvas.create_line(self.xc-25,self.yc+50,self.xc+25,self.yc+50,width=6)
        #self.canvas.pack()
        #Variables of time
        self.time_eoi = 2000
        self.time_eod = 2000
        self.time_eb = 2000

    def set_name(self,name):
        self.canvas.delete(self.name)
        self.name = self.canvas.create_text(self.xc-30,self.yc-60,text=name)

    def set_eyes(self,s,flag):
        if s == 0:
            if flag == 0:
                self.canvas.delete(self.left_eye)
                self.canvas.delete(self.right_eye)
                self.left_eye = self.create_circle(self.xc-50,self.yc-20,20,"black")
                self.right_eye = self.create_circle(self.xc+50,self.yc-20,20,"black")
            elif flag ==1:
                #self.time_eoi -= 2000
                self.canvas.delete(self.left_eye)
                self.left_eye = self.create_circle(self.xc-50,self.yc-20,20,"black")
            elif flag ==2:
                #self.time_eod -= 2000
                self.canvas.delete(self.right_eye)
                self.right_eye = self.create_circle(self.xc+50,self.yc-20,20,"black")
        elif s == 3:
            if flag == 0:
                self.canvas.delete(self.left_eye)
                self.canvas.delete(self.right_eye)
                self.left_eye = self.canvas.create_line(self.xc-70,self.yc-20,self.xc-30,self.yc-20,width=3)
                self.right_eye = self.canvas.create_line(self.xc+30,self.yc-20,self.xc+70,self.yc-20,width=5)
            elif flag ==1:
                #self.time_eoi -= 2000
                self.canvas.delete(self.left_eye)
                self.left_eye = self.canvas.create_line(self.xc-70,self.yc-20,self.xc-30,self.yc-20,width=5)
            elif flag ==2:
                #self.time_eod -= 2000
                self.canvas.delete(self.right_eye)
                self.right_eye = self.canvas.create_line(self.xc+30,self.yc-20,self.xc+70,self.yc-20,width=5)
    
    def delete_face(self):
        self.canvas.delete(self.left_eye)
        self.canvas.delete(self.right_eye)
        self.canvas.delete(self.face)
        self.canvas.delete(self.name)
        if type(self.mouth) == tuple:
            self.canvas.delete(self.mouth[0])
            self.canvas.delete(self.mouth[1])
        else:
            self.canvas.delete(self.mouth)


    def set_mouth(self,flag):
        #self.time_eb -= 2000
        if type(self.mouth) == tuple:
            self.canvas.delete(self.mouth[0])
            self.canvas.delete(self.mouth[1])
        else:
            self.canvas.delete(self.mouth)

        if flag == 0:
            self.mouth = self.create_circle(self.xc,self.yc+50,25,"black")
        elif flag == 1:
            self.mouth = self.create_semi_circle(self.xc,self.yc+50,25,180)
        elif flag == 2:
            self.mouth = self.create_semi_circle(self.xc,self.yc+50,25,0)
        elif flag == 3:
            self.mouth = self.canvas.create_line(self.xc-25,self.yc+50,self.xc+25,self.yc+50,width=6)
        elif flag == 4:
            self.mouth = self.canvas.create_line(self.xc,self.yc+50,self.xc-35,self.yc+75,width=5),self.canvas.create_line(self.xc,self.yc+50,self.xc+35,self.yc+75,width=5)


class Interface():

    def __init__(self,window):        
        self.win = window
        self.frame_editor = LabelFrame(window,text="Editor")
        self.frame_editor.place(x=10,y=60,width=800,height=600)
        self.scroll_editor_y = Scrollbar(self.frame_editor,orient=VERTICAL)
        self.scroll_editor_y.pack(side=RIGHT,fill=Y)
        self.scroll_editor_x = Scrollbar(self.frame_editor,orient=HORIZONTAL)
        self.scroll_editor_x.pack(side=BOTTOM,fill=X)
        self.text_editor = Text(self.frame_editor,font=("Courier",12),yscrollcommand=self.scroll_editor_y.set,xscrollcommand=self.scroll_editor_x.set,wrap=NONE)
        self.text_editor.pack(side=LEFT,fill=Y)
        self.scroll_editor_y.config(command=self.text_editor.yview)
        self.scroll_editor_x.config(command=self.text_editor.xview)
        
        self.frame_errors = Labelframe(window,text="Panel de errores")
        self.frame_errors.place(x=10,y=670,width=800,height=190)
        self.scroll_errors_y = Scrollbar(self.frame_errors,orient=VERTICAL)
        self.scroll_errors_x = Scrollbar(self.frame_errors,orient=HORIZONTAL)
        self.scroll_errors_y.pack(side=RIGHT,fill=Y)
        self.scroll_errors_x.pack(side=BOTTOM,fill=X)
        self.text_error = Text(self.frame_errors,font=("Courier",12),yscrollcommand=self.scroll_errors_y.set,xscrollcommand=self.scroll_errors_x.set,wrap=NONE)
        self.text_error.pack(side=LEFT,fill=Y)
        self.scroll_errors_y.config(command=self.text_error.yview)
        self.scroll_errors_x.config(command=self.text_error.xview)
        
        self.frame_interpret = LabelFrame(window,text="Interprete")
        self.frame_interpret.place(x=820,y=60,width=800,height=800)

        self.frame_options = LabelFrame(window)
        self.frame_options.place(x=10,y=10,width=1610,height=50)
        self.button_1 = Button(self.frame_options,text="Archivo",command=self.read_file)
        self.button_1.pack(side=LEFT,padx=10)
        self.button_2 = Button(self.frame_options,text="Guardar",command=self.save_file)
        self.button_2.pack(side=LEFT,padx=10)
        self.button_3 = Button(self.frame_options,text="Interpretar",command=self.interpret)
        self.button_3.pack(side=LEFT,padx=10)
        self.button_4 = Button(self.frame_options,text="Salir",command=self.exi_t)
        self.button_4.pack(side=RIGHT,padx=10)

        self.canvas = Canvas(self.frame_interpret,height=800,width=800)
        self.canvas.grid()
        
        #Automata
        self.automata = None
        #Variable para leer el archivo de texto
        self.name = ""
        #Tabla de símbolos
        self.simbol_table = None
        #Nombre del programa
        self.program_name = None
        #variable global
        self.name_face = None

    def read_file(self):
        file = askopenfile(mode='r',filetypes=[('JUST TEXT FILES','*.txt')])
        if file is not None:
            content = file.read()
            self.text_editor.delete(1.0,"end")
            self.text_editor.insert(1.0,content)
            self.name = file.name
            self.win.title(self.name)

    def save_file(self):
        file = asksaveasfile(mode="w",filetypes=[('TEXT FILES','*.txt')],defaultextension=[('TEXT FILES','*.txt')])
        if file is not None:
            file.write(self.text_editor.get(1.0,"end"))
            self.name = file.name
            self.win.title(self.name)

    def interpret(self):
        self.name_face = None
        self.simbol_table = {"estadoOjoIzq":"abierto","estadoOjoDer":"abierto","estadoBoca":"cerrado"}
        self.canvas.delete("all")
        self.automata = crearAutomata("automataProyecto.txt")
        self.automata.guardar_reservadas("palabras_reservadasProyecto.txt")
        if self.name != "":
            with open(self.name,"w") as file:
                file.write(self.text_editor.get(1.0,"end"))
                file.close()
            self.automata.guardar_codigo(self.name)
            try:
                self.Ini()
            except Error_Lexico as e:
                self.text_error.delete(1.0,"end")
                self.text_error.insert(1.0,e)
            except Error_Sintactico as e:
                self.text_error.delete(1.0,"end")
                self.text_error.insert(1.0,e)
            except Error_Semantico as e:
                    self.text_error.delete(1.0,"end")
                    self.text_error.insert(1.0,e)
            else:
                self.text_error.delete(1.0,"end")
        else:
            self.save_file()
            if self.name != "":
                with open(self.name,"w") as file:
                    file.write(self.text_editor.get(1.0,"end"))
                    file.close()
                self.automata.guardar_codigo(self.name)
                try:
                    self.Ini()
                except Error_Lexico as e:
                    self.text_error.delete(1.0,"end")
                    self.text_error.insert(1.0,e)
                except Error_Sintactico as e:
                    self.text_error.delete(1.0,"end")
                    self.text_error.insert(1.0,e)
                except Error_Semantico as e:
                    self.text_error.delete(1.0,"end")
                    self.text_error.insert(1.0,e)
                else:
                    self.text_error.delete(1.0,"end")
            else:
                messagebox.showerror("Saving error...","Hay que guardar el archivo antes de su ejecución!!!")

    def exi_t(self):
        self.win.destroy()

    #Analizador sintáctico LL1 ASDR
    def E2(self,token):
        if token[0] == "snr":
            self.simbol_table["estadoBoca"] = "sonriente"
            return 1
        elif token[0] == "enj":
            self.simbol_table["estadoBoca"] = "enojado"
            return 4
        elif token[0] == "trt":
            self.simbol_table["estadoBoca"] = "triste"
            return 2
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])

    def OJO(self,token):
        if token[0] == "dr":
            time = self.simbol_table[self.name_face].time_eod
            self.simbol_table[self.name_face].time_eod += 2000
            return 2,time
        elif token[0] == "izq":
            time = self.simbol_table[self.name_face].time_eod
            self.simbol_table[self.name_face].time_eod += 2000
            return 1,time
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def CP(self,token,elemento):
        if token[0] == "igualdad":
            return (lambda x: x==elemento)
        elif token[0] == "desigualdad":
            return (lambda x: x!=elemento)
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def E1(self,token,part):
        if token[0] == "abr":
            if part == 3:
                self.simbol_table["estadoBoca"] = "abierto"
            elif part == 1:
                self.simbol_table["estadoOjoIzq"] = "abierto"
            elif part == 2:
                self.simbol_table["estadoOjoDer"] = "abierto"
            elif part == 0:
                self.simbol_table["estadoOjoIzq"] = "abierto"
                self.simbol_table["estadoOjoDer"] = "abierto"
            return 0
        elif token[0] == "crr":
            if part == 3:
                self.simbol_table["estadoBoca"] = "cerrado"
            elif part == 1:
                self.simbol_table["estadoOjoIzq"] = "cerrado"
            elif part == 2:
                self.simbol_table["estadoOjoDer"] = "cerrado"
            elif part == 0:
                self.simbol_table["estadoOjoIzq"] = "cerrado"
                self.simbol_table["estadoOjoDer"] = "cerrado"
            return 3
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def PR(self,token):
        if token[0] == "eoi":
            return self.simbol_table["estadoOjoIzq"]
        elif token[0] == "eod":
            return self.simbol_table["estadoOjoDer"]
        elif token[0] == "eb":
            return self.simbol_table["estadoBoca"]
        elif token[0] in ["dr","izq"]:
            return token[1]
        elif token[0] in ["abr","crr"]:
            return token[1]
        elif token[0] in ["snr","enj","trt"]:
            return token[1]
        elif token[0] == "numero":
            return int(token[1])
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def ES_prima(self,token,flag):
        if token[0] == "fns":
            ...
        elif token[0] == "sino":

            if flag:
                #Saltar tokens que no se van a ejecutar
                tokens_list =[]
                while self.automata.token != 'EOF':
                    self.automata.analex()
                    if self.automata.token[0] in ["si","sino"]:
                        tokens_list.append(self.automata.token)
                    elif self.automata.token[0] == "fns":
                        if len(tokens_list) != 0:
                            aux = tokens_list.pop()
                            if aux[0] == "sino":
                                tokens_list.pop()
                        else:
                            token = self.automata.token
                            break
                if self.automata.token == 'EOF':
                    manejadorErrores(" la última línea ","Error sintáctico"," no se cierra")
            
            else:
                self.automata.analex()
                token = self.Z(self.automata.token)

            if token[0] == "fns":
                ...
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def ES(self,token):
        if token[0] == "si":
            self.automata.analex()
            aux_1 = self.PR(self.automata.token)
            self.automata.analex()
            f = self.CP(self.automata.token,aux_1)
            self.automata.analex()
            aux_2 = self.PR(self.automata.token)
            #TODO completar el if statement
            flag = False
            if f(aux_2):
                flag = True
                self.automata.analex()
                if self.automata.token[0] == "ents":
                    self.automata.analex()
                    token = self.Z(self.automata.token)
                else:
                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
            else:
                #Saltar tokens
                tokens_list =[]
                while self.automata.token != 'EOF':
                    self.automata.analex()
                    if self.automata.token[0] in ["si"]:
                        tokens_list.append(self.automata.token)
                    elif self.automata.token[0] == "sino":
                        if len(tokens_list) != 0:
                            tokens_list.append(self.automata.token)
                        else:
                            token = self.automata.token
                            break
                    elif self.automata.token[0] == "fns":
                        if len(tokens_list) != 0:
                            aux = tokens_list.pop()
                            if aux[0] == "sino":
                                tokens_list.pop()
                        else:
                            token = self.automata.token
                            break
                if self.automata.token == 'EOF':
                    manejadorErrores(" la última línea ","Error sintáctico"," no se cierra")

            self.ES_prima(token,flag)#######################################
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def EC(self,token):
        if token[0] == "cl":
            self.automata.analex()
            if self.automata.token[0] == "numero":
                numero = int(self.automata.token[1])
                copy_code = copy.deepcopy(self.automata.codigo)
                copy_linea = copy.deepcopy(self.automata.linea)
                for x in range(0,numero):
                    self.automata.analex()
                    token = self.Z(self.automata.token)

                    if x < numero-1:
                        self.automata.codigo = copy.deepcopy(copy_code)
                        self.automata.linea = copy.deepcopy(copy_linea)
                        continue

                    if token[0] == "fc":
                        pass
                    else:
                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def F2_prima(self,token):
        if token[0] in ["dr","izq"]:
            eye,time = self.OJO(token)
            self.automata.analex()
            if self.automata.token[0] == "coma":
                self.automata.analex()
                if self.automata.token[0] in ["abr","crr"]:
                    action = self.E1(self.automata.token,eye)
                    self.automata.analex()
                    if self.automata.token[0] == "parentesisCierra":
                        self.canvas.after(time,self.simbol_table[self.name_face].set_eyes,action,eye)
                    else:
                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[1])
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        elif token[0] in ["abr","crr"]:
            action = self.E1(token,0)
            self.automata.analex()
            if self.automata.token[0] == "parentesisCierra":
                self.canvas.after(self.simbol_table[self.name_face].time_eoi,self.simbol_table[self.name_face].set_eyes,action,1)
                self.canvas.after(self.simbol_table[self.name_face].time_eod,self.simbol_table[self.name_face].set_eyes,action,2)
                self.simbol_table[self.name_face].time_eoi += 2000
                self.simbol_table[self.name_face].time_eod += 2000
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        else:
           manejadorErrores(token[2],"Error sintáctico",token[1])
    def F2(self,token):
        if token[0] == "ceo":
            self.automata.analex()
            if self.automata.token[0] == "parentesisAbre":
                self.automata.analex()
                if self.automata.token[0] == "id":
                    self.name_face = self.automata.token[1]
                    if self.automata.token[1] not in self.simbol_table.keys() and (self.automata.token[1] not in ["estadoOjoIzq","estadoOjoDer","estadoBoca",self.program_name]):
                        manejadorErrores(self.automata.token[2],"Error semántico"," no hay una cara con el nombre " + self.automata.token[1])
                    self.automata.analex()
                    if self.automata.token[0] == "coma":
                        self.automata.analex()
                        self.F2_prima(self.automata.token)
                    else:
                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def F1_prima(self,token):
        if token[0] in {"abr","crr"}:
            action = self.E1(token,3)
            self.automata.analex()
            if self.automata.token[0] == "parentesisCierra":
                self.canvas.after(self.simbol_table[self.name_face].time_eb,self.simbol_table[self.name_face].set_mouth,action)
                self.simbol_table[self.name_face].time_eb += 2000
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        elif token[0] in {"snr","enj","trt"}:
            action = self.E2(token)
            self.automata.analex()
            if self.automata.token[0] == "parentesisCierra":
                self.canvas.after(self.simbol_table[self.name_face].time_eb,self.simbol_table[self.name_face].set_mouth,action)
                self.simbol_table[self.name_face].time_eb += 2000
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def F1(self,token):
        #Crear cara
        if token[0] == "cc":
            self.automata.analex()
            if self.automata.token[0] == "parentesisAbre":
                self.automata.analex()
                if self.automata.token[0] == "id":
                    name_face = self.automata.token[1]
                    if name_face in self.simbol_table.keys():
                        manejadorErrores(self.automata.token[2],"Error semántico"," el identificador " + name_face + " ya está en uso.")
                    self.automata.analex()
                    if self.automata.token[0] == "coma":
                        self.automata.analex()
                        if self.automata.token[0] == "numero":
                            c_x = int(self.automata.token[1])
                            self.automata.analex()
                            if self.automata.token[0] == "coma":
                                self.automata.analex()
                                if self.automata.token[0] == "numero":
                                    c_y = int(self.automata.token[1])
                                    self.automata.analex()
                                    if self.automata.token[0] == "parentesisCierra":
                                        cara = Face(name_face,c_x,c_y,self.canvas)
                                        self.simbol_table[name_face] = cara
                                    else:
                                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                                else:
                                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                            else:
                                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                        else:
                            manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                    else:
                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        elif token[0] == "bc":#borra cara
            self.automata.analex()
            if self.automata.token[0] == "parentesisAbre":
                self.automata.analex()
                if self.automata.token[0] == "id":
                    name_face = self.automata.token[1]
                    if self.automata.token[1] not in self.simbol_table.keys() and (self.automata.token[1] not in ["estadoOjoIzq","estadoOjoDer","estadoBoca",self.program_name]):
                        manejadorErrores(self.automata.token[2],"Error semántico"," no hay una cara con el nombre " + self.automata.token[1])
                    self.automata.analex()
                    if self.automata.token[0] == "parentesisCierra":
                        time = self.simbol_table[name_face].time_eb
                        if time < self.simbol_table[name_face].time_eoi:
                            time = self.simbol_table[name_face].time_eoi
                        if time <self.simbol_table[name_face].time_eod:
                            time = self.simbol_table[name_face].time_eod
                        
                        self.canvas.after(time+2000,self.simbol_table[name_face].delete_face)
                        #self.canvas.after(time+2000,self.canvas.delete,self.simbol_table[name_face].right_eye)
                        #self.canvas.after(time+2000,self.canvas.delete,self.simbol_table[name_face].face)
                        #self.canvas.after(time+2000,self.canvas.delete,self.simbol_table[name_face].name)
                        #if type(self.simbol_table[name_face].mouth) == tuple:
                        #    self.canvas.after(time+2000,self.canvas.delete,self.simbol_table[name_face].mouth[0])
                        #    self.canvas.after(time+2000,self.canvas.delete,self.simbol_table[name_face].mouth[1])
                        #else:
                        #    self.canvas.after(time+2000,self.canvas.delete,self.simbol_table[name_face].mouth)

                        self.simbol_table.pop(name_face)
                    else:
                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        elif token[0] == "cn":#cambiar nombre
            self.automata.analex()
            if self.automata.token[0] == "parentesisAbre":
                self.automata.analex()
                if self.automata.token[0] == "id":
                    name_face = self.automata.token[1]
                    if self.automata.token[1] not in self.simbol_table.keys() and (self.automata.token[1] not in ["estadoOjoIzq","estadoOjoDer","estadoBoca",self.program_name]):
                        manejadorErrores(self.automata.token[2],"Error semántico"," no hay una cara con el nombre " + self.automata.token[1])
                    self.automata.analex()
                    if self.automata.token[0] == "coma":
                        self.automata.analex()
                        if self.automata.token[0] == "id":
                            new_name_face = self.automata.token[1]
                            if new_name_face in self.simbol_table.keys():
                                manejadorErrores(self.automata.token[2],"Error semántico"," el identificador " + name_face + " ya está en uso.")
                            self.automata.analex()
                            if self.automata.token[0] == "parentesisCierra":
                                time = self.simbol_table[name_face].time_eb
                                if time < self.simbol_table[name_face].time_eoi:
                                    time = self.simbol_table[name_face].time_eoi
                                if time <self.simbol_table[name_face].time_eod:
                                    time = self.simbol_table[name_face].time_eod

                                cara = self.simbol_table[name_face]
                                self.simbol_table.pop(name_face)
                                self.simbol_table[new_name_face] = cara
                                self.canvas.after(time+2000,self.simbol_table[new_name_face].set_name,new_name_face)
                            else:
                               manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                        else:
                           manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                    else:
                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        elif token[0] == "ceb":
            self.automata.analex()
            if self.automata.token[0] == "parentesisAbre":
                self.automata.analex()
                if self.automata.token[0] == "id":
                    self.name_face = self.automata.token[1]
                    if self.name_face not in self.simbol_table.keys():
                        manejadorErrores(self.automata.token[2],"Error semántico","la cara con el identificador " + self.name_face + " no existe.")
                    if self.name_face in ["estadoOjoIzq","estadoOjoDer","estadoBoca",self.program_name]:
                        manejadorErrores(self.automata.token[2],"Error semántico"," el identificador " + self.name_face + " no pertenece a una cara.")
                    self.automata.analex()
                    if self.automata.token[0] == "coma":
                        self.automata.analex()
                        self.F1_prima(self.automata.token)
                    else:
                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def F(self,token):
        if token[0] in {"cc","bc","cn","ceb"}:
            self.F1(token)
            return
        elif token[0] == "ceo":
            self.F2(token)
            return
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def Z(self,token):
        if token[0] in {"fn","fc","fns","sino"}:
            return token
        elif token[0] in {"cc","bc","cn","ceb","ceo"}:
            self.F(self.automata.token)
            self.automata.analex()
            token = self.Z(self.automata.token)
            return token
        elif token[0] == "si":
            self.ES(self.automata.token)
            self.automata.analex()
            token = self.Z(self.automata.token)
            return token
        elif token[0] == "cl":
            self.EC(self.automata.token)
            self.automata.analex()
            token = self.Z(self.automata.token)
            return token
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])
    def I(self,token):
        if(token[0] == "prg"):
            self.automata.analex()
            if(self.automata.token[0] == "id"):
                self.simbol_table[self.automata.token[1]] = self.automata.token[1]#
                self.program_name = self.automata.token[1]
                self.automata.analex()
                if(self.automata.token[0] == "ini"):
                    self.automata.analex()
                    token = self.Z(self.automata.token)
                    if token[0] == "fn":
                        print("¡¡¡¡Programa concluido con éxito!!!!")
                    else:
                        manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
                else:
                    manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
            else:
                manejadorErrores(token[2],"Error sintáctico",self.automata.token[0])
        else:
            manejadorErrores(token[2],"Error sintáctico",token[0])

    def Ini(self):
        self.automata.analex()
        self.I(self.automata.token)


