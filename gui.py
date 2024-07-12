import tkinter as tk 
from tkinter import filedialog

#Function to import file 
def import_file():
    file_path = filedialog.askopenfilename(title="Select Import File", filetypes=[("Excel File",".xlsx"),("All Files","*.*")])
    if file_path:
        #Process the file 
        print("Selected file:",file_path)

#Initialize the GUI
root = tk.Tk()
root.title("Jobber to ACES Generator")

#Create a file import button "Jobber"
import_button = tk.Button(root, text = "Import Jobber", command=import_file)
import_button.pack(pady=100)

#Create a file import button "ACES"
import_button = tk.Button(root, text = "Import ACES", command=import_file)
import_button.pack(pady=100)

#Run the shit
root.mainloop()
