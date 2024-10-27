import flet as ft
import functools


class QnA(ft.Row):
    def __init__(self, question):
        super().__init__()
        self.question = ft.Text(value=question)
        self.ans = ft.TextField()
        self.controls = [self.question, self.ans]
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.expand = True


class QnRadio(ft.Row):
    def __init__(self, question, ans_lst, page):
        super().__init__()
        self.page = page
        self.Q = question
        self.question = ft.Text(value=question)
        content = list(map(lambda ans: ft.Radio(value=ans, label=ans), ans_lst))
        self.radioGroup = ft.RadioGroup(content = ft.Row(content), on_change=lambda e: self.change(e))
        self.controls = [self.question, self.radioGroup]
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.expand = True
        

    def change(self, e):
        self.question.value = self.Q + " " + str(self.radioGroup.value)
        self.page.update()






class Wrapper(ft.Container):
    def __init__(self, ctrl):
        super().__init__(ctrl)


class TextEditor(ft.Container):
    def __init__(self):
        super().__init__()
        self.text_field = ft.TextField(multiline=True, autofocus=True, min_lines=80, content_padding=30, cursor_color="green")
        self.content = self.text_field
        self.expand = True

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
        self.date_picker = ft.DatePicker(on_change=lambda _: self.change_date(), on_dismiss=lambda _: self.on_cancel())
        self.edit_date_btn = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: self.date_picker.pick_date())
        
        self.edit_date = ft.Row([self.edit_date_display, self.date_picker, self.edit_date_btn], visible=False, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=400)
        self.edit_view = ft.Row([self.edit_display, self.edit_display_btn], visible=False, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=400)
        
        self.controls = [ft.Column([self.display_view, self.edit_view, self.edit_date], horizontal_alignment=ft.CrossAxisAlignment.CENTER)]

    def on_cancel(self):
        self.edit_date_display.value = "2000-01-01"
        self.page.update()

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
        self.header = ft.TextField(value="Do self reflection", label="What needs to be done")
        self.add_btn = ft.IconButton(icon=ft.icons.ADD, on_click=lambda x: TodoApp.add_task(self))
        self.header_row = ft.Row([self.header, self.add_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=400)
        
        self.header_date = ft.TextField(value="2000-01-01", label="Pick Date")
        self.date_picker = ft.DatePicker(on_change=lambda _: self.change_date(), date_picker_mode=ft.DatePickerEntryMode.CALENDAR_ONLY)
        self.date_btn = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: self.date_picker.pick_date())
        self.header_date_row = ft.Row([self.header_date, self.date_picker, self.date_btn], width=400, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.controls = [self.header_row, self.header_date_row]
        self.width=400
        

    def add_task(self):
        self.controls.append(Task(self.page, self.header.value, self.delete_task, self.header_date.value))
        self.page.update()
    
    def delete_task(self, task):
        self.controls.remove(task)
        self.page.update()

    def change_date(self):
        self.header_date.value = str(self.date_picker.value)[:10]
        self.page.update()




class Pg(ft.View):
    def __init__(self, route, pgNum, page):
        super().__init__()
        self.route = route
        self.pgNum = pgNum
        self.page = page
        self.bgcolor = ft.colors.BLUE_100
        self.btn_nxt = ft.ElevatedButton("next")
        self.title = ft.Text(value='Page ' + str(pgNum))
        self.btn_prev = ft.ElevatedButton("prev")
        self.row = ft.Row([self.btn_prev, self.title, self.btn_nxt], alignment=ft.MainAxisAlignment.CENTER)
        self.ctn = ft.Container(self.row, alignment=ft.alignment.Alignment(0, 1), expand=True)
        #ctn.border = ft.border.all(10, ft.colors.AMBER)
        self.controls.append(self.ctn)
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

    def set_next_page(self, pg):
        self.btn_nxt.on_click = (lambda x: self.page.go(pg.route))

    def set_prev_page(self, pg):
        self.btn_prev.on_click = (lambda x: self.page.go(pg.route))

    def add_controls(self, lst_controls):
        for i in range(len(lst_controls) - 1, -1, -1):
            self.controls.insert(0, lst_controls[i])
        
        


def generate_text():
    file = open('advice.txt', 'r')
    lst = []
    for i in range(20):
        lst.append(file.readline())
        if i == 19:
            lst[19] += '\n'
    return lst


def router_change(page, route, lst):
    route_lst = list(map(lambda x: x.route, lst))
    page.views.clear()
    page.views.append(lst[0])
    
    index = route_lst.index(route)
    print(index)
    page.views.append(lst[index])
    page.update()










def main(page: ft.Page):
    page.title = "My Journal"
    page.scroll = True
    page0 = Pg("/", 0, page)
    img0_1 = ft.Image(src="journal.jpeg", fit=ft.ImageFit.COVER, width=800, height=480)
    txt0_1 = ft.Text(value='Self Discovery and Growth', size=50)
    txt0_2 = ft.Text(value='Daily Journal', size=25)
    page0.add_controls([img0_1, txt0_1, txt0_2])

    
    
    
    page1 = Pg("/page1", 1, page)
    img1_1 = ft.Image(src="person.jpeg", fit=ft.ImageFit.FIT_WIDTH, width=800, height=500)
    txt1_1 = ft.Text(value='This Journal belongs to', size=25)
    entry1_1 = ft.TextField(text_align=ft.TextAlign.CENTER, width=200)
    page1.add_controls([img1_1, txt1_1, entry1_1])

    
    
    
    page2 = Pg("/page2", 2, page)
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    lv_wrapped = Wrapper(lv)
    lv_wrapped.expand = True
    lst = generate_text()
    for str in lst:
        lv.controls.append(ft.Text(value=str, text_align=ft.TextAlign.CENTER))
    entry2_1 = ft.TextField(hint_text='Add words of affirmation')
    
    def func(entry, dest):
        dest.controls.append(ft.Text(value=entry.value + '\n', text_align=ft.TextAlign.CENTER))
        entry.value=""
        page.update()
    
    btn2_1 = ft.ElevatedButton(text="Add", on_click=lambda _:func(entry2_1, lv))
    text2_1 = ft.Text(value='Words of Affirmation', size=30)
    page2.ctn.expand = False
    page2.add_controls([text2_1, ft.Row([entry2_1, btn2_1], alignment=ft.MainAxisAlignment.CENTER), lv_wrapped])



    page3 = Pg("/page3", 3, page)
    txt3_1 = ft.Text(value="Quick questions", size=40)
    q1 = QnA("How are you feeling today?")
    q2 = QnA("Things you are grateful for")
    q3 = QnA("Affirmation for today")
    q4 = QnRadio("My mood today is", ["Calm", "Happy", "Sad", "Annoyed", "Angry", "Frustrated"], page=page)
    page3.add_controls([txt3_1, q1, q2, q3, q4])
     
    page4 = Pg("/page4", 4, page)
    txt4_1 = ft.Text(value="Rant Page", size= 50)
    txtField4_1 = TextEditor()
    page4.add_controls([txt4_1, txtField4_1])
    page4.ctn.expand = False

    page5 = Pg("/page5", 5, page)
    txt5_1 = ft.Text(value="Tasks for today", size=40)
    t = TodoApp(page)
    page5.add_controls([txt5_1, t])
    page5.horizontal_alignment = ft.CrossAxisAlignment.START
    


    page0.set_next_page(page1)
    page0.set_prev_page(page5)
    
    page1.set_next_page(page2)
    page1.set_prev_page(page0)
    
    page2.set_next_page(page3)
    page2.set_prev_page(page1)
    
    page3.set_next_page(page4)
    page3.set_prev_page(page2)

    page4.set_next_page(page5)
    page4.set_prev_page(page3)

    page5.set_next_page(page0)
    page5.set_prev_page(page4)


    pg_lst = [page0, page1, page2, page3, page4, page5]
   

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = lambda _: router_change(page, page.route, pg_lst)
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(main)