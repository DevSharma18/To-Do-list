import tkinter as tk
from tkinter import simpledialog
import customtkinter as ctk

# Appearance and theme setup for customtkinter
ctk.set_appearance_mode("System")  # Switches based on system theme
ctk.set_default_color_theme("blue")  # Available themes: blue (default), dark-blue, green

# Sample task data
tasks = [
    {"task": "Buy groceries", "completed": False},
    {"task": "Finish homework", "completed": False}
]

# Function to refresh task list display
def update_tasks():
    for widget in task_list_frame.winfo_children():
        widget.destroy()  # Remove existing widgets
    
    # Render each task as a checkbox with Edit and Delete buttons
    for idx, task in enumerate(tasks):
        completed_var = tk.BooleanVar(value=task['completed'])  # CheckButton state
        
        checkbox = tk.Checkbutton(
            task_list_frame,
            text=task["task"],
            variable=completed_var,
            onvalue=True,
            offvalue=False,
            command=lambda idx=idx, var=completed_var: toggle_task_completion(idx, var),
            bg="#edf7F6",
            fg="black",
            font=("Sour-Gummy", 12)
        )
        checkbox.grid(row=idx, column=0, sticky='w', padx=10, pady=5)

        # Edit button to modify task
        edit_button = ctk.CTkButton(
            task_list_frame,
            text="Edit",
            command=lambda idx=idx: edit_task(idx),
            fg_color="lightblue",
            text_color="black",
            width=60
        )
        edit_button.grid(row=idx, column=1, padx=10, pady=5)
        
        # Delete button to remove specific task
        delete_button = ctk.CTkButton(
            task_list_frame,
            text="Delete",
            command=lambda idx=idx: delete_task(idx),
            fg_color="lightblue",
            text_color="black",
            width=60
        )
        delete_button.grid(row=idx, column=2, padx=10, pady=5)
    
    task_list_canvas.update_idletasks()  # Update scroll region
    task_list_canvas.config(scrollregion=task_list_canvas.bbox("all"))

# Toggle completion status for a task
def toggle_task_completion(idx, var):
    tasks[idx]['completed'] = var.get()
    update_tasks()

# Clear all tasks
def delete_all_tasks():
    tasks.clear()
    update_tasks()

# Delete a specific task by index
def delete_task(idx):
    tasks.pop(idx)  # Remove the task from the list
    update_tasks()

# Add a new task from the entry input
def add_task(event=None):
    task_text = task_entry.get()
    if task_text:
        tasks.append({"task": task_text, "completed": False})
        task_entry.delete(0, tk.END)
        update_tasks()

# Edit a task's text
def edit_task(idx):
    new_text = simpledialog.askstring("Edit Task", "Enter new task text:", initialvalue=tasks[idx]["task"])
    if new_text:
        tasks[idx]["task"] = new_text
        update_tasks()

# Main window setup
root = ctk.CTk()
root.title("To-Do List")
root.geometry("400x400+100+100")
root.config(bg="#edf7F6")

# Frame for task list with scroll functionality
task_frame = tk.Frame(root, bg="#edf7F6")
task_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

task_list_canvas = tk.Canvas(task_frame, bg="#edf7F6")
task_list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(task_frame, orient="vertical", command=task_list_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")

# Frame inside canvas for task items
task_list_frame = tk.Frame(task_list_canvas, bg="#edf7F6")
task_list_canvas.create_window((0, 0), window=task_list_frame, anchor="nw")

task_list_canvas.config(yscrollcommand=scrollbar.set)

# Frame for entry and buttons at the bottom
button_frame = tk.Frame(root, bg="#ffa8B6")
button_frame.pack(fill=tk.X, side=tk.BOTTOM)

task_entry = ctk.CTkEntry(button_frame, fg_color="white", text_color="black", font=("Poppins", 12))
task_entry.pack(side=tk.LEFT, padx=10, pady=5)

add_button = ctk.CTkButton(button_frame, text="Add Task", command=add_task, fg_color="lightcoral", text_color="black")
add_button.pack(side=tk.LEFT, padx=10, pady=5)

delete_all_button = ctk.CTkButton(button_frame, text="Clear", command=delete_all_tasks, fg_color="lightcoral", text_color="black")
delete_all_button.pack(side=tk.LEFT, padx=10, pady=5)

task_entry.bind("<Return>", add_task)

# Initial population of tasks
update_tasks()

# Enable mouse wheel scrolling
task_list_canvas.bind_all("<MouseWheel>", lambda event: task_list_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

# Start the application
root.mainloop()
