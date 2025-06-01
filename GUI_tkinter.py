import tkinter as tk

from typing import Callable

class TkTools:

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