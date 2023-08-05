import tkinter as tk
import tkinter.messagebox
import duckdb
import os

def load_homework():
    base_dir = os.path.dirname(__file__) 
    folder_path = os.path.join(base_dir, './homework')
    filename = folder_path + "/homework.db"
    homework = duckdb.connect(filename)
    homework.sql("CREATE TABLE IF NOT EXISTS homework(Id int primary key, Entry varchar(255), Difficulty varchar(255), Amount varchar(255), Completed varchar(255))")
    homework.sql("CREATE SEQUENCE IF NOT EXISTS seq_id START 1")
    return homework

def create_homework():
    if tkinter.messagebox.askokcancel("创建并覆盖", "创建新的作业集将覆盖原来的作业集, 你真的要这么做吗？"):
        base_dir = os.path.dirname(__file__) 
        folder_path = os.path.join(base_dir, './homework')
        filename = folder_path + "/homework.db"
        homework = duckdb.connect(filename)
        homework.sql("DROP TABLE IF EXISTS homework")
        homework.sql("DROP SEQUENCE IF EXISTS seq_id")
        homework.sql("CREATE TABLE homework(Id int primary key, Entry varchar(255), Difficulty varchar(255), Amount varchar(255), Completed varchar(255))")
        homework.sql("CREATE SEQUENCE IF NOT EXISTS seq_id START 1")
        p2.homework = homework

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

