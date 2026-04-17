import customtkinter as ctk
import sqlite3
from tkinter import messagebox

ctk.set_appearance_mode("Light") 

class ContactManagerPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Contact Management System")
        self.geometry("650x850")
        self.configure(fg_color="#FFFFFF")

        self.conn = sqlite3.connect("pro_contacts.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT)")
        self.conn.commit()

        self.show_welcome_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_screen()
        bg_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        bg_frame.pack(fill="both", expand=True)
        ctk.CTkLabel(bg_frame, text="WELCOME TO\nCONTACT MANAGER", font=("Rockwell", 45, "bold"), text_color="#C71585").pack(pady=(120, 20))
        ctk.CTkLabel(bg_frame, text="Prepared by:\nALLAL Khaoula Samah\nBRIDJA Sara\nKADRI Imane", font=("Arial", 18, "bold"), text_color="#333333").pack(pady=20)
        ctk.CTkButton(bg_frame, text="GET STARTED", command=self.show_main_dashboard, width=280, height=60, corner_radius=30, fg_color="#C71585", font=("Arial", 20, "bold")).pack(pady=20)

    def show_main_dashboard(self):
        self.clear_screen()
        ctk.CTkLabel(self, text="DASHBOARD", font=("Arial", 38, "bold"), text_color="#C71585").pack(pady=(100, 60)) 
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()
        ctk.CTkButton(btn_frame, text="+ ADD CONTACT", command=self.show_add_form, width=220, height=60, font=("Arial", 16, "bold"), fg_color="#C71585").grid(row=0, column=0, padx=15)
        ctk.CTkButton(btn_frame, text="🔍 VIEW LIST", command=self.show_contact_list, width=220, height=60, font=("Arial", 16, "bold"), fg_color="#000000").grid(row=0, column=1, padx=15)

    def show_add_form(self):
        self.clear_screen()
        ctk.CTkButton(self, text="← BACK", command=self.show_main_dashboard, width=90, fg_color="transparent", text_color="#C71585", font=("Arial", 14, "bold")).pack(anchor="nw", padx=20, pady=20)
        ctk.CTkLabel(self, text="Create New Contact", font=("Arial", 28, "bold")).pack(pady=10)

        # Container for inputs to keep them centered
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=20)

        # 1. Full Name Section
        ctk.CTkLabel(form_frame, text="Full Name:", font=("Arial", 14, "bold"), text_color="#333333").pack(anchor="w", padx=5)
        self.name_input = ctk.CTkEntry(form_frame, placeholder_text="Enter Name", width=400, height=45, border_color="#C71585")
        self.name_input.pack(pady=(0, 20))

        # 2. Phone Number Section (RE-DESIGNED)
        ctk.CTkLabel(form_frame, text="Phone Number:", font=("Arial", 14, "bold"), text_color="#333333").pack(anchor="w", padx=5)
        
        # Validation for numbers only
        vcmd = (self.register(self.validate_phone), '%P')
        self.phone_input = ctk.CTkEntry(
            form_frame, 
            width=400, height=45, 
            border_color="#C71585",
            validate='key', 
            validatecommand=vcmd
        )
        self.phone_input.pack(pady=(0, 20))

        # 3. Email Section
        ctk.CTkLabel(form_frame, text="Email Address:", font=("Arial", 14, "bold"), text_color="#333333").pack(anchor="w", padx=5)
        self.email_input = ctk.CTkEntry(form_frame, placeholder_text="Enter Email", width=400, height=45, border_color="#C71585")
        self.email_input.pack(pady=(0, 30))

        ctk.CTkButton(self, text="SAVE CONTACT", command=self.save_to_db, width=400, height=60, fg_color="#C71585", font=("Arial", 20, "bold")).pack()

    def validate_phone(self, current_val):
        # Only allow numbers. Empty is okay for clearing.
        return current_val == "" or current_val.isdigit()
    def save_to_db(self):
        n, p, e = self.name_input.get(), self.phone_input.get(), self.email_input.get()
        if n and p:
            self.cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (n, p, e))
            self.conn.commit()
            messagebox.showinfo("Success", "Contact Saved!")
            self.show_contact_list()
        else:
            messagebox.showerror("Error", "Name and Phone are required!")

    def show_contact_list(self):
        self.clear_screen()
        ctk.CTkButton(self, text="← BACK", command=self.show_main_dashboard, width=90, fg_color="transparent", text_color="#C71585", font=("Arial", 14, "bold")).pack(anchor="nw", padx=20, pady=20)
        ctk.CTkLabel(self, text="MY CONTACTS", font=("Arial", 28, "bold")).pack(pady=15)
        scroll = ctk.CTkScrollableFrame(self, width=600, height=550, fg_color="#F8F8F8")
        scroll.pack(fill="both", expand=True, padx=25, pady=10)

        self.cursor.execute("SELECT * FROM contacts ORDER BY name ASC")
        for c in self.cursor.fetchall():
            card = ctk.CTkFrame(scroll, border_width=2, border_color="#C71585", fg_color="#FFFFFF")
            card.pack(fill="x", pady=12, padx=10)
            ctk.CTkLabel(card, text=f"{c[1].upper()}\n{c[2]}", font=("Arial", 18, "bold"), text_color="#C71585", justify="left").pack(side="left", padx=25, pady=15)
            ctk.CTkButton(card, text="DELETE", width=80, fg_color="#922b21", command=lambda idx=c[0]: self.delete_contact(idx)).pack(side="right", padx=15)

    def delete_contact(self, idx):
        if messagebox.askyesno("Confirm", "Delete this contact?"):
            self.cursor.execute("DELETE FROM contacts WHERE id=?", (idx,))
            self.conn.commit()
            self.show_contact_list()

if __name__ == "__main__":
    app = ContactManagerPro()
    app.mainloop()