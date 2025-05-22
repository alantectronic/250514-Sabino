import flet as ft
from components import AppBar_, TextField_, Button_, Text_
import os
import config
from helpers import list_active_printers, extract_data

def main(page: ft.Page):
    info_qr = {}
    registros = []  # Lista que guarda todos los datos escaneados
    table_rows = []  # Lista de filas para la tabla

    def onChange_PRINTER(e):
        global printer_name
        printer_name = e.control.value
        page.update()

    def toggle_printer_select():
        printer_select.visible = not printer_select.visible
        page.update()

    # Tabla vacía inicial
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Color", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Peso (KG)", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Lote", color=ft.Colors.WHITE, expand=True)),
        ],
        rows=[],
        expand=True,
        heading_row_color="#052b47",

    )

    # Función para procesar escaneo
    def send(_):
        nonlocal info_qr, table_rows, registros
        info_qr = extract_data(input_codigo.value)

        if info_qr:
            registros.append(info_qr)

            # Añadir nueva fila
            new_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(info_qr.get("Producto", ""), expand=True)),
                    ft.DataCell(ft.Text(info_qr.get("Color", ""), expand=True)),
                    ft.DataCell(ft.Text(str(info_qr.get("Peso", "")))),
                    ft.DataCell(ft.Text(info_qr.get("Lote", ""), expand=True)),
                ]
            )
            table_rows.append(new_row)
            data_table.rows = table_rows

            # Actualizar resumen
            producto_texto.value = f"PRODUCTOS ESCANEADOS: {len(registros)}"
            peso_total = sum(item.get("Peso", 0) for item in registros)
            peso_texto.value = f"PESO TOTAL: {peso_total:.3f} KG"

        input_codigo.value = ""
        input_codigo.focus()
        page.update()

    # Inputs y botones
    input_codigo = TextField_(label="Información del QR", on_sumit=send).create()
    input_codigo.border_radius = 30
    input_codigo.width = 700

    send_button = Button_(on_click=lambda _: send(_), text="ENVIAR", color="#052b47", height=50, width=100).create()

    exportar_button = Button_(
        on_click=lambda _: print("Exportar no implementado aún"),
        icon=ft.Icons.DOWNLOAD,
        icon_color="052b47",
        text="EXPORTAR",
        color="#052b47",
        height=50,
        width=150
    ).create()

    # Selección de impresora
    printer_icon_button = ft.IconButton(
        icon=ft.icons.PRINT,
        icon_color=ft.Colors.WHITE,
        tooltip="Configurar impresora",
        on_click=lambda e: toggle_printer_select()
    )

    printers = list_active_printers()
    printer = ""
    printers_list = [ft.dropdown.Option(i) for i in printers]

    printer_select = ft.Dropdown(
        options=printers_list,
        on_change=onChange_PRINTER,
        value=printer,
        label="Selecciona Impresora",
        label_style={"color": ft.Colors.WHITE},
        width=250,
        border_color=ft.Colors.WHITE,
    )

    ayuda_button = ft.TextButton("AYUDA", icon=ft.Icons.HELP_ROUNDED, icon_color=ft.Colors.WHITE, style=ft.ButtonStyle(color=ft.Colors.WHITE))

    # Appbar y bottom bar
    page.appbar = AppBar_(
        controls=[printer_icon_button, printer_select, ayuda_button], name="SAN FRANCISCO TEXTIL"
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

    # Fila superior
    fila_contenido = ft.Row(
        controls=[
            ft.Row([input_codigo, send_button], spacing=10),
            ft.Container(expand=True),
            exportar_button
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Texto resumen
    producto_texto = Text_(value="PRODUCTOS ESCANEADOS: ", color="#052b47", size=30).create()
    peso_texto = Text_(value="PESO TOTAL: ", color="#052b47", size=30).create()

    fila_texto = ft.Container(
        ft.Row(
            controls=[
                producto_texto,
                peso_texto
            ],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=150
        ),
        padding=ft.padding.only(right=50, top=25)
    )

    # Agrega todos los elementos a la página
    page.add(
        fila_contenido,
        fila_texto,
        ft.Row([
            data_table
        ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
    )

ft.app(main)
