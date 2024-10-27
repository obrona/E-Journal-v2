import flet as ft
import datetime

class Task(ft.Row):
    def __init__(self, page, task_name, task_delete, task_date="2000-01-01"):
        super().__init__()
        self.page = page
        
        self.display_txt = ft.Text(value=task_name)
        self.display_date = ft.Text(value=task_date)
        self.edit_btn = ft.IconButton(icon=ft.icons.CREATE, on_click=lambda _: self.edit())
        self.del_btn = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda _:task_delete(self))
        self.display_view = ft.Row([self.display_txt, self.display_date, ft.Row([self.edit_btn, self.del_btn])], visible=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=400)

        self.edit_display = ft.TextField(value=self.display_txt.value, label="Edit Task", border=ft.InputBorder.UNDERLINE)
        self.edit_display_btn = ft.IconButton(icon=ft.icons.DONE, on_click=lambda _: self.save())
        
        self.edit_date_display = ft.TextField(value=self.display_date.value, label="Edit Date", border=ft.InputBorder.UNDERLINE)
        self.date_picker = ft.DatePicker(on_change=lambda _: self.change_date())
        self.edit_date_btn = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: self.date_picker.pick_date())
        
        self.edit_date = ft.Row([self.edit_date_display, self.date_picker, self.edit_date_btn], visible=False, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=400)
        self.edit_view = ft.Row([self.edit_display, self.edit_display_btn], visible=False, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=400)
        
        self.controls = [ft.Column([self.display_view, self.edit_view, self.edit_date], horizontal_alignment=ft.CrossAxisAlignment.CENTER)]


    def change_date(self):
        self.edit_date_display.value = str(self.date_picker.value)[:10]
        self.page.update()

    def edit(self):
        self.edit_display.value = self.display_txt.value
        self.display_view.visible = False
        self.edit_view.visible = True
        self.edit_date.visible = True
        self.page.update()

    def save(self):
        self.display_txt.value=self.edit_display.value
        self.display_view.visible = True
        self.display_date.value = self.edit_date_display.value
        self.edit_view.visible = False
        self.edit_date.visible = False
        self.page.update()
    

class TodoApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.header = ft.TextField(value="xxx", label="What needs to be done")
        self.add_btn = ft.IconButton(icon=ft.icons.ADD, on_click=lambda x: TodoApp.add_task(self))
        self.header_row = ft.Row([self.header, self.add_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=400)
        
        self.header_date = ft.TextField(value="2000-01-01", label="Pick Date")
        self.date_picker = ft.DatePicker(on_change=lambda _: self.change_date(), date_picker_mode=ft.DatePickerEntryMode.CALENDAR_ONLY)
        self.date_btn = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: self.date_picker.pick_date())
        self.header_date_row = ft.Row([self.header_date, self.date_picker, self.date_btn], width=400, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.controls = [self.header_row, self.header_date_row]
        self.width=400
        

    def add_task(self):
        self.controls.append(Task(self.page, self.header.value, self.delete_task, str(self.date_picker.value)[:10]))
        self.page.update()
    
    def delete_task(self, task):
        self.controls.remove(task)
        self.page.update()

    def change_date(self):
        self.header_date.value = str(self.date_picker.value)[:10]
        self.page.update()






def main(page):
   page.add(TodoApp(page))


ft.app(main)
