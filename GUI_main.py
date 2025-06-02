import tkinter as tk

from typing import Callable

from GUI_tkinter import TkTools
from GUI_vars import DEF_INI_FILAS
from GUI_panel_de_control import GUIPanelDeControl
from GUI_visualizacion_apd import GUIVisualizacionApd

# Bajo el contexto de Autómatas Push Down (APD),
# este programa recibe a través de una interfaz
# grafíca, una función de transición de la forma:
#
# f(x1, x2, ..., xn)=(y1, y2, ..., ym) | con n>0 y m>0
#
# y verifica si una cadena de simbolos
# pertence o no al APD definido.

class GUIMain:

    def __init__(self):
        self.ventana_principal:tk.Tk = None
        def ventana_principal():
            '''Ventana principal del programa.'''
            self.ventana_principal = tk.Tk()

            self.ventana_principal.title("Simulador - APD")
            self.ventana_principal.resizable(True, True)

            TkTools.configurar_pesos(self.ventana_principal, {0:0}, {0:1, 1:0})

        self.visualizacion_apd:GUIVisualizacionApd = None
        def visualizacion_apd():
            '''Marco donde se construirá el APD basado en sus transiciones.'''        
            self.visualizacion_apd = GUIVisualizacionApd(self.ventana_principal)
            self.visualizacion_apd.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.panel_de_control:GUIPanelDeControl = None
        def panel_de_control():
            '''Marco donde se controlarán los parametros para la construcción del APD.'''        
            self.panel_de_control = GUIPanelDeControl(self.ventana_principal)
            self.panel_de_control.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

        def construir_gui():
            '''Crear, posicionar y configurar widgets de la interfaz gráfica. El orden de construcción importa.'''
            ventana_principal()
            visualizacion_apd()
            panel_de_control()

            self.visualizacion_apd.f_estado_inicial = self.panel_de_control.obtener_estado_inicial
            self.visualizacion_apd.f_simbolo_stack = self.panel_de_control.obtener_simbolo_stack
            self.visualizacion_apd.f_simbolo_vacio = self.panel_de_control.obtener_simbolo_vacio

            self.panel_de_control.f_anadir_fila = self._anadir_fila
            self.panel_de_control.f_eliminar_fila = self._eliminar_fila
            self.panel_de_control.f_actualizar_texto_info_apd = self.visualizacion_apd.actualizar_texto_info_apd

        def anadir_filas_por_defecto():
            '''Añade las filas con las que la interfaz gráfica inicia.'''
            for _ in range(DEF_INI_FILAS): self.visualizacion_apd.anadir_fila()

        # ========== ALGORITMO DEL CONSTRUCTOR ==========
        construir_gui()
        anadir_filas_por_defecto()
        TkTools.actualizar_widget(self.ventana_principal)

        self.visualizacion_apd.canvas.config(width=self.visualizacion_apd.marco_canvas.winfo_reqwidth())
        alto_total, ancho_total = TkTools.calcular_dimensiones([self.ventana_principal], [self.visualizacion_apd.marco_canvas, self.panel_de_control], margen_extra_h=100)
        self.ventana_principal.geometry(f"{ancho_total}x{alto_total}")
        self.ventana_principal.resizable(False, False)

        self.ventana_principal.bind_all("<Button-1>", self._focus_on_click, add='+')
        self.ventana_principal.mainloop()
        # =========== ALGORITMO DEL CONSTRUCTOR ===========

    def _focus_on_click(self, event:tk.Event):
        '''Actualiza el focus de la App al Widget que fue clieckeado.'''
        widget:tk.Widget = event.widget
        try: widget.focus_set()
        except: self.ventana_principal.focus_set()

    def _anadir_fila(self, *args):
        self.visualizacion_apd.anadir_fila()
        if len(self.visualizacion_apd.matriz_entradas) > 1: self.panel_de_control.boton_eliminar.configure(state=tk.NORMAL)
        else: self.panel_de_control.boton_eliminar.configure(state=tk.DISABLED)

    def _eliminar_fila(self, *args):
        self.visualizacion_apd.eliminar_fila()
        if len(self.visualizacion_apd.matriz_entradas) <= 1: self.panel_de_control.boton_eliminar.configure(state=tk.DISABLED)
        else: self.panel_de_control.boton_eliminar.configure(state=tk.NORMAL)
        

if __name__ == "__main__":
    GUIMain()
