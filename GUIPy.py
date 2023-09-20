import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import time
import datetime

last_timestamp = ""
loop_iteration = 0
loop_running = False  # Flag to indicate if the loop is running
selected_file_path = None  # Store the selected file path
loop_frequency = 1.0  # Default loop frequency in seconds

def update_text_widget(text):
    global last_timestamp

    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")

    # Check if the timestamp is different from the last one
    if timestamp != last_timestamp:
        last_timestamp = timestamp
        separator = "\n" + "-" * 40 + "\n"  # Line separator after each entry
        formatted_text = "\nLoop iteration " + str(loop_iteration) + ". " + timestamp + "\n" + text  # Add the timestamp to the text
    else:
        formatted_text = text
        separator = ""

    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, formatted_text + separator)
    output_text.see(tk.END)  # Scroll to the end of the text
    output_text.config(state=tk.DISABLED)

# Function to open a file dialog and set the selected file path
def select_script():
    global selected_file_path
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        selected_file_path = file_path
        selected_file.set(selected_file_path)

# Function to run the script
def run_script():
    global loop_iteration, loop_running, loop_frequency
    loop_iteration = 0
    while loop_running:
        if selected_file_path:
            try:
                process = subprocess.Popen(
                    ["python", selected_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                )

                # Read and display the output line by line
                for line in process.stdout:
                    update_text_widget(line)
                for line in process.stderr:
                    update_text_widget(line)

                loop_iteration += 1
                time.sleep(loop_frequency)  # Sleep for the specified frequency
            except Exception as e:
                update_text_widget(f"An error occurred: {str(e)}\n")
        else:
            break

# Function to start or stop the script execution
def toggle_execution():
    global loop_running
    if loop_running:
        loop_running = False
        control_button.config(text="Start")
    else:
        loop_running = True
        control_button.config(text="Stop")
        execution_thread = threading.Thread(target=run_script)
        execution_thread.daemon = True
        execution_thread.start()

# Function to execute the script once
def execute_once():
    global loop_iteration
    loop_iteration = 0  # Reset loop iteration count
    if selected_file_path:
        try:
            process = subprocess.Popen(
                ["python", selected_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            # Read and display the output line by line
            for line in process.stdout:
                update_text_widget(line)
            for line in process.stderr:
                update_text_widget(line)
        except Exception as e:
            update_text_widget(f"An error occurred: {str(e)}\n")

# Function to hide a list of widgets
def hide_widgets(*widgets):
    for widget in widgets:
        widget.pack_forget()

# Function to show a list of widgets
def show_widgets(*widgets):
    for widget in widgets:
        widget.pack()

# Function to handle changes in loop frequency
def on_frequency_change():
    global loop_frequency
    frequency_str = frequency_input.get()
    try:
        loop_frequency = float(frequency_str)
        frequency_input_echo.config(text=f"Current Frequency (seconds): {loop_frequency}")
    except ValueError:
        pass  # Handle invalid input gracefully

# Create the main application window
app = tk.Tk()
app.title("Hack's GUI Py")

# Create a frame for the text widget and scrollbar
output_frame = tk.Frame(app)
scrollbar = tk.Scrollbar(output_frame, orient=tk.VERTICAL)
output_text = tk.Text(output_frame, wrap=tk.WORD, height=20, width=80, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
output_text.config(state=tk.DISABLED)  # Make the text widget read-only
scrollbar.config(command=output_text.yview)

# Place the scrollbar and text widget inside the output_frame using grid
scrollbar.grid(row=0, column=1, sticky="ns")
output_text.grid(row=0, column=0, sticky="nsew")

# Configure weights for grid to allow expansion
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

# Organize the layout using grid
output_frame.pack()

# Create a button to select a Python script
select_button = tk.Button(app, text="Select Python Script", command=select_script, font=("Helvetica", 12))
select_button.pack(pady=10)

# Create an entry widget to display the selected file path
selected_file = tk.StringVar()
file_entry = tk.Entry(app, textvariable=selected_file, width=60, font=("Helvetica", 12))
file_entry.pack()

# Create "Run Once" and "Start Script" buttons side by side
button_frame = tk.Frame(app)
run_once_button = tk.Button(button_frame, text="Run Once", command=execute_once, font=("Helvetica", 12))
run_once_button.pack(side=tk.LEFT, padx=5)
control_button = tk.Button(button_frame, text="Start", command=toggle_execution, font=("Helvetica", 12))
control_button.pack(side=tk.LEFT, padx=5)
button_frame.pack()

# Create a label for loop frequency
frequency_label = tk.Label(app, text="Loop Frequency (seconds):", font=("Helvetica", 12))
frequency_label.pack()

# Create an input field for loop frequency
frequency_input = tk.Entry(app, font=("Helvetica", 12))
frequency_input.pack()

# Create a label to echo the input frequency
frequency_input_echo = tk.Label(app, text="", font=("Helvetica", 12))
frequency_input_echo.pack()

# Create a button to apply loop frequency
apply_frequency_button = tk.Button(app, text="Apply Frequency", command=on_frequency_change, font=("Helvetica", 12))
apply_frequency_button.pack()

# Calculate the minimum size required based on content
app.update_idletasks()
min_width = app.winfo_reqwidth() + 50
min_height = app.winfo_reqheight() + 50
app.minsize(min_width, min_height)

app.mainloop()
