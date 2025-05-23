import flet as ft
from components import AppBar_, TextField_, Button_, Text_
import os
import config
from helpers import list_active_printers, extract_data
import pandas as pd
from datetime import datetime

def main(page: ft.Page):
    info_qr = {}
    registros = []
    table_rows = []

    snackbar = ft.SnackBar(content=ft.Text(""), open=False)

    # Tabla con encabezados
    data_table = ft.DataTable(
        border=ft.border.all(2, "#052b47"),
        vertical_lines=ft.border.BorderSide(3, "#052b47"),
        horizontal_lines=ft.border.BorderSide(1, "#052b47"),
        bgcolor="#138db8",
        data_row_color= ft.colors.WHITE,
        
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Producto", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Color", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Peso (kg)", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Lote", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Fecha", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Hora", color=ft.Colors.WHITE)),
        ],
        rows=[],
        expand=True,
        heading_text_style=ft.TextStyle( size=20, weight=ft.FontWeight.BOLD),
        data_text_style=ft.TextStyle(color="#052b47", size=14, weight=ft.FontWeight.BOLD),
    )

    # Función principal al presionar ENVIAR
    def send(_):
        nonlocal info_qr, table_rows, registros
        info_qr = extract_data(input_codigo.value)

        if info_qr:
            now = datetime.now()
            info_qr["Fecha"] = now.strftime("%Y-%m-%d")
            info_qr["Hora"] = now.strftime("%H:%M:%S")
            registros.append(info_qr)
            current_id = len(registros)

            new_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(current_id))),
                    ft.DataCell(ft.Text(info_qr.get("Producto", ""), expand=True)),
                    ft.DataCell(ft.Text(info_qr.get("Color", ""), expand=True)),
                    ft.DataCell(ft.Text(str(info_qr.get("Peso", "")))),
                    ft.DataCell(ft.Text(info_qr.get("Lote", ""), expand=True)),
                    ft.DataCell(ft.Text(info_qr.get("Fecha", ""))),
                    ft.DataCell(ft.Text(info_qr.get("Hora", ""))),
                ]
            )
            table_rows.append(new_row)
            data_table.rows = table_rows

            producto_texto.value = f"PRODUCTOS ESCANEADOS: {len(registros)}"
            peso_total = sum(item.get("Peso", 0) for item in registros)
            peso_texto.value = f"PESO TOTAL: {peso_total:.3f} kg"

        input_codigo.value = ""
        input_codigo.focus()
        page.update()

    # Función para exportar a Excel
    def export():
        nonlocal registros, table_rows
        if not registros:
            return

        if not os.path.exists("reportes"):
            os.makedirs("reportes")

        df = pd.DataFrame(registros)
        df.insert(0, "ID", range(1, len(df) + 1))

        resumen = {
            "Total de productos escaneados": [len(registros)],
            "Suma total de peso (kg)": [sum(item.get("Peso", 0) for item in registros)]
        }
        df_resumen = pd.DataFrame(resumen)

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_archivo = f"reportes/reporte_{fecha}.xlsx"

        with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Registros", index=False)
            df_resumen.to_excel(writer, sheet_name="Resumen", index=False)

        registros.clear()
        table_rows.clear()
        data_table.rows = []
        producto_texto.value = "PRODUCTOS ESCANEADOS: 0"
        peso_texto.value = "PESO TOTAL: 0.000 kg"

        # Mostrar confirmación
        snackbar.content.value = f"Reporte exportado exitosamente como {ruta_archivo}"
        page.open(snackbar)
        page.update()

    # Inputs y botones
    input_codigo = TextField_(label="Información del QR", on_sumit=send).create()
    input_codigo.border_radius = 30
    input_codigo.width = 700

    send_button = Button_(on_click=lambda _: send(_), text="ENVIAR", color="#052b47",bgcolor=ft.Colors.WHITE,brdcolor="#052b47", height=50, width=100).create()
    exportar_button = Button_(
        on_click=lambda _: export(),
        icon=ft.Icons.DOWNLOAD,
        icon_color="052b47",
        text="EXPORTAR",
        color="#052b47",
        bgcolor=ft.Colors.WHITE,
        brdcolor="#052b47",
        height=50,
        width=150
    ).create()

   

    ayuda_button = ft.TextButton(
        "AYUDA",
        icon=ft.Icons.HELP_ROUNDED,
        icon_color=ft.Colors.WHITE,
        style=ft.ButtonStyle(color=ft.Colors.WHITE)
    )

    #AlertDialog
    alert_repeat = ft.AlertDialog(
        modal=True,
        content=ft.Text("EL PRODUCTO YA HA SIDO REGISTRADO", size=25, weight="bold", color="#052b47"),
        actions=[
            Button_(on_click=lambda e: page.close(alert_repeat), text="ELIMINAR", color=ft.colors.WHITE,bgcolor=ft.Colors.GREEN,brdcolor=ft.Colors.GREEN, height=50, width=100).create(),
            Button_(on_click=lambda e: page.close(alert_repeat), text="REGISTRAR", color=ft.colors.WHITE,bgcolor=ft.Colors.RED,brdcolor=ft.Colors.RED, height=50, width=120).create(),
    
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    example_button =ft.ElevatedButton("ALERTA", on_click=lambda e: page.open(alert_repeat))
    page.add(example_button)

    # Appbar y bottom
    page.appbar = AppBar_(
        controls=[ayuda_button],
        name="SAN FRANCISCO TEXTIL"
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
        controls=[ft.Row([input_codigo, send_button], spacing=10), ft.Container(expand=True), exportar_button],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    producto_texto = Text_(value="PRODUCTOS ESCANEADOS: 0", color="#052b47", size=30).create()
    peso_texto = Text_(value="PESO TOTAL: 0.000 kg", color="#052b47", size=30).create()

    fila_texto = ft.Container(
        ft.Row(
            controls=[producto_texto, peso_texto],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=150
        ),
        padding=ft.padding.only(right=50, top=25)
    )
    page.title = "GENERADOR DE REPORTES - SAN FRANCISCO TEXTIL"
    page.add(
        fila_contenido,
        fila_texto,

        ft.Row([data_table], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
    )

ft.app(main)
