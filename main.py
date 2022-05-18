from gui import *

window = Tk()
window.geometry("1630x880")
window.title("Interprete")
window.resizable(False,False)
window.iconphoto(False,PhotoImage(file="icono.png"))
i = Interface(window)
window.mainloop()