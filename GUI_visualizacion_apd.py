import tkinter as tk

from typing import Callable

from GUI_tkinter import TkTools
from GUI_vars import DEF_N, DEF_CAMPOS, DEF_SIMBOLO_STACK, DEF_SIMBOLO_VACIO, DEF_ESTADO_INICIAL

class GUIVisualizacionApd(tk.Frame):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):
        self.f_simbolo_stack:Callable = None
        self.f_simbolo_vacio:Callable = None
        self.f_estado_inicial:Callable = None

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

        super().__init__(master, **kwargs)
        TkTools.configurar_pesos(self, {0:1, 1:0}, {0:1})

        self.marco_canvas_scrollbars:tk.Frame = None
        def marco_canvas_scrollbars():
            '''Marco de canvas con scrollbar.'''        
            self.marco_canvas_scrollbars = tk.Frame(self)
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
            self.marco_info_apd = tk.Frame(self)
            TkTools.configurar_pesos(self.marco_info_apd, {0:0}, {0:0})
            self.marco_info_apd.grid(row=1, column=0, sticky=tk.NSEW)

        self.transiciones:dict[tuple, tuple] = {}
        self.estados:list[str] = []
        self.alfabeto_lenguaje:list[str] = []
        self.alfabeto_stack:list[str] = []

        self.texto_info_apd:tk.StringVar = None
        self.etiqueta_info_apd:tk.Label = None
        def etiqueta_texto_info_apd():
            '''Etiqueta de la información del APD extraida GUI.'''
            self.texto_info_apd = tk.StringVar()
            self.actualizar_texto_info_apd()
            self.etiqueta_info_apd = tk.Label(self.marco_info_apd, textvariable=self.texto_info_apd)
            self.etiqueta_info_apd.grid(row=0, column=0, sticky=tk.NSEW)

        # =========== ALGORITMO DEL CONSTRUCTOR ===========
        marco_canvas_scrollbars()
        canvas()
        marco_canvas()
        TkTools.marco_canavas_unir(self.canvas, self.marco_canvas)
        TkTools.canvas_interaccion(self.canvas, self.actualizar_scrollregion)
        scrollbar_v()
        scrollbar_h()
        TkTools.configurar_scrollbars(self.canvas, self.scrollbar_v, self.scrollbar_h)

        marco_info_apd()
        etiqueta_texto_info_apd()
        # =========== ALGORITMO DEL CONSTRUCTOR ===========

    def actualizar_scrollregion(self, *args):
        '''Actualiza el canvas para que los scrollbars consideres el area scrolleable.'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def actualizar_texto_info_apd(self, *args):
        '''Actualiza el texto que muestra la info del APD.'''
        self.extraer_info_apd()
        self.texto_info_apd.set(f"Estados:{self.estados} ; Alfabeto Lenguaje:{self.alfabeto_lenguaje} ; Alfabeto Stack:{self.alfabeto_stack}")

    def anadir_fila(self):
        '''Añade fila de widgets a la interfaz grafica.'''

        entrys:list[tk.Entry] = []
        stringsvars:list[tk.StringVar] = []

        def anadir_entrada(fila:int, columna:int):
            '''Añade widget de tipo tk.Entry a una fila y columna especifica del marco en el canvas.'''
            TkTools.configurar_pesos(self.marco_canvas, columnas={columna:0})
            e_var = tk.StringVar()
            e_var.trace_add("write", self.actualizar_texto_info_apd)
            stringsvars.append(e_var)

            def limitar_caracteres(n_max): return self.register(lambda texto: len(texto) <= n_max)

            # Define límites solo para ciertos tk.Entry según su columna
            columna_indice = len(entrys)
            limites = {
                # 0: estado origen - sin limite
                1: 1,  # símbolo entrada
                2: 1,  # símbolo pila
                # 3: estado llegada - sin límite
                # 4: símbolo a escribir - sin limite
            }

            if columna_indice in limites:
                n_max = limites[columna_indice]
                # %P representa el contenido del Entry después del cambio.
                vcmd = (limitar_caracteres(n_max), "%P")
                e = tk.Entry(self.marco_canvas, width=12, justify=tk.CENTER, textvariable=e_var, validate="key", validatecommand=vcmd)
            else:
                e = tk.Entry(self.marco_canvas, width=12, justify=tk.CENTER, textvariable=e_var)

            e.grid(row=fila, column=columna, padx=3, pady=2)
            entrys.append(e)

        def anadir_label(fila:int, columna:int, texto:str):
            '''Añade widget de tipo tk.Label a una fila y columna especifica del marco en el canvas.'''
            TkTools.configurar_pesos(self.marco_canvas, columnas={columna:0})
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

        TkTools.actualizar_widget(self.marco_canvas)
        self.actualizar_scrollregion()
        self.actualizar_texto_info_apd()
        # ========== ALGORITMO DEL MÉTODO ==========

    def eliminar_fila(self):
        '''Eliminar fila de widgets a la interfaz grafica.'''
        # ========== ALGORITMO DEL MÉTODO ==========
        
        # Elimina la última fila de la matriz de widgets
        self.matriz_entradas.pop()
        self.matriz_strings.pop()

        # ELimina la última fila de la interfaz gráfica
        for widget in self.marco_canvas.grid_slaves():
            if widget.grid_info()['row'] == len(self.matriz_entradas): widget.destroy()
        
        self.marco_canvas.update_idletasks()
        self.actualizar_scrollregion()
        self.actualizar_texto_info_apd()
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
        estados_1 = set(clave[0] for clave in self.transiciones.keys())
        estados_2 = set(valor[0] for valor in self.transiciones.values())
        estados_3 = {self.f_estado_inicial() if self.f_estado_inicial else DEF_ESTADO_INICIAL}
        self.estados = list(estados_1 | estados_2 | estados_3)
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
        alfabeto_1 = set(clave[2] for clave in self.transiciones.keys())
        alfabeto_2 = set(simbolo for valor in self.transiciones.values() for simbolo in valor[1])
        alfabeto_3 = {self.f_simbolo_stack() if self.f_simbolo_stack else DEF_SIMBOLO_STACK}
        self.alfabeto_stack = list( alfabeto_1| alfabeto_2 | alfabeto_3)
        return self.alfabeto_stack
        # ========== ALGORITMO DEL MÉTODO ==========

    def extraer_info_apd(self) -> tuple[list[str], list[str], list[str]]:
        '''Método para extraer toda la información del APD actualizada.'''
        # ========== ALGORITMO DEL MÉTODO ==========
        self.transiciones = self.extraer_transiciones()
        self.estados = self.extraer_estados()
        self.alfabeto_lenguaje = self.extraer_alfabeto_lenguaje()
        self.alfabeto_stack = self.extraer_alfabeto_stack()

        return self.estados, self.alfabeto_lenguaje, self.alfabeto_stack
        # ========== ALGORITMO DEL MÉTODO ==========