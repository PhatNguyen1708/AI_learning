import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
#colors
co0 = "#ffffff" #trang
co2 = "#4456F0"  #xanh

class NQueens:
    def __init__(self, size):
        self.size = size
        self.board = [0] * self.size
        self.initialize_board()
        self.conflicts=self.calculate_conflicts(self.board)

    def initialize_board(self):
        #random vị trí quân hậu
        self.board = list(range(self.size))
        random.shuffle(self.board) 
        self.x=self.calculate_conflicts(self.board)

    def calculate_conflicts(self, board):
        # Tạo các bộ đếm để đếm số quân hậu trên mỗi hàng và các đường chéo
        row_count = [0] * self.size
        main_diag = [0] * (2 * self.size - 1)
        anti_diag = [0] * (2 * self.size - 1)
        
        for col in range(self.size):
            row = board[col]
            row_count[row] += 1
            main_diag[row - col + self.size - 1] += 1
            anti_diag[row + col] += 1
        
        conflicts = 0
        for count in row_count:
            if count > 1:
                conflicts += (count * (count - 1)) // 2
        for count in main_diag:
            if count > 1:
                conflicts += (count * (count - 1)) // 2
        for count in anti_diag:
            if count > 1:
                conflicts += (count * (count - 1)) // 2 
        return conflicts

    def get_neighbors(self):
        neighbors = []
        for col in range(self.size):
            for row in range(self.size):
                if self.board[col] != row:
                    neighbor = list(self.board)
                    neighbor[col] = row
                    neighbors.append(neighbor)
        return neighbors

    def hill_climbing(self):
        current_conflicts = self.calculate_conflicts(self.board)
        while True:
            neighbors = self.get_neighbors()
            neighbor_conflicts = [self.calculate_conflicts(neighbor) for neighbor in neighbors]
            min_conflict = min(neighbor_conflicts)
            if min_conflict >= current_conflicts:
                break
            current_conflicts = min_conflict
            self.board = neighbors[neighbor_conflicts.index(min_conflict)]
        return self.board, current_conflicts == 0

class HILL_CLIMBING:
    def __init__(self,GUI):
        self.GUI = GUI
        self.contruction()

    def draw_board(self):
        # Vẽ bàn cờ và các quân hậu
        self.GUI.frame_board.delete("all")
        size = self.queens.size
        self.queen_image = Image.open("queen.png")
        self.queen_image = self.queen_image.resize((300//size, 300//size))
        self.queen_photo = ImageTk.PhotoImage(self.queen_image)
        cell_size = min(400 // size, 400 // size)
        for i in range(size):
            for j in range(size):
                color = "#DDA15E" if (i + j) % 2 == 0 else "#BC6C25"
                self.GUI.frame_board.create_rectangle(i * cell_size, j * cell_size, (i + 1) * cell_size, (j + 1) * cell_size, fill=color)
                if self.queens.board[j] == i:
                    self.GUI.frame_board.create_image(i * cell_size + cell_size // 2, j * cell_size + cell_size // 2, image=self.queen_photo)
        self.GUI.conflicts_entry.config(state="normal")
        self.GUI.conflicts_entry.delete(0,tk.END)
        self.GUI.conflicts_entry.insert(0,self.queens.conflicts)
        self.GUI.conflicts_entry.config(state="disabled")

    def display_board(self):
        try:
            size = int(self.GUI.size_entry.get())
            if size < 4:
                messagebox.showerror("Error", "Số lượng quân hậu phải từ 4 trở lên.")
                return
            self.queens = NQueens(size)
            self.draw_board()
        except ValueError:
            messagebox.showerror("Error", "Vui lòng nhập một số hợp lệ.")
    
    def solve(self):
        if not self.queens:
            messagebox.showerror("Error", "Vui lòng hiển thị bàn cờ trước.")
            return
        # Lặp lại quá trình giải cho đến khi tìm được giải pháp
        while True:
            solved_board, solved = self.queens.hill_climbing()
            self.draw_board()
            if solved:
                messagebox.showinfo("Kết quả", "Đã tìm thấy giải pháp.")
                self.queens.conflicts=0
                self.GUI.conflicts_entry.config(state="normal")
                self.GUI.conflicts_entry.delete(0,tk.END)
                self.GUI.conflicts_entry.insert(0,self.queens.conflicts)
                self.GUI.conflicts_entry.config(state="disabled")
                break
            else:
                # Nếu không tìm được, khởi tạo lại bàn cờ ngẫu nhiên và thử lại
                self.queens.initialize_board()

    def contruction(self):
        self.GUI.title ("HILL CLIMBING")
        self.GUI.geometry('424x580+600+100')
        self.GUI.configure(background=co0)
        self.GUI.resizable(width=tk.FALSE, height=tk.FALSE)

        self.GUI.frame_up = tk.Frame(self.GUI, width=420, height=50, bg = "#33FFFF",highlightbackground="black", highlightthickness=2)
        self.GUI.frame_up.grid(row= 0, column=0, padx=0, pady=0)

        self.GUI.frame_function = tk.Frame(self.GUI, width=404, height=90, bg = co0,highlightbackground="black", highlightthickness=2)
        self.GUI.frame_function.place(x=10, y=470)

        self.GUI.frame_board= tk.Canvas(self.GUI, width=399, height=399, bg = co0,highlightbackground="black", highlightthickness=2, relief="flat")
        self.GUI.frame_board.place(x=10, y=60)

        self.GUI.size_lable = tk.Label(self.GUI.frame_function, text="N-Queen:", height=1, font=('Verdana 10 bold'), bg=co0 ,fg="black")
        self.GUI.size_lable.place(x=10, y=10)

        self.GUI.size_entry = tk.Entry(self.GUI.frame_function,width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.size_entry.place(x=90, y=10)
        self.GUI.size_entry.insert(0, "8")

        self.GUI.conflicts_lable = tk.Label(self.GUI.frame_function, text="Conflicts:", height=1, font=('Verdana 10 bold'), bg=co0 ,fg="black")
        self.GUI.conflicts_lable.place(x=200, y=10)

        self.GUI.conflicts_entry = tk.Entry(self.GUI.frame_function,width=9, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
        self.GUI.conflicts_entry.place(x=280, y=10)
        self.GUI.conflicts_entry.insert(0, "0")
        self.GUI.conflicts_entry.config(state="disabled")

        self.GUI.display_button = tk.Button(self.GUI.frame_function, text="Hiển thị bàn cờ", command=self.display_board)
        self.GUI.display_button.place(x=10, y=40)

        self.GUI.solve_button = tk.Button(self.GUI.frame_function, text="Giải bài toán", command=self.solve)
        self.GUI.solve_button.place(x=120, y=40)

        self.queens = None

        app_name = tk.Label(self.GUI.frame_up, text="N-Queen Problem", height=1, font=('Verdana 17 bold'), bg="#33FFFF" ,fg="black")
        app_name.place(x=5, y=5)
    
if __name__ == "__main__":
    GUI = tk.Tk()
    obj = HILL_CLIMBING(GUI)
    GUI.mainloop()