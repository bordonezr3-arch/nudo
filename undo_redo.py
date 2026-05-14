import tkinter as tk
from tkinter import messagebox


# =========================
# CLASE DEQUE
# =========================

class Deque:

    def __init__(self):
        self.items = []

    def add_front(self, item):
        self.items.insert(0, item)

    def add_rear(self, item):
        self.items.append(item)

    def remove_front(self):
        if self.is_empty():
            raise IndexError("Deque vacía")
        return self.items.pop(0)

    def remove_rear(self):
        if self.is_empty():
            raise IndexError("Deque vacía")
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

    def get_items(self):
        return self.items.copy()


# =========================
# SISTEMA UNDO/REDO
# =========================

class UndoRedoSystem:

    def __init__(self):

        self.undo_stack = Deque()
        self.redo_stack = Deque()
        self.current_state = []

    def add_action(self, action):

        if not action.strip():
            raise ValueError("La acción no puede estar vacía")

        self.undo_stack.add_rear(action)

        self.current_state.append(action)

        self.redo_stack.clear()

    def undo(self):

        if self.undo_stack.is_empty():
            raise Exception("No hay acciones para deshacer")

        action = self.undo_stack.remove_rear()

        self.redo_stack.add_rear(action)

        self.current_state.pop()

        return action

    def redo(self):

        if self.redo_stack.is_empty():
            raise Exception("No hay acciones para rehacer")

        action = self.redo_stack.remove_rear()

        self.undo_stack.add_rear(action)

        self.current_state.append(action)

        return action

    def get_history(self):
        return self.undo_stack.get_items()

    def get_redo_history(self):
        return self.redo_stack.get_items()

    def get_current_state(self):
        return self.current_state


# =========================
# INTERFAZ GRÁFICA
# =========================

class UndoRedoGUI:

    def __init__(self, root):

        self.system = UndoRedoSystem()

        self.root = root
        self.root.title("Sistema Undo y Redo")
        self.root.geometry("700x600")

        title = tk.Label(
            root,
            text="Sistema Undo y Redo con Deque",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        self.entry = tk.Entry(root, width=40, font=("Arial", 12))
        self.entry.pack(pady=10)

        add_button = tk.Button(
            root,
            text="Agregar Acción",
            command=self.add_action,
            bg="green",
            fg="white",
            width=20
        )
        add_button.pack(pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        undo_button = tk.Button(
            button_frame,
            text="UNDO",
            command=self.undo_action,
            bg="orange",
            fg="white",
            width=15
        )
        undo_button.grid(row=0, column=0, padx=10)

        redo_button = tk.Button(
            button_frame,
            text="REDO",
            command=self.redo_action,
            bg="blue",
            fg="white",
            width=15
        )
        redo_button.grid(row=0, column=1, padx=10)

        tk.Label(
            root,
            text="Historial de Acciones",
            font=("Arial", 14, "bold")
        ).pack()

        self.history_box = tk.Text(root, height=10, width=60)
        self.history_box.pack(pady=10)

        tk.Label(
            root,
            text="Estado Actual",
            font=("Arial", 14, "bold")
        ).pack()

        self.state_label = tk.Label(
            root,
            text="",
            font=("Arial", 12),
            width=60,
            height=2,
            relief="solid"
        )
        self.state_label.pack(pady=10)

        self.update_display()

    def add_action(self):

        action = self.entry.get()

        try:

            self.system.add_action(action)

            self.entry.delete(0, tk.END)

            self.update_display()

        except ValueError as error:

            messagebox.showerror("Error", str(error))

    def undo_action(self):

        try:

            self.system.undo()

            self.update_display()

        except Exception as error:

            messagebox.showwarning("Aviso", str(error))

    def redo_action(self):

        try:

            self.system.redo()

            self.update_display()

        except Exception as error:

            messagebox.showwarning("Aviso", str(error))

    def update_display(self):

        self.history_box.delete(1.0, tk.END)

        history = self.system.get_history()

        if not history:

            self.history_box.insert(
                tk.END,
                "No hay acciones registradas"
            )

        else:

            for i, action in enumerate(history, start=1):

                self.history_box.insert(
                    tk.END,
                    f"{i}. {action}\n"
                )

        current_state = self.system.get_current_state()

        if not current_state:

            self.state_label.config(
                text="Sin acciones"
            )

        else:

            self.state_label.config(
                text=" | ".join(current_state)
            )


# =========================
# EJECUCIÓN
# =========================

root = tk.Tk()

app = UndoRedoGUI(root)

root.mainloop()