from GUI_main import GUIMain

class Main:

    def __init__(self):
        self.programa = GUIMain()
        self.programa.panel_de_control.palabra_test.widgets[1].exe_presionar_boton = self.apd_acepta
        self.programa.mainloop()

    def apd_acepta(self):
        self.programa.update_idletasks()

        transiciones = self.programa.extraer_transiciones()
        palabra = self.programa.panel_de_control.palabra_test.widgets[0].stringVar.get()

        simbolo_pila = self.programa.panel_de_control.simbolos_def.widgets[0][0].stringVar.get()
        simbolo_vacio = self.programa.panel_de_control.simbolos_def.widgets[1][0].stringVar.get()
        stack_vacio = self.programa.panel_de_control.criterio_aceptacion.widgets[0].booleanVar.get()

        estado_inicial = self.programa.estado_inicial
        estado_final = self.programa.estado_final

        pila = [simbolo_pila]
        estado = estado_inicial
        i = 0
        feedback = "("
        while True:
            pila_actual = ''.join(pila[::-1])
            palabra_actual = palabra[i:]

            feedback += f"{estado}, {palabra_actual if palabra_actual else simbolo_vacio}, {pila_actual if pila_actual else simbolo_vacio})"

            simbolo_entrada = palabra[i] if i < len(palabra) else simbolo_vacio
            tope_pila = pila.pop() if pila else simbolo_vacio

            if  stack_vacio and tope_pila == simbolo_vacio: 
                print(f"{feedback} [{simbolo_vacio}: Stack Vacio]\nAceptada")
                return True
            if estado == estado_final:
                print(f"{feedback} [{estado}: Estado Final]\nAceptada")
                return True

            clave = (estado, simbolo_entrada, tope_pila)
            if clave not in transiciones:
                # la tupla de entrada no existe
                print(f"{feedback}|--- X\nRechazada")
                return False

            nuevo_estado, apilar = transiciones[clave]
            estado = nuevo_estado
            feedback += "|---("

            if apilar != simbolo_vacio:
                for simbolo in reversed(apilar): pila.append(simbolo)

            i += 1

if __name__ == "__main__":
    Main()