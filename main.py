import tkinter as tk
from tkinter import messagebox
import random
import time


class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.geometry("800x600")
        self.root.config(bg="lightblue")

        # Array-related attributes
        self.array = []
        self.array_size = 0
        self.bar_width = 50
        self.element_count = 0

        # Create a frame for the canvas with a border
        self.canvas_frame = tk.Frame(self.root, bd=5, relief="solid", bg="blue")  # Blue border around canvas
        self.canvas_frame.pack(padx=10, pady=10)

        # Canvas for visualization inside the frame
        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=400, bg="blue")  # Canvas with blue background
        self.canvas.pack()

        # Frame for controls
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=10)

        # Input controls
        tk.Label(self.controls_frame, text="Size:").grid(row=0, column=0, padx=5)
        self.size_entry = tk.Entry(self.controls_frame, width=5)
        self.size_entry.grid(row=0, column=1, padx=5)
        tk.Button(self.controls_frame, text="Set Size", command=self.set_size).grid(row=0, column=2, padx=5)

        tk.Label(self.controls_frame, text="Element:").grid(row=1, column=0, padx=5)
        self.element_entry = tk.Entry(self.controls_frame, width=5)
        self.element_entry.grid(row=1, column=1, padx=5)
        self.element_button = tk.Button(self.controls_frame, text="Insert", command=self.insert_element, state=tk.DISABLED)
        self.element_button.grid(row=1, column=2, padx=5)

        tk.Label(self.controls_frame, text="Delete Index:").grid(row=2, column=0, padx=5)
        self.delete_entry = tk.Entry(self.controls_frame, width=5)
        self.delete_entry.grid(row=2, column=1, padx=5)
        self.delete_button = tk.Button(self.controls_frame, text="Delete", command=self.delete_element, state=tk.DISABLED)
        self.delete_button.grid(row=2, column=2, padx=5)

        self.reset_button = tk.Button(self.controls_frame, text="Reset", command=self.reset, state=tk.DISABLED)
        self.reset_button.grid(row=3, column=0, columnspan=3, pady=5)

        # Sorting buttons
        self.add_sort_buttons()

    def add_sort_buttons(self):
        tk.Button(self.controls_frame, text="Bubble Sort", command=self.bubble_sort, state=tk.DISABLED).grid(row=4, column=0, padx=5)
        tk.Button(self.controls_frame, text="Insertion Sort", command=self.insertion_sort, state=tk.DISABLED).grid(row=4, column=1, padx=5)
        tk.Button(self.controls_frame, text="Quick Sort", command=lambda: self.quick_sort(0, len(self.array) - 1), state=tk.DISABLED).grid(row=4, column=2, padx=5)

        self.sort_buttons = self.controls_frame.winfo_children()

    def enable_controls(self):
        for btn in self.sort_buttons:
            btn.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

    def disable_controls(self):
        for btn in self.controls_frame.winfo_children():
            btn.config(state=tk.DISABLED)
        self.element_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

    def set_size(self):
        try:
            size = int(self.size_entry.get())
            if 0 < size <= 20:
                self.array_size = size
                self.array = []
                self.element_count = 0
                self.element_button.config(state=tk.NORMAL)
                messagebox.showinfo("Info", f"Enter {self.array_size} elements one by one.")
            else:
                messagebox.showerror("Error", "Size must be between 1 to 20")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for array size")

    def insert_element(self):
        try:
            element = int(self.element_entry.get())
            if self.element_count < self.array_size:
                self.array.append(element)
                self.element_count += 1
                self.element_entry.delete(0, tk.END)
                self.draw_array()
                if self.element_count == self.array_size:
                    self.element_button.config(state=tk.DISABLED)
                    self.enable_controls()
                    messagebox.showinfo("Info", "All elements inserted. Choose a sorting technique.")
            else:
                messagebox.showerror("Error", "Array is full")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for element")

    def delete_element(self):
        try:
            index = int(self.delete_entry.get())
            if 0 <= index < len(self.array):
                self.array.pop(index)
                self.draw_array()
            else:
                messagebox.showerror("Error", "Invalid input for index")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for index")

    def reset(self):
        self.array = []
        self.array_size = 0
        self.element_count = 0
        self.size_entry.delete(0, tk.END)
        self.element_entry.delete(0, tk.END)
        self.delete_entry.delete(0, tk.END)
        self.disable_controls()
        self.draw_array()
        messagebox.showinfo("Info", "Reset completed. Start again!")

    def draw_array(self, highlight_index=None):
        self.canvas.delete("all")
        if self.array:
            canvas_width = 800
            self.bar_width = canvas_width / (len(self.array) + 1)
            for i, value in enumerate(self.array):
                x0 = i * self.bar_width
                y0 = 400 - (value * 5)
                x1 = x0 + self.bar_width - 2
                y1 = 400
                color = "red" if i == highlight_index else "lightblue"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                self.canvas.create_text(x0 + self.bar_width / 2, y0 - 10, text=str(value), font=("Arial", 10, "bold"))
        self.root.update_idletasks()

    def bubble_sort(self):
        for i in range(len(self.array)):
            for j in range(len(self.array) - i - 1):
                self.draw_array(highlight_index=j)
                time.sleep(0.5)
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
        self.draw_array()

    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            while j >= 0 and key < self.array[j]:
                self.array[j + 1] = self.array[j]
                j -= 1
                self.draw_array(highlight_index=j)
                time.sleep(0.5)
            self.array[j + 1] = key
        self.draw_array()

    def quick_sort(self, low, high):
        if low < high:
            pivot_index = self.partition(low, high)
            self.draw_array(highlight_index=pivot_index)  # Highlight pivot
            time.sleep(0.5)  # Delay for visualization
            self.quick_sort(low, pivot_index - 1)
            self.quick_sort(pivot_index + 1, high)
        self.draw_array()

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            if self.array[j] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()

	
