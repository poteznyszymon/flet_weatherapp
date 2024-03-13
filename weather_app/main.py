import flet as ft
import requests


def main(page: ft.Page) -> None:
    page.window_height = 270
    page.window_width = 400
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(
        title=ft.Text('Weather app', font_family='Bebas Neue', size=30),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED)
        ]
    )

    city_input = [
        ft.TextField(height=50, text_size=20, bgcolor=ft.colors.BLACK),
    ]

    def return_weather(e):
        key = '1a18751a19333f3cad6a1da2e54e2aca'
        city = city_input[0].value
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}'
        response = requests.get(url)
        if response.status_code == 200:
            temp_celsius = to_celsius(response.json()['main']['temp'])
            return f"Temperature in {city}: {temp_celsius}°C"
        else:
            return "Unable to fetch weather data"

    def to_celsius(kelvin: float) -> int:
        return round(kelvin - 273.15)

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text('Weather app', font_family='Bebas Neue', size=30),
                              bgcolor=ft.colors.SURFACE_VARIANT,
                              actions=[
                                  ft.IconButton(ft.icons.WB_SUNNY_OUTLINED)
                              ]
                              ),
                    ft.Column(
                        [ft.Text('Enter city:', size=25, font_family='Bebas Neue'),
                         city_input[0],
                         ft.FilledButton(
                             content=ft.Text('enter', style=ft.TextStyle(color=ft.colors.WHITE), size=25,
                                             font_family='Bebas Neue'),
                             width=400,
                             height=50,
                             on_click=lambda _: page.go("/weather"),
                             style=ft.ButtonStyle(
                                 bgcolor=ft.colors.SURFACE_VARIANT,
                                 shape=ft.RoundedRectangleBorder(radius=4),
                             ),
                         ),
                         ],
                    )
                ],
            )
        )
        if page.route == "/weather":
            page.views.append(
                ft.View(
                    "/weather",
                    [
                        ft.AppBar(title=ft.Text('Weather app', font_family='Bebas Neue', size=30),
                                  leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: page.go("/"), ),
                                  bgcolor=ft.colors.SURFACE_VARIANT,
                                  actions=[
                                      ft.IconButton(ft.icons.WB_SUNNY_OUTLINED)
                                  ]
                                  ),
                        ft.Row(
                            [ft.Text(return_weather(None), font_family='Bebas Neue', size=30),
                             ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            height=160
                        ),
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main)
