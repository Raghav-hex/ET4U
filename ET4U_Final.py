import mysql.connector as ms
from tkinter import *
from tkinter import ttk
from geopy.geocoders import Nominatim
import requests
import sys
from tkinter import messagebox
from tkinter.messagebox import showerror, showwarning, showinfo
main_bg="#2B7C8C"
text_fg="#000000"
text_bg="#2B7C8C"
Button_fg="#000000"
Button_bg="#0DADE9"

def get_db_connection():
    return ms.connect(host='localhost', user='root', passwd='Raghav2007', database='EduTrip4U')
def Main():
    global w
    global w2
    def Sign_up():
        Signup()
    def Log_in():
        Login()
    
    w=Tk()
    style =ttk.Style(w)
    style.theme_use("classic")
    
    w.geometry('450x450')
    w.title('ET4U')
    w.config(bg=main_bg)
    a=Label(w,text="EduTrip4U",font=("Bauhaus 93",50),relief="raised",borderwidth='5',bg="#8AB8BD",fg=text_fg)
    a.pack(pady=20)
    but_teach=Button(w,text="Log-In",relief='raised',font=("arial",20),fg=Button_fg,bg=Button_bg,command=Log_in)
    but_teach.pack(pady=5)
    but_Stud=Button(w,text="Sign-Up",relief='raised',font=("arial",20),fg=Button_fg,bg=Button_bg,command=Sign_up)
    but_Stud.pack(pady=5)
    but_Exit=Button(w,text="Exit",relief='raised',font=("arial",20),fg=Button_fg,bg=Button_bg,command=sys.exit)
    but_Exit.pack(pady=5)
    w.mainloop()
U=""
def Signup():
    global Name
    def close():
        w.deiconify()
        w2.destroy()
    def Submit_Signup():
        global N,U,P,ST
        N=Name_input.get()
        U=Usern_input.get()
        P=Passwd_input.get()
        ST=Stud_Teach.get()
        con=ms.connect(host='localhost',user='root',passwd='root')
        cur=con.cursor()
        cur.execute("Create database if not exists Project_uhh")
        cur.execute('use Project_uhh')
        cur.execute('''Create table if not exists signup
(Name varchar(20) not null,
Usern varchar(10) primary key,
Passwd varchar(10) not null,
TS char(7))''')
        cur.execute("Insert into signup values('{}','{}','{}','{}')".format(N,U,P,ST))
        con.commit()
        con.close()
    w.withdraw()
    w2=Toplevel(w)
    w2.config(bg=main_bg)
    w2.geometry('450x450')
    a=Label(w2,text="Sign-Up",font=("impact",20),bg=text_bg,fg=text_fg)
    a.pack(pady=5)
    Name=Label(w2,text="Enter name:",font=("impact",15),bg=text_bg,fg=text_fg)
    Name.pack(pady=5)
    Name_input=Entry(w2)
    Name_input.pack(pady=5)
    Name.pack(pady=5)
    Usern=Label(w2,text="Enter username:",font=("impact",15),bg=text_bg,fg=text_fg)
    Usern.pack(pady=5)
    Usern_input=Entry(w2)
    Usern_input.pack(pady=5)
    Passwd=Label(w2,text="Enter Password:",font=("impact",15),bg=text_bg,fg=text_fg)
    Passwd.pack(pady=5)
    Passwd_input=Entry(w2,show="*")
    Passwd_input.pack(pady=5)
    Choice_user=StringVar()
    Stud_Teach=ttk.Combobox(w2,textvariable=Choice_user)
    Stud_Teach['values']=["Teacher","Student"]
    Stud_Teach['state']='readonly'
    Stud_Teach.pack()
    Submit_but=Button(w2,text="Submit",font=("impact",15),bg=text_bg,fg=text_fg,command=Submit_Signup)
    Submit_but.pack(pady=5)
    but_back=Button(w2,text="Back",relief='raised',font=("arial",20),fg=Button_fg,bg=Button_bg,command=close)
    but_back.pack(pady=5)
    w2.mainloop()
def Login_check():
        global UN, PA
        UN=Usern_input.get()
        PA=Passwd_input.get()
        con=ms.connect(host='localhost',user='root',passwd='root')
        cur=con.cursor()
        cur.execute('use Project_uhh')
        cur.execute('select * from signup')
        r=cur.fetchall()
        L=[]
        for i in r:
            L.append([i[1],i[2]])
        if [UN,PA] in L:
            for i in r:
                if UN==i[1] and PA==i[2]:
                    if i[3]=='Teacher':
                        Teach_Win()
                    else:
                        Stud_Winq()
        else:
                messagebox.showerror(title='Invalid ',message='Enter a Valid Username or Password.')   
 
