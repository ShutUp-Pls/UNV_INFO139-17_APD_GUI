import tkinter as tk

from typing import Callable

from GUI_tkinter import TkTools
from GUI_vars import DEF_SIMBOLO_STACK, DEF_SIMBOLO_VACIO, DEF_ESTADO_INICIAL

class GUIPanelDeControl(tk.Frame):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):
        self.f_anadir_fila:Callable = None
        self.f_eliminar_fila:Callable = None
        self.f_actualizar_texto_info_apd:Callable = None

        super().__init__(master, **kwargs)
        TkTools.configurar_pesos(self, {0:0, 1:0}, {0:0})

        self.marco_botones:tk.Frame = None
        def marco_botones():
            '''Marco de botones y panel de control.'''
            self.marco_botones = tk.Frame(self)
            TkTools.configurar_pesos(self.marco_botones, {0:0}, {0:1, 1:0, 2:0, 3:1})
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

        self.marco_simbolos_def:tk.Frame = None
        def marco_simbolos_def():
            '''Marco en el que se definirán los simbolos por defecto del stack y para el simbolo vacío'''
            self.marco_simbolos_def = tk.Frame(self)
            TkTools.configurar_pesos(self.marco_simbolos_def, {0:0, 1:0, 2:0}, {0:0, 1:0})
            self.marco_simbolos_def.grid(row=1, column=0, sticky=tk.NSEW)

        self.simbolo_stack:str = DEF_SIMBOLO_STACK
        self.string_simbolo_stack:tk.StringVar = None
        self.entrada_simbolo_stack:tk.Entry = None
        self.etiqueta_simbolo_stack:tk.Label = None
        def entradas_simbolos_stack():
            '''Añade entrada para definir el simbolo inicial del Stack.'''
            self.string_simbolo_stack = tk.StringVar()
            self.string_simbolo_stack.trace_add('write', self._actualizar_simbolo_stack)
            self._actualizar_simbolo_stack()

            def limitar_caracteres(n_max): return self.register(lambda texto: len(texto) <= n_max)

            self.entrada_simbolo_stack = tk.Entry(self.marco_simbolos_def, justify=tk.CENTER, textvariable=self.string_simbolo_stack, validate='key', validatecommand=(limitar_caracteres(1), "%P"))
            self.entrada_simbolo_stack.grid(row=0, column=0, sticky=tk.NSEW)
            self.entrada_simbolo_stack.bind("<FocusOut>", self._validar_entrada_simbolo_stack)
            self._validar_entrada_simbolo_stack()

            self.etiqueta_simbolo_stack = tk.Label(self.marco_simbolos_def, text="Simbolo inicial\nen stack")
            self.etiqueta_simbolo_stack.grid(row=0, column=1, sticky=tk.NSEW)

        self.simbolo_vacio:str = DEF_SIMBOLO_VACIO
        self.string_simbolo_vacio:tk.StringVar = None
        self.entrada_simbolo_vacio:tk.Entry = None
        self.etiqueta_simbolo_vacio:tk.Label = None
        def entradas_simbolos_vacio():
            '''Añade entrada para definir el simbolo de la palabra vacia.'''
            self.string_simbolo_vacio = tk.StringVar()
            self.string_simbolo_vacio.trace_add('write', self._actualizar_simbolo_vacio)

            def limitar_caracteres(n_max): return self.register(lambda texto: len(texto) <= n_max)

            self.entrada_simbolo_vacio = tk.Entry(self.marco_simbolos_def, justify=tk.CENTER, textvariable=self.string_simbolo_vacio, validate='key', validatecommand=(limitar_caracteres(1), "%P"))
            self.entrada_simbolo_vacio.grid(row=1, column=0, sticky=tk.NSEW)
            self.entrada_simbolo_vacio.bind("<FocusOut>", self._validar_entrada_simbolo_vacio)
            self._validar_entrada_simbolo_vacio()

            self.etiqueta_simbolo_vacio = tk.Label(self.marco_simbolos_def, text="Simbolo\npalabra vacia")
            self.etiqueta_simbolo_vacio.grid(row=1, column=1, sticky=tk.NSEW)

        self.estado_inicial:str = DEF_ESTADO_INICIAL
        self.string_estado_inicial:tk.StringVar = None
        self.entrada_estado_inicial:tk.Entry = None
        self.etiqueta_estado_inicial:tk.Label = None
        def entradas_estado_inicial():
            '''Añade entrada para definir el estado inicial del APD.'''
            self.string_estado_inicial = tk.StringVar()
            self.string_estado_inicial.trace_add('write', self._actualizar_estado_inicial)

            self.entrada_estado_inicial = tk.Entry(self.marco_simbolos_def, justify=tk.CENTER, textvariable=self.string_estado_inicial)
            self.entrada_estado_inicial.grid(row=2, column=0, sticky=tk.NSEW)
            self.entrada_estado_inicial.bind("<FocusOut>", self._validar_entrada_estado_inicial)
            self._validar_entrada_estado_inicial()

            self.etiqueta_estado_inicial = tk.Label(self.marco_simbolos_def, text="Estado\nInicial")
            self.etiqueta_estado_inicial.grid(row=2, column=1, sticky=tk.NSEW)

        marco_botones()
        boton_anadir()
        boton_eliminar()

        marco_simbolos_def()
        entradas_simbolos_stack()
        entradas_simbolos_vacio()
        entradas_estado_inicial()

    def anadir_fila(self, *args):
        if self.f_anadir_fila: self.f_anadir_fila()

    def eliminar_fila(self, *args):
        if self.f_eliminar_fila: self.f_eliminar_fila()

    def obtener_estado_inicial(self, *args):
        return self.estado_inicial
    
    def obtener_simbolo_stack(self, *args):
        return self.simbolo_stack
    
    def obtener_simbolo_vacio(self, *args):
        return self.simbolo_vacio    

    def _actualizar_simbolo_stack(self, *args):
        '''Actualiza el simbolo base del stack.'''
        simbolo = self.string_simbolo_stack.get()

        if not simbolo: self.simbolo_stack = DEF_SIMBOLO_STACK
        else: self.simbolo_stack = simbolo

        if self.f_actualizar_texto_info_apd: self.f_actualizar_texto_info_apd()

    def _actualizar_simbolo_vacio(self, *args):
        '''Actualiza el simbolo de la palabra vacía.'''
        simbolo = self.string_simbolo_vacio.get()

        if not simbolo: self.simbolo_vacio = DEF_SIMBOLO_VACIO
        else: self.simbolo_vacio = simbolo

        if self.f_actualizar_texto_info_apd: self.f_actualizar_texto_info_apd()

    def _actualizar_estado_inicial(self, *args):
        '''Actualiza el estado inicial del APD.'''
        simbolo = self.string_estado_inicial.get()

        if not simbolo: self.estado_inicial = DEF_ESTADO_INICIAL
        else:  self.estado_inicial = simbolo

        if self.f_actualizar_texto_info_apd: self.f_actualizar_texto_info_apd()

    def _validar_entrada_simbolo_stack(self, *args):
        '''Cada que se cambia el focus de los tk.Entry se ejecuta una comprobación para ver si están vacios.'''
        self._actualizar_simbolo_stack()
        if self.simbolo_stack == DEF_SIMBOLO_STACK: self.string_simbolo_stack.set(DEF_SIMBOLO_STACK)

    def _validar_entrada_simbolo_vacio(self, *args):
        '''Cada que se cambia el focus de los tk.Entry se ejecuta una comprobación para ver si están vacios.'''
        self._actualizar_simbolo_vacio()
        if self.simbolo_vacio == DEF_SIMBOLO_VACIO: self.string_simbolo_vacio.set(DEF_SIMBOLO_VACIO)

    def _validar_entrada_estado_inicial(self, *args):
        '''Cada que se cambia el focus de los tk.Entry se ejecuta una comprobación para ver si están vacios.'''
        self._actualizar_estado_inicial()
        if self.estado_inicial == DEF_ESTADO_INICIAL: self.string_estado_inicial.set(DEF_ESTADO_INICIAL)