from tkinter import ttk
from tkinter import *
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

'''============Конструктор класса для хранения информации об игре=========='''
class GameShop:
    def __init__(self, title, genre, price, developer):
        self.title = title
        self.genre = genre
        self.price = price
        self.developer = developer
        self.t = (self.title, self.genre, self.price, self.developer)
    """==========Строковое представление объекта для отладки=========="""
    def __str__(self):
        return f"{self.title} {self.genre} {self.price} {self.developer}"

'''========Теперь считаем нашу заполненную базу данных и сохраним ее в список экземпляров класса========='''
game_list = []
con = sqlite3.connect("GameShop.db")
cur = con.cursor()
sqlite_select_query = """SELECT title, genre, price, developer from games"""
cur.execute(sqlite_select_query)

'''===========Создадим экземпляр и добавляем его в список с помощью .append========='''
records = cur.fetchall()
for row in records:
    game_list.append(GameShop(row[0], row[1], row[2], row[3]))
cur.close()

"""================Создание главного окна==========="""
root = Tk()
root.geometry("1100x500")
root.configure(background="#2E3440")

"""==========Задание стиля для таблицы=============="""
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background='#3B4252',
                foreground="#ECEFF4",
                fieldbackground="#3B4252",
                font=('Helvetica', 10))
style.configure("Treeview.Heading",
                background="#5E81AC",
                foreground="#ECEFF4",
                font=('Helvetica', 10, 'bold'))
style.map("Treeview", background=[('selected', '#4C566A')])

"""=============Стиль для левой части нашего окна, для таблиц==========="""
left_frame = Frame(root, bg='#5E81AC')
left_frame.pack(side=LEFT, padx= 5, pady=20, fill=BOTH, expand=True)

"""==========Стиль для правой части нашего окна, для кнопок управления и взаимодействия==========="""
right_frame = Frame(root, bg='#5E81AC', width=300)
right_frame.pack(side=RIGHT, padx=20, pady=20, fill=Y)

"""==========Стиль для заголовков================"""
Label(right_frame, text="Фильтры и сортировка",
      bg='#5E81AC', fg="#ECEFF4", font=('Helvetica', 12, 'bold')).pack(pady=10)

"""==============Создаем список для нашей панели управления=============="""
languages = ["Сортировка по жанру (A-Z)", "Сортировка по цене (дешевые)", "Разработчик: Valve", "Разработчик: CD Projekt Red",
    "Разработчик: Rockstar Games", "Жанр: RPG", "Жанр: MOBA"]
languages_var = Variable(value=languages)
languages_listbox = Listbox(
    right_frame,
    listvariable=languages_var,
    selectmode=SINGLE,
    bg="#2E3440",
    fg="#ECEFF4",
    font=('Helvetica', 10),
    height=len(languages),
    borderwidth=0,
    highlightthickness=0
)
languages_listbox.pack(fill=X, pady=10)


columns = ("title", "genre", "price", "developer")
tree = ttk.Treeview(columns=columns, show="headings")

"""===========Настраиваем заголовки столбцов==========="""
tree.heading("title", text="Название", anchor=W)
tree.heading("genre", text="Жанр", anchor=W)
tree.heading("price", text="Цена ($)", anchor=W)
tree.heading("developer", text="Разработчик", anchor=W)

"""========Создаем список кортежей============="""
mylist = [obj.t for obj in game_list]

"""=========Добавляем данные============"""
for game in mylist:
    tree.insert("", "end", values=game)
tree.place(x=10, y=25, width=800, height=150)

"""=======Таблица для отображения результатов фильтрации======="""
tree1 = ttk.Treeview(columns=columns, show="headings")
tree1.place(x=10, y=200, width=800, height=150)
tree1.heading("title", text="Название", anchor=W)
tree1.heading("genre", text="Жанр", anchor=W)
tree1.heading("price", text="Цена ($)", anchor=W)
tree1.heading("developer", text="Разработчик", anchor=W)


"""==========Обработка листа=============="""
def selected(event):
    selected_index = languages_listbox.curselection()
    selected_index = selected_index[0]
    tree1.delete(*tree1.get_children())
    if selected_index == 0:
        el = sorted(mylist, key=lambda x: x[1])
        for game in el:
            tree1.insert("", END, values=game)
    if selected_index == 1:
        el = sorted(mylist, key=lambda x: x[2])
        for game in el:
            tree1.insert("", END, values=game)
    if selected_index == 2:
        for game in filter(lambda l: l[3] == "Valve", mylist):
            tree1.insert("", END, values=game)
    if selected_index == 3:
        for game in filter(lambda l: l[3] == "CD Projekt Red", mylist):
            tree1.insert("", END, values=game)
    if selected_index == 4:
        for game in filter(lambda l: l[3] == "Rockstar Games", mylist):
            tree1.insert("", END, values=game)
    if selected_index == 5:
        for game in filter(lambda l: l[1] == "RPG", mylist):
            tree1.insert("", END, values=game)
    if selected_index == 6:
        for game in filter(lambda l: l[1] == "MOBA", mylist):
            tree1.insert("", END, values=game)

languages_listbox.bind("<<ListboxSelect>>", selected)
x = []
y = []
for t in game_list:
    x.append(t.title)
    y.append(t.price)

def graph():
    figure(figsize=(20, 20))
    plt.barh(x, y, height=0.5, color="#A3BE8C")
    plt.yticks(fontsize=5)
    plt.title("")
    plt.show()

c1 = 0
c2 = 0
c3 = 0
for t in game_list:
    if t.price == 0.00:
        c1 += 1
    elif t.price >= 15.00 and t.price < 30.00:
        c2 += 1
    elif t.price >= 30.00:
        c3 += 1
x1 = [c1, c2, c3]
y1 = ["Price = 0", "15.00 <= Price < 30.00", 'Price >=30.00']


def graph1():
    figure(figsize=(10, 10))
    plt.pie(x1, labels=y1, autopct = '%.1f%%')
    plt.title("")
    plt.show()

button_style = {
    'bg': "#88C0D0",
    'fg': "#2E3440",
    'font': ('Helvetica', 10, 'bold'),
    'borderwidth': 0,
    'highlightthickness': 0,
    'padx': 10,
    'pady': 5
}

Button(right_frame, text="График цен", command=lambda: graph(), **button_style).pack(fill=X, pady=5)
Button(right_frame, text="Распределение цен", command=lambda: graph1(), **button_style).pack(fill=X, pady=5)

root.mainloop()
