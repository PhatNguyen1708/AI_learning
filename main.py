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
co3 = "#ff69b4"   #hotpink
co4 = "#6495ED"   #hongnhat
co5 = "#dda0dd"


class HILL_CLIMBING:
    def __init__(self,GUI):
        self.GUI = GUI
        self.fig, self.ax = plt.subplots(figsize=(6, 4.43))
        self.GUI.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = None
        self.visual = []
        self.visual_temp = []
        self.contruction()

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
        temp = [a, b]
        temp_1 = [a,b,c]
        self.visual.append(temp)
        self.visual_temp.append(temp_1)  

    def draw_graph(self):
        if not self.canvas:
            self.graph_data()
        self.ax.clear() 
        self.G = nx.Graph()
        self.G.add_edges_from(self.visual)
        nx.draw(
            self.G,
            ax=self.ax,
            with_labels=True,
            node_color="skyblue",
            node_size=700,
            font_size=15,
            font_color="black",
            edge_color="gray",
        )
        self.canvas.draw()

    def add_graph(self):
        a=self.GUI.e_A.get()
        b=self.GUI.e_B.get()
        c=self.GUI.e_C.get()
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
            print(len(self.visual))
        else:
            messagebox.showinfo("Fail", "Trùng cạnh đã nhập" )

    def reset_graph(self):
        self.visual = []
        self.visual_temp = []
        self.draw_graph()

    #def get_neighbors_graph(self):


    # def Hill_Climbing(self):
        

    def contruction(self):
        self.GUI.title ("HILL CLIMBING")
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

        self.GUI.e_A = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_A.place(x=20, y=40)

        self.GUI.e_B = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_B.place(x=110, y=40)

        self.GUI.e_C = tk.Entry(self.GUI.frame_function, width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.e_C.place(x=200, y=40)

        self.GUI.b_draw_graph = tk.Button(self.GUI.frame_function, text="draw grap", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.add_graph)
        self.GUI.b_draw_graph.place(x=30, y=110)

        self.GUI.b_reset_graph = tk.Button(self.GUI.frame_function, text="reset", width=10, height=1, bg=co4, font=('Ivy 8 bold'),command=self.reset_graph)
        self.GUI.b_reset_graph.place(x=110, y=110)

        app_name = tk.Label(self.GUI.frame_up, text="HILL CLIMBING", height=1, font=('Verdana 17 bold'), bg=co4 ,fg=co1)
        app_name.place(x=5, y=5)
    
    def on_closing(self):
        plt.close('all')
        self.GUI.quit()
        self.GUI.destroy()
if __name__ == "__main__":
    GUI = tk.Tk()
    obj = HILL_CLIMBING(GUI)
    GUI.mainloop()