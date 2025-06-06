import tkinter as tk

from GUI_tkModulo import tkTools

DEF_N:int = 3
'''
Números de campos de entrada de la función:

DEF_N = n <=> f(x1, x2, ..., xn)
'''

DEF_M:int = 2
'''
Número de campos de salida de la función.

DEF_M = m <=> (y1, y2, ..., ym)
'''

DEF_CAMPOS:int = DEF_N + DEF_M
'''Número de campos necesarios para describir la función.'''

DEF_INI_FILAS:int = 2
'''Número de filas al iniciar el programa.'''

DEF_SIMBOLO_STACK = "R"
'''Símbolo base del stack.'''

DEF_SIMBOLO_VACIO = "E"
'''Símbolo de la palabra vacía.'''

DEF_ESTADO_INICIAL = "q0"
'''Estado inicial del APD.'''

# Bajo el contexto de Autómatas Push Down (APD),
# este programa recibe a través de una interfaz
# grafíca, una función de transición de la forma:
#
# f(x1, x2, ..., xn)=(y1, y2, ..., ym) | con n>0 y m>0
#
# y verifica si una cadena de simbolos
# pertence o no al APD definido.

class GUIPanelDeControl(tk.Frame):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):

        super().__init__(master, **kwargs)
        tkTools.configurar_pesos(self, {0:1, 1:1, 2:1, 3:1, 4:1}, {0:0})

        '''Marco de botones y panel de control.'''
        self.botones_anadir_eliminar_frame = tk.LabelFrame(self, text="Manejar Número de Transiciones:")
        tkTools.configurar_pesos(self.botones_anadir_eliminar_frame, {0:0}, {0:1})
        self.botones_anadir_eliminar = tkTools.BotoneraHorizontal(self.botones_anadir_eliminar_frame, ["Añadir fila", "Eliminar fila"])
        
        self.botones_anadir_eliminar.grid(row=0, column=0, sticky=tk.NSEW)
        self.botones_anadir_eliminar_frame.grid(row=0, column=0, sticky=tk.NSEW, ipadx=5, ipady=5, padx=5, pady=5)

        '''Marco en el que se definirán los simbolos por defecto del stack y para el simbolo vacío.'''
        self.simbolos_def_frame = tk.LabelFrame(self, text="Simbolos especiales:")
        tkTools.configurar_pesos(self.simbolos_def_frame, {0:0}, {0:1})
        self.simbolos_def = tkTools.EntradasVertical(self.simbolos_def_frame, ["Simbolo inicial Stack", "Simbolo palabra vacia", "Estado inicial"])

        self.simbolos_def.widgets[0][0].exe_focus_out = self._focus_out_simbolo_stack
        self.simbolos_def.widgets[1][0].exe_focus_out = self._focus_out_simbolo_vacio
        self.simbolos_def.widgets[2][0].exe_focus_out = self._focus_out_estado_inicial

        self.simbolos_def.grid(row=0, column=0)
        self.simbolos_def_frame.grid(row=1, column=0, sticky=tk.NSEW, ipadx=5, ipady=5, padx=5, pady=5)

        '''Marco en el que se definirán el criterio de aceptación del APD.'''
        self.criterio_aceptacion_frame = tk.LabelFrame(self, text="Criterio de aceptacion:")
        tkTools.configurar_pesos(self.criterio_aceptacion_frame, {0:0}, {0:1})
        self.criterio_aceptacion = tkTools.ChecksVertical(self.criterio_aceptacion_frame, ["Stack vacío.", "Estado final:"])

        self.criterio_aceptacion.widgets[1].exe_al_clickear = self._es_estado_final
        
        self.criterio_aceptacion.grid(row=0, column=0)
        self.criterio_aceptacion_frame.grid(row=2, column=0, sticky=tk.NSEW, ipadx=5, ipady=5, padx=5, pady=5)

        '''Marco en el que se definirán el estado final del APD en caso de tener activado el criterio de aceptación correspondiente.'''
        self.estado_final = tkTools.Entry(self.criterio_aceptacion, justify=tk.CENTER)
        self.estado_final.exe_focus_out = self._focus_out_estado_final
        tkTools.configurar_pesos(self.criterio_aceptacion, {2:0}, {0:1})
        self.estado_final.grid(row=2, column=0)
        self.estado_final.config(width=tkTools.px_to_entry_chars(self.estado_final, self.criterio_aceptacion.widgets[0].winfo_reqwidth()))

        '''Marco en el que se ingresará palabra a comprobar en el APD definido.'''
        self.palabra_test = tkTools.EntradaYBotonVertical(self, text="Verificar palabra")
        self.palabra_test.grid(row=4, column=0, sticky=tk.NSEW)

        self.criterio_aceptacion.widgets[1].exe_al_clickear()

    def _focus_out_simbolo_stack(self, *_):
        if not self.simbolos_def.widgets[0][0].stringVar.get():
            self.simbolos_def.widgets[0][0].stringVar.set(DEF_SIMBOLO_STACK)

    def _focus_out_simbolo_vacio(self, *_):
        if not self.simbolos_def.widgets[1][0].stringVar.get():
            self.simbolos_def.widgets[1][0].stringVar.set(DEF_SIMBOLO_VACIO)

    def _focus_out_estado_inicial(self, *_):
        if not self.simbolos_def.widgets[2][0].stringVar.get():
            self.simbolos_def.widgets[2][0].stringVar.set(DEF_ESTADO_INICIAL)

    def _focus_out_estado_final(self, *_):
        if not self.estado_final.stringVar.get() and self.criterio_aceptacion.widgets[1].booleanVar.get():
            self.estado_final.stringVar.set(DEF_ESTADO_INICIAL)

    def _es_estado_final(self, *_):
        if self.criterio_aceptacion.widgets[1].booleanVar.get():
            self.estado_final.config(state=tk.NORMAL)
            self.estado_final.stringVar.set(DEF_ESTADO_INICIAL)
        else:
            self.estado_final.config(state=tk.DISABLED)
            self.estado_final.stringVar.set("")

