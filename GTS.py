import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext
from PIL import Image,ImageTk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
#colors
co0 = "#ffffff" #trang
co1 = "#000000"  #den
co2 = "#4456F0"  #xanh
co4 = "#6495ED"   #hongnhat
co5 = "#dda0dd"


class GTS:
    def __init__(self,GUI):
        self.GUI = GUI
        self.fig, self.ax = plt.subplots(figsize=(6, 4.43))
        self.GUI.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = None
        self.visual = []
        self.visual_temp = []
        self.contruction()
        self.edge_colors = {}
        self.show()

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def graph_data(self):
        if self.canvas:
            return
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.GUI.frame_graph)
        self.canvas.get_tk_widget().pack()
    
    def addEdge(self, a, b,c): 
        temp = [a, b,c]
        self.visual.append(temp)
        self.edge_colors[(a, b)] = "gray"  

    def draw_graph(self):

        if not self.canvas:
            self.graph_data()

        self.ax.clear() 
        self.G_main = nx.Graph()

        for edges in self.visual:
            self.G_main.add_edge(edges[0],edges[1],weight=edges[2])

        pos=nx.spring_layout(self.G_main)

        nx.draw(
            self.G_main,
            pos,
            ax=self.ax,
            with_labels=True,
            node_color="skyblue",
            node_size=700,
            font_size=15,
            font_color="black",
            edge_color=[self.edge_colors[(a, b)] if (a, b) in self.edge_colors else "gray" for a, b in self.G_main.edges()],
        )
        edge_labels = nx.get_edge_attributes(self.G_main, 'weight')
        nx.draw_networkx_edge_labels(self.G_main, pos, edge_labels=edge_labels)
        self.canvas.draw()

    def add_graph(self):
        a=self.GUI.e_dinh1.get()
        b=self.GUI.e_dinh2.get()
        c=self.GUI.e_khoangcach.get()
        a=a.upper()
        b=b.upper()
        check_c = self.is_number(c)
        check =0
        if a == '' or b == '' or c == ''or not check_c:
            messagebox.showinfo("Fail", "Dữ liệu sai" )
            return
        for i in range(len(self.visual)):
            if (self.visual[i][0]==a and self.visual[i][1]==b) or (self.visual[i][0]==b and self.visual[i][1]==a):
                check=1
        if check==0:
            self.addEdge(a,b,c)
            self.draw_graph()
            self.show()
        else:
            messagebox.showinfo("Fail", "Trùng cạnh đã nhập" )

    def reset_graph(self):
        self.visual = []
        self.visual_temp = []
        self.edge_colors = {}
        self.draw_graph()
        self.show()

    def show(self):
        global tree

        listheader = ['Đỉnh 1','Đỉnh 2','Khoảng cách']

        tree =ttk.Treeview(self.GUI.frame_product, selectmode="extended", columns=listheader, show="headings")

        scrolly = ttk.Scrollbar(self.GUI.frame_product, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=scrolly.set)

        tree.place(x=10,y=10,width=245,height=150)
        scrolly.place(x=260,y=10,height=150)

        tree.heading(0, text='Đỉnh 1', anchor=tk.NW)
        tree.heading(1, text='Đỉnh 2', anchor=tk.NW)
        tree.heading(2, text='Khoảng cách', anchor=tk.NW)
            
        tree.column(0, width=80,minwidth=80,anchor='nw')
        tree.column(1, width=80,minwidth=80, anchor='nw')
        tree.column(2, width=80,minwidth=80, anchor='nw')

        tree.bind('<Motion>', 'break')

        for item in self.visual:
            tree.insert('', 'end',values=(item[0],item[1],item[2]))
    
    def draw_GTS(self):
        color_input = "red"
        for data in self.visual_temp:   
            if (data[0], data[1]) in self.edge_colors or (data[1], data[0])  in self.edge_colors:
                self.edge_colors[(data[0], data[1])] = color_input
                self.edge_colors[(data[1], data[0])] = color_input
                
        self.draw_graph()

    def GTS(self):
        start = self.GUI.e_start.get()
        start = start.upper()
        check_data=0
        for data in self.visual:
            if start == data[0] or start == data[1]:
                check_data =1
        if check_data == 0:
            return
        self.visual_temp = []
        check_visual = []
        solve = 0
        flat = start
        check = 0
        min_visual = None
        slove = 0
        while True:
            min_line = 1000000000000000
            for data in self.visual:
                if (data[0]== start and data[1] not in check_visual) or (data[1] == start and data[0] not in check_visual):
                    if int(data[2]) < min_line:
                        min_line = int(data[2])
                        if data[0] != start:
                            min_visual = data[0]
                        else:
                            min_visual = data[1]
                        if min_line != 1000000000000000:
                            slove += min_line
                            self.visual_temp.append(data)
            if start not in check_visual:
                check_visual.append(start)
            if check == len(check_visual):
                check_visual.remove(flat)
                check = 10000000000
            start = min_visual
            if check < len(check_visual):
                check = len(check_visual)
            if start == flat:
                self.draw_GTS()
                self.GUI.l_solve.config(text = f"Độ dài đường đi là: {slove}")
                break

        
    def contruction(self):
        self.GUI.title ("GTS")
        self.GUI.geometry('960x520+300+150')
        self.GUI.configure(background=co0)
        self.GUI.resizable(width=tk.FALSE, height=tk.FALSE)

        self.GUI.frame_up = tk.Frame(self.GUI, width=960, height=50, bg = co4)
        self.GUI.frame_up.grid(row= 0, column=0, padx=0, pady=0)

        self.GUI.frame_function = tk.Frame(self.GUI, width=300, height=150, bg = co0,highlightbackground=co1, highlightthickness=2)
        self.GUI.frame_function.place(x=650, y=60)

        self.GUI.frame_product = tk.Frame(self.GUI, width=300, height=287, bg = co0,highlightbackground=co1, highlightthickness=2)
        self.GUI.frame_product.place(x=650, y=220)

        self.GUI.frame_graph = tk.Frame(self.GUI, width=604, height=447, bg = co0,highlightbackground=co1, highlightthickness=2, relief="flat")
        self.GUI.frame_graph.place(x=10, y=60)

        self.GUI.l_dinh1=tk.Label(self.GUI.frame_function, text="Đỉnh 1:", font=('Ivy', 11), bg=co0,fg=co1)
        self.GUI.l_dinh1.place(x=10, y=10)

        self.GUI.l_dinh2=tk.Label(self.GUI.frame_function, text="Đỉnh 2:", font=('Ivy', 11), bg=co0,fg=co1)
        self.GUI.l_dinh2.place(x=10, y=40)

        self.GUI.l_khoangcach=tk.Label(self.GUI.frame_function, text="Khoảng cách:", font=('Ivy', 11), bg=co0,fg=co1)
        self.GUI.l_khoangcach.place(x=10, y=70)

        self.GUI.e_dinh1 = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_dinh1.place(x=105, y=10)  

        self.GUI.e_dinh2 = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_dinh2.place(x=105, y=40)

        self.GUI.e_khoangcach = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_khoangcach.place(x=105, y=70)

        self.GUI.b_draw_graph = tk.Button(self.GUI.frame_function, text="draw grap", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.add_graph)
        self.GUI.b_draw_graph.place(x=10, y=110)

        self.GUI.b_reset_graph = tk.Button(self.GUI.frame_function, text="reset", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.reset_graph)
        self.GUI.b_reset_graph.place(x=110, y=110)

        self.GUI.b_reset_graph = tk.Button(self.GUI.frame_function, text="GTS", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.GTS)
        self.GUI.b_reset_graph.place(x=200, y=110)

        self.GUI.e_start = tk.Entry(self.GUI.frame_product, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_start.place(x=10, y=170)

        self.GUI.l_solve = tk.Label(self.GUI.frame_product, font=('Ivy', 11), bg=co0,fg=co1)
        self.GUI.l_solve.place(x=10, y=200)

        app_name = tk.Label(self.GUI.frame_up, text="GTS", height=1, font=('Verdana 17 bold'), bg=co4 ,fg=co1)
        app_name.place(x=5, y=5) 
    
    def on_closing(self):
        plt.close('all')
        self.GUI.quit()
        self.GUI.destroy()
if __name__ == "__main__":
    GUI = tk.Tk()
    obj = GTS(GUI)
    GUI.mainloop()