import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as sd
import tkinter.messagebox as ms
import os

class blocks_art_display():
    colors_list = [["#C5E3FF", ["#0310FF", "#0310AA"]], ["#1D3F31", ["#81FF5B", "#81B85B"]]]
    colors_list_choose = 0
    press_color = colors_list[colors_list_choose][0]
    unpress_colors = colors_list[colors_list_choose][1]
    def __init__(self, root):
        self.root = root
        self.root.title("Blocks art display")
        self.root.geometry("+0+0")
        self.root.resizable(False, False)
        self.grid_background = tk.Frame(self.root, bd = 20, bg = "black", relief = "raised")
        self.grid_background.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.grid_width_default = (11 / 12) * self.root.winfo_screenwidth()
        self.grid_height_default = (1 / 3) * self.root.winfo_screenheight()
        self.grid_rows = 16
        self.grid_columns = 80
        self.block_rows = 8
        self.block_columns = 5
        self.grid_blocks = []
        self.small_block = []
        self.menus_background = tk.Frame(self.root, bd = 10, relief = "ridge", bg = "yellow")
        self.menus_background.grid(row = 1, column = 0, sticky = tk.NSEW)
        if "saved_draws" not in os.listdir(os.getcwd()):
            os.mkdir(os.getcwd() + "/saved_draws")
        
        ## Make grid menu
        self.make_grid_menu_background = tk.Frame(self.menus_background, bd = 5, relief = "solid", bg = "yellow")
        self.make_grid_menu_background.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.make_grid_menu_label = tk.Label(self.make_grid_menu_background, text = "Make grid menu", font = "Arial 25 bold italic", fg = "white", bg = "brown")
        self.make_grid_menu_label.grid(row = 0, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.grid_rows_label = tk.Label(self.make_grid_menu_background, text = "grid rows:", font = "Arial 18 bold", fg = "white", bg = "red")
        self.grid_rows_label.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.grid_rows_choose = ttk.Combobox(self.make_grid_menu_background, font = 'Calibri 20', state = 'readonly', width = 5, values = list(range(1, 41)))
        self.grid_rows_choose.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.grid_columns_label = tk.Label(self.make_grid_menu_background, text = "grid columns:", font = "Arial 18 bold", fg = "white", bg = "red")
        self.grid_columns_label.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.grid_columns_choose = ttk.Combobox(self.make_grid_menu_background, font = 'Calibri 20', state = 'readonly', width = 5, values = list(range(1, 81)))
        self.grid_columns_choose.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.block_rows_label = tk.Label(self.make_grid_menu_background, text = "block rows:", font = "Arial 18 bold", fg = "white", bg = "red")
        self.block_rows_label.grid(row = 3, column = 0, sticky = tk.NSEW)
        self.block_rows_choose = ttk.Combobox(self.make_grid_menu_background, font = 'Calibri 20', state = 'readonly', width = 5, values = self.find_divisors(self.grid_rows))
        self.block_rows_choose.grid(row = 3, column = 1, sticky = tk.NSEW)
        self.block_columns_label = tk.Label(self.make_grid_menu_background, text = "block columns:", font = "Arial 18 bold", fg = "white", bg = "red")
        self.block_columns_label.grid(row = 4, column = 0, sticky = tk.NSEW)
        self.block_columns_choose = ttk.Combobox(self.make_grid_menu_background, font = 'Calibri 20', state = 'readonly', width = 5, values = self.find_divisors(self.grid_columns))
        self.block_columns_choose.grid(row = 4, column = 1, sticky = tk.NSEW)
        self.blocks_number_label = tk.Label(self.make_grid_menu_background, text = "blocks number:", font = "Arial 18 bold", fg = "white", bg = "red")
        self.blocks_number_label.grid(row = 5, column = 0, sticky = tk.NSEW)
        self.blocks_number_info = tk.Label(self.make_grid_menu_background, font = 'Calibri 20', text = "", width = 5, fg = "black", bg = "white")
        self.blocks_number_info.grid(row = 5, column = 1, sticky = tk.NSEW)
        self.show_current_grid_info()
        self.grid_rows_choose.bind("<<ComboboxSelected>>", self.change_block_rows_columns)
        self.grid_columns_choose.bind("<<ComboboxSelected>>", self.change_block_rows_columns)
        self.block_rows_choose.bind("<<ComboboxSelected>>", lambda event: self.blocks_number_info.configure(text = int(int(self.grid_rows_choose.get()) * int(self.grid_columns_choose.get()) / (int(self.block_rows_choose.get()) * int(self.block_columns_choose.get())))))
        self.block_columns_choose.bind("<<ComboboxSelected>>", lambda event: self.blocks_number_info.configure(text = int(int(self.grid_rows_choose.get()) * int(self.grid_columns_choose.get()) / (int(self.block_rows_choose.get()) * int(self.block_columns_choose.get())))))
        self.make_new_grid_button = tk.Button(self.make_grid_menu_background, text = "new grid", font = "Arial 19 bold", fg = "white", bg = "violet",\
                                              command = lambda: self.make_new_grid(self.grid_width_default, self.grid_height_default, int(self.grid_rows_choose.get()), int(self.grid_columns_choose.get()), int(self.block_rows_choose.get()), int(self.block_columns_choose.get())))
        self.make_new_grid_button.grid(row = 7, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.change_blocks_only_button = tk.Button(self.make_grid_menu_background, text = "change blocks only", font = "Arial 19 bold", fg = "white", bg = "violet", command = self.change_blocks_only)
        self.change_blocks_only_button.grid(row = 8, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.current_grid_info_button = tk.Button(self.make_grid_menu_background, text = "show current info", font = "Arial 19 bold", fg = "white", bg = "violet", command = self.show_current_grid_info)
        self.current_grid_info_button.grid(row = 9, column = 0, columnspan = 2, sticky = tk.NSEW)
        
        ## Main menu
        self.main_menu_background = tk.Frame(self.menus_background, bd = 5, relief = "solid", bg = "yellow")
        self.main_menu_background.grid(row = 0, column = 1, sticky = tk.NSEW)
        self.main_menu_label = tk.Label(self.main_menu_background, text = "Main menu", font = "Arial 25 bold italic", fg = "white", bg = "green")
        self.main_menu_label.grid(row = 0, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.clear_button = tk.Button(self.main_menu_background, text = "clear", font = "Arial 20 bold", fg = "white", bg = "black", command = lambda: self.inverse_clear_grid(inverse_mode = False))
        self.clear_button.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.inverse_button = tk.Button(self.main_menu_background, text = "inverse", font = "Arial 20 bold", fg = "white", bg = "black", command = lambda: self.inverse_clear_grid(inverse_mode = True))
        self.inverse_button.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.grid_colors_button = tk.Button(self.main_menu_background, width = 6, text = "◼", font = "Arial 20 bold", fg = blocks_art_display.press_color, bg = blocks_art_display.unpress_colors[0], command = self.change_grid_colors)
        self.grid_colors_button.grid(row = 1, column = 1, rowspan = 2, sticky = tk.NSEW)
        self.square_grid_button = tk.Button(self.main_menu_background, text = "square grid", font = "Arial 20 bold", fg = "white", bg = "black", command = self.square_grid)
        self.square_grid_button.grid(row = 3, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.show_blocks_button = tk.Button(self.main_menu_background, text = "show blocks", font = "Arial 20 bold", fg = "white", bg = "black", command = self.show_blocks)
        self.show_blocks_button.grid(row = 4, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.save_draw_button = tk.Button(self.main_menu_background, text = "save draw", font = "Arial 20 bold", fg = "white", bg = "black", command = self.save_draw)
        self.save_draw_button.grid(row = 5, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.load_draw_label = tk.Label(self.main_menu_background, text = "load draw:", font = "Arial 20 bold", fg = "white", bg = "red")
        self.load_draw_label.grid(row = 6, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.load_draw_list = ttk.Combobox(self.main_menu_background, font = "Calibri 18", state = "readonly", width = 5, values = [file[:-4] for file in os.listdir(os.getcwd() + "/saved_draws")])
        self.load_draw_list.grid(row = 7, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.load_draw_list.bind("<<ComboboxSelected>>", self.load_draw)

        ## Blocks editor menu
        self.blocks_editor_menu_background = tk.Frame(self.menus_background, bd = 5, relief = "solid", bg = "yellow")
        self.blocks_editor_menu_background.grid(row = 0, column = 2, sticky = tk.NSEW)
        self.blocks_editor_menu_label = tk.Label(self.blocks_editor_menu_background, text = "Blocks editor menu", font = "Arial 25 bold italic", fg = "white", bg = "blue")
        self.blocks_editor_menu_label.grid(row = 0, column = 0, columnspan = 3, sticky = tk.NSEW)
        self.current_block_label = tk.Label(self.blocks_editor_menu_background, text = "pointing block:", font = "Arial 18 bold", fg = "white", bg = "red")
        self.current_block_label.grid(row = 1, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.current_block_info = tk.Label(self.blocks_editor_menu_background, font = 'Calibri 20', text = "", width = 5, fg = "black", bg = "white")
        self.current_block_info.grid(row = 1, column = 2, sticky = tk.NSEW)
        self.block_background = tk.Frame(self.blocks_editor_menu_background, bd = 5, relief = "raised")
        self.block_background.grid(row = 2, column = 0, rowspan = 3, sticky = tk.NW)
        self.block_index_label = tk.Label(self.blocks_editor_menu_background, text = "block:", font = "Arial 18 bold", fg = "white", bg = "red")
        self.block_index_label.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.block_index = ttk.Combobox(self.blocks_editor_menu_background, font = "Calibri 20", state = "readonly", width = 5, values = [])
        self.block_index.grid(row = 2, column = 2, sticky = tk.NSEW)
        self.block_index.bind("<<ComboboxSelected>>", self.change_small_block_index)
        self.move_from_to_grid_button = tk.Button(self.blocks_editor_menu_background, text = "from\ngrid", font = "Arial 15 bold", fg = "black", bg = "cyan", command = self.move_from_to_grid)
        self.move_from_to_grid_button.grid(row = 3, column = 1, sticky = tk.NSEW)
        self.move_auto_manual_button = tk.Button(self.blocks_editor_menu_background, text = "auto", width = 6, font = "Arial 15 bold", fg = "black", bg = "cyan", command = self.move_auto_manual)
        self.move_auto_manual_button.grid(row = 4, column = 1, sticky = tk.NSEW)
        self.move_block_button = tk.Button(self.blocks_editor_menu_background, text = "move", font = "Arial 20 bold", fg = "brown", bg = "cyan", command = self.move_small_block)
        self.move_block_button.grid(row = 3, column = 2, sticky = tk.NSEW)
        self.copy_block_button = tk.Button(self.blocks_editor_menu_background, text = "copy", font = "Arial 20 bold", fg = "brown", bg = "cyan", command = self.copy_small_block)
        self.copy_block_button.grid(row = 4, column = 2, sticky = tk.NSEW)
        self.input_block_seq_label = tk.Label(self.blocks_editor_menu_background, text = "binary input:", font = "Arial 18 bold", fg = "white", bg = "red")
        self.input_block_seq_label.grid(row = 5, column = 0, sticky = tk.NSEW)
        self.block_sequence = tk.Text(self.blocks_editor_menu_background, font = "Calibri 10 bold", state = "normal", width = 5, height = 2)
        self.block_sequence.grid(row = 5, column = 1, columnspan = 2, sticky = tk.NSEW)
        self.block_sequence.bind("<Return>", self.get_small_block_sequence)
        self.clear_small_block_button = tk.Button(self.blocks_editor_menu_background, text = "clear", font = "Arial 20 bold", fg = "brown", bg = "cyan", command = lambda: self.inverse_clear_small_block(inverse_mode = False))
        self.clear_small_block_button.grid(row = 6, column = 0, sticky = tk.NSEW)
        self.inverse_small_block_button = tk.Button(self.blocks_editor_menu_background, text = "inverse", font = "Arial 20 bold", fg = "brown", bg = "cyan", command = lambda: self.inverse_clear_small_block(inverse_mode = True))
        self.inverse_small_block_button.grid(row = 6, column = 1, columnspan = 2, sticky = tk.NSEW)
        self.rotate_small_block_anticlockwise_button = tk.Button(self.blocks_editor_menu_background, text = "rotate", font = "Arial 20 bold", fg = "brown", bg = "cyan", command = self.rotate_small_block)
        self.rotate_small_block_anticlockwise_button.grid(row = 7, column = 0, rowspan = 2, sticky = tk.NSEW)
        self.rotate_small_block_anticlockwise_button = tk.Button(self.blocks_editor_menu_background, text = "rotate: ⭯", font = "Arial 10 bold", fg = "brown", bg = "cyan", command = lambda: self.rotate_small_block("anticlockwise"))
        self.rotate_small_block_anticlockwise_button.grid(row = 7, column = 0, sticky = tk.NSEW)
        self.rotate_small_block_clockwise_button = tk.Button(self.blocks_editor_menu_background, text = "rotate: ⭮", font = "Arial 10 bold", fg = "brown", bg = "cyan", command = lambda: self.rotate_small_block("clockwise"))
        self.rotate_small_block_clockwise_button.grid(row = 8, column = 0, sticky = tk.NSEW)
        self.reflect_small_block_left_right_button = tk.Button(self.blocks_editor_menu_background, text = "reflect: left⬌right", font = "Arial 10 bold", fg = "brown", bg = "cyan", command = lambda: self.reflect_small_block("left-right"))
        self.reflect_small_block_left_right_button.grid(row = 7, column = 1, columnspan = 2, sticky = tk.NSEW)
        self.reflect_small_block_up_down_button = tk.Button(self.blocks_editor_menu_background, text = "reflect: up⬌down", font = "Arial 10 bold", fg = "brown", bg = "cyan", command = lambda: self.reflect_small_block("up-down"))
        self.reflect_small_block_up_down_button.grid(row = 8, column = 1, columnspan = 2, sticky = tk.NSEW)

        ## Blocks info menu
        self.blocks_info_menu_background = tk.Frame(self.menus_background, bd = 5, relief = "solid", bg = "yellow")
        self.blocks_info_menu_background.grid(row = 0, column = 3, sticky = tk.NSEW)
        self.blocks_info_menu_label = tk.Label(self.blocks_info_menu_background, text = "Blocks info menu", font = "Arial 25 bold italic", fg = "white", bg = "black")
        self.blocks_info_menu_label.grid(row = 0, column = 0, columnspan = 5, sticky = tk.NSEW)
        self.info_box_background = tk.Frame(self.blocks_info_menu_background, bd = 2, relief = "solid")
        self.info_box_background.grid(row = 1, column = 0, columnspan = 5, sticky = tk.NSEW)
        self.info_box = tk.Text(self.info_box_background, font = "Calibri 12 bold", state = "normal", width = 64, height = 15)
        self.info_box.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.first_printed_block = ttk.Combobox(self.blocks_info_menu_background, font = "Calibri 20", state = "readonly", width = 2, values = [])
        self.first_printed_block.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.first_printed_block.bind("<<ComboboxSelected>>", self.change_first_printed_block)
        self.seperating_dash = tk.Label(self.blocks_info_menu_background, text = "🡄 from\nto 🡆", font = "Calibri 12 bold", fg = "white", bg = "red")
        self.seperating_dash.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.last_printed_block = ttk.Combobox(self.blocks_info_menu_background, font = "Calibri 20", state = "readonly", width = 2, values = [])
        self.last_printed_block.grid(row = 2, column = 2, sticky = tk.NSEW)
        self.last_printed_block.bind("<<ComboboxSelected>>", self.change_last_printed_block)
        self.print_blocks_button = tk.Button(self.blocks_info_menu_background, text = "print\nblocks", font = "Arial 14 bold", fg = "black", bg = "yellow", command = self.print_blocks)
        self.print_blocks_button.grid(row = 2, column = 3, sticky = tk.NSEW)
        self.make_arduino_instructions_button = tk.Button(self.blocks_info_menu_background, text = "make arduino\ninstructions", font = "Arial 14 bold", fg = "black", bg = "yellow", command = self.make_arduino_instructions)
        self.make_arduino_instructions_button.grid(row = 2, column = 4, sticky = tk.NSEW)

        self.make_new_grid(self.grid_width_default, self.grid_height_default,\
                            int(self.grid_rows_choose.get()), int(self.grid_columns_choose.get()), int(self.block_rows_choose.get()), int(self.block_columns_choose.get()))
        self.show_blocks("show blocks")

    def find_divisors(self, number):
        divisors = []
        for divisor in range(1, int(number / 2 + 1)):
            if number % divisor == 0:
                divisors.append(divisor)
        divisors.append(number)
        return divisors
    def change_block_rows_columns(self, event):
        if event.widget == self.grid_rows_choose:
            self.block_rows_choose["values"] = self.find_divisors(int(self.grid_rows_choose.get()))
            self.block_rows_choose.set(self.block_rows_choose["values"][int(len(self.block_rows_choose["values"]) / 2)])
        if event.widget == self.grid_columns_choose:
            self.block_columns_choose["values"] = self.find_divisors(int(self.grid_columns_choose.get()))
            self.block_columns_choose.set(self.block_columns_choose["values"][int(len(self.block_columns_choose["values"]) / 2)])
        self.blocks_number_info.configure(text = int(int(self.grid_rows_choose.get()) * int(self.grid_columns_choose.get()) / (int(self.block_rows_choose.get()) * int(self.block_columns_choose.get()))))
    def show_current_grid_info(self):
        self.grid_rows_choose.set(self.grid_rows)
        self.grid_columns_choose.set(self.grid_columns)
        self.block_rows_choose.set(self.block_rows)
        self.block_columns_choose.set(self.block_columns)
        self.block_rows_choose["values"] = self.find_divisors(int(self.grid_rows_choose.get()))
        self.block_columns_choose["values"] = self.find_divisors(int(self.grid_columns_choose.get()))
        self.blocks_number_info.configure(text = int(self.grid_rows * self.grid_columns / (self.block_rows * self.block_columns)))
    def make_new_grid(self, grid_width, grid_height, grid_rows, grid_columns, block_rows, block_columns):
        self.grid_rows = grid_rows
        self.grid_columns = grid_columns
        self.block_rows = block_rows
        self.block_columns = block_columns
        for widget in self.grid_background.winfo_children():
            widget.destroy()
        pixel_width = int(grid_width / self.grid_columns)
        pixel_height = int(grid_height / self.grid_rows)
        self.grid_blocks = []
        for i in range(int((self.grid_rows * self.grid_columns) / (self.block_rows * self.block_columns))):
            block = []
            for j in range(self.block_rows):
                for k in range(self.block_columns):
                    block.append(pixel_button(self.grid_background, pixel_width, pixel_height, len(self.grid_blocks), j, k, 0))
                    block[-1].frame_button_grid(((i * self.block_columns) // self.grid_columns) * self.block_rows + j, ((i * self.block_columns) % self.grid_columns) + k)
            self.grid_blocks.append(block)
        self.final_actions_for_grid()
    def change_blocks_only(self):
        if self.grid_rows != int(self.grid_rows_choose.get()) or self.grid_columns != int(self.grid_columns_choose.get()):
            self.show_current_grid_info()
            ms.showwarning("Warning", "You can not change grid rows or grid columns if you want \"change blocks only\" to work! You can only mess with block rows and block columns!")
        else:
            block_rows_previous = self.block_rows
            block_columns_previous = self.block_columns
            self.grid_pixels = []
            for i in range(int(self.grid_rows / block_rows_previous)):
                for j in range(block_rows_previous):
                    for k in range(int(self.grid_columns / block_columns_previous)):
                        for l in range(block_columns_previous):
                            self.grid_pixels.append(self.grid_blocks[i * int(self.grid_columns / block_columns_previous) + k][j * block_columns_previous + l])
            self.block_rows = int(self.block_rows_choose.get())
            self.block_columns = int(self.block_columns_choose.get())
            self.grid_blocks = []
            for i in range(int((self.grid_rows * self.grid_columns) / (self.block_rows * self.block_columns))):
                block = []
                for j in range(self.block_rows):
                    for k in range(self.block_columns):
                        block.append(self.grid_pixels[int((i // (self.grid_columns / self.block_columns)) * (self.block_rows * self.grid_columns) + (i % (self.grid_columns / self.block_columns)) * self.block_columns + j * self.grid_columns + k)])
                        block[-1].block_index = len(self.grid_blocks)
                        block[-1].block_row = j
                        block[-1].block_column = k
                self.grid_blocks.append(block)
            self.final_actions_for_grid()
    def final_actions_for_grid(self):
        self.show_current_grid_info()
        if self.show_blocks_button["text"] == "hide blocks":
            self.show_blocks("show blocks")
        if self.square_grid_button["text"] == "orthogonal grid":
            self.square_grid("square grid")
        for widget in self.block_background.winfo_children():
            widget.destroy()
        self.make_small_block(len(self.grid_blocks), self.block_rows, self.block_columns)
        self.block_index["values"] = list(range(self.blocks_number_info["text"]))
        self.block_index.set(0)
        self.first_printed_block["values"] = list(range(self.blocks_number_info["text"]))
        self.last_printed_block["values"] = list(range(self.blocks_number_info["text"]))
        self.first_printed_block.set(0)
        self.last_printed_block.set(self.blocks_number_info["text"] - 1)
    def make_small_block(self, block_number, block_rows, block_columns):
        pixel_width = int(160 / block_columns)
        pixel_height = int(160 / block_rows)
        self.small_block = []
        for row in range(block_rows):
            for column in range(block_columns):
                self.small_block.append(pixel_button(self.block_background, pixel_width, pixel_height, block_number, row, column, 0))
                self.small_block[-1].frame_button_grid(row, column)
    def make_changes_to_small_block(self):
        small_block_index = int(self.block_index.get())
        for i in range(len(self.small_block)):
            if self.small_block[i].button_is_pressed ^ self.grid_blocks[small_block_index][i].button_is_pressed:
                if self.move_from_to_grid_button["text"] == "to\ngrid":
                    self.grid_blocks[small_block_index][i].press_button()
                elif self.move_from_to_grid_button["text"] == "from\ngrid":
                    self.small_block[i].press_button()
    def change_small_block_index(self, event):
        if self.move_auto_manual_button["text"] == "auto":
            self.make_changes_to_small_block()
    def move_from_to_grid(self):
        self.move_from_to_grid_button.configure(text = ["from\ngrid", "to\ngrid"][[True, False].index(self.move_from_to_grid_button["text"] == "to\ngrid")])
    def move_auto_manual(self):
        self.move_auto_manual_button.configure(text = ["manual", "auto"][[True, False].index(self.move_auto_manual_button["text"] == "auto")])
        if self.move_auto_manual_button["text"] == "auto":
            self.make_changes_to_small_block()        
    def move_small_block(self):
        if self.move_auto_manual_button["text"] == "manual":
            self.make_changes_to_small_block()
    def copy_small_block(self):
        self.copy_block_button.configure(text = ["stop", "copy"][[True, False].index(self.copy_block_button["text"] == "copy")])
    def inverse_clear_small_block(self, inverse_mode):
        for pixel in self.small_block:
            if pixel.button_is_pressed or inverse_mode:
                pixel.press_button()
    def rotate_small_block(self, rotate_direction):
        small_block_info = [self.small_block[x].button_is_pressed for x in range(len(self.small_block))]
        for yold in range(self.block_rows):
            for xold in range(self.block_columns):
                if self.block_rows == self.block_columns:
                    if rotate_direction == "anticlockwise":
                        xnew = yold
                        ynew = -xold + self.block_rows - 1
                    elif rotate_direction == "clockwise":
                        xnew = -yold + self.block_rows - 1
                        ynew = xold
                else:
                    xnew = self.block_columns - 1 - xold
                    ynew = self.block_rows - 1 - yold
                if small_block_info[yold * self.block_columns + xold] ^ self.small_block[ynew * self.block_columns + xnew].button_is_pressed:
                    self.small_block[ynew * self.block_columns + xnew].press_button()
    def reflect_small_block(self, reflect_direction):
        self.small_block_info = [self.small_block[x].button_is_pressed for x in range(len(self.small_block))]
        for i in range(self.block_rows):
            for j in range(self.block_columns):
                if reflect_direction == "left-right":
                    new_row = i
                    new_column = self.block_columns - 1 - j
                elif reflect_direction == "up-down":
                    new_column = j
                    new_row = self.block_rows - 1 - i
                if  self.small_block_info[i * self.block_columns + j] ^ self.small_block[new_row * self.block_columns + new_column].button_is_pressed:
                    self.small_block[new_row * self.block_columns + new_column].press_button()
    def get_small_block_sequence(self, event):
        get_text = self.block_sequence.get("1.0", "end")
        block_seq = ""
        for i in range(len(get_text)):
            if get_text[i] in "01":
                block_seq += get_text[i]
        if self.block_rows * self.block_columns >= len(block_seq):
            block_seq += int(self.block_rows * self.block_columns - len(block_seq)) * "0"
        else:
            block_seq = block_seq[:int(self.block_rows * self.block_columns - len(block_seq))]
        self.inverse_clear_small_block(inverse_mode = False)
        for i in range(len(self.small_block)):
            if block_seq[i] == "1":
                self.small_block[i].press_button()
    def inverse_clear_grid(self, inverse_mode):
        for block in self.grid_blocks:
            for pixel in block:
                if pixel.button_is_pressed or inverse_mode:
                    pixel.press_button()
    def change_grid_colors(self):
        blocks_art_display.colors_list_choose = (blocks_art_display.colors_list_choose + 1) % 2
        blocks_art_display.press_color = blocks_art_display.colors_list[blocks_art_display.colors_list_choose][0]
        blocks_art_display.unpress_colors = blocks_art_display.colors_list[blocks_art_display.colors_list_choose][1]
        self.grid_colors_button.configure(fg = blocks_art_display.press_color, bg = blocks_art_display.unpress_colors[0])
        for block in self.grid_blocks:
            for pixel in block:
                pixel.frame_button.configure(bg = blocks_art_display.unpress_colors[0])
                if pixel.button_is_pressed:
                    pixel.button.configure(bg = blocks_art_display.press_color)
                else:
                    pixel.button.configure(bg = blocks_art_display.unpress_colors[pixel.bg_color])
        for pixel in self.small_block:
            pixel.frame_button.configure(bg = blocks_art_display.unpress_colors[0])
            if pixel.button_is_pressed:
                pixel.button.configure(bg = blocks_art_display.press_color)
            else:
                pixel.button.configure(bg = blocks_art_display.unpress_colors[pixel.bg_color])
    def square_grid(self, action = None):
        if action == None:
            action = self.square_grid_button["text"]
        if action == "orthogonal grid":
            grid_width = self.grid_width_default
            grid_height = self.grid_height_default
        elif action == "square grid":
            if self.grid_rows / self.grid_columns >= self.grid_height_default / (self.grid_width_default):
                grid_height = self.grid_height_default
                grid_width = (self.grid_columns / self.grid_rows) * grid_height
            else:
                grid_width = self.grid_width_default
                grid_height = (self.grid_rows / self.grid_columns) * grid_width
        for block in self.grid_blocks:
            for pixel in block:
                pixel.frame_button.configure(width = grid_width / self.grid_columns, height = grid_height / self.grid_rows)
        self.square_grid_button.configure(text = ["orthogonal grid", "square grid"][[True, False].index(action == "square grid")])
    def show_blocks(self, action = None):
        pixel_bg_color = 0
        if action == None:
            action = self.show_blocks_button["text"]
        for i in range(len(self.grid_blocks)):
            if action == "show blocks":
                pixel_bg_color += 1
                if int(self.grid_columns / self.block_columns) % 2 == 0 and i % int(self.grid_columns / self.block_columns) == 0:
                    pixel_bg_color += 1
            for pixel in self.grid_blocks[i]:
                pixel.bg_color = pixel_bg_color % 2
                if not pixel.button_is_pressed:
                    pixel.button.configure(bg = self.unpress_colors[pixel.bg_color])
        self.show_blocks_button.configure(text = ["hide blocks", "show blocks"][[True, False].index(action == "show blocks")])
    def save_draw(self):
        empty_grid = True
        for block in self.grid_blocks:
            for pixel in block:
                if pixel.button_is_pressed:
                    empty_grid = False
        if not empty_grid:
            ask_draw_name = sd.askstring(parent = self.root, title = 'Draw name', prompt = 'Give the name of the draw:')
            if ask_draw_name != None and ask_draw_name != "":
                overwrite_file_accept = False
                if (ask_draw_name + ".txt") in os.listdir(os.getcwd() + "/saved_draws"):
                    overwrite_file_accept = ms.askyesno("Question", "There is already a file with this name. Do you want to overwrite it?")
                if (ask_draw_name + ".txt") not in os.listdir(os.getcwd() + "/saved_draws") or overwrite_file_accept:
                    draw_file = open(os.getcwd() + "/saved_draws/{}.txt".format(ask_draw_name), "w")
                    draw_file.write("{},{},{},{}\n".format(self.grid_rows, self.grid_columns, self.block_rows, self.block_columns))
                    for block in self.grid_blocks:
                        block_info = ""
                        for pixel in block:
                            if pixel.button_is_pressed:
                                block_info += "1"
                            else:
                                block_info += "0"
                        draw_file.write(block_info + "\n")
                    draw_file.close()
                    ms.showinfo("Information", "File saved successfully!")
                    if not overwrite_file_accept:
                        self.load_draw_list["values"] = (*self.load_draw_list["values"], ask_draw_name)
                else:
                    ms.showinfo("Information", "File was not saved!")
        else:
            ms.showwarning("Warning", "There is nothing to save!")
    def load_draw(self, event):
        draw_file = self.load_draw_list.get() + ".txt"
        load_draw_accept = ms.askyesno("Question", "Are you sure you want to load the file {}?".format(draw_file))
        if load_draw_accept:
            self.draw_info = []
            with open(os.getcwd() + "/saved_draws/{}.txt".format(self.load_draw_list.get()), "r", encoding = "UTF-8") as file:
                for line in file:
                    self.draw_info.append(line[:-1])
            self.grid_info = self.draw_info[0].split(",")
            self.make_new_grid(self.grid_width_default, self.grid_height_default, int(self.grid_info[0]), int(self.grid_info[1]), int(self.grid_info[2]), int(self.grid_info[3]))
            self.pixels_info = self.draw_info[1:]
            for i in range(len(self.grid_blocks)):
                for j in range(len(self.grid_blocks[i])):
                    if int(self.pixels_info[i][j]) == 1:
                        self.grid_blocks[i][j].press_button()
    def write_information_box(self, note, note_color, message):
        text_pointer = self.info_box.index("end")
        self.info_box.insert("end", "\n********************************\n{}: {}".format(note, message))
        self.info_box.tag_add('{}'.format(note), str(float(text_pointer) + 1.0), format(float(text_pointer) + 1.00 + float(len(note) / 100), ".2f"))
        self.info_box.tag_configure("{}".format(note), foreground = note_color, font = "Calibri 14 bold")
        self.info_box.see("end")
    def change_first_printed_block(self, event):
        if int(self.first_printed_block.get()) > int(self.last_printed_block.get()):
            self.last_printed_block.set(int(self.first_printed_block.get()))
    def change_last_printed_block(self, event):
        if int(self.last_printed_block.get()) < int(self.first_printed_block.get()):
            self.first_printed_block.set(int(self.last_printed_block.get()))
    def print_blocks(self):
        first_block = int(self.first_printed_block.get())
        last_block = int(self.last_printed_block.get())
        printed_blocks = ""
        for i in range(last_block - first_block + 1):
            printed_blocks += "\nblock{}: ".format(first_block + i)
            for j in range(self.block_rows):
                block_row = ""
                for k in range(self.block_columns):
                    if self.grid_blocks[first_block + i][j * self.block_columns + k].button_is_pressed:
                        block_row += "1"
                    else:
                        block_row += "0"
                    pass
                printed_blocks += block_row + " "
        self.write_information_box("Printed blocks from {} to {}".format(first_block, last_block), "blue", printed_blocks)
    def make_arduino_instructions(self):
        first_block = int(self.first_printed_block.get())
        last_block = int(self.last_printed_block.get())
        arduino_instructions = ""
        for i in range(last_block - first_block + 1):
            arduino_instructions += "\nbyte block{}[{}] = ".format(i, self.block_rows) + "{"
            for j in range(self.block_rows):
                byte = "B"
                for k in range(self.block_columns):
                    if self.grid_blocks[i][j * self.block_columns + k].button_is_pressed:
                        byte += "1"
                    else:
                        byte += "0"
                    pass
                if j == self.block_rows - 1:
                    arduino_instructions += byte + "};"
                else:
                    arduino_instructions += byte + ", "
        arduino_instructions += "\nbyte *matrix[{}] = ".format(last_block - first_block + 1) + "{"
        for i in range(last_block - first_block):
            arduino_instructions += "block{}, ".format(i)
        arduino_instructions += "block{}".format(last_block - first_block) + "};"
        arduino_instructions += "\n\ncreate_chars();"
        arduino_instructions += "\nlcd_display_show();"
        arduino_instructions += "\n\nvoid create_chars() " + "{" + "\n  for(int i = 0; i < {}; i++)".format(last_block - first_block + 1) + " {" + "\n    lcd.createChar(i, matrix[i]);\n  " + "}\n}"
        arduino_instructions += "\n\nvoid lcd_display_show() {" + "\n  for(int i = 0; i < {}; i++)".format(last_block - first_block + 1) + " {" + "\n    lcd.setCursor(i, 0);\n    lcd.write((uint8_t)i);\n  " + "}\n}"
        self.write_information_box("Arduino instructions for blocks {} - {}".format(first_block, last_block), "red", arduino_instructions)
    
class pixel_button():
    enter_button_state = "highlight"
    continuous_paint_state = "mark"
    highlight_color = "red"
    copy_mode_on = False
    def __init__(self, grid_background, button_width, button_height, block_index, block_row, block_column, bg_color):
        self.grid_background = grid_background
        self.button_width = button_width
        self.button_height = button_height
        self.block_index = block_index
        self.block_row = block_row
        self.block_column = block_column
        self.bg_color = bg_color
        self.button_is_pressed = False
        self.control_highlight = 0
        self.frame_button = tk.Frame(self.grid_background, bd = 1, relief = "solid", width = self.button_width, height = self.button_height, bg = blocks_art_display.unpress_colors[0])
        self.frame_button.grid_propagate(0)
        self.button = tk.Label(self.frame_button, bg = blocks_art_display.unpress_colors[self.bg_color], width = self.button_width, height = self.button_height, compound = "center")
        self.button.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.button.bind("<Button-1>", self.press_button)
        self.button.bind("<Button-2>", self.change_enter_button_mode)
        self.button.bind("<Button-3>", self.change_continuous_paint_state)
        self.button.bind("<Enter>", self.highlight_button_paint_continuously)
        self.button.bind("<Leave>", self.unhighlight_button)
    def frame_button_grid(self, row, column):
        self.frame_button.grid(row = row, column = column, sticky = tk.NSEW)
    def change_enter_button_mode(self, event):
        if pixel_button.enter_button_state == "highlight":
            pixel_button.enter_button_state = "paint"
        elif pixel_button.enter_button_state == "paint":
            pixel_button.enter_button_state = "highlight"
    def change_continuous_paint_state(self, event):
        if pixel_button.continuous_paint_state == "mark":
            pixel_button.continuous_paint_state = "erase"
        elif pixel_button.continuous_paint_state == "erase":
            pixel_button.continuous_paint_state = "mark"
    def highlight_button_paint_continuously(self, event):
        blocks_art_display_root.current_block_info.configure(text = self.block_index)
        if pixel_button.enter_button_state == "highlight":
            if blocks_art_display_root.copy_block_button["text"] == "copy":
                self.button.configure(bg = pixel_button.highlight_color)
            elif blocks_art_display_root.copy_block_button["text"] == "stop":
                self.button.configure(bg = "black")
        elif pixel_button.enter_button_state == "paint":
            if pixel_button.continuous_paint_state == "mark":
                if not self.button_is_pressed:
                    self.press_button()
            elif pixel_button.continuous_paint_state == "erase":
                if self.button_is_pressed:
                    self.press_button()
    def unhighlight_button(self, event):
        try:
            if self.control_highlight == 0:
                self.button.configure(bg = blocks_art_display.unpress_colors[self.bg_color])
            elif self.control_highlight == 1:
                self.button.configure(bg = blocks_art_display.press_color)
        except:
            pass
    def press_button(self, event = None):
        if blocks_art_display_root.copy_block_button["text"] == "stop" and pixel_button.copy_mode_on == False and self.block_index != len(blocks_art_display_root.grid_blocks):
            pixel_button.copy_mode_on = True
            blocks_art_display_root.move_from_to_grid_button.configure(text = "to\ngrid")
            blocks_art_display_root.block_index.set(self.block_index)
            blocks_art_display_root.make_changes_to_small_block()
            self.press_button()
            pixel_button.copy_mode_on = False
        if self.block_index == len(blocks_art_display_root.grid_blocks) and blocks_art_display_root.move_from_to_grid_button["text"] == "to\ngrid" and blocks_art_display_root.move_auto_manual_button["text"] == "auto":
            blocks_art_display_root.grid_blocks[int(blocks_art_display_root.block_index.get())][self.block_row * blocks_art_display_root.block_columns + self.block_column].press_button()
        elif self.block_index == int(blocks_art_display_root.block_index.get()) and blocks_art_display_root.move_from_to_grid_button["text"] == "from\ngrid" and blocks_art_display_root.move_auto_manual_button["text"] == "auto":
            blocks_art_display_root.small_block[self.block_row * blocks_art_display_root.block_columns + self.block_column].press_button()
        if self.button_is_pressed:
            self.button.configure(bg = blocks_art_display.unpress_colors[self.bg_color])
            self.control_highlight = 0
        else:
            self.button.configure(bg = blocks_art_display.press_color)
            self.control_highlight = 1
        self.button_is_pressed = not self.button_is_pressed
            
root = tk.Tk()
blocks_art_display_root = blocks_art_display(root)
root.mainloop()