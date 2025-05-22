import flet as ft
from components import AppBar_, TextField_, Button_, Text_
import os
import config
from helpers import list_active_printers, validate_code
def main(page: ft.Page):
    
    def onChange_PRINTER(e):
        """
        Updates the global printer_name variable with the selected printer.

        This function is triggered when the printer selection changes in the UI.
        It updates the global `printer_name` variable with the value from the
        control event and refreshes the page.

        Parameters
        ----------
        e : Event
            The event object containing the control with the new printer value.
        """

        global printer_name
        printer_name = e.control.value
        page.update()

    def toggle_printer_select():
        printer_select.visible = not printer_select.visible
        page.update()
    # inputs & buttons
    input_codigo= TextField_(label= "INGRESE EL CODIGO").create()
    input_codigo.border_radius = 30
    input_codigo.width = 700
    send_button = Button_(on_click=lambda _: validate_code(), text= "ENVIAR", color="#052b47", height=50, width=100).create()
    exportar_button = Button_(on_click=lambda _: validate_code(), text= "EXPORTAR", color="#052b47", height=50, width=150).create()
    

    # selects
    printer_icon_button = ft.IconButton(
        icon=ft.icons.PRINT,
        icon_color=ft.Colors.WHITE,
        tooltip="Configurar impresora",
        on_click=lambda e: toggle_printer_select()
    )
    printers = list_active_printers()
    printer = ""
    printers_list = [ft.dropdown.Option(i) for i in printers]
    printer_select =  ft.Dropdown(
                        options=printers_list,
                        on_change=onChange_PRINTER,    
                        value=printer,
                        label="Selecciona Impresora",
                        label_style={"color":ft.Colors.WHITE},
                        width=250,
                        border_color=ft.Colors.WHITE,
                                            )


    ayuda_button = ft.TextButton("AYUDA", icon=ft.Icons.HELP_ROUNDED, icon_color=ft.Colors.WHITE,style=ft.ButtonStyle(
        color=ft.Colors.WHITE))

    page.appbar = AppBar_(
        controls=[printer_icon_button, printer_select, ayuda_button], name= "SAN FRANCISCO TEXTIL"
    ).create()
    page.bottom_appbar = ft.BottomAppBar(
    bgcolor="#052b47",
    height=40,
    content=ft.Row(
        controls=[
            ft.Text("© 2025 CORPORACION TECTRONIC", color=ft.Colors.WHITE),
            ft.Text("Versión 1.0", color=ft.Colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    fila_contenido = ft.Row(
        controls=[
            ft.Row([input_codigo, send_button], spacing=10), 
            ft.Container(expand=True), 
            exportar_button 
        ],
        alignment=ft.MainAxisAlignment.START, 
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    #resumen
    producto_texto = Text_(value="PRODUCTOS ESCANEADOS: ", color="#052b47", size=30).create()
    peso_texto = Text_(value="PESO TOTAL: ", color="#052b47", size=30).create()
    fila_texto=ft.Container( ft.Row(
        controls=[
            producto_texto,
            peso_texto
        ],
        alignment=ft.MainAxisAlignment.END, 
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=150
    ),
    padding= ft.padding.only(right=50 ,top= 25))
    page.add(fila_contenido, fila_texto)

ft.app(main)
