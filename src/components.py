import flet as ft

color_tectronic= "#052b47"
class AppBar_():
    def __init__(self,controls, name):
        self.controls = controls
        self.name = name

    def create(self):
        return ft.AppBar(
        elevation=1,
        leading_width=200,
        toolbar_height=70,
        bgcolor= color_tectronic,
        
        title=ft.Text(
            spans=[
                ft.TextSpan(
                    self.name,
                    ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
              
                    ),
                ),
            ],
        ),
        actions=[
                ft.Container(
                    padding=ft.padding.only(right=30, top=5, bottom=10),
                    content=ft.Row(
                        controls=self.controls,
                        spacing=20,
                    ),
                ),
            ],
    )

    
class TextField_:
    def __init__(self,  on_sumit, label: str):
        self.label = label
        self.on_sumit = on_sumit
     
    def create(self):
        return ft.TextField(
        on_submit=self.on_sumit,
        expand=True,
        label=self.label,
        label_style={"color": color_tectronic},
        border_color=color_tectronic,
        col={"sm": 6, "md": 4, "xl": 3},
    )

class Button_():
    def __init__(self, on_click, text: str, color:ft.Colors, icon=ft.Icons, width=None, height=None, icon_color=ft.Colors.BLACK):
        self.text = text
        self.icon = icon
        self.on_click = on_click
        self.color = color
        self.width = width
        self.height = height
        self.icon_color = icon_color

    def create(self):
        return ft.ElevatedButton(
        col={"sm": 6, "md": 4, "xl": 2},
        text=self.text,
        on_click=self.on_click,
        icon_color=self.icon_color,
        bgcolor= ft.Colors.WHITE,
        color= self.color,
        icon= self.icon,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=30),
            side={"": ft.BorderSide(1,self.color)}
        ),
        width=self.width,
        height=self.height,

)
    
class Text_():
    def __init__(self, value, color=ft.Colors.WHITE, size = None):
        self.value = value
        self.color = color
        self.size = size

    def create(self):
        return ft.Text(
        value=self.value,
        size=self.size,
        weight=ft.FontWeight.BOLD,
        color= self.color,
    )