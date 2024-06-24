import customtkinter as ctk
import pygetwindow as gw
import pyautogui
import win32gui
import os
import sys


class MouseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Tracker")
        self.root.geometry("600x400")
        self.root.resizable(False, False)  # Make the window non-resizable

        # 아이콘 설정
        if hasattr(sys, "_MEIPASS"):
            icon_path = os.path.join(sys._MEIPASS, "icons", "program_icon.ico")
        else:
            icon_path = os.path.join(
                os.path.dirname(__file__), "icons", "program_icon.ico"
            )
        self.root.iconbitmap(icon_path)

        self.selected_program = ctk.StringVar()
        self.hwnd = None  # 초기화 시 hwnd를 None으로 설정

        self.create_widgets()
        self.update_mouse_position()
        self.update_program_list_periodically()

    def get_program_list(self):
        windows = gw.getAllTitles()
        return [win for win in windows if win]

    def create_widgets(self):
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Title Label
        title_label = ctk.CTkLabel(
            self.root, text="Mouse Tracker", font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Program Selection
        program_label = ctk.CTkLabel(
            self.root, text="Select Program:", font=("Arial", 16)
        )
        program_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="e")

        self.program_combo = ctk.CTkComboBox(
            self.root,
            variable=self.selected_program,
            values=self.get_program_list(),
            command=self.update_program_handle,  # Use command parameter
            font=("Arial", 14),
        )
        self.program_combo.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="w")

        # Absolute Position Label
        self.absolute_label = ctk.CTkLabel(
            self.root, text="Absolute Position: ", anchor="w", font=("Arial", 14)
        )
        self.absolute_label.grid(
            row=2, column=0, padx=(20, 10), pady=10, columnspan=2, sticky="w"
        )

        # Relative Position Label
        self.relative_label = ctk.CTkLabel(
            self.root, text="Relative Position: ", anchor="w", font=("Arial", 14)
        )
        self.relative_label.grid(
            row=3, column=0, padx=(20, 10), pady=10, columnspan=2, sticky="w"
        )

        # Program Size Label
        self.size_label = ctk.CTkLabel(
            self.root, text="Program Size: ", anchor="w", font=("Arial", 14)
        )
        self.size_label.grid(
            row=4, column=0, padx=(20, 10), pady=10, columnspan=2, sticky="w"
        )

    def update_program_handle(self, selected_title):
        print(f"Selected Program: {selected_title}")  # 선택된 프로그램 이름 출력
        self.hwnd = None
        for title in self.get_program_list():
            if selected_title in title:
                self.hwnd = win32gui.FindWindow(None, title)
                print(f"Matching window found: {title}")  # Debug statement
                break
        print(f"Selected hwnd: {self.hwnd}")  # Debug statement
        self.update_program_size_and_position()

    def update_program_size_and_position(self):
        if self.hwnd:
            try:
                left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
                print(
                    f"Window coordinates: left={left}, top={top}, right={right}, bottom={bottom}"
                )  # Debug statement
                width = right - left
                height = bottom - top
                self.size_label.configure(text=f"Program Size: {width}x{height}")
                x, y = pyautogui.position()
                relative_x = x - left
                relative_y = y - top
                self.relative_label.configure(
                    text=f"Relative Position: {relative_x}, {relative_y}"
                )
            except Exception as e:
                print(f"Error getting window rect: {e}")  # Debug statement
                self.size_label.configure(text="Program Size: N/A")
                self.relative_label.configure(text=f"Relative Position: N/A ({str(e)})")
        else:
            self.size_label.configure(text="Program Size: N/A")
            self.relative_label.configure(text="Relative Position: N/A")

    def update_mouse_position(self):
        x, y = pyautogui.position()
        self.absolute_label.configure(text=f"Absolute Position: {x}, {y}")
        self.update_program_size_and_position()
        self.root.after(100, self.update_mouse_position)

    def update_program_list_periodically(self):
        new_program_list = self.get_program_list()
        current_values = self.program_combo.cget("values")
        if set(new_program_list) != set(current_values):
            self.program_combo.configure(values=new_program_list)
        self.root.after(100, self.update_program_list_periodically)  # 1초마다 업데이트


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    app = MouseTrackerApp(root)
    root.mainloop()
