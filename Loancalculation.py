import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class LoanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SBI Loan Scheme")
        self.geometry("650x550")
        self.configure(padx=20, pady=20)
        
        # In-memory dictionary to store registered users
        self.users_db = {}
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main Title
        title_lbl = ttk.Label(self, text="SBI Loan Scheme Application", font=("Helvetica", 18, "bold"))
        title_lbl.pack(pady=(0, 20))
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        
        self.tab_register = ttk.Frame(self.notebook, padding=10)
        self.tab_profile = ttk.Frame(self.notebook, padding=10)
        self.tab_repay = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.tab_register, text="1. Register Loan")
        self.notebook.add(self.tab_profile, text="2. Check Profile")
        self.notebook.add(self.tab_repay, text="3. Repay Loan")
        
        self.setup_register_tab()
        self.setup_profile_tab()
        self.setup_repay_tab()
        
    def setup_register_tab(self):
        frame = self.tab_register
        
        # Variables
        self.reg_name = tk.StringVar()
        self.reg_contact = tk.StringVar()
        self.reg_address = tk.StringVar()
        self.reg_username = tk.StringVar()
        self.reg_password = tk.StringVar()
        self.reg_amount = tk.IntVar(value=10000)
        self.reg_time = tk.IntVar(value=1)
        
        # Registration Form
        fields = [
            ("Name:", self.reg_name),
            ("Contact Number:", self.reg_contact),
            ("Address:", self.reg_address),
            ("Username:", self.reg_username),
            ("Password:", self.reg_password, True),  # True marks password field
            ("Principle Amount (In Rs):", self.reg_amount),
            ("Time Limit (in Years):", self.reg_time)
        ]
        
        row_idx = 0
        for field in fields:
            ttk.Label(frame, text=field[0], font=("Arial", 10)).grid(row=row_idx, column=0, sticky='w', pady=8, padx=5)
            is_password = len(field) > 2 and field[2]
            entry = ttk.Entry(frame, textvariable=field[1], show="*" if is_password else "", width=30)
            entry.grid(row=row_idx, column=1, sticky='ew', pady=8, padx=5)
            row_idx += 1
            
        frame.columnconfigure(1, weight=1)
        
        # Rates Info
        rates_text = (
            "--- SBI Loan Interest Rates ---\n"
            "Amount 10,000 to 50,000  ->  10% Interest\n"
            "Amount 50,001 to 100,000 ->  5% Interest\n"
            "Amount 100,000 or Above  ->  2% Interest"
        )
        ttk.Label(frame, text=rates_text, justify=tk.LEFT, foreground="blue", font=("Arial", 10, "italic")).grid(row=row_idx, column=0, columnspan=2, pady=15)
        row_idx += 1
        
        # Register Button
        reg_btn = ttk.Button(frame, text="Submit Registration", command=self.register_user)
        reg_btn.grid(row=row_idx, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)
        
    def register_user(self):
        try:
            name = self.reg_name.get()
            contact = self.reg_contact.get()
            address = self.reg_address.get()
            username = self.reg_username.get()
            password = self.reg_password.get()
            amount = self.reg_amount.get()
            time_limit = self.reg_time.get()
            
            if not all([name, contact, address, username, password]):
                messagebox.showerror("Validation Error", "Please fill in all textual fields.")
                return
                
            if amount < 10000:
                messagebox.showerror("Validation Error", "Please enter a valid Principle Amount (>= 10000).")
                return
                
            # Determining Interest Rate
            if amount <= 50000:
                rate = 10
            elif amount <= 100000:
                rate = 5
            else:
                rate = 2
                
            # Formula for Calculating Interest
            interest = (amount * rate * time_limit) / 100
            paying_amount = amount + interest
            
            self.users_db[username] = {
                "password": password,
                "name": name,
                "contact": contact,
                "address": address,
                "borrowed": amount,
                "time_limit": time_limit,
                "rate": rate,
                "paying_amount": paying_amount
            }
            
            msg = f"Thank You! Your Borrowed Amount is {amount} Rs for {time_limit} Years.\n\n"
            msg += f"Applicable Rate of Interest: {rate}%\n"
            msg += f"Total amount to be paid: {paying_amount} Rs\n\n"
            msg += "Note: If the loan is not paid in the given time, Compound Interest will be charged."
            
            messagebox.showinfo("Registration Successful", msg)
            
            # Reset the form
            self.reg_name.set("")
            self.reg_contact.set("")
            self.reg_address.set("")
            self.reg_username.set("")
            self.reg_password.set("")
            self.reg_amount.set(10000)
            self.reg_time.set(1)
            
        except tk.TclError:
            messagebox.showerror("Type Error", "Invalid numeric value entered for Amount or Time limit.")

    def setup_profile_tab(self):
        frame = self.tab_profile
        
        self.prof_user = tk.StringVar()
        self.prof_pass = tk.StringVar()
        
        login_frame = ttk.LabelFrame(frame, text="Login to view Profile", padding=15)
        login_frame.pack(fill='x', pady=10)
        
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(login_frame, textvariable=self.prof_user).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(login_frame, textvariable=self.prof_pass, show="*").grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        login_frame.columnconfigure(1, weight=1)
        
        ttk.Button(login_frame, text="Check Profile", command=self.check_profile).grid(row=2, column=0, columnspan=2, pady=15)
        
        self.prof_text = tk.Text(frame, height=12, width=60, state='disabled', font=("Courier", 10), bg="#f4f4f4")
        self.prof_text.pack(pady=10, fill='both', expand=True)
        
    def check_profile(self):
        user = self.prof_user.get()
        pwd = self.prof_pass.get()
        
        if user in self.users_db and self.users_db[user]["password"] == pwd:
            data = self.users_db[user]
            info = (
                "--------------------------------------------------\n"
                "                   YOUR PROFILE                   \n"
                "--------------------------------------------------\n"
                f"Name               : {data['name']}\n"
                f"Mobile Number      : {data['contact']}\n"
                f"Address            : {data['address']}\n"
                f"Borrowed Amount    : {data['borrowed']} Rs\n"
                f"Time Limit         : {data['time_limit']} Years\n"
                f"Rate Of Interest   : {data['rate']}%\n"
                f"Total Paying Amount: {data['paying_amount']} Rs\n"
                "--------------------------------------------------\n"
            )
            self.prof_text.config(state='normal')
            self.prof_text.delete(1.0, tk.END)
            self.prof_text.insert(tk.END, info)
            self.prof_text.config(state='disabled')
            
            # Clear password for security
            self.prof_pass.set("")
        else:
            messagebox.showerror("Authentication Failed", "User not found or Incorrect Password.")

    def setup_repay_tab(self):
        frame = self.tab_repay
        
        self.repay_user = tk.StringVar()
        self.repay_pass = tk.StringVar()
        self.repay_time = tk.StringVar()
        self.repay_paid_amount = tk.StringVar()
        
        # State variables for payment tracking
        self.current_dues = 0.0
        self.current_user = ""
        
        login_frame = ttk.LabelFrame(frame, text="Login to Repay Loan", padding=15)
        login_frame.pack(fill='x', pady=5)
        
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(login_frame, textvariable=self.repay_user).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(login_frame, textvariable=self.repay_pass, show="*").grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(login_frame, text="Time taken to Repay (Years):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(login_frame, textvariable=self.repay_time).grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        login_frame.columnconfigure(1, weight=1)
        
        ttk.Button(login_frame, text="Calculate Outstanding Dues", command=self.calculate_dues).grid(row=3, column=0, columnspan=2, pady=15)
        
        self.repay_info_text = tk.Text(frame, height=8, width=60, state='disabled', font=("Courier", 10), bg="#eef9f1")
        self.repay_info_text.pack(pady=10, fill='both', expand=True)
        
        pay_frame = ttk.Frame(frame)
        pay_frame.pack(fill='x', pady=5)
        
        ttk.Label(pay_frame, text="Enter Paying Amount:").pack(side='left', padx=5)
        ttk.Entry(pay_frame, textvariable=self.repay_paid_amount).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(pay_frame, text="Pay Now", command=self.pay_now).pack(side='left', padx=10)
        
    def calculate_dues(self):
        user = self.repay_user.get()
        pwd = self.repay_pass.get()
        
        try:
            t1 = int(self.repay_time.get())
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid numeric time taken (in years).")
            return
            
        if user in self.users_db and self.users_db[user]["password"] == pwd:
            data = self.users_db[user]
            t = data["time_limit"]
            rate = data["rate"]
            paying_amount = data["paying_amount"]
            
            if t1 <= t:
                final_paying_amount = paying_amount
                info = (
                    "------ Status: Paid Within Time Limit ------\n"
                    f"Name             : {data['name']}\n"
                    f"Borrowed Amount  : {data['borrowed']} Rs\n"
                    f"Time Taken       : {t1} Years (Limit: {t} Years)\n"
                    f"Rate of Interest : {rate}%\n"
                    f"--------------------------------------------\n"
                    f"Final Amount Due : {final_paying_amount} Rs\n"
                )
            else:
                # Need to calculate compounding interest for extra years
                t2 = t1 - t
                temp_amount = paying_amount
                for n in range(t2):
                    interest = temp_amount * rate / 100
                    temp_amount = temp_amount + interest
                final_paying_amount = temp_amount
                
                info = (
                    "------ Status: OVERDUE (Compound Interest Applied) ------\n"
                    f"Name             : {data['name']}\n"
                    f"Borrowed Amount  : {data['borrowed']} Rs\n"
                    f"Time Taken       : {t1} Years (Limit: {t} Years)\n"
                    f"Rate of Interest : {rate}%\n"
                    f"Penalty          : Overdue by {t2} years.\n"
                    f"---------------------------------------------------------\n"
                    f"Final Amount Due : {final_paying_amount:.2f} Rs\n"
                )
                
            self.repay_info_text.config(state='normal')
            self.repay_info_text.delete(1.0, tk.END)
            self.repay_info_text.insert(tk.END, info)
            self.repay_info_text.config(state='disabled')
            
            self.current_dues = final_paying_amount
            self.current_user = user
            self.repay_pass.set("") # Clear password
        else:
            messagebox.showerror("Authentication Failed", "User not found or Incorrect Password.")

    def pay_now(self):
        if not self.current_user:
            messagebox.showwarning("Action Required", "Please calculate your dues first by entering your credentials and time taken.")
            return
            
        try:
            paid = float(self.repay_paid_amount.get())
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter the exact numeric amount you want to pay.")
            return
            
        # Due to floating point math, we'll check if absolute difference is negligible
        if abs(paid - self.current_dues) < 0.05:
            name = self.users_db[self.current_user]["name"]
            messagebox.showinfo("Payment Successful", f"Processing payment...\n\nThank You Mr/Ms {name}. You have successfully paid off your loan.")
            
            # Clear user debt (remove user or mark as paid)
            self.users_db.pop(self.current_user)
            
            # Clear UI fields
            self.repay_user.set("")
            self.repay_pass.set("")
            self.repay_time.set("")
            self.repay_paid_amount.set("")
            self.repay_info_text.config(state='normal')
            self.repay_info_text.delete(1.0, tk.END)
            self.repay_info_text.config(state='disabled')
            
            # Reset internal state tracking
            self.current_user = ""
            self.current_dues = 0.0
        else:
            messagebox.showerror("Incorrect Payment Amount", f"Payment Denied. Please pay the EXACt Amount Due:\n{self.current_dues:.2f} Rs")

if __name__ == "__main__":
    app = LoanApp()
    app.mainloop()
