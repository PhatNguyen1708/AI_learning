import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext
from PIL import Image,ImageTk
from tkinter import filedialog 
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
#colors
co0 = "#ffffff" 
co1 = "#000000"  
co2 = "#4456F0"  
co4 = "#6495ED"   
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
        if self.visual == []:
                messagebox.showinfo("Fail", "Chưa nhập đồ thị")
                return

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
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
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
        way =f"{start} -->"
        check_data=0
        if start == "":
            messagebox.showinfo("Fail", "Chưa nhập đỉnh bắt đầu")
            return
        
        for data in self.visual:
            if start == data[0] or start == data[1]:
                check_data =1
        if check_data == 0:
            messagebox.showinfo("Fail", "Đỉnh không tồn tại")
            return
        
        vertices = set()
        for edge in self.visual:
            vertices.add(edge[0])
            vertices.add(edge[1])

        if len(vertices) < 2:
            messagebox.showinfo("Fail", "Đồ thị phải có hơn 2 đỉnh")
            return
        
        flag = start
        slove = 0
        unvisited = vertices - {start}

        while unvisited:
            min_vertices = None
            min_distance = float('inf')
            for data in self.visual:
                if data[0] == flag and data[1] in unvisited and float(data[2])<min_distance:
                    min_distance = float(data[2])
                    min_vertices = data[1]
                elif data[1] == flag and data[0] in unvisited and float(data[2])<min_distance:
                    min_distance = float(data[2])
                    min_vertices = data[0]

            if min_vertices is None:
                messagebox.showinfo("Fail", "Đồ thị không liên thông")
                return
            
            data =[flag,min_vertices]
            self.visual_temp.append(data)
            slove += min_distance
            flag = min_vertices
            way += f"{min_vertices} -->"
            unvisited.remove(min_vertices)
        
        min_vertices = None
        for data in self.visual:
            if (data[0] == flag and data[1] == start) or (data[1] == flag and data[0] == start):
                slove += float(data[2])
                min_vertices = float(data[2])
                way += f"{start}"
                last_data =[data[0],data[1]]
                self.visual_temp.append(last_data)
                break

        if min_vertices is None:
                self.visual_temp=[]
                messagebox.showinfo("Fail", "Đồ thị không liên thông")
                return
        
        self.draw_GTS()

        self.GUI.e_solve.configure(state="normal")
        self.GUI.e_solve.delete(0, 'end')
        self.GUI.e_solve.insert(0,slove)
        self.GUI.e_solve.configure(state="disabled")
        
        self.GUI.e_way.configure(state="normal")
        self.GUI.e_way.delete(0, 'end')
        self.GUI.e_way.insert(0,way)
        self.GUI.e_way.configure(state="disabled")

    def save_file(self):
        if self.visual == []:
            messagebox.showerror("Error", f"Chưa có dữ liệu đồ thị")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Lưu đồ thị"
        )

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for edge in self.visual:
                        file.write(f"{edge[0]} - {edge[1]} - {edge[2]}\n")
                messagebox.showinfo("Success", f"Đã lưu đồ thị vào file '{file_path}' thành công!")
            except Exception as e:
                messagebox.showerror("Error", f"Lỗi khi lưu file: {str(e)}")

    def open_file(self):
        file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Mở file đồ thị"
        )

        if file_path:
            try:
                self.visual = [] 
                self.edge_colors = {}  
                with open(file_path, 'r') as file:
                    for edge in file:
                        parts = edge.strip().split(' - ')
                        if len(parts) == 3 and self.is_number(parts[2]):
                            a, b, c = parts[0], parts[1], parts[2]
                            self.addEdge(a, b, c)
                        self.draw_graph()
                        self.show()
                    messagebox.showinfo("Success", f"tải đồ thị từ file '{file_path}' thành công!")
            except Exception as e:
                messagebox.showerror("Error", f"Lỗi khi mở file: {str(e)}")


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

        self.GUI.b_draw_graph = tk.Button(self.GUI.frame_function, text="Draw grap", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.draw_graph)
        self.GUI.b_draw_graph.place(x=10, y=110)

        self.GUI.b_add_distance = tk.Button(self.GUI.frame_function, text="Add distance", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.add_graph)
        self.GUI.b_add_distance.place(x=210, y=40)

        self.GUI.b_reset_graph = tk.Button(self.GUI.frame_function, text="Reset", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.reset_graph)
        self.GUI.b_reset_graph.place(x=110, y=110)

        self.GUI.b_save_graph = tk.Button(self.GUI.frame_function, text="Save to file", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.save_file)
        self.GUI.b_save_graph.place(x=210, y=110)

        self.GUI.b_open_graph = tk.Button(self.GUI.frame_function, text="Open file", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.open_file)
        self.GUI.b_open_graph.place(x=210, y=10)

        self.GUI.e_start = tk.Entry(self.GUI.frame_product, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_start.place(x=10, y=170)

        self.GUI.b_GTS = tk.Button(self.GUI.frame_product, text="GTS", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.GTS)
        self.GUI.b_GTS.place(x=100, y=170)

        self.GUI.l_solve = tk.Label(self.GUI.frame_product,text="SLOVE:", font=('Ivy', 11), bg=co0,fg=co1)
        self.GUI.l_solve.place(x=10, y=200)

        self.GUI.e_solve = tk.Entry(self.GUI.frame_product, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_solve.place(x=70, y=200)
        self.GUI.e_solve.configure(state="disabled")

        self.GUI.l_way = tk.Label(self.GUI.frame_product,text="WAY:" ,font=('Ivy', 11), bg=co0,fg=co1)
        self.GUI.l_way.place(x=10, y=230)

        scrollx = ttk.Scrollbar(self.GUI.frame_product, orient="horizontal")
        scrollx.place(x=70, y=250,width=160)


        self.GUI.e_way = tk.Entry(self.GUI.frame_product, width=25, justify='left' ,highlightthickness=1,xscrollcommand=scrollx.set, relief="solid")
        self.GUI.e_way.place(x=70, y=230)
        self.GUI.e_way.configure(state="disabled")
        scrollx.config(command=self.GUI.e_way.xview)

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