def Login():
    def close():
        w.deiconify()
        w2.destroy()
    global w2
    global Usern_input, Passwd_input
    w.withdraw()
    w2=Toplevel(w)
    w2.config(bg=main_bg)
    w2.geometry('450x450')
    a=Label(w2,text="Log-in",font=("impact",20),bg=text_bg,fg=text_fg)
    a.pack(pady=5)
    Usern=Label(w2,text="Enter username:",font=("impact",15),bg=text_bg,fg=text_fg)
    Usern.pack(pady=5)
    Usern_input=Entry(w2)
    Usern_input.pack(pady=5)
    Passwd=Label(w2,text="Enter Password:",font=("impact",15),bg=text_bg,fg=text_fg)
    Passwd.pack(pady=5)
    Passwd_input=Entry(w2,show='*')
    Passwd_input.pack(pady=5)
    Submit_but=Button(w2,text="Submit",font=("impact",15),bg=text_bg,fg=text_fg,command=Login_check)
    Submit_but.pack(pady=5)
    but_back=Button(w2,text="Back",relief='raised',font=("arial",20),fg=Button_fg,bg=Button_bg,command=close)
    but_back.pack(pady=5)
    w2.mainloop()
    
def Stud_Winq():
    def close():
        w.deiconify()
        w2.destroy()
    def take_quiz():
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("USE EduTrip4U")
        cur.execute("SELECT * FROM quizzes")
        quizzes = cur.fetchall()
        
        def submit_answers():
            score = 0
            for idx, quiz in enumerate(quizzes):
                user_answer = user_answers[idx].get()
                if user_answer == quiz[6]:
                    score += 1
            messagebox.showinfo("Score", f"You got {score}/{len(quizzes)} correct!")
        user_answers = []
        for idx, quiz in enumerate(quizzes):
            Label(w2, text=quiz[1], font=("impact", 15), bg=text_bg, fg=text_fg).pack(pady=5)
            answer = StringVar()
            user_answers.append(answer)
            
            Radiobutton(w2, text=quiz[2], variable=answer, value='A', bg=text_bg, fg=text_fg).pack()
            Radiobutton(w2, text=quiz[3], variable=answer, value='B', bg=text_bg, fg=text_fg).pack()
            Radiobutton(w2, text=quiz[4], variable=answer, value='C', bg=text_bg, fg=text_fg).pack()
            Radiobutton(w2, text=quiz[5], variable=answer, value='D', bg=text_bg, fg=text_fg).pack()
        submit_button = Button(w2, text="Submit", font=("impact", 15), bg=text_bg, fg=text_fg, command=submit_answers)
        submit_button.pack(pady=5)
               



    

    w.withdraw()
    w2 = Toplevel(w)
    w2.config(bg=main_bg)
    w2.geometry('450x450')

    a = Label(w2, text="Take Quiz", font=("impact", 20), bg=text_bg, fg=text_fg)
    a.pack(pady=5)

    take_quiz_button = Button(w2, text="Start Quiz", font=("impact", 15), bg=text_bg, fg=text_fg, command=take_quiz)
    take_quiz_button.pack(pady=5)

    but_back = Button(w2, text="Back", relief='raised', font=("arial", 20), fg=Button_fg, bg=Button_bg, command=close)
    but_back.pack(pady=5)

    w2.mainloop()
    w2.withdraw()
    w3=Toplevel(w2)
    w3.config(bg=main_bg)
    w3.geometry('450x450')
    a=Label(w3,text="Welcome!",font=("impact",20),bg=text_bg,fg=text_fg)
    w3.title('Student')
    notebook =ttk.Notebook(w3)
    notebook.pack(pady=10, expand=True)
    frame1 =Frame(notebook, width=400, height=280)
    frame2 =Frame(notebook, width=400, height=280)
    frame3 =Frame(notebook, width=400, height=280)
    notebook.add(frame1, text='Profile')
    notebook.add(frame2, text='Quiz')
    notebook.add(frame3, text='Trip-Details')
    con=ms.connect(host='localhost',user='root',passwd='root')
    cur=con.cursor()
    cur.execute('use Project_uhh')
    cur.execute('select * from signup')
    L=cur.fetchall()
    for i in L:
        if i[1]==UN:
            A=Label(frame1,text=('Name:',i[0]),font=("impact",10),bg="white",fg=text_fg).pack()
            B=Label(frame1,text=('Username:',i[1]),font=("impact",10),bg="white",fg=text_fg).pack()
            C=Label(frame1,text=('Password:',i[2]),font=("impact",10),bg="white",fg=text_fg).pack()
            D=Label(frame1,text=('I_am_a:',i[3]),font=("impact",10),bg="white",fg=text_fg).pack()
    Button_Attend=Button(frame2,text="Show quizzes.",relief='raised',font=("arial",10),fg=Button_fg,bg=Button_bg,command=take_quiz).pack()
    but_back=Button(w3,text="Logout",relief='raised',font=("arial",10),fg=Button_fg,bg=Button_bg,command=close).pack()
    
