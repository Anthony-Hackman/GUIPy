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
        hide_widgets(select_button, file_entry)
        show_widgets(run_button, frequency_label, frequency_slider)  # Show the run button and frequency-related widgets
        stop_button.pack_forget()  # Hide the stop button
        start_button.pack()  # Show the start button

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

def start_periodic_execution():
    global loop_running
    if not loop_running:
        loop_running = True
        execution_thread = threading.Thread(target=run_script)
        execution_thread.daemon = True
        execution_thread.start()
        start_button.pack_forget()  # Hide the start button
        stop_button.pack()  # Show the stop button

def stop_periodic_execution():
    global loop_running
    if loop_running:
        loop_running = False
        show_widgets(select_button, file_entry, run_button)  # Show the select and run buttons
        hide_widgets(stop_button, frequency_label, frequency_slider)  # Hide the stop button and frequency-related widgets

# Function to hide a list of widgets
def hide_widgets(*widgets):
    for widget in widgets:
        widget.pack_forget()

# Function to show a list of widgets
def show_widgets(*widgets):
    for widget in widgets:
        widget.pack()

# Function to handle changes in loop frequency
def on_frequency_change(value):
    global loop_frequency
    loop_frequency = float(value)

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

# Create a slider to adjust the loop frequency
frequency_label = tk.Label(app, text="Loop Frequency (seconds):", font=("Helvetica", 12, "bold"))
frequency_label.pack()
frequency_slider = tk.Scale(app, from_=0.1, to=5.0, resolution=0.1, orient="horizontal", length=300, command=on_frequency_change)
frequency_slider.set(loop_frequency)
frequency_slider.pack()

# Create a button to select a Python script
select_button = tk.Button(app, text="Select Python Script", command=select_script, font=("Helvetica", 12, "bold"))
select_button.pack()

# Create an entry widget to display the selected file path (hidden by default)
selected_file = tk.StringVar()
file_entry = tk.Entry(app, textvariable=selected_file, width=60, font=("Helvetica", 12, "bold"))
file_entry.pack()

# Create a "Run Script" button
run_button = tk.Button(app, text="Run Script", command=start_periodic_execution, font=("Helvetica", 12, "bold"))
run_button.pack()

# "Stop Script" button (hidden by default)
stop_button = tk.Button(app, text="Stop Script", command=stop_periodic_execution, font=("Helvetica", 12, "bold"))
stop_button.pack()
stop_button.pack_forget()

# "Start Script" button (hidden by default)
start_button = tk.Button(app, text="Start Script", command=start_periodic_execution, font=("Helvetica", 12, "bold"))
start_button.pack()
start_button.pack_forget()

# Calculate the minimum size required based on content
app.update_idletasks()
min_width = app.winfo_reqwidth()
min_height = app.winfo_reqheight()
app.minsize(min_width, min_height)

app.mainloop()
