import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import time

# Function to execute the selected Python script
def run_script():
    if selected_file.get():
        try:
            file_path = selected_file.get()
            result = subprocess.run(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, result.stdout)
            output_text.insert(tk.END, result.stderr)
        except Exception as e:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"An error occurred: {str(e)}")

# Function to open a file dialog and set the selected file path
def select_script():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        selected_file.set(file_path)
        # Hide the "Select Python Script" button and entry widget
        select_button.pack_forget()
        file_entry.pack_forget()
        # Show the "Unload Script" button
        unload_button.pack()
        # Change the label of the "Hide Options" button to "Options"
        toggle_options_button.config(text="Options")

# Function to unload the selected Python script
def unload_script():
    selected_file.set("")
    # Show the "Select Python Script" button and entry widget
    select_button.pack()
    file_entry.pack()
    # Hide the "Unload Script" button
    unload_button.pack_forget()
    # Change the label of the "Hide Options" button back to "Hide Options"
    toggle_options_button.config(text="Hide Options")

# Function to run the script periodically
def run_periodically():
    if selected_file.get() and execution_interval.get() > 0:
        while not stop_execution.is_set():
            run_script()
            time.sleep(execution_interval.get() * 60)  # Convert minutes to seconds

# Function to start periodic execution
def start_periodic_execution():
    global execution_thread, stop_execution
    if execution_thread is None or not execution_thread.is_alive():
        stop_execution = threading.Event()
        execution_thread = threading.Thread(target=run_periodically)
        execution_thread.daemon = True
        execution_thread.start()

# Function to stop periodic execution
def stop_periodic_execution():
    global stop_execution
    if execution_thread and execution_thread.is_alive():
        stop_execution.set()
        execution_thread.join()

# Function to toggle the visibility of additional options
def toggle_additional_options():
    if additional_options_frame.winfo_ismapped():
        additional_options_frame.pack_forget()
        # Change the label of the "Hide Options" button to "Options"
        toggle_options_button.config(text="Options")
    else:
        additional_options_frame.pack()
        # Change the label of the "Hide Options" button back to "Hide Options"
        toggle_options_button.config(text="Hide Options")

# Create the main application window
app = tk.Tk()
app.title("Hack's GUI Py")

# Create a button to select a Python script
select_button = tk.Button(app, text="Select Python Script", command=select_script)
select_button.pack(pady=10)

# Create an entry widget to display the selected file path (hidden by default)
selected_file = tk.StringVar()
file_entry = tk.Entry(app, textvariable=selected_file, width=40)
file_entry.pack()

# Create a "Run Script" button
run_button = tk.Button(app, text="Run Script", command=run_script)
run_button.pack(pady=10)

# "Unload Script" button (hidden by default)
unload_button = tk.Button(app, text="Unload Script", command=unload_script)
unload_button.pack()
unload_button.pack_forget()

# text widget for displaying the script's output
output_text = tk.Text(app, wrap=tk.WORD, height=10, width=40)
output_text.pack()

# Create a frame for additional options (hidden by default)
additional_options_frame = tk.Frame(app)

# Create an option menu for execution interval
execution_interval_label = tk.Label(additional_options_frame, text="Execution Interval (minutes):")
execution_interval_label.pack()
execution_interval = tk.DoubleVar()
execution_interval.set(1)  # Default interval
interval_option_menu = tk.OptionMenu(additional_options_frame, execution_interval, 1, 5, 10, 15)
interval_option_menu.pack()

# "Start" and "Stop" buttons for periodic execution
start_button = tk.Button(additional_options_frame, text="Start Periodic Execution", command=start_periodic_execution)
start_button.pack(pady=5)
stop_button = tk.Button(additional_options_frame, text="Stop Periodic Execution", command=stop_periodic_execution)
stop_button.pack()

# "Hide Options" button to toggle additional options visibility
toggle_options_button = tk.Button(app, text="Options", command=toggle_additional_options)
toggle_options_button.pack()

# Calculate the minimum size required based on content
app.update_idletasks()
min_width = app.winfo_reqwidth()
min_height = app.winfo_reqheight()
app.minsize(min_width, min_height)

app.mainloop()