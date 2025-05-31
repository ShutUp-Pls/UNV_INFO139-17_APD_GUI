import tkinter as tk

# Bajo el contexto de Autómatas Push Down (APD),
# este programa recibe a través de una interfaz
# grafíca, una función de transición de la forma:
#
# f(x1, x2, ..., xn)=(y1, y2, ..., ym) | con n>0 y m>0
#
# y verifica si una cadena de simbolos
# pertence o no al APD definido.

# Números de campos de entrada de la función:
# # DEF_N = n <=> f(x1, x2, ..., xn)
DEF_N = 3

# Número de campos de salida de la función.
# DEF_M = m <=> (y1, y2, ..., ym)
DEF_M = 2

# Número de campos necesarios para describir la función.
DEF_CAMPOS = DEF_N + DEF_M

# Número de filas al iniciar el programa.
DEF_INI_FILAS = 2

class TuplaApp:

    # Constructor de la clase
    def __init__(self):

        # Matriz de widgets dentro de la interfaz gráfica.
        self.matriz_widgets = []
        # - self.filas = [
        #       [widget-1.1, widget-1.2, ..., widget-1.n],
        #       [widget-2.1, widget-2.2, ..., widget-2.n],
        #       ...
        #       [widget-1.m, widget-2.m, ..., widget-n.m]
        #   ]

        # Ventana principal del programa.
        self.ventana_main = tk.Tk()
        self.ventana_main.title("Simulador - APD")
        #self.ventana_main.geometry("600x400")
        self.ventana_main.resizable(True, True)

        self.ventana_main.rowconfigure(0, weight=1)
        self.ventana_main.rowconfigure(1, weight=0)
        self.ventana_main.columnconfigure(0, weight=1)
        self.ventana_main.columnconfigure(1, weight=0)
        
        # Marco de canvas con scrollbar.
        marco_canvas = tk.Frame(self.ventana_main)
        marco_canvas.rowconfigure(0, weight=1)
        marco_canvas.rowconfigure(1, weight=0)
        marco_canvas.columnconfigure(0, weight=1)
        marco_canvas.columnconfigure(1, weight=0)
        marco_canvas.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # Canvas donde irá el frame de filas
        self.canvas_filas = tk.Canvas(marco_canvas, borderwidth=0)
        self.canvas_filas.grid(row=0, column=0, sticky=tk.NSEW)

        # Scrollbar vertical y horizontal
        scrollbar_v = tk.Scrollbar(marco_canvas, orient=tk.VERTICAL, command=self.canvas_filas.yview)
        scrollbar_v.grid(row=0, column=1, sticky=tk.NS)

        scrollbar_h = tk.Scrollbar(marco_canvas, orient=tk.HORIZONTAL, command=self.canvas_filas.xview)
        scrollbar_h.grid(row=1, column=0, sticky=tk.EW)

        # Configurar el canvas para que use ambos scrollbars
        self.canvas_filas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        # Marco interior que contendrá las filas de widgets
        self.marco_filas = tk.Frame(self.canvas_filas)
        self.marco_filas.columnconfigure((0, DEF_CAMPOS+1), weight=1)
        for i in range(1, DEF_CAMPOS+1): self.marco_filas.columnconfigure(i, weight=0)

        # Crear ventana interna (window) en el canvas para el frame
        self.marco_window_id = self.canvas_filas.create_window((0, 0), window=self.marco_filas, anchor="nw")
        self.canvas_filas.bind("<Configure>", self._on_canvas_configure)
        
        # Marco de botones.
        marco_botones = tk.Frame(self.ventana_main)
        marco_botones.columnconfigure((0, 4), weight=1)
        marco_botones.columnconfigure((1, 2, 3), weight=0)
        marco_botones.grid(row=0, column=1, sticky=tk.NSEW)
        
        # Botones para controlar filas e imprimir.
        self.button_anadir = tk.Button(marco_botones, text="Añadir fila", command=self.añadir_fila)
        self.button_anadir.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.button_eliminar = tk.Button(marco_botones, text="Eliminar fila", command=self.eliminar_fila)
        self.button_eliminar.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        self.button_imprimir = tk.Button(marco_botones, text="Imprimir diccionario", command=self.imprimir_dicc)
        self.button_imprimir.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Añadimos filas por defecto.
        for _ in range(DEF_INI_FILAS): self.añadir_fila()
        
        # Se lanza la interfaz del programa.
        self.ventana_main.mainloop()

    def _on_canvas_configure(self, evento):
        # evento.width y evento.height son las dimensiones del canvas
        self.canvas_filas.itemconfig(
            self.marco_window_id,
            width=evento.width,
            height=evento.height  # Si quieres que también crezca en alto
        )

    # Método para añadir una fila a la interfaz gráfica.
    def añadir_fila(self):
        if len(self.matriz_widgets) > 1: self.button_eliminar.configure(state=tk.NORMAL)

        # Agrega una fila de widgets a la interfaz.
        widgets = []
        for col in range(DEF_CAMPOS):
            e = tk.Entry(self.marco_filas, width=12)
            e.grid(row=len(self.matriz_widgets), column=1+col, padx=3, pady=2)
            widgets.append(e)
        
        # Agregar la lista de widgets como última fila de la matriz de widgets.
        self.matriz_widgets.append(widgets)

        if len(self.matriz_widgets) > 1: self.button_eliminar.configure(state=tk.NORMAL)

        self.marco_filas.update_idletasks()
        self.canvas_filas.configure(scrollregion=self.canvas_filas.bbox("all"))

    # Método para eliminar una fila a la interfaz gráfica.
    def eliminar_fila(self):
        
        if len(self.matriz_widgets) <= 1:
            self.button_eliminar.configure(state=tk.DISABLED)
            return

        # Elimina la última fila de la matriz de widgets
        ult_fila = self.matriz_widgets.pop()

        # ELimina la última fila de la interfaz gráfica
        for entry in ult_fila: entry.destroy()

        if len(self.matriz_widgets) <= 1:
            self.button_eliminar.configure(state=tk.DISABLED)
            return
        
        self.marco_filas.update_idletasks()
        self.canvas_filas.configure(scrollregion=self.canvas_filas.bbox("all"))

    # Método para extraer diccionario de transiciones bajo
    # el formato definido en el informe:.
    #
    # dicc = {
    #       (x1.1, x1.2, ..., x1.n):(y1.1, y1.2, ..., y1.m),
    #       (x2.1, x2.2, ..., x2.n):(y2.1, y2.2, ..., y2.m),
    #       ...
    #       (xf.1, xf.2, ..., xf.n):(yn.1, yn.2, ..., yf.m)
    # }
    #
    def extraer_dicc(self):
        dicc = {}
        for widgets in self.matriz_widgets:
            # Obtener los textos de la matríz de widgets
            textos = [e.get().strip() for e in widgets]
            
            # Formatea los textos como tuplas bajos las constantes iniciales
            key = tuple(textos[:DEF_N])
            valor = tuple(textos[DEF_N:DEF_CAMPOS])
            dicc[key] = valor

        return dicc

    # Método para imprimir diccionario de transiciones
    def imprimir_dicc(self):
        print(self.extraer_dicc())


if __name__ == "__main__":
    TuplaApp()