def Teach_Win():
   
           
                
                
            
    def Teach_Winq():
        def close():
            w.deiconify()
            w2.destroy()

        def create_quiz():
            question = question_input.get()
            option_a = option_a_input.get()
            option_b = option_b_input.get()
            option_c = option_c_input.get()
            option_d = option_d_input.get()
            correct_option = correct_option_input.get()

            if not question or not option_a or not option_b or not option_c or not option_d or not correct_option:
                messagebox.showerror("Error", "All fields are required.")
                return
            
            con = get_db_connection()
            cur = con.cursor()

            # Create quiz table if not exists
            cur.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question VARCHAR(255),
                option_a VARCHAR(100),
                option_b VARCHAR(100),
                option_c VARCHAR(100),
                option_d VARCHAR(100),
                correct_option CHAR(1)
            )''')

            # Insert quiz into database
            cur.execute("INSERT INTO quizzes (question, option_a, option_b, option_c, option_d, correct_option) VALUES (%s, %s, %s, %s, %s, %s)",
                        (question, option_a, option_b, option_c, option_d, correct_option))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Quiz created successfully!")
        def clear_quiz():
            cur.execute("USE EduTrip4U")
            cur.execute('Delete from quizzes')
            con.commit()

        def view_quizzes():
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("USE EduTrip4U")
            cur.execute("SELECT * FROM quizzes")
            quizzes = cur.fetchall()
            
            # Display quizzes
            quizzes_text = ""
            for quiz in quizzes:
                quizzes_text += f"Q: {quiz[1]}\nA: {quiz[2]}  B: {quiz[3]}  C: {quiz[4]}  D: {quiz[5]}\nCorrect Answer: {quiz[6]}\n\n"
            
            messagebox.showinfo("Questions", quizzes_text)
            con.close()

        w.withdraw()
        w2 = Toplevel(w)
        w2.config(bg=main_bg)
        w2.geometry('450x450')
        
        a = Label(w2, text="Create Quiz", font=("impact", 20), bg=text_bg, fg=text_fg)
        a.pack(pady=5)

        question_label = Label(w2, text="Enter question:", font=("impact", 15), bg=text_bg, fg=text_fg)
        question_label.pack(pady=5)
        question_input = Entry(w2)
        question_input.pack(pady=5)

        option_a_label = Label(w2, text="Option A:", font=("impact", 15), bg=text_bg, fg=text_fg)
        option_a_label.pack(pady=5)
        option_a_input = Entry(w2)
        option_a_input.pack(pady=5)

        option_b_label = Label(w2, text="Option B:", font=("impact", 15), bg=text_bg, fg=text_fg)
        option_b_label.pack(pady=5)
        option_b_input = Entry(w2)
        option_b_input.pack(pady=5)

        option_c_label = Label(w2, text="Option C:", font=("impact", 15), bg=text_bg, fg=text_fg)
        option_c_label.pack(pady=5)
        option_c_input = Entry(w2)
        option_c_input.pack(pady=5)

        option_d_label = Label(w2, text="Option D:", font=("impact", 15), bg=text_bg, fg=text_fg)
        option_d_label.pack(pady=5)
        option_d_input = Entry(w2)
        option_d_input.pack(pady=5)

        correct_option_label = Label(w2, text="Correct Option (A/B/C/D):", font=("impact", 15), bg=text_bg, fg=text_fg)
        correct_option_label.pack(pady=5)
        correct_option_input = Entry(w2)
        correct_option_input.pack(pady=5)

        create_button = Button(w2, text="Create Quiz", font=("impact", 15), bg=text_bg, fg=text_fg, command=create_quiz)
        create_button.pack(pady=5)

        view_button = Button(w2, text="View Questions", font=("impact", 15), bg=text_bg, fg=text_fg, command=view_quizzes)
        view_button.pack(pady=5)

        but_back = Button(w2, text="Back", relief='raised', font=("arial", 20), fg=Button_fg, bg=Button_bg, command=close)
        but_back.pack(pady=5)
        
        clear_quizbut = Button(w2, text="Clear questions", relief='raised', font=("arial", 20), fg=Button_fg, bg=Button_bg, command=clear_quiz)
        clear_quizbut.pack(pady=5)
        w2.mainloop()

    def Change_Password():

        global PASS_O,PASS_N,USER_O,USER_N
        def Confirm_New():
            
            U1=USER_O.get()
            U2=USER_N.get()
            P1=PASS_O.get()
            P2=PASS_N.get()
            ask=messagebox.askyesno(title='Sure?',message='Are you sure you wanna change your Username and password?')    
            if ask == False:
                w3.deiconify()
                w4.destroy()
            else:
                con=ms.connect(host='localhost',user='root',passwd='root')
                cur=con.cursor()
                cur.execute('use Project_uhh')
                cur.execute('select * from signup')
                r=cur.fetchall()
                L=[]
                for i in r:
                    L.append([i[1],i[2]])
                if [U1,P1] in L:
                    for i in r:
                        if U1==i[1] and P1==i[2]:
                            UUU='Update signup set Usern=%s where Passwd=%s'
                            cur.execute(UUU,(U2,P1))
                            PPP='Update signup set Passwd=%s where Usern=%s' 
                            cur.execute(PPP,(P2,U2))
                            con.commit()                          
                else:
                    messagebox.showerror(title='Invalid ',message='Enter a Valid Username or Password.')              
                w3.deiconify()
                w4.destroy()
        def closeda():
            w3.deiconify()
            w4.destroy()
        w3.withdraw()
        w4=Toplevel(w3)
        w4.config(bg=main_bg)
        w4.geometry('450x450')
        a=Label(w4,text="Change Password",font=("impact",20),bg=text_bg,fg=text_fg).pack()
        Label(w4,text="Enter old username:",font=("impact",15),bg=text_bg,fg=text_fg).pack()
        USER_O=Entry(w4)
        USER_O.pack()
        Label(w4,text="Enter new username:",font=("impact",15),bg=text_bg,fg=text_fg).pack()
        USER_N=Entry(w4)
        USER_N.pack()
        Label(w4,text="Enter old password:",font=("impact",15),bg=text_bg,fg=text_fg).pack()
        PASS_O=Entry(w4)
        PASS_O.pack()
        Label(w4,text="Enter new password",font=("impact",15),bg=text_bg,fg=text_fg).pack()
        PASS_N=Entry(w4)
        PASS_N.pack()
        
        Confirm_But=Button(w4,text="Confirm?",font=("impact",15),bg=text_bg,fg=text_fg,command=Confirm_New).pack()
        backk=Button(w4,text="Back",relief='raised',font=("arial",10),fg=Button_fg,bg=Button_bg,command=closeda)
        backk.pack(pady=5)
        
        

        
        
        
    def close():
        w.deiconify()
        w3.destroy()
    global w3
    w2.withdraw()
    w3=Toplevel(w2)
    w3.config(bg=main_bg)
    w3.geometry('450x450')
    a=Label(w3,text="Welcome!",font=("impact",20),bg=text_bg,fg=text_fg).pack()
    w3.title('Teacher')
    notebook =ttk.Notebook(w3)
    notebook.pack(pady=10, expand=True)
    ProfileTab =Frame(notebook, width=400, height=280)
    BookingTab=Frame(notebook, width=400, height=280)
    QuizTab=Frame(notebook, width=400, height=280)
    AddQuiz=Button(QuizTab,text="+",font=("impact",20),bg=text_bg,fg=text_fg,command=Teach_Winq).pack()
    change_pass=Button(ProfileTab,text="Change Password",font=("impact",20),bg=text_bg,fg=text_fg,command=Change_Password).pack()
    but_back=Button(w3,text="Logout",relief='raised',font=("arial",10),fg=Button_fg,bg=Button_bg,command=close).pack()
    notebook.add(ProfileTab, text='Profile')
    notebook.add(BookingTab, text='Booking')
    notebook.add(QuizTab, text='Quiz')


    def Trip_up():
        def get_location_from_input(location_input):
            geolocator = Nominatim(user_agent="amenities_finder")
            location = geolocator.geocode(location_input)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None

      

        def fetch_amenities(lat, lon, selected_amenities):
            # Define the amenity tags with expanded options for hotels
            amenities_tags = {
                "restaurants": "amenity=restaurant",
                "hotels": ["amenity=hotel", "tourism=hotel"],  # Multiple tags for hotels
                "tourist_spots": "tourism=attraction"
            }

            # Increase search radius to ensure coverage
            search_radius = 5000  # 5000 meters (5 km)

            # Build the Overpass API query
            query = "[out:json];"
            for amenity in selected_amenities:
                tags = amenities_tags.get(amenity)
                if tags:
                    if isinstance(tags, list):
                        # If multiple tags exist (for hotels), add each one to the query
                        for tag in tags:
                            query += f"node(around:{search_radius},{lat},{lon})[{tag}];"
                    else:
                        # Single tag case
                        query += f"node(around:{search_radius},{lat},{lon})[{tags}];"
            query += "out;"

            # Print the URL for debugging
            print("Debug: Query URL:", f"https://overpass-api.de/api/interpreter?data={query}")

            # Create the full URL
            url = f"https://overpass-api.de/api/interpreter?data={query}"

            try:
                # Send the request to the Overpass API
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP request errors

                # Parse the JSON response
                try:
                    data = response.json()
                    print("Debug: Raw JSON Response:", data)  # Debug print

                except ValueError:
                    messagebox.showerror("Error", "Failed to decode JSON response.")
                    return []

                # Extract amenities from the response
                amenities = []
                for element in data.get('elements', []):
                    amenity = element.get('tags', {}).get('amenity', element.get('tags', {}).get('tourism', 'Unknown'))
                    name = element.get('tags', {}).get('name', 'Unnamed')
                    amenities.append(f"{name} ({amenity})")

                # Return the list of amenities or a message if none were found
                if not amenities:
                    amenities.append("No amenities found nearby.")
                return amenities

            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to fetch amenities: {e}")
                return []


        def display_output(amenities):
            output_window =  Toplevel()
            output_window.title("Nearby Amenities")
            
            if not amenities:
                amenities = ["No amenities found nearby."]
            
            label =  Label(output_window, text="Nearby Amenities:", font=("Arial", 14))
            label.pack(pady=10)

            listbox =  Listbox(output_window, width=50, height=10)
            listbox.pack(pady=10)

            for amenity in amenities:
                listbox.insert( END, amenity)

        input_window =  Toplevel()
        input_window.title("Search Nearby Amenities")
        
        location_label =  Label(input_window, text="Enter Location (city or coordinates):", font=("Arial", 12))
        location_label.pack(pady=10)

        location_entry =  Entry(input_window, font=("Arial", 12), width=25)
        location_entry.pack(pady=5)

        restaurant_var =  BooleanVar()
        hotel_var =  BooleanVar()
        tourist_spot_var =  BooleanVar()

        restaurant_checkbox =  Checkbutton(input_window, text="Restaurants", variable=restaurant_var, font=("Arial", 12))
        restaurant_checkbox.pack(pady=5)

        hotel_checkbox =  Checkbutton(input_window, text="Hotels", variable=hotel_var, font=("Arial", 12))
        hotel_checkbox.pack(pady=5)

        tourist_spot_checkbox =  Checkbutton(input_window, text="Tourist Spots", variable=tourist_spot_var, font=("Arial", 12))
        tourist_spot_checkbox.pack(pady=5)

        def on_submit():
            location_input = location_entry.get()
            
            selected_amenities = []
            if restaurant_var.get():
                selected_amenities.append("restaurants")
            if hotel_var.get():
                selected_amenities.append("hotels")
            if tourist_spot_var.get():
                selected_amenities.append("tourist_spots")
            
            if not selected_amenities:
                messagebox.showerror("Error", "Please select at least one amenity to search for.")
                return

            lat, lon = get_location_from_input(location_input)
            if lat is None or lon is None:
                messagebox.showerror("Error", "Unable to fetch location.")
                return

            amenities = fetch_amenities(lat, lon, selected_amenities)
            display_output(amenities)
            input_window.destroy()

        submit_button =  Button(input_window, text="Submit", font=("Arial", 12), command=on_submit)
        submit_button.pack(pady=20)


    Trip_Button=Button(BookingTab,text="Trip Up!",font=("impact",20),bg=text_bg,fg=text_fg,command=Trip_up)
    Trip_Button.pack()


    con=ms.connect(host='localhost',user='root',passwd='root')
    cur=con.cursor()
    cur.execute('use Project_uhh')
    cur.execute('select * from signup')
    L=cur.fetchall()
    for i in L:
        if i[1]==UN:
            A=Label(ProfileTab,text=('Name:',i[0]),font=("impact",10),bg="white",fg=text_fg).pack()
            B=Label(ProfileTab,text=('Username:',i[1]),font=("impact",10),bg="white",fg=text_fg).pack()
            C=Label(ProfileTab,text=('Password:',i[2]),font=("impact",10),bg="white",fg=text_fg).pack()
            D=Label(ProfileTab,text=('I_am_a:',i[3]),font=("impact",10),bg="white",fg=text_fg).pack()
    

        

    
            
    
Main()
