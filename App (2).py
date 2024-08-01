import tkinter as tk
from tkinter import ttk,  simpledialog, messagebox
import wikipediaapi
import mysql.connector
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="bank"
)
from PIL import Image, ImageTk
import cv2
import requests
import urllib.parse
import webbrowser
import speech_recognition as sr
from googletrans import Translator

class TechConnectApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tech Connect")
        self.geometry("1024x768")
        self.configure(bg="#ffb800")
        
        self.video_label = None
        self.cap = None

        self.language = tk.StringVar(value="English")
        self.category = tk.StringVar()
        self.bank_option = tk.StringVar()
        
        self.education_option = tk.StringVar()
        self.reservation_type = tk.StringVar()
        self.shopping_category = tk.StringVar()
        self.entertainment_option = tk.StringVar()
        self.initialize_database()
        
        self.create_banking_page()
        
        self.create_ui()

    def create_ui(self):
        # Add your main application widgets here

        # Button to open the chatbot
        self.chat_button = ttk.Button(self, text="Open ChatBot", command=self.open_chatbot)
        self.chat_button.pack(pady=10)

    def open_chatbot(self):
        chatbot = ChatBot(self)
        chatbot.grab_set()  

        
    def initialize_database(self):
        # Setup the database connection
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bank"
        )
        self.cursor = self.con.cursor()

        self.education_option = tk.StringVar()
        self.reservation_type = tk.StringVar()
        self.shopping_category = tk.StringVar()
        self.entertainment_option = tk.StringVar()

        self.translator = Translator()
        self.recognizer = sr.Recognizer()

        self.style = ttk.Style()
        self.style.configure("Large.TRadiobutton", font=("Arial", 24),background="#90EE90")

        # Configure the style for Large.TButton with the desired font size
        self.style.configure("Large.TButton", font=("Arial", 18), background="#ff0000")  # Adjust the font and size as needed

        

        self.video_path = (r"C:\Users\ansu2\AppData\Local\Programs\Python\Python311\bg.mp4")

        self.create_welcome_page(r"C:\Users\ansu2\AppData\Local\Programs\Python\Python311\bg.mp4")
        self.create_category_selection_page(self.video_path)

    def play_video(self, video_path):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                self.video_label.configure(image=frame)
                self.video_label.image = frame
                self.video_label.after(10, self.play_video, video_path)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.play_video(video_path)
        else:
            print("Failed to open video file")

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 40))  # Set a larger default font size

        # Configure style for the Next button
        self.style.configure('Next.TButton', font=('Arial', 40), background='#00ff00', foreground='#ffffff')
        self.style.map('Next.TButton', background=[('active', '#00cc00')])

        # Configure style for the Back button
        self.style.configure('Back.TButton', font=('Arial', 40), background='#ff0000', foreground='#ffffff')
        self.style.map('Back.TButton', background=[('active', '#cc0000')])

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        if self.cap:
            self.cap.release()
            self.cap = None

    def translate_text(self, text):
        if self.language.get() == "English":
            return text
        try:
            return self.translator.translate(text, dest=self.language.get()).text
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Fall back to the original text if translation fails

    def create_welcome_page(self, video_path):
        self.clear_frame()
        try:
            self.attributes("-fullscreen", True)

            # Load the background video
            self.cap = cv2.VideoCapture(video_path)

            # Create a label widget to display the video
            self.video_label = tk.Label(self)
            self.video_label.pack(fill="both", expand=True)

            # Start playing the video
            self.play_video(video_path)


            heading_text = "Welcome to Tech Connect"
            heading = tk.Label(self, text=heading_text, font=("Helvetica", 70, "bold"), fg="#ffffff", bg="#ff4500")
            heading.place(relx=0.5, rely=0.15, anchor="center")

            
            label_text = ("We are here to help you to learn technology. "
                      "Welcome to this App. It will help you perform "
                      "various tasks easily.")
            label = tk.Label(self, text=label_text, font=("Times New Roman", 40), fg="#000080", bg="#f0f8ff",  wraplength=800, justify="center")
            label.place(relx=0.5, rely=0.45, anchor="center")
        
        # Create a frame for the button
            button_frame = tk.Frame(self, bg="#f0f8ff")
            button_frame.place(relx=0.5, rely=0.7, anchor="center")
        
        # Create the button
            next_button = ttk.Button(button_frame, text="Next", command=lambda: self.create_language_selection_page(self.video_path), style="Large.TButton")
            next_button.pack(padx=50, pady=20)



        except Exception as e:
            print("Error creating welcome page:", e)

    def create_language_selection_page(self, video_path):
        self.clear_frame()
        try:
            self.attributes("-fullscreen", True)

            # Load the background video
            self.cap = cv2.VideoCapture(video_path)

            # Create a label widget to display the video
            self.video_label = tk.Label(self)
            self.video_label.pack(fill="both", expand=True)

            # Start playing the video
            self.play_video(video_path)

            label = tk.Label(self, text="Choose Language", font=("Times New Roman", 60, "bold"), fg="#000080", bg="#f0f8ff")
            label.place(relx=0.5, rely=0.1, anchor="center")

            button_frame = tk.Frame(self, bg="#f0f8ff")
            button_frame.place(relx=0.5, rely=0.5, anchor="center")

            languages = ["Hindi", "Marathi", "English", "Punjabi", "Telugu", "Tamil", "Malayalam","Bhojpuri"]
            for idx, lang in enumerate(languages, start=1):
                button = ttk.Button(button_frame, text=lang, command=lambda l=lang: self.language.set(l),style='Large.TButton')
                button.pack(pady=10, ipadx=15, ipady=5)

            nav_button_frame = tk.Frame(self, bg="#ffa500")
            nav_button_frame.place(relx=0.5, rely=0.8, anchor="center")  # Adjust position of the frame

            next_button = ttk.Button(nav_button_frame, text=self.translate_text("Next"), command=lambda: self.create_category_selection_page(self.video_path),style="Large.TButton")
            next_button.pack(side="right", padx=(500,0), pady=30, ipadx=20, ipady=10)

            back_button = ttk.Button(nav_button_frame, text=self.translate_text("Back"), command=lambda: self.create_welcome_page(self.video_path),style="Large.TButton")
            back_button.pack(side="left", padx=(0,500), pady=30, ipadx=20, ipady=10)

        except Exception as e:
            print("Error creating language selection page:", e)

    def create_category_selection_page(self, video_path):
        self.clear_frame()
        try:
            self.attributes("-fullscreen", True)

            # Load the background video
            self.cap = cv2.VideoCapture(video_path)

            # Create a label widget to display the video
            self.video_label = tk.Label(self)
            self.video_label.pack(fill="both", expand=True)

            # Start playing the video
            self.play_video(video_path)

            label = tk.Label(self, text=self.translate_text("Choose Category"), font=("Comic Sans MS", 60, "bold"), fg="#000080", bg="#f0f8ff")
            label.place(relx=0.5, rely=0.2, anchor="center")

            button_frame = tk.Frame(self, bg="#f0f8ff")
            button_frame.place(relx=0.5, rely=0.5, anchor="center")

            # Create and place category buttons
            categories = ["Banking", "Education", "Reservation", "Shopping", "Entertainment"]
            for idx, cat in enumerate(categories, start=1):
                button = ttk.Button(button_frame, text=self.translate_text(cat), command=lambda c=cat: self.category.set(c), style='Large.TRadiobutton')
                button.pack(pady=10, ipadx=20, ipady=10)

            nav_button_frame = tk.Frame(self, bg="#ffa500")
            nav_button_frame.place(relx=0.5, rely=0.8, anchor="center")  # Adjust position of the frame

            next_button = ttk.Button(nav_button_frame, text=self.translate_text("Next"), command=self.create_category_page, style="Large.TButton")
            next_button.pack(side="right", padx=(500,0), pady=30, ipadx=20, ipady=10)  # Adjust padding as needed

            back_button = ttk.Button(nav_button_frame, text=self.translate_text("Back"), command=lambda: self.create_language_selection_page(self.video_path), style="Large.TButton")
            back_button.pack(side="left", padx=(0,500), pady=30, ipadx=20, ipady=10)

            
        except Exception as e:
            print("Error creating category selection page:", e)

    def create_category_page(self):
        category = self.category.get()
        if category == "Banking":
            self.create_banking_page()
        elif category == "Education":
            self.create_education_page()
        elif category == "Reservation":
            self.create_reservation_page()
        elif category == "Shopping":
            self.create_shopping_page()
        elif category == "Entertainment":
            self.create_entertainment_page()

    def openAcc(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Enter Your Details"), font=("Helvetica", 30, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        self.create_entry("Enter Name")
        self.create_entry("Enter Account No.")
        self.create_entry("Enter D.O.B")
        self.create_entry("Enter Address")
        self.create_entry("Enter Phone No.")
        self.create_entry("Enter Opening Balance")

        submit_button = ttk.Button(self, text=self.translate_text("Submit"), command=self.submit_open_acc, style="Large.TButton")
        submit_button.pack(side="right", padx=50)

        back_button = ttk.Button(self, text=self.translate_text("Back"), command=self.create_banking_page, style="Large.TButton")
        back_button.pack(side="left", padx=50)


    def create_entry(self, placeholder):
        entry = ttk.Entry(self)
        entry.pack(pady=10)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e: self.on_focus_in(e, placeholder))
        entry.bind("<FocusOut>", lambda e: self.on_focus_out(e, placeholder))
        # Store placeholder text in the widget's `placeholder` attribute
        entry.placeholder = placeholder

    def on_focus_in(self, event, placeholder):
        widget = event.widget
        if widget.get() == placeholder:
            widget.delete(0, tk.END)

    def on_focus_out(self, event, placeholder):
        widget = event.widget
        if widget.get() == "":
            widget.insert(0, placeholder)

       
    def submit_open_acc(self):
        n = self.name_entry.get()
        ac = self.ac_entry.get()
        db = self.db_entry.get()
        address = self.address_entry.get()
        p = self.p_entry.get()
        ob = self.ob_entry.get()
        data1 = (n, ac, db, address, p, ob)
        data2 = (n, ac, ob)
        sql1 = 'INSERT INTO account VALUES(%s, %s, %s, %s, %s, %s)'
        sql2 = 'INSERT INTO amount VALUES(%s, %s, %s)'
        c = self.con.cursor()
        c.execute(sql1, data1)
        c.execute(sql2, data2)
        self.con.commit()
        print("Data Entered Successfully")
        self.create_banking_page()

    def depoAmo(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Deposit Amount"), font=("Helvetica", 30, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        self.am_entry = ttk.Entry(self)
        self.am_entry.pack(pady=10)
        self.am_entry.insert(0, "Enter Amount")

        self.ac_entry = ttk.Entry(self)
        self.ac_entry.pack(pady=10)
        self.ac_entry.insert(0, "Enter Account No.")

        submit_button = ttk.Button(self, text=self.translate_text("Submit"), command=self.submit_depo_amo, style="Large.TButton")
        submit_button.pack(side="right", padx=50)

        back_button = ttk.Button(self, text=self.translate_text("Back"), command=self.create_banking_page, style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def submit_depo_amo(self):
        am = int(self.am_entry.get())
        ac = self.ac_entry.get()
        a = "SELECT balance FROM amount WHERE acno=%s"
        data = (ac,)
        c = self.con.cursor()
        c.execute(a, data)
        myresult = c.fetchone()
        tam = myresult[0] + am
        sql = "UPDATE amount SET balance=%s WHERE acno=%s"
        d = (tam, ac)
        c.execute(sql, d)
        self.con.commit()
        self.create_banking_page()

    def witham(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Withdraw Amount"), font=("Helvetica", 30, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        self.am_entry = ttk.Entry(self)
        self.am_entry.pack(pady=10)
        self.am_entry.insert(0, "Enter Amount")

        self.ac_entry = ttk.Entry(self)
        self.ac_entry.pack(pady=10)
        self.ac_entry.insert(0, "Enter Account No.")

        submit_button = ttk.Button(self, text=self.translate_text("Submit"), command=self.submit_witham, style="Large.TButton")
        submit_button.pack(side="right", padx=50)

        back_button = ttk.Button(self, text=self.translate_text("Back"), command=self.create_banking_page, style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def submit_witham(self):
        am = int(self.am_entry.get())
        ac = self.ac_entry.get()
        a = "SELECT balance FROM amount WHERE acno=%s"
        data = (ac,)
        c = self.con.cursor()
        c.execute(a, data)
        myresult = c.fetchone()
        tam = myresult[0] - am
        sql = "UPDATE amount SET balance=%s WHERE acno=%s"
        d = (tam, ac)
        c.execute(sql, d)
        self.con.commit()
        self.create_banking_page()

    def balance(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Check Balance"), font=("Helvetica", 30, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        self.ac_entry = ttk.Entry(self)
        self.ac_entry.pack(pady=10)
        self.ac_entry.insert(0, "Enter Account No.")

        submit_button = ttk.Button(self, text=self.translate_text("Submit"), command=self.submit_balance, style="Large.TButton")
        submit_button.pack(side="right", padx=50)

        back_button = ttk.Button(self, text=self.translate_text("Back"), command=self.create_banking_page, style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def submit_balance(self):
        ac = self.ac_entry.get()
        a = "SELECT balance FROM amount WHERE acno=%s"
        data = (ac,)
        c = self.con.cursor()
        c.execute(a, data)
        myresult = c.fetchone()
        balance = myresult[0]
        print(f"Balance for Account: {ac} is {balance}")
        self.create_banking_page()

    def displayacc(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Enter Account No."), font=("Helvetica", 30, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        self.ac_entry = ttk.Entry(self, font=("Helvetica", 20))
        self.ac_entry.pack(pady=10)

        submit_button = ttk.Button(self, text=self.translate_text("Submit"), command=self.submit_displayacc, style="Large.TButton")
        submit_button.pack(side="right", padx=50)

        back_button = ttk.Button(self, text=self.translate_text("Back"), command=self.create_banking_page, style="Large.TButton")
        back_button.pack(side="left", padx=50)


    def submit_displayacc(self):
        acc = self.ac_entry.get()
        try:
            query = "SELECT * FROM account WHERE acno = %s"
            self.cursor.execute(query, (acc,))
            myresult = self.cursor.fetchone()
        
            if myresult:
                self.clear_frame()
                label = tk.Label(self, text="Account Details", font=("Helvetica", 40, "bold"), fg="#000080", bg="#f0f8ff")
                label.pack(pady=20)

                details = [
                    f"Name: {myresult[0]}",
                    f"Account No.: {myresult[1]}",
                    f"Date of Birth: {myresult[2]}",
                    f"Address: {myresult[3]}",
                    f"Phone No.: {myresult[4]}",
                    f"Opening Balance: {myresult[5]}" ]
                for detail in details:
                    detail_label = tk.Label(self, text=detail, font=("Helvetica", 20), fg="#000080", bg="#f0f8ff")
                    detail_label.pack(pady=5)

                back_button = ttk.Button(self, text="Back", command=self.create_banking_page, style="Large.TButton")
                back_button.pack(pady=20)

            else:
                self.show_message("No account found with this number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def show_message(self, message):
        self.clear_frame()
        label = tk.Label(self, text=message, font=("Helvetica", 20), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        back_button = ttk.Button(self, text="Back", command=self.create_banking_page, style="Large.TButton")
        back_button.pack(pady=20)


    def closeacc(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Close Account"), font=("Helvetica", 30, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        self.ac_entry = ttk.Entry(self)
        self.ac_entry.pack(pady=10)
        self.ac_entry.insert(0, "Enter Account No.")

        submit_button = ttk.Button(self, text=self.translate_text("Submit"), command=self.submit_closeacc, style="Large.TButton")
        submit_button.pack(side="right", padx=50)

        back_button = ttk.Button(self, text=self.translate_text("Back"), command=self.create_banking_page, style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def submit_closeacc(self):
        ac = self.ac_entry.get()
        sql1 = "DELETE FROM account WHERE acno=%s"
        sql2 = "DELETE FROM amount WHERE acno=%s"
        data = (ac,)
        c = self.con.cursor()
        c.execute(sql1, data)
        c.execute(sql2, data)
        self.con.commit()
        self.create_banking_page()

    def create_banking_page(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Banking Options"), font=("Comic Sans MS", 40, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        banking_options = ["Open an Account", "Check Balance", "Deposit Amount", "Withdraw Amount", "Display Account", "Close an Account"]
        banking_frame = tk.Frame(self, bg="#f0f8ff")
        banking_frame.pack(pady=30, padx=30)

        left_frame = tk.Frame(banking_frame, bg="#f0f8ff")
        left_frame.grid(row=0, column=0, padx=10, pady=10)
        right_frame = tk.Frame(banking_frame, bg="#f0f8ff")
        right_frame.grid(row=0, column=1, padx=10, pady=10)

        for i, option in enumerate(banking_options):
            target_frame = left_frame if i < len(banking_options) / 2 else right_frame
            ttk.Radiobutton(target_frame, text=self.translate_text(option), variable=self.bank_option, value=option, style="Large.TRadiobutton").pack(pady=20)

        button_frame = tk.Frame(self, bg="#f0f8ff")
        button_frame.pack(fill="x", pady=(0, 50))

        next_button = ttk.Button(button_frame, text=self.translate_text("Next"), command=self.handle_banking_option, style="Large.TButton")
        next_button.pack(side="right", padx=50)  # Align Next button to the right with padding

        back_button = ttk.Button(button_frame, text=self.translate_text("Back"), command=lambda: self.create_category_selection_page(self.video_path), style="Large.TButton")
        back_button.pack(side="left", padx=50)


    def handle_banking_option(self):
        option = self.bank_option.get()
        if option == "Open an Account":
            self.openAcc()
        elif option == "Check Balance":
            self.balance()
        elif option == "Deposit Amount":
            self.depoAmo()
        elif option == "Withdraw Amount":
            self.witham()
        elif option == "Display Account":
            self.displayacc()
        elif option == "Close an Account":
            self.closeacc()
        else:
            webbrowser.open("https://www.hdfcbank.com/personal/pay/money-transfer")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


    def search_google(self, query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    def create_education_page(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Education Options"), font=("Comic Sans MS", 90, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=(10,50), fill="x")

        education_options = ["Find Schools", "Access Materials", "Online Courses", "Refer Videos", "Scholarships", "Ask Queries"]

        for option in education_options:
            ttk.Radiobutton(self, text=self.translate_text(option), variable=self.education_option, value=option, style="Large.TRadiobutton").pack(pady=10)

        button_frame = tk.Frame(self, bg="#f0f8ff")
        button_frame.pack(fill="x", pady=(0, 50))

        next_button = ttk.Button(button_frame, text=self.translate_text("Next"), command=self.handle_education_option, style="Large.TButton")
        next_button.pack(side="right", padx=50)

        back_button = ttk.Button(button_frame, text=self.translate_text("Back"), command=lambda: self.create_category_selection_page(self.video_path), style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def handle_education_option(self):
        option = self.education_option.get()
        if option == "Find Schools":
            self.search_google("find schools near me")
        elif option == "Access Materials":
            prompt = self.get_user_prompt("Enter the material you want to search for:")
            self.search_google(f"{prompt}")
        elif option == "Online Courses":
            self.search_google("best online courses")
        elif option == "Refer Videos":
            prompt = self.get_user_prompt("Enter the video topic you want to search for:")
            self.search_youtube(f"{prompt}")
        elif option == "Scholarships":
            self.search_google("available scholarships")
        elif option == "Ask Queries":
            prompt = self.get_user_prompt("Enter your query:")
            self.redirect_to_custom_service(prompt)
        
        self.create_education_page()
        

    def fetch_wikipedia_summary(self, query):
        page = self.wiki_wiki.page(query)
        if page.exists():
            summary = page.summary[:500]  # Limit summary to 500 characters
            messagebox.showinfo("Wikipedia Summary", summary)
        else:
            messagebox.showinfo("Wikipedia Summary", "No information found on Wikipedia for your query.")




    def get_user_prompt(self, message):
        return simpledialog.askstring("Input", message)

    
    def redirect_to_custom_service(self, prompt):
    # Replace with your own web service URL
        custom_service_url = f"https://chatgpt.com//?query={urllib.parse.quote(prompt)}"
        webbrowser.open(custom_service_url)

    def create_reservation_page(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Reservation Options"), font=("Comic Sans MS", 90, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=50)

        reservation_types = ["Train", "Flight", "Bus"]
        reservation_frame = tk.Frame(self, bg="#f0f8ff")
        reservation_frame.pack(pady=40)

        for rtype in reservation_types:
            ttk.Radiobutton(reservation_frame, text=self.translate_text(rtype), variable=self.reservation_type, value=rtype,  style="Large.TRadiobutton").pack(pady=40)


        button_frame = tk.Frame(self, bg="#f0f8ff")
        button_frame.pack(fill="x", pady=(0, 70))
        
        next_button = ttk.Button(button_frame, text=self.translate_text("Next"), command=self.handle_reservation_option, style="Large.TButton")
        next_button.pack(side="right", padx=50)  # Align Next button to the right with padding

        back_button = ttk.Button(button_frame, text=self.translate_text("Back"), command=lambda: self.create_category_selection_page(self.video_path), style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def handle_reservation_option(self):
        rtype = self.reservation_type.get()
        if rtype == "Bus":
            self.search_reservation("redbus")
        elif rtype == "Train":
            self.search_reservation("irctc")
        elif rtype == "Flight":
            self.search_reservation("ixigo")

    def search_reservation(self, service):

        if service == "redbus":
            url = f"https://www.redbus.in"
        elif service == "irctc":
            url = f"https://www.irctc.co.in"
        elif service == "ixigo":
            url = f"https://www.ixigo.com"

        
        webbrowser.open(url)

   
    def create_shopping_page(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Shopping Options"), font=("Comic Sans MS", 90, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=50)

        shopping_categories = ["Electronics", "Clothing", "Groceries"]
        shopping_frame = tk.Frame(self, bg="#f0f8ff")
        shopping_frame.pack(pady=40)

        for category in shopping_categories:
            ttk.Radiobutton(shopping_frame, text=self.translate_text(category), variable=self.shopping_category, value=category,  style="Large.TRadiobutton").pack(pady=40)

        button_frame = tk.Frame(self, bg="#f0f8ff")
        button_frame.pack(fill="x", pady=(0, 70))

        next_button = ttk.Button(button_frame, text=self.translate_text("Next"), command=self.handle_shopping_option, style="Large.TButton")
        next_button.pack(side="right", padx=50)

        back_button = ttk.Button(button_frame, text=self.translate_text("Back"), command=lambda: self.create_category_selection_page(self.video_path), style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def handle_shopping_option(self):
        category = self.shopping_category.get()
        recommended_products = self.get_recommendations(category)
        best_price_url = self.get_best_price_url(category)

        if recommended_products:
            print("Recommended Products for {}: {}".format(category, recommended_products))
        if best_price_url:
            webbrowser.open(best_price_url)

    def get_recommendations(self, category):
        # Simple static recommendations based on category
        recommendations = {
            "Electronics": ["Smartphone - High-end", "Laptop - Gaming", "Wireless Headphones"],
            "Clothing": ["Casual T-shirt", "Stylish Jeans", "Winter Jacket"],
            "Groceries": ["Organic Milk", "Whole Wheat Bread", "Fresh Fruits"]
        }
        return recommendations.get(category, [])

    def get_best_price_url(self, category):
        # Static URLs for demonstration purposes
        price_comparison_urls = {
            "Electronics": "https://www.electronicsbazaar.com/",
            "Clothing": "https://www.myntra.com/",
            "Groceries": "https://www.amazon.in/s?k=amazon+food+delivery"
        }
        return price_comparison_urls.get(category)
    def create_entertainment_page(self):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text("Entertainment Options"), font=("Comic Sans MS", 90, "bold"), fg="#000080", bg="#f0f8ff")
        label.pack(pady=50)

        entertainment_options = ["Watch Movies/Shows", "Listen to Music"]
        entertainment_frame = tk.Frame(self, bg="#f0f8ff")
        entertainment_frame.pack(pady=40)

        for option in entertainment_options:
            ttk.Radiobutton(entertainment_frame, text=self.translate_text(option), variable=self.entertainment_option, value=option,  style="Large.TRadiobutton").pack(pady=40)

        button_frame = tk.Frame(self, bg="#f0f8ff")
        button_frame.pack(fill="x", pady=(0, 70))

        next_button = ttk.Button(button_frame, text=self.translate_text("Next"), command=self.handle_entertainment_option, style="Large.TButton")
        next_button.pack(side="right", padx=50)

        back_button = ttk.Button(button_frame, text=self.translate_text("Back"), command=lambda: self.create_category_selection_page(self.video_path), style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def handle_entertainment_option(self):
        option = self.entertainment_option.get()
        if option == "Watch Movies/Shows":
            self.show_recommendations("movies")
        elif option == "Listen to Music":
            self.show_recommendations("music")

    def show_recommendations(self, category):
        self.clear_frame()
        label = tk.Label(self, text=self.translate_text(f"Recommended {category.capitalize()}"), font=("Helvetica", 30), fg="#000080", bg="#f0f8ff")
        label.pack(pady=20)

        recommendations = self.get_recommendations(category)
        for item in recommendations:
            tk.Label(self, text=item, font=("Helvetica", 18), bg="#f0f8ff").pack(pady=5)

        search_label = tk.Label(self, text=self.translate_text(f"Or search for specific {category}:"), font=("Helvetica", 18), fg="#000080", bg="#f0f8ff")
        search_label.pack(pady=20)

        self.prompt_entry = ttk.Entry(self)
        self.prompt_entry.pack(pady=5)

        submit_button = ttk.Button(self, text=self.translate_text("Submit"), command=lambda: self.search_content(category), style="Large.TButton")
        submit_button.pack(side="right", padx=50)

        back_button = ttk.Button(self, text=self.translate_text("Back"), command=self.create_entertainment_page, style="Large.TButton")
        back_button.pack(side="left", padx=50)

    def get_recommendations(self, category):
        # Placeholder for AI-based recommendation system
        if category == "movies":
            return ["Inception", "The Matrix", "Interstellar"]
        elif category == "music":
            return ["Bohemian Rhapsody", "Imagine", "Hotel California"]

    def search_content(self, category):
        query = self.prompt_entry.get()
        if category == "movies":
            self.search_youtube(f"movies {query}")
        elif category == "music":
            self.search_youtube(f"music {query}")
        self.create_entertainment_page()

    def handle_back_to_previous(self):
        self.clear_frame()
        # Handle logic to navigate back to the appropriate previous page
        if self.category.get() == "Banking":
            self.create_banking_page()
        elif self.category.get() == "Education":
            self.create_education_page()
        elif self.category.get() == "Reservation":
            self.create_reservation_page()
        elif self.category.get() == "Shopping":
            self.create_shopping_page()
        elif self.category.get() == "Entertainment":
            self.create_entertainment_page()

    def submit_prompt(self):
        self.prompt_response = self.prompt_entry.get()

    def search_google(self, query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    def search_youtube(self, query):
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)

    def search_electronicsbazaar(self, query):
        url = f"https://www.electronicsbazaar.com/search?q={query}"
        webbrowser.open(url)

    def search_myntra(self, query):
        url = f"https://www.myntra.com/search?q={query}"
        webbrowser.open(url)

    def search_amazon(self, query):
        url = f"https://www.amazon.com/search?q={query}"
        webbrowser.open(url)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


    
if __name__ == "__main__":
    app = TechConnectApp()
    app.mainloop()

