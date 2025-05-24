import flet as ft
from components import AppBar_, TextField_, Button_, Text_
import os
from helpers import extract_data
import pandas as pd
from datetime import datetime
from fpdf import FPDF

def main(page: ft.Page):
    info_qr = {}
    registros = []
    table_rows = []
    ruta_archivo = ""

    snackbar = ft.SnackBar(content=ft.Row(height=40), open=False, duration=10000)

    data_table = ft.DataTable(
        border=ft.border.all(2, "#052b47"),
        vertical_lines=ft.border.BorderSide(3, "#052b47"),
        horizontal_lines=ft.border.BorderSide(1, "#052b47"),
        bgcolor="#138db8",
        data_row_color=ft.colors.WHITE,
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Producto", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Color", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Peso (kg)", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Lote", color=ft.Colors.WHITE, expand=True)),
            ft.DataColumn(ft.Text("Fecha", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Hora", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Acciones", color=ft.Colors.WHITE)),
        ],
        rows=[],
        expand=True,
        heading_text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
        data_text_style=ft.TextStyle(color="#052b47", size=14, weight=ft.FontWeight.BOLD),
    )

    def password(_, identificator):
        alert = ft.AlertDialog(
            modal=True,
            title=ft.Text("Contraseña"),
            content=ft.TextField(label="Contraseña", password=True, on_submit=lambda e: open_delete(e, identificator)),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_alert(e)),
                ft.TextButton("Aceptar", on_click=lambda e: open_delete(e, identificator)),
            ],
        )
        page.overlay.append(alert)
        page.update()

        def close_alert(_):
            alert.open = False
            page.update()

        def open_delete(_, identificator):
            print(alert.content.value)
            if alert.content.value == "1234":
                delete(_, identificator)
                alert.open = False
            else:
                alert.content.value = ""
                alert.content.error_text = "Contraseña incorrecta"
                alert.content.focus()
            page.update()

        alert.open = True
        page.update()

    def delete(e, current_id):
        nonlocal registros, table_rows
        registros = list(filter(lambda x: x.get("identificator") != current_id, registros))
        table_rows = []
        for  index, registro in enumerate(registros):
            ident = registro.get("identificator")
            new_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(index + 1))),
                    ft.DataCell(ft.Text(registro.get("Producto", ""), expand=True)),
                    ft.DataCell(ft.Text(registro.get("Color", ""), expand=True)),
                    ft.DataCell(ft.Text(str(registro.get("Peso", "")))),

                    ft.DataCell(ft.Text(registro.get("Lote", ""), expand=True)),
                    ft.DataCell(ft.Text(registro.get("Fecha", ""))),
                    ft.DataCell(ft.Text(registro.get("Hora", ""))),
                    ft.DataCell(
                        ft.ElevatedButton(
                            "Eliminar",
                            on_click=lambda e, ident=ident: password(e, ident)
                        )
                    ),
                ]
            )
            table_rows.append(new_row)
        data_table.rows = table_rows
        producto_texto.value = f"PRODUCTOS ESCANEADOS: {len(registros)}"
        peso_total = sum(item.get("Peso", 0) for item in registros)
        peso_texto.value = f"PESO TOTAL: {peso_total:.3f} kg"
        input_codigo.focus()
        page.update()

    def send(_):
        nonlocal info_qr, table_rows, registros
        info_qr = extract_data(input_codigo.value)

        if info_qr:
            now = datetime.now()
            info_qr["Fecha"] = now.strftime("%Y-%m-%d")
            info_qr["Hora"] = now.strftime("%H:%M:%S")
            info_qr["identificator"] = now.strftime("%Y%m%d%H%M%S%f")  # más preciso

            duplicate = list(filter(lambda x: x.get("Lote") == info_qr.get("Lote") and
                                              x.get("Peso") == info_qr.get("Peso") and
                                              x.get("Producto") == info_qr.get("Producto") and
                                              x.get("Color") == info_qr.get("Color"), registros))

            if duplicate:
                page.open(alert_repeat)
                page.update()
            else:
                current_id = len(registros) + 1
                info_qr["ID"] = current_id
                registros.append(info_qr)

                new_row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(current_id))),
                        ft.DataCell(ft.Text(info_qr.get("Producto", ""), expand=True)),
                        ft.DataCell(ft.Text(info_qr.get("Color", ""), expand=True)),
                        ft.DataCell(ft.Text(str(info_qr.get("Peso", "")))),
                        ft.DataCell(ft.Text(info_qr.get("Lote", ""), expand=True)),
                        ft.DataCell(ft.Text(info_qr.get("Fecha", ""))),
                        ft.DataCell(ft.Text(info_qr.get("Hora", ""))),
                        ft.DataCell(ft.ElevatedButton("Eliminar", on_click=lambda e, ident=info_qr["identificator"]: password(e, ident))),
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

    def export():
        nonlocal registros, table_rows, ruta_archivo
        if not registros:
            return

        if not os.path.exists("reportes"):
            os.makedirs("reportes")

        df = pd.DataFrame(registros)

        resumen = {
            "Total de productos escaneados": [len(registros)],
            "Suma total de peso (kg)": [sum(item.get("Peso", 0) for item in registros)]
        }
        df_resumen = pd.DataFrame(resumen)

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_archivo = f"reportes/reporte_{fecha}.xlsx"
        ruta_pdf = f"reportes/reporte_{fecha}.pdf"

        # Guardar Excel
        with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Registros", index=False)
            df_resumen.to_excel(writer, sheet_name="Resumen", index=False)

        # Crear PDF
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "REPORTE DE ESCANEOS - SAN FRANCISCO TEXTIL", ln=True, align='C')
        pdf.set_font("Arial", '', 10)

        # Encabezado
        headers = ["ID", "Producto", "Color", "Peso (kg)", "Lote", "Fecha", "Hora"]
        for header in headers:
            pdf.cell(40, 10, header, border=1)
        pdf.ln()


        # Datos
        for reg in registros:
            pdf.cell(40, 10, str(reg.get("ID", "")), border=1)
            pdf.cell(40, 10, str(reg.get("Producto", ""))[:15], border=1)
            pdf.cell(40, 10, str(reg.get("Color", ""))[:15], border=1)
            pdf.cell(40, 10, str(reg.get("Peso", "")), border=1)
            pdf.cell(40, 10, str(reg.get("Lote", "")), border=1)
            pdf.cell(40, 10, str(reg.get("Fecha", "")), border=1)
            pdf.cell(40, 10, str(reg.get("Hora", "")), border=1)
            pdf.ln()

        # Resumen
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Total de productos escaneados: {len(registros)}", ln=True)
        peso_total = sum(item.get("Peso", 0) for item in registros)
        pdf.cell(0, 10, f"Suma total de peso (kg): {peso_total:.3f}", ln=True)
        # Fecha del reporte
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f"Fecha de generación del reporte: {fecha_actual}", ln=True, align='C')

        pdf.output(ruta_pdf)

        registros.clear()
        table_rows.clear()
        data_table.rows = []
        producto_texto.value = "PRODUCTOS ESCANEADOS: 0"
        peso_texto.value = "PESO TOTAL: 0.000 kg"

        snackbar.content = ft.Row([
            ft.Text(f"Reporte exportado exitosamente como {ruta_archivo} y PDF", size=12),
            ft.TextButton("Ver Excel", on_click=lambda e: os.startfile(os.path.abspath(ruta_archivo)), style=ft.ButtonStyle(color=ft.Colors.WHITE), height=30),
            ft.TextButton("Ver PDF", on_click=lambda e: os.startfile(os.path.abspath(ruta_pdf)), style=ft.ButtonStyle(color=ft.Colors.WHITE), height=30),
        ])
        input_codigo.focus()
        page.open(snackbar)
        page.update()


    def remove_register(_):
        input_codigo.value = ""
        input_codigo.focus()
        alert_repeat.open = False
        page.update()

    def add_to_table(_):
        nonlocal info_qr, table_rows, registros
        current_id = len(registros) + 1
        info_qr["ID"] = current_id
        registros.append(info_qr)

        new_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(current_id))),
                ft.DataCell(ft.Text(info_qr.get("Producto", ""), expand=True)),
                ft.DataCell(ft.Text(info_qr.get("Color", ""), expand=True)),
                ft.DataCell(ft.Text(str(info_qr.get("Peso", "")))),
                ft.DataCell(ft.Text(info_qr.get("Lote", ""), expand=True)),
                ft.DataCell(ft.Text(info_qr.get("Fecha", ""))),
                ft.DataCell(ft.Text(info_qr.get("Hora", ""))),
                ft.DataCell(ft.ElevatedButton("Eliminar", on_click=lambda e, ident=info_qr.get("identificator"): password(e, ident))),
            ]
        )
        table_rows.append(new_row)
        data_table.rows = table_rows

        producto_texto.value = f"PRODUCTOS ESCANEADOS: {len(registros)}"
        peso_total = sum(item.get("Peso", 0) for item in registros)
        peso_texto.value = f"PESO TOTAL: {peso_total:.3f} kg"

        input_codigo.value = ""
        input_codigo.focus()
        alert_repeat.open = False
        page.update()

    input_codigo = TextField_(label="Información del QR", on_sumit=send).create()
    input_codigo.border_radius = 30
    input_codigo.width = 700

    send_button = Button_(on_click=lambda _: send(_), text="ENVIAR", color="#052b47", bgcolor=ft.Colors.WHITE, brdcolor="#052b47", height=50, width=100).create()
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

    producto_texto = Text_(value="PRODUCTOS ESCANEADOS: 0", color="#052b47", size=30).create()
    peso_texto = Text_(value="PESO TOTAL: 0.000 kg", color="#052b47", size=30).create()

    ayuda_button = ft.TextButton("AYUDA", icon=ft.Icons.HELP_ROUNDED, icon_color=ft.Colors.WHITE, style=ft.ButtonStyle(color=ft.Colors.WHITE))

    alert_repeat = ft.AlertDialog(
        modal=True,
        content=ft.Text("EL PRODUCTO YA HA SIDO REGISTRADO", size=25, weight="bold", color="#052b47"),
        actions=[
            Button_(on_click=lambda e: remove_register(e), text="ELIMINAR", color=ft.colors.WHITE, bgcolor=ft.Colors.GREEN, brdcolor=ft.Colors.GREEN, height=50, width=100).create(),
            Button_(on_click=lambda e: add_to_table(e), text="REGISTRAR", color=ft.colors.WHITE, bgcolor=ft.Colors.RED, brdcolor=ft.Colors.RED, height=50, width=120).create(),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    page.appbar = AppBar_(controls=[ayuda_button], name="SAN FRANCISCO TEXTIL").create()
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
    page.add(fila_contenido, fila_texto, ft.Row([data_table], expand=True, vertical_alignment=ft.CrossAxisAlignment.START))
    page.window_full_screen = True
    input_codigo.focus()

ft.app(main)
