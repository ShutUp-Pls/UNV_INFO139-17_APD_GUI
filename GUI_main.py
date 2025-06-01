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

class AppGUI:

    def __init__(self):

        self.matriz_widgets:list[list] = []
        '''
        Matriz de widgets dentro de la interfaz gráfica.

        self.matriz_widgets = [
            [widget-1.1, widget-1.2, ..., widget-1.n],
            [widget-2.1, widget-2.2, ..., widget-2.n],
            ...
            [widget-1.m, widget-2.m, ..., widget-n.m]
        ]
        '''

        self.ventana_principal:tk.Tk = None
        def ventana_principal():
            '''Ventana principal del programa.'''
            self.ventana_principal = tk.Tk()

            self.ventana_principal.title("Simulador - APD")
            self.ventana_principal.resizable(True, True)

            TkTools.configurar_pesos(self.ventana_principal, {0:1}, {0:1, 1:0})

        self.marco_canvas_scrollbars:tk.Frame = None
        def marco_canvas_scrollbars():
            '''Marco de canvas con scrollbar.'''        
            self.marco_canvas_scrollbars = tk.Frame(self.ventana_principal)
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

        self.marco_botones:tk.Frame = None
        def marco_botones():
            '''Marco de botones y panel de control.'''
            self.marco_botones = tk.Frame(self.ventana_principal)
            TkTools.configurar_pesos(self.marco_botones, {0:1, 3:1}, {1:0, 2:0})
            self.marco_botones.grid(row=0, column=1, sticky=tk.NSEW)

        self.boton_anadir:tk.Button = None
        def boton_anadir():
            '''Boton para añadir fila al GUI.'''
            self.boton_anadir = tk.Button(self.marco_botones, text="Añadir fila", command=self.anadir_fila)
            self.boton_anadir.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.boton_eliminar:tk.Button = None
        def boton_eliminar():
            '''Botón para eliminar última fila del GUI.'''
            self.boton_eliminar = tk.Button(self.marco_botones, text="Eliminar fila", command=self.eliminar_fila)
            self.boton_eliminar.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        self.boton_imprimir_transiciones:tk.Button = None
        def boton_imprimir_transiciones():
            '''Botón para imprimir transiciones extraída del GUI.'''
            self.boton_imprimir_transiciones = tk.Button(self.marco_botones, text="Imprimir transiciones", command=self.imprimir_transiciones)
            self.boton_imprimir_transiciones.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW, columnspan=2)

        def construir_gui():
            '''Crear, posicionar y configurar widgets de la interfaz gráfica.'''
            ventana_principal()

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

        def anadir_filas_por_defecto():
            '''Añade las filas con las que la interfaz gráfica inicia.'''
            for _ in range(DEF_INI_FILAS): self.anadir_fila()

        # ========== ALGORITMO DEL CONSTRUCTOR ==========
        construir_gui()
        anadir_filas_por_defecto()
        TkTools.actualizar_widget(self.ventana_principal)

        self.canvas.config(width=self.marco_canvas.winfo_reqwidth())
        alto_total, ancho_total = TkTools.calcular_dimensiones([self.ventana_principal], [self.marco_canvas, self.marco_botones], margen_extra_h=50)
        self.ventana_principal.geometry(f"{ancho_total}x{alto_total}")

        self.ventana_principal.mainloop()
        # =========== ALGORITMO DEL CONSTRUCTOR ===========

    def _actualizar_scrollregion(self, evento=None):
        '''Actualiza el canvas para que los scrollbars consideres el area scrolleable.'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def anadir_fila(self):
        '''Añade fila de widgets a la interfaz grafica.'''

        widgets:list[tk.Widget] = []

        def anadir_entrada(fila:int, columna:int):
            '''Añade widget de tipo tk.Entry a una fila y columna especifica del marco en el canvas.'''
            self.marco_canvas.columnconfigure(columna, weight=0)
            e = tk.Entry(self.marco_canvas, width=12, justify=tk.CENTER)
            e.grid(row=fila, column=columna, padx=3, pady=2)
            widgets.append(e)

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
            fila_actual = len(self.matriz_widgets)
            widgets_actual = len(widgets)
            siguiente_columna = TkTools.next_grid_col(fila_actual, self.marco_canvas)

            if widgets_actual == 0:
                anadir_entrada_y_label(fila_actual, siguiente_columna, "δ(")

            elif widgets_actual < DEF_N:
                anadir_entrada_y_label(fila_actual, siguiente_columna, ",")
                
                if len(widgets) >= DEF_N and widgets_actual <= DEF_CAMPOS:
                    anadir_entrada_y_label(fila_actual, siguiente_columna + 2, ")=(")

            elif widgets_actual > DEF_N and widgets_actual < DEF_CAMPOS:
                anadir_entrada_y_label(fila_actual, siguiente_columna, ",")

                if len(widgets) >= DEF_CAMPOS:
                    anadir_label(fila_actual, siguiente_columna + 2, ")")
        
        self.matriz_widgets.append(widgets)
        if len(self.matriz_widgets) > 1: self.boton_eliminar.configure(state=tk.NORMAL)

        TkTools.actualizar_widget(self.marco_canvas)
        self._actualizar_scrollregion()
        # ========== ALGORITMO DEL MÉTODO ==========

    def eliminar_fila(self):
        '''Eliminar fila de widgets a la interfaz grafica.'''
        # ========== ALGORITMO DEL MÉTODO ==========
        if len(self.matriz_widgets) <= 1:
            self.boton_eliminar.configure(state=tk.DISABLED)
            return

        # Elimina la última fila de la matriz de widgets
        self.matriz_widgets.pop()

        # ELimina la última fila de la interfaz gráfica
        for widget in self.marco_canvas.grid_slaves():
            if widget.grid_info()['row'] == len(self.matriz_widgets): widget.destroy()

        if len(self.matriz_widgets) <= 1:
            self.boton_eliminar.configure(state=tk.DISABLED)
        
        self.marco_canvas.update_idletasks()
        self._actualizar_scrollregion()
        # ========== ALGORITMO DEL MÉTODO ==========

    def extraer_transiciones(self):
        '''
        Método para extraer diccionario de transiciones bajo el formato definido en el informe:.
        
        dicc = {
            (x1.1, x1.2, ..., x1.n):(y1.1, y1.2, ..., y1.m),
            (x2.1, x2.2, ..., x2.n):(y2.1, y2.2, ..., y2.m),
            ...
            (xf.1, xf.2, ..., xf.n):(yn.1, yn.2, ..., yf.m)
        }
        '''
        dicc = {}
        for widgets in self.matriz_widgets:
            textos = [e.get().strip() for e in widgets]
            
            key = tuple(textos[:DEF_N])
            valor = tuple(textos[DEF_N:DEF_CAMPOS])
            dicc[key] = valor

        return dicc

    def imprimir_transiciones(self):
        '''Método para imprimir diccionario de transiciones.'''
        print(self.extraer_transiciones())

if __name__ == "__main__":
    AppGUI()
