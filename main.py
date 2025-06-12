import tkinter as tk

from gui_app import GUIMain
from gui_tkinter import tkTools, tkWidgets

DESC_BOX = "[=========][Descripcion instantanea][=========]"

class Main:

    def __init__(self):
        self.__verbose:tuple[bool, bool] = (False, True)

        self.programa = GUIMain()
        self.programa.panel_de_control.palabra_test.widgets[1].exe_presionar_boton = self.verificar_palabra_apd
        self.programa.mainloop()

    @property
    def verbose(self):
        return self.__verbose
    
    @verbose.setter
    def verbose(self, verb:tuple[bool, bool]):
        self.__verbose = verb

    def verificar_palabra_apd(self):

        def print_feedback(feed:str = ""):
            '''Imprime feedback según atributos de clase.'''
            if self.__verbose[0]: print(feed)
            if self.__verbose[1]: self.mostrar_feedback(feed)

        self.programa.update_idletasks()

        transiciones = self.programa.extraer_transiciones()
        palabra = self.programa.panel_de_control.palabra_test.widgets[0].stringVar.get()

        simbolo_pila = self.programa.panel_de_control.simbolos_def.widgets[0][0].stringVar.get()
        simbolo_vacio = self.programa.panel_de_control.simbolos_def.widgets[1][0].stringVar.get()
        stack_vacio = self.programa.panel_de_control.criterio_aceptacion.widgets[0].booleanVar.get()

        estado_actual = self.programa.estado_inicial
        estado_final = self.programa.estado_final

        pila = [simbolo_pila]
        i = 0
        feedback = f"{DESC_BOX}\n\n"
        descripciones = []
        while True:
            pila_actual = ''.join(pila[::-1])
            palabra_actual = palabra[i:]

            desc_inst = (estado_actual, palabra_actual if palabra_actual else simbolo_vacio, pila_actual if pila_actual else simbolo_vacio)
            feedback += f"{desc_inst}"
            simbolo_entrada = palabra[i] if i < len(palabra) else simbolo_vacio
            tope_pila = pila.pop() if pila else simbolo_vacio

            print(desc_inst)

            if  stack_vacio and tope_pila == simbolo_vacio:
                print_feedback(feedback + f"\n\n{DESC_BOX}\n\n[{simbolo_vacio}: Stack Vacio]\n\nPalabara ACEPTADA")
                return True

            if estado_actual == estado_final:
                print_feedback(feedback + f"\n\n{DESC_BOX}\n\n[{estado_actual}: Estado Final]\n\nPalabara ACEPTADA")
                return True

            if (estado_actual, simbolo_entrada, tope_pila) not in transiciones:
                print_feedback(feedback + f"|---X\n\n{DESC_BOX}\n\n[No existe función de transición para los parametros de entrada]\n\nPalabara RECHAZADA")
                return False
            
            if desc_inst in descripciones:
                print_feedback(feedback + f"|---X\n\n{DESC_BOX}\n\n[Ciclo: {desc_inst}|--- * {desc_inst}]\n\nPalabara RECHAZADA")
                return False
            
            else: descripciones.append(desc_inst)

            nuevo_estado, apilar = transiciones[(estado_actual, simbolo_entrada, tope_pila)]
            estado_actual = nuevo_estado

            if apilar != simbolo_vacio:
                for simbolo in reversed(apilar): pila.append(simbolo)

            i += 1
            feedback += "|---\n"

    def mostrar_feedback(self, feedback:str):
        ventana = tk.Toplevel(self.programa)

        tkTools.configurar_pesos(ventana, {0: 1, 1: 0}, {0: 1})
        ventana.title("Resultado de la ejecución")
        ventana.transient(self.programa)
        ventana.grab_set()

        scroll = tkWidgets.ScrollableFrame(ventana)
        tkTools.configurar_pesos(scroll, {0:1}, {0:1})
        scroll.configurar_scrollbars_visibles(True, False)
        scroll.grid(row=0, column=0, pady=5, sticky=tk.NSEW)

        text = tk.Text(scroll, wrap=tk.WORD)
        text.insert("1.0", feedback)
        text.config(state=tk.DISABLED)
        text.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        btn_cerrar = tk.Button(ventana, text="Continuar", command=ventana.destroy)
        btn_cerrar.grid(row=1, column=0, pady=5)

        ventana.update_idletasks()
        scroll.lienzo_dibujo.config(width=text.winfo_reqwidth())
        ventana.maxsize(text.winfo_reqwidth(), ventana.winfo_height())

        ventana.wait_window()


if __name__ == "__main__":
    Main()