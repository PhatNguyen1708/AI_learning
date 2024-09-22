import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

# colors
co0 = "#ffffff"  # trắng
co1 = "#000000"  # đen
co2 = "#4456F0"  # xanh
co4 = "#6495ED"  # xanh dương nhạt
co5 = "#dda0dd"  # hồng nhạt


class GTS:
    def __init__(self, GUI):
        self.GUI = GUI
        self.fig, self.ax = plt.subplots(figsize=(6, 4.43))
        self.GUI.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = None
        self.visual = []
        self.visual_temp = []
        self.edge_colors = {}  # Lưu màu của từng cạnh
        self.contruction()

    def is_number(self, s):
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

    def addEdge(self, a, b, c):
        temp = [a, b]
        temp_1 = [a, b, c]
        self.visual.append(temp)
        self.visual_temp.append(temp_1)
        self.edge_colors[(a, b)] = "gray"

    def draw_graph(self):
        if not self.canvas:
            self.graph_data()
        self.ax.clear()
        self.G = nx.Graph()

        # Thêm các cạnh với trọng số
        for edge in self.visual_temp:
            self.G.add_edge(edge[0], edge[1], weight=edge[2])

        # Vị trí các đỉnh trên đồ thị
        pos = nx.spring_layout(self.G)

        # Vẽ các đỉnh và cạnh với màu cạnh từ edge_colors
        nx.draw(
            self.G,
            pos,
            ax=self.ax,
            with_labels=True,
            node_color="skyblue",
            node_size=700,
            font_size=15,
            font_color="black",
            edge_color=[self.edge_colors[(a, b)] if (a, b) in self.edge_colors else "gray" for a, b in self.G.edges()],
        )

        # Lấy trọng số (khoảng cách) từ các cạnh và hiển thị trên đồ thị
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)

        self.canvas.draw()

    def add_graph(self):
        a = self.GUI.e_A.get()
        b = self.GUI.e_B.get()
        c = self.GUI.e_C.get()
        check_c = self.is_number(c)
        check = 0
        if a == '' or b == '' or c == '' or not check_c:
            messagebox.showinfo("Fail", "Dữ liệu sai")
            return
        for i in range(len(self.visual)):
            if (self.visual[i][0] == a and self.visual[i][1] == b) or (self.visual[i][0] == b and self.visual[i][1] == a):
                check = 1
        if check == 0:
            self.addEdge(a, b, float(c))  # Chuyển c thành float để hiển thị đúng
            self.draw_graph()
        else:
            messagebox.showinfo("Fail", "Trùng cạnh đã nhập")

    def reset_graph(self):
        self.visual = []
        self.visual_temp = []
        self.edge_colors = {} 
        self.draw_graph()

    def change_edge_color(self):
        edge_input = self.GUI.e_edge_color.get()
        color_input = self.GUI.e_color.get()
        try:
            a, b = edge_input.split(",")  # Giả sử người dùng nhập "A,B"
            a, b = a.strip(), b.strip()
            if (a, b) in self.edge_colors or (b, a) in self.edge_colors:
                self.edge_colors[(a, b)] = color_input
                self.edge_colors[(b, a)] = color_input
                self.draw_graph()
            else:
                messagebox.showinfo("Fail", "Cạnh không tồn tại")
        except:
            messagebox.showinfo("Fail", "Dữ liệu sai. Nhập cạnh dưới dạng 'A,B'.")

    def contruction(self):
        self.GUI.title("GTS")
        self.GUI.geometry('960x520+300+150')
        self.GUI.configure(background=co0)
        self.GUI.resizable(width=tk.FALSE, height=tk.FALSE)

        self.GUI.frame_up = tk.Frame(self.GUI, width=960, height=50, bg=co4)
        self.GUI.frame_up.grid(row=0, column=0, padx=0, pady=0)

        self.GUI.frame_function = tk.Frame(self.GUI, width=300, height=200, bg=co0, highlightbackground=co1, highlightthickness=2)
        self.GUI.frame_function.place(x=650, y=60)

        self.GUI.frame_product = tk.Frame(self.GUI, width=300, height=237, bg=co0, highlightbackground=co1, highlightthickness=2)
        self.GUI.frame_product.place(x=650, y=270)

        self.GUI.frame_graph = tk.Frame(self.GUI, width=604, height=447, bg=co0, highlightbackground=co1, highlightthickness=2, relief="flat")
        self.GUI.frame_graph.place(x=10, y=60)

        self.GUI.e_A = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_A.place(x=20, y=40)

        self.GUI.e_B = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_B.place(x=110, y=40)

        self.GUI.e_C = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_C.place(x=200, y=40)

        self.GUI.b_draw_graph = tk.Button(self.GUI.frame_function, text="Draw Graph", width=10, height=1, bg=co4, font=('Ivy 8 bold'), command=self.add_graph)
        self.GUI.b_draw_graph.place(x=30, y=110)

        self.GUI.b_reset_graph = tk.Button(self.GUI.frame_function, text="Reset", width=10, height=1, bg=co4, font=('Ivy 8 bold'), command=self.reset_graph)
        self.GUI.b_reset_graph.place(x=110, y=110)

        # Thêm các mục nhập và nút cho chức năng đổi màu cạnh
        self.GUI.e_edge_color = tk.Entry(self.GUI.frame_function, width=15, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_edge_color.place(x=20, y=160)
        self.GUI.e_edge_color.insert(0, "A,B")  # Hướng dẫn người dùng nhập đúng định dạng

        self.GUI.e_color = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_color.place(x=180, y=160)
        self.GUI.e_color.insert(0, "red")  # Màu mặc định

        self.GUI.b_change_color = tk.Button(self.GUI.frame_function, text="Change Color", width=10, height=1, bg=co4, font=('Ivy 8 bold'), command=self.change_edge_color)
        self.GUI.b_change_color.place(x=110, y=190)

        self.GUI.l_idle = tk.Label(self.GUI.frame_product, text="Chỗ để dữ liệu của đồ thị. \n Ví dụ: độ dài của cạnh nối giữa 2 điểm. \nÝ tưởng là dùng ttk.Treeview. \n Có thể sẽ để kết quả", font=('Ivy', 11), bg=co0, fg=co1)
        self.GUI.l_idle.place(x=5, y=5)

        app_name = tk.Label(self.GUI.frame_up, text="GTS", height=1, font=('Verdana 17 bold'), bg=co4, fg=co1)
        app_name.place(x=5, y=5)

    def on_closing(self):
        plt.close('all')
        self.GUI.quit()
        self.GUI.destroy()


if __name__ == "__main__":
    GUI = tk.Tk()
    obj = GTS(GUI)
    GUI.mainloop()
