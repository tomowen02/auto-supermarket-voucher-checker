from pprint import pprint
from time import sleep
import customtkinter as ctkinter
import tkinter
import asda_data_interpreter
from threading import Thread

START_INDEX = 0
MAX_ROWS = 0

excel_file_path = "Not selected"


ctkinter.set_appearance_mode("light")
ctkinter.set_default_color_theme("dark-blue")

class App(ctkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Variables
        self.excel_file_path = "Not selected"
        
        # Configure window
        self.title("ASDA vouchers")
        self.geometry("525x725")

        self.frame = ctkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.logo_label = ctkinter.CTkLabel(master=self.frame, text="Automatic ASDA voucher code receiver", font=ctkinter.CTkFont(size=20, weight="bold")).pack(anchor='n', pady=10)

        self.select_file_button = ctkinter.CTkButton(master=self.frame, text="Select excel file", command=self.select_file).pack(anchor='n', pady=10)
        self.file_path_label = ctkinter.CTkLabel(master=self.frame, text=f"File path: {excel_file_path}", font=ctkinter.CTkFont(weight="bold"), wraplength=250)
        self.file_path_label.pack(anchor='n', pady=10)
        
        self.ref_var = tkinter.StringVar(self, "B")
        self.ref_label = ctkinter.CTkLabel(master=self.frame, text="Select which column is the reference:")
        self.ref_label.pack(anchor='n', pady=5)
        self.col_A_ref_radiobutton = ctkinter.CTkRadioButton(master=self.frame, variable=self.ref_var, text="A", value="A").pack(anchor='n', pady=5)
        self.col_B_ref_radiobutton = ctkinter.CTkRadioButton(master=self.frame, variable=self.ref_var, text="B", value="B").pack(anchor='n', pady=5)
        self.col_C_ref_radiobutton = ctkinter.CTkRadioButton(master=self.frame, variable=self.ref_var, text="C", value="C").pack(anchor='n', pady=5)
        
        self.urls_label = ctkinter.CTkLabel(master=self.frame, text="Select which columns contain voucher links (remember about rows with multiple vouchers):", wraplength=400)
        self.urls_label.pack(anchor='n', pady=5)
        self.col_J_var = tkinter.BooleanVar()
        self.col_K_var = tkinter.BooleanVar()
        self.col_L_var = tkinter.BooleanVar()
        self.col_M_var = tkinter.BooleanVar()
        self.col_N_var = tkinter.BooleanVar()
        self.col_O_var = tkinter.BooleanVar()
        self.col_J_urls_checkbox = ctkinter.CTkCheckBox(master=self.frame, variable=self.col_J_var, text="J").pack(anchor='n', pady=5)
        self.col_K_urls_checkbox = ctkinter.CTkCheckBox(master=self.frame, variable=self.col_K_var, text="K").pack(anchor='n', pady=5)
        self.col_L_urls_checkbox = ctkinter.CTkCheckBox(master=self.frame, variable=self.col_L_var, text="L").pack(anchor='n', pady=5)
        self.col_M_urls_checkbox = ctkinter.CTkCheckBox(master=self.frame, variable=self.col_M_var, text="M").pack(anchor='n', pady=5)
        self.col_N_urls_checkbox = ctkinter.CTkCheckBox(master=self.frame, variable=self.col_N_var, text="N").pack(anchor='n', pady=5)
        self.col_O_urls_checkbox = ctkinter.CTkCheckBox(master=self.frame, variable=self.col_O_var, text="O").pack(anchor='n', pady=5)
                
        self.start = ctkinter.CTkButton(master=self.frame, text="Start the process", command=Thread(target=self.start_process, daemon=True).start).pack(pady=10)
        
        self.progress_bar_label = ctkinter.CTkLabel(master=self.frame, text="Progress: ").pack(anchor='n', pady=5)
        self.progress_bar = ctkinter.CTkProgressBar(self.frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=(20), pady=(5, 5), anchor="n")
        
        self.message_label = ctkinter.CTkLabel(master=self.frame, text="", font=ctkinter.CTkFont(weight="bold"))
        self.message_label.pack(anchor='n', pady=5)
        
    def select_file(self):
        file_types = [('Excel file', '*.xlsx')]
        filename = ctkinter.filedialog.askopenfilename(
            title='Select an excel file',
            filetypes=file_types
        )
        self.excel_file_path = filename if filename != "" else "Not selected"
        self.file_path_label.configure(text=f"File path: {self.excel_file_path}")
    
    def update_progress(self, done, remaining):
        self.progress_bar.set(round(done/remaining, 3))
        
    def disable_widgets(self, children):
        for child in children:
            if id(child) == id(self.progress_bar):
                return
            if id(child) == id(self.message_label):
                return
            child.configure(state='disabled')
    
    def get_url_columns(self):
        selected_cols = []
        if self.col_J_var.get(): selected_cols.append("J")
        if self.col_K_var.get(): selected_cols.append("K")
        if self.col_L_var.get(): selected_cols.append("L")
        if self.col_M_var.get(): selected_cols.append("M")
        if self.col_N_var.get(): selected_cols.append("N")
        if self.col_O_var.get(): selected_cols.append("O")
        return ','.join(selected_cols)
    
    def is_ready(self):
        if self.excel_file_path == "Not selected": return False
        if self.get_url_columns() == "": return False
        return True
    
    def set_message(self, message):
        self.message_label.configure(text=message)
    
    def popup(self, title, message):
        tkinter.messagebox.showinfo(title=title, message=message)
    
    def start_process(self):
        ref_column = self.ref_var.get()
        url_columns = self.get_url_columns()
        if not self.is_ready():
            self.popup("Error", "Please fill out all of the required information")
            print("NOT READY!")
            return
        self.disable_widgets(self.frame.winfo_children())
        self.popup("Starting task", "The process will begin after this message is dismissed. IT MAY TAKE UP TO 20 MINUTES")
        
        self.set_message("Reading excel file...")
        print("Reading excel file...")
        try:
            refs_and_urls = asda_data_interpreter.get_refs_and_urls_from_excel(self.excel_file_path, ref_column, url_columns)
            if len(refs_and_urls) == 0:
                self.set_message("ERROR: NO DATA FOUND")
                print("ERROR: NO DATA FOUND")
                return
        except:
            self.set_message("Something went wrong while reading the file.")
            self.popup("ERROR", "Something went wrong while reading the file.")
            print("Something went wrong while reading the file.")
            return
        
        self.set_message("Receiving data from the web. This may take up to 20 minutes...")
        print(f"Receiving data from the web. This may take up to 20 minutes...")
        refs_and_vouchers = [] # Once we receive the details for the vouchers, the urls are no longer needed
        rows_done = 0 # This is used when checking if we've reached the limit of rows. Mainly when degugging
        upper_limit = len(refs_and_urls) if MAX_ROWS == 0 else START_INDEX + MAX_ROWS
        for i in range(START_INDEX, upper_limit):
            row = refs_and_urls[i]
            # row is a dict in the form: {ref: xxx, urls: []}
            vouchers = []
            for url in row['urls']:
                try:
                    vouchers.append(asda_data_interpreter.get_voucher_details_from_url(url))
                    self.set_message(f"{i+1} rows of spreadsheet done. {upper_limit-(i+1)} remaining...")
                    print(f"{i} rows of spreadsheet done. {upper_limit - i} remaining...")
                except:
                    self.set_message("Something went wrong while reading webpage. This may be a connection issue or the urls are not in the correct format/ column")
                    self.popup("ERROR", "Something went wrong while reading webpage. This may be a connection issue or the urls are not in the correct format/ column")
                    print("Something went wrong while reading webpage. This may be a connection issue or the urls are not in the correct format/ column")
                    return
            try:
                refs_and_vouchers.append({
                    'ref': row['ref'],
                    'vouchers': vouchers
                })
                self.update_progress(len(refs_and_vouchers), upper_limit)
            except:
                self.set_message("Data is in the wrong format")
                self.popup("ERROR", "Data is in the wrong format")
                print("Data is in the wrong format")
                return
            rows_done += 1
        print("Data received!")
        print("Theses are the voucher codes and pins received:")
        try:
            pprint(refs_and_vouchers)
        except:
            pass

        self.set_message("Saving data...")
        print("Saving data...")
        try:
            asda_data_interpreter.save_data_to_excel(refs_and_vouchers, "asda_result.xlsx")
        except:
            self.set_message("There was an error saving the excel file.")
            self.popup("ERROR", "Data is in the wrong format")
            print("There was an error saving the excel file.")
            return

        self.set_message("Done!")
        print("Done!")
        self.popup("Finished", "The task has completed. The output file is saved as 'asda_result.xlsx' in the same folder as this program.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()