class GUIVisualizacionApd(tk.Frame):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):

        self.transiciones:dict[tuple[list[tkTools.Entry|tkTools.Label]], tuple[list[tkTools.Entry|tkTools.Label]]] = {}
        '''
        Diccionario de transiciones definido en el informe.

        self.transiciones = {
            (x1.1, x1.2, ..., x1.n):(y1.1, y1.2, ..., y1.m),
            (x2.1, x2.2, ..., x2.n):(y2.1, y2.2, ..., y2.m),
            ...
            (xf.1, xf.2, ..., xf.n):(yn.1, yn.2, ..., yf.m)
        }
        '''

        super().__init__(master, **kwargs)
        tkTools.configurar_pesos(self, {0:0, 1:1}, {0:0})

        '''Marco contenedor de la matriz de widgets de entrada y etiquetas.'''
        self.entradas_apd:tkTools.EntryLabelMatriz = tkTools.EntryLabelMatriz(self, def_filas=2, esquema="δ(0,0,0)=(0,0)")
        self.entradas_apd.configurar_scrollbars_visibles(True, False)
        self.entradas_apd.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.info_apd:tkTools.ScrollableFrame = tkTools.ScrollableFrame(self)
        tkTools.configurar_pesos(self.info_apd, {0:1}, {0:1})
        self.info_apd.lienzo_dibujo.config(background="white")
        self.info_apd.configurar_scrollbars_visibles(True, False)
        self.info_apd.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        '''Marco de la información del APD extraida GUI.'''
        self.label:tkTools.Label = tkTools.Label(self.info_apd)
        self.label.config(background="white")
        self.label.grid(row=0, column=0, sticky=tk.NSEW)

        tkTools.actualizar_widget(self)

    def extraer_transiciones(self, n:int=1, m:int=1) -> dict[tuple,tuple]:
        '''Método retorna una diccionario 'self.transiciones' con las transiciones del APD.'''
        self.transiciones = {}
        for fila in range(len(self.entradas_apd.widgets)):
            entradas = tkTools.filtrar_por_tipo(self.entradas_apd.widgets[fila], tkTools.Entry)
            textos = [entrada.stringVar.get().strip() for entrada in entradas]

            key = tuple(textos[:n])
            valor = tuple(textos[n:n+m])
            self.transiciones[key] = valor

