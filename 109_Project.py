# Variable names that start with a letter or underscore, followed by letters, digits and underscore

import tkinter as tk
from tkinter import ttk, messagebox
import time

class FiniteVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Checking")

        # states
        self.states = {
            'q0' : {'_' : 'q1', 'letter' : 'q1', 'other' : 'q_trap', 'digit' : 'q_trap'},
            'q1' : {'_' : 'q1', 'letter' : 'q1', 'digit' : 'q1', 'other' : 'q_trap',},
            'q_trap' : {} #trapstate
        }
        self.current_state = 'q0'
        self.accept_state = {'q1'}

        #create widget
        self.create_widgets()

        # draw
        self.draw_dfa()
        self.highlight_state(self.current_state) #hhighlight initial state

    def create_widgets(self):
        #input
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Enter variable name:").pack(side=tk.LEFT)
        self.entry = ttk.Entry(input_frame, width=30)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<Return>', self.validate_name)

        ttk.Button(input_frame, text="Validate", command=self.validate_name).pack(side=tk.LEFT)

        # Visualization
        v_frame = ttk.Frame(self.root, padding="10")
        v_frame.pack(fill=tk.BOTH, expand=True)

        # canvas
        self.canvas = tk.Canvas(v_frame, width=600, height=300, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status label
        self.status_label = ttk.Label(self.root, text="Current state: q0", padding="10")
        self.status_label.pack(fill=tk.X)

    def draw_dfa(self):
        self.canvas.delete("all")

        #draw state
        self.q0 = self.canvas.create_oval(50, 150, 100, 200, outline='black', width=2)
        self.canvas.create_text(75, 175, text="q0")

        self.q1 = self.canvas.create_oval(200, 150, 250, 200, outline='black', width=2)
        self.canvas.create_text(225, 175, text="q1")
        self.canvas.create_oval(195, 145, 255, 205, outline="black", width=2)  #2nd circle

        self.q_trap = self.canvas.create_oval(350, 150, 400, 200, outline="black", width=2, fill='lightgray')
        self.canvas.create_text(375, 175, text="q_trap")


        #transition
        self.canvas.create_line(100, 175, 200, 175, arrow=tk.LAST, width=2)
        self.canvas.create_text(150, 155, text="underscore, letter")

        self.canvas.create_line(75, 200, 75, 250, 375, 250, 375, 200, arrow=tk.LAST, width=2)
        self.canvas.create_text(150, 240, text="other, digit")

        self.canvas.create_line(225, 200, 225, 250, 375, 250, 375, 200, arrow=tk.LAST, width=2)
        self.canvas.create_text(300, 240, text="other")

        self.canvas.create_line(250, 175, 350, 175, arrow=tk.LAST, width=2)
        self.canvas.create_text(300, 155, text="other")

        self.canvas.create_arc(200, 100, 250, 150, start=0, extent=180, style=tk.ARC , width=2)
        self.canvas.create_text(225, 90, text="underscore, letter, digit")


    def highlight_state(self, state):
        # reset color to normal
        self.canvas.itemconfig(self.q0, fill='white')
        self.canvas.itemconfig(self.q1, fill='white')
        self.canvas.itemconfig(self.q_trap, fill='lightgray')

        # highlight current
        if state == 'q0':
            self.canvas.itemconfig(self.q0, fill='lightblue')
        elif state == 'q1':
            self.canvas.itemconfig(self.q1, fill='lightblue')
        elif state == 'q_trap':
            self.canvas.itemconfig(self.q_trap, fill='salmon')

        self.status_label.config(text=f"Current state: {state}")
        self.root.update()

    def _get_char_type(self, char):
        # return val of input
        if char == '_':
            return '_'
        elif char.isalpha():
            return 'letter'
        elif char.isdigit():
            return 'digit'
        else: 
            return 'other'
        

    def reset_dfa(self):
        # reset
        self.current_state = 'q0'
        self.highlight_state(self.current_state)

    def validate_name(self, event=None):
        name = self.entry.get()

        if not name:
            messagebox.showwarning("Input Error", "Please enter a variable name")
            return
        
        self.reset_dfa()

        for i, char in enumerate(name):
            char_type = self._get_char_type(char)

            # check if valid then move to next state if true
            if self.current_state in self.states and char_type in self.states[self.current_state]:
                self.current_state = self.states[self.current_state][char_type]
            else:
                self.current_state = 'q_trap'

            self.highlight_state(self.current_state)
            self.root.update()
            time.sleep(0.5) #delay for visual 

            if self.current_state == 'q_trap':
                break
        
        # display
        is_valid = self.current_state in self.accept_state
        result = "VALID" if is_valid else "INVALID"
        messagebox.showinfo("Result", f"the variable name '{name}' is {result}")

        self.reset_dfa()

if __name__ == "__main__":
    root = tk.Tk()
    app = FiniteVisualizer(root)
    root.mainloop()



