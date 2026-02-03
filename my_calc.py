import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import numpy as np
import sympy as sp

# Appearance settings
ctk.set_appearance_mode("dark")

class Casio991ES(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python fx-991ES Plus")
        self.geometry("420x720")
        self.resizable(False, False)
        self.configure(fg_color="#3b3b3b") # Real Casio body color

        self.last_result = "0"

        # --- Screen Section ---
        self.screen_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=10)
        self.screen_frame.pack(pady=20, padx=20, fill="x")

        self.screen = ctk.CTkEntry(
            self.screen_frame, 
            width=380, 
            height=100, 
            font=("Consolas", 32), 
            justify='right', 
            fg_color="#99b399", # Iconic Green LCD
            text_color="#1a1a1a",
            border_width=0
        )
        self.screen.pack(pady=10, padx=10)

        # --- Button Layout Configuration ---
        # (Text, Row, Col, Color_Type)
        # Types: 'func' (dark), 'num' (light), 'action' (orange)
        buttons = [
            ('abs', 0, 0, 'func'), ('x³', 0, 1, 'func'), ('x²', 0, 2, 'func'), ('^', 0, 3, 'func'), ('log', 0, 4, 'func'),
            ('sin', 1, 0, 'func'), ('cos', 1, 1, 'func'), ('tan', 1, 2, 'func'), ('(', 1, 3, 'func'), (')', 1, 4, 'func'),
            ('sqrt', 2, 0, 'func'), ('7', 2, 1, 'num'), ('8', 2, 2, 'num'), ('9', 2, 3, 'num'), ('DEL', 2, 4, 'action'),
            ('π', 3, 0, 'func'), ('4', 3, 1, 'num'), ('5', 3, 2, 'num'), ('6', 3, 3, 'num'), ('AC', 3, 4, 'action'),
            ('e', 4, 0, 'func'), ('1', 4, 1, 'num'), ('2', 4, 2, 'num'), ('3', 4, 3, 'num'), ('*', 4, 4, 'num'),
            ('0', 5, 0, 'num'), ('.', 5, 1, 'num'), ('x10^x', 5, 2, 'num'), ('Ans', 5, 3, 'num'), ('+', 5, 4, 'num'),
            ('-', 6, 0, 'num'), ('/', 6, 1, 'num'), ('=', 6, 2, 'equal', 3) # Equal spans 3 columns
        ]

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(pady=10, padx=20)

        self.create_buttons(buttons)

    def create_buttons(self, buttons):
        for btn in buttons:
            text, r, c, btype = btn[0], btn[1], btn[2], btn[3]
            colspan = btn[4] if len(btn) > 4 else 1
            
            # Color Logic
            if btype == 'num':
                fg, hover = "#505050", "#666666"
            elif btype == 'action':
                fg, hover = "#8b4513", "#a0522d" # Dark orange/brown
            elif btype == 'equal':
                fg, hover = "#2d5a27", "#3e7a36" # Greenish
            else:
                fg, hover = "#2b2b2b", "#404040"

            button = ctk.CTkButton(
                self.grid_frame, text=text, width=70 * colspan, height=55,
                fg_color=fg, hover_color=hover, font=("Arial", 14, "bold"),
                command=lambda x=text: self.on_click(x)
            )
            button.grid(row=r, column=c, columnspan=colspan, padx=4, pady=4, sticky="nsew")

    def on_click(self, btn):
        curr = self.screen.get()
        
        if btn == 'AC':
            self.screen.delete(0, tk.END)
        elif btn == 'DEL':
            self.screen.delete(len(curr)-1)
        elif btn == '=':
            self.calculate()
        elif btn == 'Ans':
            self.screen.insert(tk.END, self.last_result)
        elif btn == 'x10^x':
            self.screen.insert(tk.END, "*10^")
        elif btn in ['sin', 'cos', 'tan', 'sqrt', 'log', 'abs']:
            self.screen.insert(tk.END, f"{btn}(")
        elif btn == 'x²':
            self.screen.insert(tk.END, "^2")
        elif btn == 'x³':
            self.screen.insert(tk.END, "^3")
        elif btn == 'π':
            self.screen.insert(tk.END, "pi")
        else:
            self.screen.insert(tk.END, btn)

    def calculate(self):
        raw_expr = self.screen.get()
        # Pre-processing for Python math compatibility
        expr = raw_expr.replace('^', '**')
        
        try:
            # Symbolic logic for equations containing 'x'
            if "x" in expr and "=" not in expr:
                 # If just an expression with x, don't solve, just sympify
                 res = sp.sympify(expr)
                 result = res
            elif "=" in expr:
                left, right = expr.split('=')
                equation = sp.Eq(sp.sympify(left), sp.sympify(right))
                result = sp.solve(equation)
            else:
                # Standard Calculation
                safe_dict = {
                    "sin": lambda x: np.sin(np.deg2rad(float(x))),
                    "cos": lambda x: np.cos(np.deg2rad(float(x))),
                    "tan": lambda x: np.tan(np.deg2rad(float(x))),
                    "log": np.log10,
                    "sqrt": np.sqrt,
                    "abs": np.abs,
                    "pi": np.pi,
                    "e": np.e
                }
                result = eval(expr, {"__builtins__": None}, safe_dict)
                
                # Format result
                if isinstance(result, float):
                    result = round(result, 10)

            self.last_result = str(result)
            self.screen.delete(0, tk.END)
            self.screen.insert(0, self.last_result)
            
        except Exception as e:
            messagebox.showerror("Math Error", "Check your syntax")
            print(f"Error: {e}")

if __name__ == "__main__":
    app = Casio991ES()
    app.mainloop()