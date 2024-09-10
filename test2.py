import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class NQueens:
    def __init__(self, size):
        self.size = size
        self.board = [0] * self.size
        self.initialize_board()
        self.conflicts = self.calculate_conflicts(self.board)

    def initialize_board(self):
        self.board = list(range(self.size)) 
        random.shuffle(self.board)
        self.conflicts = self.calculate_conflicts(self.board)

    def calculate_conflicts(self, board):
            # Tạo các bộ đếm để đếm số quân hậu trên mỗi hàng và các đường chéo
        row_count = [0] * self.size
        main_diag = [0] * (2 * self.size - 1)  # Đường chéo chính (row - col)
        anti_diag = [0] * (2 * self.size - 1)  # Đường chéo phụ (row + col)
        
        # Cập nhật các bộ đếm dựa trên vị trí các quân hậu
        for col in range(self.size):
            row = board[col]
            row_count[row] += 1
            main_diag[row - col + self.size - 1] += 1
            anti_diag[row + col] += 1
        
        # Tính tổng số xung đột
        conflicts = 0
        for count in row_count:
            if count > 1:
                conflicts += (count * (count - 1)) // 2  # Số xung đột trong hàng
        for count in main_diag:
            if count > 1:
                conflicts += (count * (count - 1)) // 2  # Số xung đột trong đường chéo chính
        for count in anti_diag:
            if count > 1:
                conflicts += (count * (count - 1)) // 2  # Số xung đột trong đường chéo phụ
        
        return conflicts

    def get_neighbors(self):
        # Tạo ra tất cả các hàng xóm có thể bằng cách di chuyển các quân hậu
        neighbors = []
        for col in range(self.size):
            for row in range(self.size):
                if self.board[col] != row:
                    neighbor = list(self.board)
                    neighbor[col] = row
                    neighbors.append(neighbor)
        return neighbors

    def hill_climbing(self):
        # Thực hiện thuật toán Hill Climbing để giải bài toán N-Queens
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

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("N Queens Problem - Hill Climbing")
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.size_entry = tk.Entry(self.master)
        self.size_entry.pack()
        self.size_entry.insert(0, "8")

        display_button = tk.Button(self.master, text="Hiển thị bàn cờ", command=self.display_board)
        display_button.pack()

        solve_button = tk.Button(self.master, text="Giải bài toán", command=self.solve)
        solve_button.pack()

        # Tải và chỉnh kích thước ảnh quân hậu
        self.queen_image = Image.open("queen.png")  # Đảm bảo đường dẫn ảnh đúng
        self.queen_image = self.queen_image.resize((50, 50))
        self.queen_photo = ImageTk.PhotoImage(self.queen_image)

        self.queens = None
        self.conflict_label = tk.Label(self.master, text="Xung đột:")
        self.conflict_label.pack()

    def draw_board(self):
        # Vẽ bàn cờ và các quân hậu
        self.canvas.delete("all")
        size = self.queens.size
        cell_size = min(400 // size, 400 // size)
        for i in range(size):
            for j in range(size):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(i * cell_size, j * cell_size, (i + 1) * cell_size, (j + 1) * cell_size, fill=color)
                if self.queens.board[j] == i:
                    self.canvas.create_image(i * cell_size + cell_size // 2, j * cell_size + cell_size // 2, image=self.queen_photo)
        # Cập nhật hiển thị số xung đột
        self.conflict_label.config(text=f"Xung đột: {self.queens.conflicts}")

    def display_board(self):
        try:
            size = int(self.size_entry.get())
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
                self.conflict_label.config(text=f"Xung đột: {self.queens.conflicts}")
                break
            else:
                # Nếu không tìm được, khởi tạo lại bàn cờ ngẫu nhiên và thử lại
                self.queens.initialize_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