# Menu
class Page1(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Homework Helper")
        label.pack(side="top", fill="both", expand=True)
        
# Create New Homework
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.label_entry = tk.Label(self, text="作业条目:")
        self.label_entry.pack()
        self.label_entry.place(x=0,y=100)
        self.input_entry = tk.Entry(self, bg = 'black')
        self.input_entry.pack()
        self.input_entry.place(x=0,y=130)
        self.label_difficulty = tk.Label(self, text="作业难易度:")
        self.label_difficulty.pack()
        self.label_difficulty.place(x=0,y=160)
        self.input_difficulty = tk.Entry(self, bg = 'black')
        self.input_difficulty.pack()
        self.input_difficulty.place(x=0,y=190)
        self.label_amount = tk.Label(self, text="总量:")
        self.label_amount.pack()
        self.label_amount.place(x=0,y=220)
        self.input_amount = tk.Entry(self, bg = 'black')
        self.input_amount.pack()
        self.input_amount.place(x=0,y=250)
        self.btn_write = tk.Button(self, text="写入", command=self.input_page)
        self.btn_write.pack()
        self.btn_write.place(x=0,y=300)
        
    def input_page(self):
        self.entry = str(self.input_entry.get())
        self.difficulty = self.input_difficulty.get()
        self.amount = self.input_amount.get()
        # Check if user input is valid
        if self.entry == '':
            tkinter.messagebox.showwarning(title="警告", message="请勿在 作业条目 栏填写空白数据")
            return

        try:
            int(self.difficulty)
        except ValueError:
            tkinter.messagebox.showwarning(title="警告", message="请勿在 作业难易度 栏填写非整数输入!")
            return

        if int(self.difficulty) <= 0 or None:
            tkinter.messagebox.showwarning(title="警告", message="请勿在 作业难易度 栏填写负数或0输入!")
            return

        try:
            int(self.amount)
        except ValueError:
            tkinter.messagebox.showwarning(title="警告", message="请勿在 总量 栏填写非整数输入!")
            return

        if int(self.amount) <= 0:
            tkinter.messagebox.showwarning(title="警告", message="请勿在 总量 栏填写负数或0输入!")
            return

        self.homework.sql("INSERT INTO homework (Id, Entry, Difficulty, Amount, Completed) VALUES (nextval('seq_id'), '{0}', {1}, {2}, 0)".format(self.entry, self.difficulty, self.amount))
        print("Homework Enrty Added: {0}: Diffifulty:{1}, Amount:{2}".format(self.entry, self.difficulty, self.amount))
        print(self.homework.sql("SELECT * FROM homework").show())
        self.clear_entry()

    # Clear values in the field
    def clear_entry(self):
        self.input_entry.delete(0, 'end')
        self.input_difficulty.delete(0, 'end')
        self.input_amount.delete(0, 'end')

# Upload Homework
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.homework = load_homework()
        print(self.homework.sql("SELECT * FROM homework").show())
        self.ENTRY = list(self.homework.sql("SELECT Entry FROM homework").fetchall())
        self.ENTRY = [i[0] for i in self.ENTRY]
        self.AMOUNT = list(self.homework.sql("SELECT Amount FROM homework").fetchall())
        self.AMOUNT = [i[0] for i in self.AMOUNT]
        self.COMPLETED = list(self.homework.sql("SELECT Completed FROM homework").fetchall())
        self.COMPLETED = [i[0] for i in self.COMPLETED]
        self.OPTIONS = []
        for m in range(0,len(self.ENTRY)):
            self.OPTIONS.append("{0}({1}/{2})".format(self.ENTRY[m], self.COMPLETED[m],self.AMOUNT[m]))
        if self.OPTIONS == []:
            self.OPTIONS = ["None"]
        self.lable_option_menu = tk.Label(self, text="作业条目:")
        self.lable_option_menu.pack()
        self.lable_option_menu.place(x=0, y=100)
        self.variable = tk.StringVar(self)
        try:
            self.variable.set(self.OPTIONS[0])
        except IndexError:
            self.variable.set("None")
        self.option_menu = tk.OptionMenu(self, self.variable, *self.OPTIONS)
        self.option_menu.pack()
        self.option_menu.place(x=0, y=130)
        self.lable_completed = tk.Label(self, text="你又完成了多少量:")
        self.lable_completed.pack()
        self.lable_completed.place(x=0, y=160)
        self.input_completed = tk.Entry(self, bg = 'black')
        self.input_completed.pack()
        self.input_completed.place(x=0, y=190)
        self.btn_write = tk.Button(self, text="写入", command=self.input_page)
        self.btn_write.pack()
        self.btn_write.place(x=0, y=240)

    def input_page(self):
        try:
            self.entry = self.variable.get()
            self.completed = self.input_completed.get()
            try:
                self.completed = int(self.completed)
            except ValueError:
                tkinter.messagebox.showwarning(title="警告", message="请勿在 你又完成了多少量 栏填写非整数输入!")
                return
            self.previous_completed = int(self.homework.sql("SELECT Completed FROM homework WHERE Entry='{0}'".format(self.ENTRY[self.OPTIONS.index(self.entry)])).fetchone()[0])
            self.amount = int(self.homework.sql("SELECT Amount FROM homework WHERE Entry='{0}'".format(self.ENTRY[self.OPTIONS.index(self.entry)])).fetchone()[0])
            if self.completed + self.previous_completed <= self.amount:
                self.homework.sql("UPDATE homework SET Completed='{0}' WHERE Entry='{1}'".format(self.completed+self.previous_completed, self.ENTRY[self.OPTIONS.index(self.entry)]))
            else:
                tkinter.messagebox.showwarning(title="警告", message="你的总完成量已经超过了总量！作业：{0}, 总完成量：{1}+{2}, 总量：{3}.".format(self.ENTRY[self.OPTIONS.index(self.entry)], self.previous_completed, self.completed, self.amount))
            print(self.homework.sql("SELECT * FROM homework").show())
            self.clear_entry()
            self.update_options()
        except Exception as error:
            tkinter.messagebox.showerror(title="错误", message=error)

    def clear_entry(self):
        self.input_completed.delete(0, 'end')

    def update_options(self):
        self.ENTRY = list(self.homework.sql("SELECT Entry FROM homework").fetchall())
        self.ENTRY = [i[0] for i in self.ENTRY]
        self.AMOUNT = list(self.homework.sql("SELECT Amount FROM homework").fetchall())
        self.AMOUNT = [i[0] for i in self.AMOUNT]
        self.COMPLETED = list(self.homework.sql("SELECT Completed FROM homework").fetchall())
        self.COMPLETED = [i[0] for i in self.COMPLETED]
        self.OPTIONS = []
        for m in range(0,len(self.ENTRY)):
            self.OPTIONS.append("{0}({1}/{2})".format(self.ENTRY[m], self.COMPLETED[m],self.AMOUNT[m]))
        if self.OPTIONS == []:
            self.OPTIONS = ["None"]
        self.variable = tk.StringVar(self)
        self.option_menu.destroy()
        self.option_menu = tk.OptionMenu(self, self.variable, *self.OPTIONS)
        self.option_menu.pack()
        self.option_menu.place(x=0, y=130)
        self.variable.set(self.OPTIONS[0])

# Statistics homework
class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.homework = load_homework()
        self.ENTRY = list(self.homework.sql("SELECT Entry FROM homework").fetchall())
        self.ENTRY = [i[0] for i in self.ENTRY]
        self.AMOUNT = list(self.homework.sql("SELECT Amount FROM homework").fetchall())
        self.AMOUNT = [i[0] for i in self.AMOUNT]
        self.COMPLETED = list(self.homework.sql("SELECT Completed FROM homework").fetchall())
        self.COMPLETED = [i[0] for i in self.COMPLETED]
        self.DIFFICULTY = list(self.homework.sql("SELECT Difficulty FROM homework").fetchall())
        self.DIFFICULTY = [i[0] for i in self.DIFFICULTY]
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side = 'right', fill = 'y')
        self.scrollbar.place(x=0, y=200)
        self.mylist = tk.Listbox(self, yscrollcommand = self.scrollbar.set)
        self.btn_statistic = tk.Button(self, text="开始统计", command=self.statistic)
        self.btn_statistic.pack()
        self.btn_statistic.place(x=0, y=100)
    
    def statistic(self):
        self.mylist.delete(0, 'end')
        self.total_difficulty_times_amount = 0
        self.total_completed = 0
        for i in self.AMOUNT:
            self.difficulty = int(self.DIFFICULTY[self.AMOUNT.index(i)])
            self.total_difficulty_times_amount += self.difficulty * int(i)
            self.completed = int(self.COMPLETED[self.AMOUNT.index(i)])
            self.total_completed += self.completed * self.difficulty
            self.completed_percentage = round(self.completed / int(i) * 100, 1)
            self.current_entry = self.ENTRY[self.AMOUNT.index(i)]
            self.mylist.insert('end', "{0} 完成度: {1} %({2}/{3})(难度:{4})".format(self.current_entry, self.completed_percentage, self.completed, i, self.difficulty))

        self.TOTAL_COMPLETED = round(self.total_completed / self.total_difficulty_times_amount * 100, 1)
        self.mylist.insert('end', "\n")
        self.mylist.insert('end', "作业总共完成度: {0}%".format(self.TOTAL_COMPLETED))
        self.mylist.pack(side = 'bottom', fill = 'both' )
        self.scrollbar.config(command = self.mylist.yview)

    def update_data(self):
        self.ENTRY = list(self.homework.sql("SELECT Entry FROM homework").fetchall())
        self.ENTRY = [i[0] for i in self.ENTRY]
        self.AMOUNT = list(self.homework.sql("SELECT Amount FROM homework").fetchall())
        self.AMOUNT = [i[0] for i in self.AMOUNT]
        self.COMPLETED = list(self.homework.sql("SELECT Completed FROM homework").fetchall())
        self.COMPLETED = [i[0] for i in self.COMPLETED]
        self.DIFFICULTY = list(self.homework.sql("SELECT Difficulty FROM homework").fetchall())
        self.DIFFICULTY = [i[0] for i in self.DIFFICULTY]

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        global p1
        global p2
        global p3
        global p4
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="主页", command=p1.show)
        # Notes: command=lambda:[f1(), f2()] means run f1 and f2 at the same time
        b2 = tk.Button(buttonframe, text="创建作业集", command=lambda:[p2.show(), create_homework()])
        b3 = tk.Button(buttonframe, text="更新作业集", command=lambda:[p3.show(), p3.update_options()])
        b4 = tk.Button(buttonframe, text="统计作业集", command=lambda:[p4.show(), p4.update_data()])

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        p1.show()

root = tk.Tk()
root.wm_geometry("500x500")
root.title("Homework Helper")
main = MainView(root)
main.pack(side="top", fill="both", expand=True)

root.mainloop()