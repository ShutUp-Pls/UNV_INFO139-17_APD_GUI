import tkinter as tk

from GUI_tkinter import TkTools

# Bajo el contexto de Autómatas Push Down (APD),
# este programa recibe a través de una interfaz
# grafíca, una función de transición de la forma:
#
# f(x1, x2, ..., xn)=(y1, y2, ..., ym) | con n>0 y m>0
#
# y verifica si una cadena de simbolos
# pertence o no al APD definido.

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

class AppGUI:

    def __init__(self):

        self.matriz_entradas:list[list] = []
        '''
        Matriz de tk.Entry dentro de la interfaz gráfica.

        self.matriz_entradas = [
            [tk.Entry-1.1, tk.Entry-1.2, ..., tk.Entry-1.n],
            [tk.Entry-2.1, tk.Entry-2.2, ..., tk.Entry-2.n],
            ...
            [tk.Entry-1.m, tk.Entry-2.m, ..., tk.Entry-n.m]
        ]
        '''

        self.matriz_strings:list[list] = []
        '''
        Matriz de tk.StringVar dentro de la interfaz gráfica.

        self.matriz_strings = [
            [tk.StringVar-1.1, tk.StringVar-1.2, ..., tk.StringVar-1.n],
            [tk.StringVar-2.1, tk.StringVar-2.2, ..., tk.StringVar-2.n],
            ...
            [tk.StringVar-1.m, tk.StringVar-2.m, ..., tk.StringVar-n.m]
        ]
        '''

        self.ventana_principal:tk.Tk = None
        def ventana_principal():
            '''Ventana principal del programa.'''
            self.ventana_principal = tk.Tk()

            self.ventana_principal.title("Simulador - APD")
            self.ventana_principal.resizable(True, True)

            TkTools.configurar_pesos(self.ventana_principal, {0:0}, {0:1, 1:0})

        self.marco_construccion:tk.Frame = None
        def marco_construccion():
            '''Marco donde se construirá el APD basado en sus transiciones.'''        
            self.marco_construccion = tk.Frame(self.ventana_principal)
            TkTools.configurar_pesos(self.marco_construccion, {0:1, 1:0}, {0:1})
            self.marco_construccion.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.marco_panel_de_control:tk.Frame = None
        def marco_panel_de_control():
            '''Marco donde se controlarán los parametros para la construcción del APD.'''        
            self.marco_panel_de_control = tk.Frame(self.ventana_principal)
            TkTools.configurar_pesos(self.marco_panel_de_control, {0:0, 1:0}, {0:0})
            self.marco_panel_de_control.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

        self.marco_canvas_scrollbars:tk.Frame = None
        def marco_canvas_scrollbars():
            '''Marco de canvas con scrollbar.'''        
            self.marco_canvas_scrollbars = tk.Frame(self.marco_construccion)
            TkTools.configurar_pesos(self.marco_canvas_scrollbars, {0:1, 1:0}, {0:1, 1:0})
            self.marco_canvas_scrollbars.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.canvas:tk.Canvas = None
        def canvas():
            '''Marco de dibujo compatible con las scrollbars.'''
            self.canvas = tk.Canvas(self.marco_canvas_scrollbars, borderwidth=0)
            self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        self.marco_canvas:tk.Frame = None
        def marco_canvas():
            '''Marco al interior del marco de dibujo.'''
            self.marco_canvas = tk.Frame(self.canvas)

        self.scrollbar_v:tk.Scrollbar = None
        def scrollbar_v():
            '''Scrollbar vertical en el marco de dibujo'''
            self.scrollbar_v = tk.Scrollbar(self.marco_canvas_scrollbars, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar_v.grid(row=0, column=1, sticky=tk.NS)

        self.scrollbar_h:tk.Scrollbar = None
        def scrollbar_h():
            '''Scrollbar horizontal en el marco de dibujo'''
            self.scrollbar_h = tk.Scrollbar(self.marco_canvas_scrollbars, orient=tk.HORIZONTAL, command=self.canvas.xview)
            self.scrollbar_h.grid(row=1, column=0, sticky=tk.EW)

        self.marco_info_apd:tk.Frame = None
        def marco_info_apd():
            '''Marco de la información del APD extraida GUI.'''
            self.marco_info_apd = tk.Frame(self.marco_construccion)
            TkTools.configurar_pesos(self.marco_info_apd, {0:0}, {0:0})
            self.marco_info_apd.grid(row=1, column=0, sticky=tk.NSEW)

        self.transiciones:dict[tuple, tuple] = {}
        self.estados:list[str] = []
        self.alfabeto_lenguaje:list[str] = []
        self.alfabeto_stack:list[str] = []

        self.simbolo_vacio = DEF_SIMBOLO_VACIO
        self.simbolo_stack = DEF_SIMBOLO_STACK

        self.texto_info_apd:tk.StringVar = None
        self.etiqueta_info_apd:tk.Label = None
        def etiqueta_texto_info_apd():
            '''Etiqueta de la información del APD extraida GUI.'''
            self.texto_info_apd = tk.StringVar()
            self._actualizar_texto_info_apd()
            self.etiqueta_info_apd = tk.Label(self.marco_info_apd, textvariable=self.texto_info_apd)
            self.etiqueta_info_apd.grid(row=0, column=0, sticky=tk.NSEW)

        self.marco_botones:tk.Frame = None
        def marco_botones():
            '''Marco de botones y panel de control.'''
            self.marco_botones = tk.Frame(self.marco_panel_de_control)
            TkTools.configurar_pesos(self.marco_botones, {0:0, 1:0}, {0:1, 1:0, 2:0, 3:1})
            self.marco_botones.grid(row=0, column=0, sticky=tk.NSEW)

        self.boton_anadir:tk.Button = None
        def boton_anadir():
            '''Boton para añadir fila al GUI.'''
            self.boton_anadir = tk.Button(self.marco_botones, text="Añadir fila", command=self.anadir_fila)
            self.boton_anadir.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        self.boton_eliminar:tk.Button = None
        def boton_eliminar():
            '''Botón para eliminar última fila del GUI.'''
            self.boton_eliminar = tk.Button(self.marco_botones, text="Eliminar fila", command=self.eliminar_fila)
            self.boton_eliminar.grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)

        self.boton_imprimir_transiciones:tk.Button = None
        def boton_imprimir_transiciones():
            '''Botón para imprimir transiciones extraídas del GUI.'''
            self.boton_imprimir_transiciones = tk.Button(self.marco_botones, text="Imprimir transiciones", command=self.imprimir_transiciones)
            self.boton_imprimir_transiciones.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW, columnspan=2)

        self.marco_simbolos_def:tk.Frame = None
        def marco_simbolos_def():
            '''Marco en el que se definirán los simbolos por defecto del stack y para el simbolo vacío'''
            self.marco_simbolos_def = tk.Frame(self.marco_panel_de_control)
            TkTools.configurar_pesos(self.marco_simbolos_def, {0:0, 1:0}, {0:0, 1:0})
            self.marco_simbolos_def.grid(row=1, column=0, sticky=tk.NSEW)

        self.string_simbolo_stack:tk.StringVar = None
        self.entrada_simbolo_stack:tk.Entry = None
        self.etiqueta_simbolo_stack:tk.Label = None
        def entradas_simbolos_stack():
            '''Añade entrada para definir el simbolo inicial del Stack.'''
            self.string_simbolo_stack = tk.StringVar()
            self.string_simbolo_stack.trace_add('write', self._actualizar_simbolo_stack)
            self._actualizar_simbolo_stack()
            self.entrada_simbolo_stack = tk.Entry(self.marco_simbolos_def, textvariable=self.string_simbolo_stack)
            self.entrada_simbolo_stack.grid(row=0, column=0, sticky=tk.NSEW)
            self.etiqueta_simbolo_stack = tk.Label(self.marco_simbolos_def, text="Simbolo inicial\nen stack")
            self.etiqueta_simbolo_stack.grid(row=0, column=1, sticky=tk.NSEW)

        self.string_simbolo_vacio:tk.StringVar = None
        self.entrada_simbolo_vacio:tk.Entry = None
        self.etiqueta_simbolo_vacio:tk.Label = None
        def entradas_simbolos_vacio():
            '''Añade entrada para definir el simbolo de la palabra vacia.'''
            self.string_simbolo_vacio = tk.StringVar()
            self.string_simbolo_vacio.trace_add('write', self._actualizar_simbolo_vacio)
            self._actualizar_simbolo_vacio()
            self.entrada_simbolo_vacio = tk.Entry(self.marco_simbolos_def, textvariable=self.string_simbolo_vacio)
            self.entrada_simbolo_vacio.grid(row=1, column=0, sticky=tk.NSEW)
            self.etiqueta_simbolo_vacio = tk.Label(self.marco_simbolos_def, text="Simbolo\npalabra vacia")
            self.etiqueta_simbolo_vacio.grid(row=1, column=1, sticky=tk.NSEW)

        def construir_gui():
            '''Crear, posicionar y configurar widgets de la interfaz gráfica.'''
            ventana_principal()
            marco_construccion()
            marco_panel_de_control()

            marco_canvas_scrollbars()
            canvas()
            marco_canvas()
            TkTools.marco_canavas_unir(self.canvas, self.marco_canvas)
            TkTools.canvas_interaccion(self.canvas, self._actualizar_scrollregion)
            scrollbar_v()
            scrollbar_h()
            TkTools.configurar_scrollbars(self.canvas, self.scrollbar_v, self.scrollbar_h)

            marco_botones()
            boton_anadir()
            boton_eliminar()
            boton_imprimir_transiciones()

            marco_simbolos_def()
            entradas_simbolos_stack()
            entradas_simbolos_vacio()
            
            marco_info_apd()
            etiqueta_texto_info_apd()

        def anadir_filas_por_defecto():
            '''Añade las filas con las que la interfaz gráfica inicia.'''
            for _ in range(DEF_INI_FILAS): self.anadir_fila()

        # ========== ALGORITMO DEL CONSTRUCTOR ==========
        construir_gui()
        anadir_filas_por_defecto()
        TkTools.actualizar_widget(self.ventana_principal)

        self.canvas.config(width=self.marco_canvas.winfo_reqwidth())
        alto_total, ancho_total = TkTools.calcular_dimensiones([self.ventana_principal], [self.marco_canvas, self.marco_panel_de_control], margen_extra_h=100)
        self.ventana_principal.geometry(f"{ancho_total}x{alto_total}")

        self.ventana_principal.mainloop()
        # =========== ALGORITMO DEL CONSTRUCTOR ===========

    def _actualizar_scrollregion(self, *args):
        '''Actualiza el canvas para que los scrollbars consideres el area scrolleable.'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _actualizar_texto_info_apd(self, *args):
        '''Actualiza el texto que muestra la info del APD.'''
        self.extraer_info_apd()
        self.texto_info_apd.set(f"Estados:{self.estados} ; Alfabeto Lenguaje:{self.alfabeto_lenguaje} ; Alfabeto Stack:{self.alfabeto_stack}")

    def _actualizar_simbolo_stack(self, *args):
        '''Actualiza el simbolo base del stack.'''
        simbolo = self.string_simbolo_stack.get()
        if not simbolo:
            self.string_simbolo_stack.set(DEF_SIMBOLO_STACK)
            self.simbolo_stack = DEF_SIMBOLO_STACK
        else: 
            self.simbolo_stack = simbolo

    def _actualizar_simbolo_vacio(self, *args):
        '''Actualiza el simbolo de la palabra vacía.'''
        simbolo = self.string_simbolo_vacio.get()
        if not simbolo:
            self.string_simbolo_vacio.set(DEF_SIMBOLO_VACIO)
            self.simbolo_vacio = DEF_SIMBOLO_VACIO
        else: 
            self.simbolo_vacio = simbolo

    def anadir_fila(self):
        '''Añade fila de widgets a la interfaz grafica.'''

        entrys:list[tk.Entry] = []
        stringsvars:list[tk.StringVar] = []

        def anadir_entrada(fila:int, columna:int):
            '''Añade widget de tipo tk.Entry a una fila y columna especifica del marco en el canvas.'''
            self.marco_canvas.columnconfigure(columna, weight=0)
            e_var = tk.StringVar()
            e_var.trace_add("write", self._actualizar_texto_info_apd)
            stringsvars.append(e_var)

            e = tk.Entry(self.marco_canvas, width=12, justify=tk.CENTER, textvariable=e_var)
            e.grid(row=fila, column=columna, padx=3, pady=2)
            entrys.append(e)

        def anadir_label(fila:int, columna:int, texto:str):
            '''Añade widget de tipo tk.Label a una fila y columna especifica del marco en el canvas.'''
            self.marco_canvas.columnconfigure(columna, weight=0)
            tk.Label(self.marco_canvas, text=texto).grid(row=fila, column=columna)

        def anadir_entrada_y_label(fila:int, columna:int, texto:str):
            '''Añade widgets de tipo tk.Label y tk.Entry a una fila y columna especifica del marco en el canvas.'''
            anadir_label(fila, columna, texto)
            anadir_entrada(fila, columna + 1)
        
        # ========== ALGORITMO DEL MÉTODO ==========
        for _ in range(DEF_CAMPOS):
            fila_actual = len(self.matriz_entradas)
            widgets_actual = len(entrys)
            siguiente_columna = TkTools.next_grid_col(fila_actual, self.marco_canvas)

            if widgets_actual == 0:
                anadir_entrada_y_label(fila_actual, siguiente_columna, "δ(")

            elif widgets_actual < DEF_N:
                anadir_entrada_y_label(fila_actual, siguiente_columna, ",")
                
                if DEF_CAMPOS > len(entrys) >= DEF_N:
                    anadir_entrada_y_label(fila_actual, siguiente_columna + 2, ")=(")

            elif  DEF_CAMPOS > widgets_actual >= DEF_N:
                anadir_entrada_y_label(fila_actual, siguiente_columna, ",")

                if len(entrys) >= DEF_CAMPOS:
                    anadir_label(fila_actual, siguiente_columna + 2, ")")
        
        self.matriz_entradas.append(entrys)
        self.matriz_strings.append(stringsvars)

        if len(self.matriz_entradas) > 1: self.boton_eliminar.configure(state=tk.NORMAL)

        TkTools.actualizar_widget(self.marco_canvas)
        self._actualizar_scrollregion()
        self._actualizar_texto_info_apd()
        # ========== ALGORITMO DEL MÉTODO ==========

    def eliminar_fila(self):
        '''Eliminar fila de widgets a la interfaz grafica.'''
        # ========== ALGORITMO DEL MÉTODO ==========
        if len(self.matriz_entradas) <= 1:
            self.boton_eliminar.configure(state=tk.DISABLED)
            return
        
        # Elimina la última fila de la matriz de widgets
        self.matriz_entradas.pop()
        self.matriz_strings.pop()

        # ELimina la última fila de la interfaz gráfica
        for widget in self.marco_canvas.grid_slaves():
            if widget.grid_info()['row'] == len(self.matriz_entradas): widget.destroy()

        if len(self.matriz_entradas) <= 1:
            self.boton_eliminar.configure(state=tk.DISABLED)
        
        self.marco_canvas.update_idletasks()
        self._actualizar_scrollregion()
        self._actualizar_texto_info_apd()
        # ========== ALGORITMO DEL MÉTODO ==========

    def extraer_transiciones(self) -> dict[tuple,tuple]:
        '''
        Método para extraer diccionario de transiciones bajo el formato definido en el informe:
        
        self.transiciones = {
            (x1.1, x1.2, ..., x1.n):(y1.1, y1.2, ..., y1.m),
            (x2.1, x2.2, ..., x2.n):(y2.1, y2.2, ..., y2.m),
            ...
            (xf.1, xf.2, ..., xf.n):(yn.1, yn.2, ..., yf.m)
        }

        Y retorna una diccionario 'self.transiciones' con las transiciones del APD.
        '''
        # ========== ALGORITMO DEL MÉTODO ==========
        self.transiciones = {}
        for widgets in self.matriz_strings:
            textos = [e.get().strip() for e in widgets]
            
            key = tuple(textos[:DEF_N])
            valor = tuple(textos[DEF_N:DEF_CAMPOS])
            self.transiciones[key] = valor


        return self.transiciones
        # ========== ALGORITMO DEL MÉTODO ==========
    
    def extraer_estados(self) -> list[str]:
        '''
        Método para extraer estados del diccionario de transiciones del APD:
        
        self.transiciones  = {
            (x1.1, x1.2, ..., x1.n):(y1.1, y1.2, ..., y1.m),
            (x2.1, x2.2, ..., x2.n):(y2.1, y2.2, ..., y2.m),
            ...
            (xf.1, xf.2, ..., xf.n):(yn.1, yn.2, ..., yf.m)
        }

        Y retorna una lista [x1.1, x2.1, ..., xf.1] con los estados del APD.
        '''
        # ========== ALGORITMO DEL MÉTODO ==========
        self.estados = list(set(clave[0] for clave in self.transiciones.keys()))
        return self.estados
        # ========== ALGORITMO DEL MÉTODO ==========
    
    def extraer_alfabeto_lenguaje(self) -> list[str]:
        '''
        Método para extraer alfabeto del diccionario de transiciones del APD:
        
        self.transiciones  = {
            (x1.1, x1.2, ..., x1.n):(y1.1, y1.2, ..., y1.m),
            (x2.1, x2.2, ..., x2.n):(y2.1, y2.2, ..., y2.m),
            ...
            (xf.1, xf.2, ..., xf.n):(yn.1, yn.2, ..., yf.m)
        }

        Y retorna una lista [x1.2, x2.2, ..., xf.2] con el alfabeto del APD.
        '''
        # ========== ALGORITMO DEL MÉTODO ==========
        self.alfabeto_lenguaje = list(set(clave[1] for clave in self.transiciones.keys()))
        return self.alfabeto_lenguaje
        # ========== ALGORITMO DEL MÉTODO ==========
    
    def extraer_alfabeto_stack(self) -> list[str]:
        '''
        Método para extraer alfabeto stack del diccionario de transiciones del APD:
        
        self.transiciones  = {
            (x1.1, x1.2, ..., x1.n):(y1.1, y1.2, ..., y1.m),
            (x2.1, x2.2, ..., x2.n):(y2.1, y2.2, ..., y2.m),
            ...
            (xf.1, xf.2, ..., xf.n):(yn.1, yn.2, ..., yf.m)
        }

        Y retorna una lista [x1.3, x2.3, ..., xf.3] con el alfabeto del APD.
        '''
        # ========== ALGORITMO DEL MÉTODO ==========
        self.alfabeto_stack = list(set(clave[2] for clave in self.transiciones.keys()) | {self.simbolo_stack})
        return self.alfabeto_stack
        # ========== ALGORITMO DEL MÉTODO ==========

    def extraer_info_apd(self) -> None:
        '''Método para extraer toda la información del APD actualizada.'''
        # ========== ALGORITMO DEL MÉTODO ==========
        self.transiciones = self.extraer_transiciones()
        self.estados = self.extraer_estados()
        self.alfabeto_lenguaje = self.extraer_alfabeto_lenguaje()
        self.alfabeto_stack = self.extraer_alfabeto_stack()
        # ========== ALGORITMO DEL MÉTODO ==========

    def imprimir_transiciones(self):
        '''Método para imprimir diccionario de transiciones.'''
        # ========== ALGORITMO DEL MÉTODO ==========
        print(self.transiciones)
        # ========== ALGORITMO DEL MÉTODO ==========

if __name__ == "__main__":
    AppGUI()
