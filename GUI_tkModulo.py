import tkinter as tk

from tkinter import font
from typing import Callable

class tkTools:

    def __init__(self): pass

    @staticmethod
    def next_grid_col(fila:int, widget:tk.Widget) -> int:
        '''Retorna el indíce de la siguiente columna 'grid' disponible en un widget sobre una fila especifica y después del último widget empaquetado.'''
        ocupadas = []
        for w in widget.grid_slaves(row=fila):
            info = w.grid_info()
            col = int(info["column"])
            span = int(info.get("columnspan", 1))
            ocupadas.extend(range(col, col + span))
        return 0 if not ocupadas else max(ocupadas) + 1
    
    @staticmethod
    def next_grid_row(columna: int, widget: tk.Widget) -> int:
        '''Retorna el índice de la siguiente fila 'grid' disponible en un widget sobre una columna específica y después del último widget empaquetado.'''
        ocupadas = []
        for w in widget.grid_slaves(column=columna):
            info = w.grid_info()
            fila = int(info["row"])
            span = int(info.get("rowspan", 1))
            ocupadas.extend(range(fila, fila + span))
        return 0 if not ocupadas else max(ocupadas) + 1
    
    @staticmethod
    def marco_canavas_unir(canvas:tk.Canvas, marco:tk.Frame):
        '''Crear ventana interna (window) en el canvas para el frame.'''
        canvas.create_window((0, 0), window=marco, anchor="nw")
    
    @staticmethod
    def canvas_interaccion(canvas:tk.Canvas, funcion:Callable):
        '''Asigna una función a ejecutar cuando el widget sufre un cambio en algun parametro de su configuración.'''
        canvas.bind("<Configure>", funcion)

    @staticmethod
    def configurar_pesos(widget:tk.Widget, filas:dict[int, int]={}, columnas:dict[int, int]={}):
        '''Asigna pesos a las filas y columnas "grid" de un widget.'''
        for fila, peso in filas.items(): widget.rowconfigure(fila, weight=peso)
        for columna, peso in columnas.items(): widget.columnconfigure(columna, weight=peso)

    @staticmethod
    def configurar_scrollbars(canvas:tk.Canvas, scrollbar_v:tk.Scrollbar=None, scrollbar_h:tk.Scrollbar=None):
        '''Configurar un canvas para que use scrollbars.'''
        if scrollbar_v is not None:
            canvas.configure(yscrollcommand=scrollbar_v.set)
            scrollbar_v.config(command=canvas.yview)

        if scrollbar_h is not None:
            canvas.configure(xscrollcommand=scrollbar_h.set)
            scrollbar_h.config(command=canvas.xview)

    @staticmethod
    def actualizar_widget(widget:tk.Widget):
        '''Forzar actualización de un Widget para cálcular de geometría de todos los Widgets en su interior.'''
        widget.update_idletasks()
        widget.update()

    @staticmethod
    def calcular_dimensiones(widget_altos:list[tk.Widget], widget_anchos:list[tk.Widget], margen_extra_v:int = 0, margen_extra_h:int = 0):
        '''Caula el alto total de una lista de widgets y el ancho total de una lista de widgets más un margen opcional para cada total.'''
        alto_total = sum(widget.winfo_reqheight() for widget in widget_altos) + margen_extra_v
        ancho_total = sum(widget.winfo_reqwidth() for widget in widget_anchos) + margen_extra_h
        return alto_total, ancho_total
    
    @staticmethod
    def filtrar_por_tipo(lista_objetos:list[object], tipo):
        '''Una lista de multiples objetos retorna una lista con solo el tipo de objeto especificado.'''
        return [obj for obj in lista_objetos if isinstance(obj, tipo)]
    
    @staticmethod
    def px_to_entry_chars(widget:tk.Widget, px:int):
        """Convierte una medida en píxeles al equivalente en caracteres para un widget de tipo Entry, usando su fuente."""
        widget_font = font.nametofont(widget.cget("font"))
        char_width_px = widget_font.measure("0") or 1  # Evita división por cero
        return px // char_width_px
    
    class Checkbutton(tk.Checkbutton):

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, value:bool=False, **kwargs):
            self.booleanVar:tk.BooleanVar = tk.BooleanVar(value=value)

            self.exe_al_clickear:Callable = None

            super().__init__(master, variable=self.booleanVar, command=self._click_on_check, **kwargs)

        def _click_on_check(self, *_):
            if self.exe_al_clickear: self.exe_al_clickear()
    
    class Button(tk.Button):

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):
            self.exe_presionar_boton:Callable = None

            super().__init__(master, command=self._click_boton, **kwargs)

        def _click_boton(self, *_):
            if self.exe_presionar_boton: self.exe_presionar_boton()

    
    class Entry(tk.Entry):

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, value:str="", **kwargs):
            self.stringVar:tk.StringVar = tk.StringVar(value=value)

            self.exe_al_escribir:Callable = None
            self.exe_focus_out:Callable = None
            self.limite_caracteres:int = 0

            super().__init__(master, textvariable=self.stringVar,**kwargs)

            self.config(validate='key', validatecommand=(self._limitar_caracteres(self.limite_caracteres), "%P"))
            self.stringVar.trace_add("write", self._al_escribir)
            self.bind("<FocusOut>", self._focus_out)

        def _limitar_caracteres(self, limite:int):
            return self.register(lambda texto: len(texto) <= limite)

        def _al_escribir(self, *_):
            if not self.exe_al_escribir is None: self.exe_al_escribir()

        def _focus_out(self, *_):
            if not self.exe_focus_out is None: self.exe_focus_out()

        def actualizar_limite_caracteres(self, nuevo_limite:int):
            self.limite_caracteres = nuevo_limite
            self.config(validate='key', validatecommand=(self._limitar_caracteres(self.limite_caracteres), "%P"))


    class Label(tk.Label):

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, value:str="", **kwargs):
            self.stringVar = tk.StringVar(value=value)

            super().__init__(master, textvariable=self.stringVar, **kwargs)

    class ScrollableFrame(tk.Frame):

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):

            self.marco_contenedor:tk.Frame = tk.Frame(master)
            self.lienzo_dibujo:tk.Canvas = tk.Canvas(self.marco_contenedor)
            self.scrollbar_v:tk.Scrollbar = tk.Scrollbar(self.marco_contenedor, orient=tk.VERTICAL)
            self.scrollbar_h:tk.Scrollbar = tk.Scrollbar(self.marco_contenedor, orient=tk.HORIZONTAL)
            super().__init__(self.lienzo_dibujo, **kwargs)

            tkTools.configurar_pesos(self.marco_contenedor, {0:1, 1:0}, {0:1, 1:0})
            tkTools.marco_canavas_unir(self.lienzo_dibujo, self)
            tkTools.canvas_interaccion(self.lienzo_dibujo, self._actualizar_scrollregion)
            tkTools.configurar_scrollbars(self.lienzo_dibujo, self.scrollbar_v, self.scrollbar_h)

            self.lienzo_dibujo.grid(row=0, column=0, sticky=tk.NSEW)
            self.scrollbar_v.grid(row=0, column=1, sticky=tk.NS)
            self.scrollbar_h.grid(row=1, column=0, sticky=tk.EW)

        def grid(self, **kwargs):
            self.marco_contenedor.grid(**kwargs)

        def _actualizar_scrollregion(self, *_):
            '''Actualiza el canvas para que los scrollbars consideres el area scrolleable.'''
            self.lienzo_dibujo.configure(scrollregion=self.lienzo_dibujo.bbox("all"))

    class EntradasVertical(tk.Frame):
            
        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, entradas:list[str]=[], **kwargs):

            self.widgets:list[list[tkTools.Entry, tk.Label]] = []
            self.n_filas = len(entradas)

            super().__init__(master, **kwargs)
            tkTools.configurar_pesos(self, {i: 0 for i in range(self.n_filas + 1)}, {0:0, 1:1})

            for value in entradas:
                entry = tkTools.Entry(self, justify=tk.CENTER)
                label = tkTools.Label(self, value=value)

                fila = tkTools.next_grid_row(0, self)
                entry.grid(row=fila, column=0, sticky=tk.NSEW)
                label.grid(row=fila, column=1, sticky=tk.NSEW)

                self.widgets.append([entry, label])
            
    class BotoneraHorizontal(tk.Frame):

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, botones:list[str]=[], **kwargs):

            self.widgets:list[tkTools.Button] = []
            self.n_columnas = len(botones)
            
            super().__init__(master, **kwargs)
            tkTools.configurar_pesos(self, {0:0}, {i:1 if i%2 else 0 for i in range((2 * self.n_columnas) + 1)})

            for texto in botones:
                boton = tkTools.Button(self, text=texto)
                boton.grid(row=0, column=tkTools.next_grid_col(0, self)+1, sticky=tk.NSEW)
                self.widgets.append(boton)

    class ChecksVertical(tk.Frame):

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, checks:list[str]=[], **kwargs):

            self.widgets:list[tkTools.Checkbutton] = []
            self.n_filas = len(checks)
            
            super().__init__(master, **kwargs)
            tkTools.configurar_pesos(self, {i: 0 for i in range(self.n_filas + 1)}, {0:1})

            for texto in checks:
                check_opcion = tkTools.Checkbutton(self, justify=tk.CENTER, text=texto)

                check_opcion.grid(row=tkTools.next_grid_row(0, self), column=0, sticky=tk.EW)
                self.widgets.append(check_opcion)

    class EntradaYBotonVertical(tk.Frame):

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):
            texto_boton = kwargs.pop('text', '')

            self.widgets:list[tkTools.Entry, tkTools.Button] = []

            super().__init__(master, **kwargs)
            tkTools.configurar_pesos(self, {0:0, 1:0}, {0:1})

            entry = tkTools.Entry(self, justify=tk.CENTER)
            entry.grid(row=0, column=0, sticky=tk.NSEW)
            self.widgets.append(entry)

            boton = tkTools.Button(self, text=texto_boton)
            boton.grid(row=1, column=0, sticky=tk.NSEW)
            self.widgets.append(boton)

    class EntryLabelMatriz(ScrollableFrame):
        '''Matriz Extensible de forma Vertical añadiendo y eliminando sus filas compuestas por tkTools.Entry y tkTools.Label.'''

        def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, def_filas:int=1, esquema:str="", **kwargs):

            self.widgets:list[list[tkTools.Entry|tkTools.Label]] = []
            '''
            Matriz de tkTools.Entry|tkTools.Label dentro de la interfaz gráfica.

            self.widgets = [
                [tkTools.Entry-1.1|tkTools.Label-1.1, tkTools.Entry-1.2|tkTools.Label-1.2, ..., tkTools.Entry-1.m|tkTools.Label-1.m],
                [tkTools.Entry-2.1|tkTools.Label-2.1, tkTools.Entry-2.2|tkTools.Label-2.2, ..., tkTools.Entry-2.m|tkTools.Label-2.m],
                ...
                [tkTools.Entry-n.1|tkTools.Label-n.1, tkTools.Entry-n.2|tkTools.Label-n.2, ..., tkTools.Entry-n.m|tkTools.Label-n.m]
            ]
            '''

            self.esquema:str = esquema
            super().__init__(master, **kwargs)

            for _ in range(def_filas): self.anadir_fila()

        def anadir_fila(self):
            '''Añade fila de widgets a la interfaz grafica.'''
            widgets:list[tkTools.Entry|tkTools.Label] = []

            def anadir_entrada(fila:int, columna:int):
                '''Añade widget de tipo tk.Entry a una fila y columna especifica del marco en el canvas.'''
                tkTools.configurar_pesos(self, {fila:0}, {columna:0})

                entry = tkTools.Entry(self, justify=tk.CENTER)
                entry.config(width=10)
                entry.grid(row=fila, column=columna)

                widgets.append(entry)

            def anadir_label(fila:int, columna:int, value:str):
                '''Añade widget de tipo tk.Label a una fila y columna especifica del marco en el canvas.'''
                tkTools.configurar_pesos(self, {fila:0}, {columna:0})
                
                label = tkTools.Label(self, value=value)
                label.grid(row=fila, column=columna)

                widgets.append(label)
            
            fila_actual = len(self.widgets)
            buffer = ""

            for caracter in self.esquema:
                if caracter == '0':
                    siguiente_columna = tkTools.next_grid_col(fila_actual, self)

                    if buffer:
                        anadir_label(fila_actual, siguiente_columna, buffer)
                        buffer = ""
                        anadir_entrada(fila_actual, siguiente_columna+1)

                    else: anadir_entrada(fila_actual, siguiente_columna)

                else: buffer += caracter

            siguiente_columna = tkTools.next_grid_col(fila_actual, self)
            if buffer:
                anadir_label(fila_actual, siguiente_columna, buffer)
                buffer = ""
            
            self.widgets.append(widgets)
            tkTools.actualizar_widget(self)

        def eliminar_fila(self):
            '''Eliminar fila de widgets a la interfaz grafica.'''
            self.widgets.pop()

            for widget in self.grid_slaves():
                if widget.grid_info()['row'] == len(self.widgets): widget.destroy()