class GUIMain:

    def __init__(self):
        self.estados:list[str] = []
        self.alfabeto_apd:list[str] = []
        self.alfabeto_stack: list[str] = []

        '''Ventana principal del programa.'''
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Simulador - APD")

        tkTools.configurar_pesos(self.ventana_principal, {0:1}, {0:1, 1:0})

        '''Marco donde se construirá el APD basado en sus transiciones.'''        
        self.visualizacion_apd = GUIVisualizacionApd(self.ventana_principal)
        self.visualizacion_apd.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        '''Marco donde se controlarán los parametros para la construcción del APD.'''        
        self.panel_de_control = GUIPanelDeControl(self.ventana_principal)
        self.panel_de_control.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

        self.panel_de_control.botones_anadir_eliminar.widgets[0].exe_presionar_boton = self._anadir_fila
        self.panel_de_control.botones_anadir_eliminar.widgets[1].exe_presionar_boton = self._eliminar_fila

        self.panel_de_control.simbolos_def.widgets[0][0].exe_al_escribir = self._actualizar_info_apd
        self.panel_de_control.simbolos_def.widgets[0][0].actualizar_limite_caracteres(1, True)
        self.panel_de_control.simbolos_def.widgets[0][0].exe_focus_out()
        self.panel_de_control.simbolos_def.widgets[0][0].config(width=10)

        self.panel_de_control.simbolos_def.widgets[1][0].exe_al_escribir = self._actualizar_info_apd
        self.panel_de_control.simbolos_def.widgets[1][0].actualizar_limite_caracteres(1, True)
        self.panel_de_control.simbolos_def.widgets[1][0].exe_focus_out()
        self.panel_de_control.simbolos_def.widgets[1][0].config(width=10)

        self.panel_de_control.simbolos_def.widgets[2][0].exe_al_escribir = self._actualizar_info_apd
        self.panel_de_control.simbolos_def.widgets[2][0].actualizar_limite_caracteres(-1, True)
        self.panel_de_control.simbolos_def.widgets[2][0].exe_focus_out()
        self.panel_de_control.simbolos_def.widgets[2][0].config(width=10)

        self.panel_de_control.estado_final.exe_al_escribir = self._actualizar_info_apd
        self.panel_de_control.estado_final.actualizar_limite_caracteres(-1, True)
        self.panel_de_control.estado_final.exe_focus_out()

        self.panel_de_control.palabra_test.widgets[0].actualizar_limite_caracteres(-1, True)
        self.panel_de_control.palabra_test.widgets[1].exe_presionar_boton = self.extraer_estados

        for _ in range(DEF_INI_FILAS): self._anadir_fila()

        '''Configración en proporciones para dimensiones del programa.'''
        tkTools.actualizar_widget(self.ventana_principal)
        self.visualizacion_apd.label.config(justify=tk.LEFT)

        self.visualizacion_apd.entradas_apd.lienzo_dibujo.config(width=self.visualizacion_apd.entradas_apd.winfo_reqwidth())
        alto_total, ancho_total = tkTools.calcular_dimensiones([self.visualizacion_apd.entradas_apd.lienzo_dibujo, self.visualizacion_apd.label], [self.visualizacion_apd.entradas_apd, self.panel_de_control.simbolos_def], margen_extra_h=100, margen_extra_v=50)
        self.ventana_principal.geometry(f"{ancho_total}x{alto_total}")
        self.ventana_principal.resizable(False, False)

        '''Configración extra y loop principal.'''
        self.ventana_principal.bind_all("<Button-1>", self._focus_on_click, add='+')
        self.ventana_principal.mainloop()

    def _focus_on_click(self, event:tk.Event):
        '''Actualiza el focus de la App al Widget que fue clieckeado.'''
        widget:tk.Widget = event.widget
        try: widget.focus_set()
        except: self.ventana_principal.focus_set()
        pass

    def _anadir_fila(self, *_):
        self.visualizacion_apd.entradas_apd.anadir_fila()
        filas = len(self.visualizacion_apd.entradas_apd.widgets)

        if filas > 1: self.panel_de_control.botones_anadir_eliminar.widgets[1].config(state=tk.NORMAL)
        else: self.panel_de_control.botones_anadir_eliminar.widgets[1].config(state=tk.DISABLED)

        tkTools.actualizar_widget(self.visualizacion_apd.entradas_apd)
        self.visualizacion_apd.entradas_apd.actualizar_scrollregion()
        self._actualizar_info_apd()

        self.visualizacion_apd.entradas_apd.actualizar_entradas(filas, 2, sin_espacios=True, exe_al_escribir=self._actualizar_info_apd)
        self.visualizacion_apd.entradas_apd.actualizar_entradas(filas, 4, limite_caracteres=1, sin_espacios=True, exe_al_escribir=self._actualizar_info_apd)
        self.visualizacion_apd.entradas_apd.actualizar_entradas(filas, 6, limite_caracteres=1, sin_espacios=True, exe_al_escribir=self._actualizar_info_apd)
        self.visualizacion_apd.entradas_apd.actualizar_entradas(filas, 8, sin_espacios=True, exe_al_escribir=self._actualizar_info_apd)
        self.visualizacion_apd.entradas_apd.actualizar_entradas(filas, 10, sin_espacios=True, exe_al_escribir=self._actualizar_info_apd)

    def _eliminar_fila(self, *_):
        self.visualizacion_apd.entradas_apd.eliminar_fila()

        if len(self.visualizacion_apd.entradas_apd.widgets) <=1: self.panel_de_control.botones_anadir_eliminar.widgets[1].config(state=tk.DISABLED)
        else: self.panel_de_control.botones_anadir_eliminar.widgets[1].config(state=tk.NORMAL)

        tkTools.actualizar_widget(self.visualizacion_apd.entradas_apd)
        self.visualizacion_apd.entradas_apd.actualizar_scrollregion()
        self._actualizar_info_apd()

    def _actualizar_info_apd(self, *_):
        self.visualizacion_apd.label.actualizar_wraplength(self.visualizacion_apd.info_apd.lienzo_dibujo)
        self.visualizacion_apd.label.stringVar.set(f"Estados: {self.extraer_estados()}\nAlfabeto APD: {self.extraer_alfabeto_apd()}\nAlfabeto Stack: {self.extraer_alfabeto_stack()}")
        self.visualizacion_apd.info_apd.actualizar_scrollregion()

    def extraer_estados(self):
        estados:list = []

        estado_temp = self.panel_de_control.estado_final.stringVar.get()
        estados.append(estado_temp)

        estado_temp = self.panel_de_control.simbolos_def.widgets[2][0].stringVar.get()
        if not estado_temp: estado_temp = DEF_ESTADO_INICIAL
        estados.append(estado_temp)

        estado_temp = self.visualizacion_apd.entradas_apd.extraer_widgets(0, 2)
        for estado in estado_temp: estados.append(estado.stringVar.get())

        estado_temp = self.visualizacion_apd.entradas_apd.extraer_widgets(0, 8)
        for estado in estado_temp: estados.append(estado.stringVar.get())

        self.estados = list(dict.fromkeys(estado for estado in estados if estado and str(estado).strip()))
        return self.estados

    def extraer_alfabeto_apd(self):
        alfabeto_apd:list = []

        alfabeto_temp = self.visualizacion_apd.entradas_apd.extraer_widgets(0, 4)
        for widget in alfabeto_temp: alfabeto_apd.append(widget.stringVar.get())

        self.alfabeto_apd = list(dict.fromkeys(simbolo for simbolo in alfabeto_apd if simbolo and str(simbolo).strip()))
        return self.alfabeto_apd

    def extraer_alfabeto_stack(self):
        alfabeto_stack:list = []

        alfabeto_stack.append(self.panel_de_control.simbolos_def.widgets[0][0].stringVar.get())

        alfabeto_temp = self.visualizacion_apd.entradas_apd.extraer_widgets(0, 6)
        for widget in alfabeto_temp: alfabeto_stack.append(widget.stringVar.get())

        alfabeto_temp = self.visualizacion_apd.entradas_apd.extraer_widgets(0, 10)
        for widget in alfabeto_temp: alfabeto_stack.extend(list(set(widget.stringVar.get())))

        self.alfabeto_stack = list(dict.fromkeys(simbolo for simbolo in alfabeto_stack if simbolo and str(simbolo).strip()))
        return self.alfabeto_stack

if __name__ == "__main__":
    GUIMain()
