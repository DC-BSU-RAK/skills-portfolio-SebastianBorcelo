import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os

class Student:
    def __init__(self, code, name, mark1, mark2, mark3, exam_mark):
        self.code = int(code)
        self.name = name
        self.mark1 = int(mark1)
        self.mark2 = int(mark2)
        self.mark3 = int(mark3)
        self.exam_mark = int(exam_mark)
    
    @property
    def coursework_total(self):
        return self.mark1 + self.mark2 + self.mark3
    
    @property
    def total_score(self):
        return self.coursework_total + self.exam_mark
    
    @property
    def percentage(self):
        return (self.total_score / 160) * 100
    
    @property
    def grade(self):
        perc = self.percentage
        if perc >= 70:
            return 'A'
        elif perc >= 60:
            return 'B'
        elif perc >= 50:
            return 'C'
        elif perc >= 40:
            return 'D'
        else:
            return 'F'

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1200x800")  # Wider window for table view
        self.root.configure(bg='#1E3A8A')  # Dark blue background
        
        # Configure styles
        self.configure_styles()
        
        # Initialize status_var early
        self.status_var = tk.StringVar()
        self.status_var.set("Initializing...")
        
        self.students = []
        self.file_paths = [
            r"C:\Users\sebas\OneDrive\Documents\GitHub\skills-portfolio-SebastianBorcelo\Assessment 1 - Skills Portfolio\A1 - Resources\studentMarks.txt",
            "Assessment 1 - Skills Portfolio/A1 - Resources/studentMarks.txt",
            "A1 - Resources/studentMarks.txt",
            "studentMarks.txt"
        ]
        self.current_file_path = None
        
        self.create_main_frame()  # Create GUI first
        self.load_data()          # Then load data
        
        self.create_menu()
    
    def configure_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        
        # Configure frame styles
        style.configure('Dark.TFrame', background='#1E3A8A')
        style.configure('Light.TFrame', background='#E6F3FF')
        
        # Configure label styles with 2x larger fonts
        style.configure('Title.TLabel', 
                       font=('Impact', 32, 'bold'),
                       background='#1E3A8A',
                       foreground='#FFD700')
        
        style.configure('Normal.TLabel',
                       font=('Impact', 20),
                       background='#1E3A8A',
                       foreground='#FFFFFF')
        
        style.configure('Status.TLabel',
                       font=('Impact', 18),
                       background='#1E3A8A',
                       foreground='#90EE90')
        
        # Configure button styles
        style.configure('Action.TButton',
                       font=('Impact', 20, 'bold'),
                       background='#4A90E2',
                       foreground='#000000')
        
        # Configure menu styles with larger fonts
        self.root.option_add('*Menu.font', 'Impact 20')
        self.root.option_add('*Menu.background', '#1E3A8A')
        self.root.option_add('*Menu.foreground', '#FFFFFF')
        self.root.option_add('*Menu.activeBackground', '#4A90E2')
        self.root.option_add('*Menu.activeForeground', '#FFD700')
    
    def find_file(self):
        """Try to find the studentMarks.txt file in different locations"""
        for file_path in self.file_paths:
            if os.path.exists(file_path):
                return file_path
        
        # If file not found, ask user to locate it
        messagebox.showinfo("File Not Found", "Please locate the studentMarks.txt file")
        file_path = filedialog.askopenfilename(
            title="Select studentMarks.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        return file_path if file_path else None
    
    def load_data(self):
        """Load student data from file"""
        self.current_file_path = self.find_file()
        
        if not self.current_file_path:
            messagebox.showerror("Error", "Could not find studentMarks.txt file!")
            self.status_var.set("Error: File not found")
            return
        
        try:
            with open(self.current_file_path, "r") as file:
                lines = file.readlines()
                if not lines:
                    messagebox.showerror("Error", "File is empty!")
                    self.status_var.set("Error: File is empty")
                    return
                
                num_students = int(lines[0].strip())
                loaded_count = 0
                
                for i in range(1, num_students + 1):
                    if i < len(lines):
                        data = lines[i].strip().split(',')
                        if len(data) == 6:
                            student = Student(data[0], data[1], data[2], data[3], data[4], data[5])
                            self.students.append(student)
                            loaded_count += 1
            
            self.status_var.set(f"Loaded {loaded_count} students from {os.path.basename(self.current_file_path)}")
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.current_file_path}")
            self.status_var.set("Error: File not found")
        except ValueError as e:
            messagebox.showerror("Error", f"Error parsing data: {str(e)}")
            self.status_var.set("Error: Invalid data format")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            self.status_var.set("Error loading data")
    
    def save_data(self):
        """Save student data to file"""
        if not self.current_file_path:
            # If we don't have a current file path, ask user where to save
            self.current_file_path = filedialog.asksaveasfilename(
                title="Save student data as",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not self.current_file_path:
                return False
        
        try:
            with open(self.current_file_path, "w") as file:
                file.write(f"{len(self.students)}\n")
                for student in self.students:
                    file.write(f"{student.code},{student.name},{student.mark1},{student.mark2},{student.mark3},{student.exam_mark}\n")
            
            self.status_var.set(f"Data saved to {os.path.basename(self.current_file_path)}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")
            self.status_var.set("Error saving data")
            return False
    
    def create_menu(self):
        """Create the main menu"""
        menubar = tk.Menu(self.root, bg='#1E3A8A', fg='#FFFFFF', activebackground='#4A90E2', activeforeground='#FFD700', font=('Impact', 20))
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg='#1E3A8A', fg='#FFFFFF', activebackground='#4A90E2', activeforeground='#FFD700', font=('Impact', 18))
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reload Data", command=self.reload_data)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Student menu
        student_menu = tk.Menu(menubar, tearoff=0, bg='#1E3A8A', fg='#FFFFFF', activebackground='#4A90E2', activeforeground='#FFD700', font=('Impact', 18))
        menubar.add_cascade(label="Student Records", menu=student_menu)
        
        student_menu.add_command(label="View All Students", command=self.view_all_students)
        student_menu.add_command(label="View Individual Student", command=self.view_individual_student)
        student_menu.add_separator()
        student_menu.add_command(label="Highest Scoring Student", command=self.show_highest_student)
        student_menu.add_command(label="Lowest Scoring Student", command=self.show_lowest_student)
        student_menu.add_separator()
        student_menu.add_command(label="Sort Students", command=self.sort_students)
        student_menu.add_command(label="Add Student", command=self.add_student)
        student_menu.add_command(label="Delete Student", command=self.delete_student)
        student_menu.add_command(label="Update Student", command=self.update_student)
    
    def reload_data(self):
        """Reload data from file"""
        self.students.clear()
        self.load_data()
        self.view_all_students()
    
    def save_as(self):
        """Save data to a different file"""
        new_path = filedialog.asksaveasfilename(
            title="Save student data as",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if new_path:
            self.current_file_path = new_path
            self.save_data()
    
    def create_main_frame(self):
        """Create the main display frame"""
        self.main_frame = ttk.Frame(self.root, padding="20", style='Dark.TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Student Manager", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Text widget for displaying results with light blue background and larger font
        self.text_display = tk.Text(self.main_frame, width=120, height=20, wrap=tk.NONE,
                                   bg='#E6F3FF',
                                   fg='#000000',
                                   font=('Courier New', 14),
                                   selectbackground='#4A90E2',
                                   selectforeground='#FFFFFF',
                                   insertbackground='#000000',
                                   padx=10, pady=10)
        self.text_display.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars for text widget
        v_scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.text_display.yview)
        v_scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        
        h_scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.text_display.xview)
        h_scrollbar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.text_display.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Status bar
        self.status_var.set("Ready - Use the Student Records menu to begin")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                              style='Status.TLabel', relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
    
    def clear_display(self):
        """Clear the text display"""
        self.text_display.delete(1.0, tk.END)
    
    def display_text(self, text):
        """Display text in the text widget"""
        self.text_display.insert(tk.END, text + "\n")
    
    def setup_text_tags(self):
        """Set up color tags for the text display"""
        # Configure colorful tags for different types of text
        self.text_display.tag_configure('title', foreground='#FF6B6B', font=('Courier New', 16, 'bold'))
        self.text_display.tag_configure('header', foreground='#4ECDC4', font=('Courier New', 14, 'bold'))
        self.text_display.tag_configure('data', foreground='#000000', font=('Courier New', 12))
        self.text_display.tag_configure('summary', foreground='#FF6B6B', font=('Courier New', 14, 'bold'))
        
        # Grade color tags - only one set with proper colors
        self.text_display.tag_configure('grade_A', foreground='#00FF00', font=('Courier New', 12, 'bold'))  # Green for A
        self.text_display.tag_configure('grade_B', foreground='#87CEEB', font=('Courier New', 12, 'bold'))  # Light Blue for B
        self.text_display.tag_configure('grade_C', foreground='#FFA500', font=('Courier New', 12, 'bold'))  # Orange for C
        self.text_display.tag_configure('grade_D', foreground='#FF69B4', font=('Courier New', 12, 'bold'))  # Pink for D
        self.text_display.tag_configure('grade_F', foreground='#FF0000', font=('Courier New', 12, 'bold'))  # Red for F
    
    def view_all_students(self):
        """Display all student records in table format"""
        self.clear_display()
        self.setup_text_tags()
        
        if not self.students:
            self.display_text("No students found.")
            return
        
        # Create table header with scores alongside maximum values
        header = ("{:<8} {:<20} {:<10} {:<10} {:<10} {:<13} {:<10} {:<8} {:<6}".format(
            "Code", "Name", "CW1", "CW2", "CW3", "CW Total", "Exam", "Perc%", "Grade"
        ))
        
        self.display_text("ALL STUDENT RECORDS")
        self.text_display.insert(tk.END, "\n")
        self.text_display.insert(tk.END, "=" * 115 + "\n", 'header')
        self.text_display.insert(tk.END, header + "\n", 'header')
        self.text_display.insert(tk.END, "=" * 115 + "\n", 'header')
        
        total_percentage = 0
        
        # Display each student in table row format
        for student in self.students:
            grade_tag = f'grade_{student.grade}'
            row = ("{:<8} {:<23} {:<11} {:<11} {:<13} {:<12} {:<12} {:<10.1f} ".format(
                student.code,
                student.name[:19],  # Truncate long names
                f"{student.mark1}/20",    # CW1 with max
                f"{student.mark2}/20",    # CW2 with max
                f"{student.mark3}/20",    # CW3 with max
                f"{student.coursework_total}/60",  # CW Total with max
                f"{student.exam_mark}/100",        # Exam with max
                student.percentage
            ))
            
            # Add the row data first
            self.text_display.insert(tk.END, row, 'data')
            # Then add the grade with color in the same line
            self.text_display.insert(tk.END, f"{student.grade}\n", grade_tag)
            
            total_percentage += student.percentage
        
        # Summary
        self.text_display.insert(tk.END, "=" * 115 + "\n", 'header')
        summary_text = ("{:<8} {:<20} {:<10} {:<10} {:<10} {:<12} {:<12} {:<8.1f}".format(
            "",
            f"Total Students: {len(self.students)}",
            "", "", "", "", "",
            total_percentage/len(self.students)
        ))
        self.text_display.insert(tk.END, summary_text + "\n", 'summary')
        self.text_display.insert(tk.END, "=" * 115 + "\n", 'header')
        
        self.status_var.set(f"Displayed {len(self.students)} students in table format")
    
    def display_student_record(self, student):
        """Display a single student's record in detailed format"""
        self.clear_display()
        self.setup_text_tags()
        
        self.text_display.insert(tk.END, "DETAILED STUDENT RECORD\n", 'title')
        self.text_display.insert(tk.END, "=" * 50 + "\n", 'header')
        
        # Display in a formatted way with scores alongside maximum values
        self.text_display.insert(tk.END, f"Student Code: {student.code}\n", 'data')
        self.text_display.insert(tk.END, f"Name: {student.name}\n", 'data')
        self.text_display.insert(tk.END, "\n", 'data')
        self.text_display.insert(tk.END, "Coursework Marks:\n", 'header')
        self.text_display.insert(tk.END, f"  Mark 1: {student.mark1}/20\n", 'data')
        self.text_display.insert(tk.END, f"  Mark 2: {student.mark2}/20\n", 'data')
        self.text_display.insert(tk.END, f"  Mark 3: {student.mark3}/20\n", 'data')
        self.text_display.insert(tk.END, f"  Total: {student.coursework_total}/60\n", 'header')
        self.text_display.insert(tk.END, "\n", 'data')
        self.text_display.insert(tk.END, f"Exam Mark: {student.exam_mark}/100\n", 'data')
        self.text_display.insert(tk.END, f"Overall Percentage: {student.percentage:.2f}%\n", 'header')
        
        grade_tag = f'grade_{student.grade}'
        self.text_display.insert(tk.END, f"Grade: ", 'data')
        self.text_display.insert(tk.END, f"{student.grade}\n", grade_tag)
        
        self.text_display.insert(tk.END, "=" * 50 + "\n", 'header')
    
    def view_individual_student(self):
        """View individual student record"""
        if not self.students:
            messagebox.showinfo("No Students", "No student records available.")
            return
        
        # Create dialog for student selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Student")
        dialog.geometry("600x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#1E3A8A')
        
        title_label = tk.Label(dialog, text="Select a student:", 
                              font=('Impact', 24, 'bold'),
                              bg='#1E3A8A', fg='#FFD700')
        title_label.pack(pady=20)
        
        # ComboBox for student selection with larger font
        student_var = tk.StringVar()
        student_names = [f"{student.code} - {student.name}" for student in self.students]
        student_combo = ttk.Combobox(dialog, textvariable=student_var, values=student_names, 
                                   state="readonly", font=('Impact', 20))
        student_combo.pack(pady=20, padx=40, fill=tk.X)
        
        def show_selected():
            selection = student_combo.get()
            if selection:
                student_code = int(selection.split(" - ")[0])
                student = next((s for s in self.students if s.code == student_code), None)
                if student:
                    self.display_student_record(student)
                    self.status_var.set(f"Displayed record for {student.name}")
                    dialog.destroy()
        
        show_button = tk.Button(dialog, text="Show Record", command=show_selected,
                               font=('Impact', 20, 'bold'),
                               bg='#4A90E2', fg='#000000',
                               activebackground='#357ABD',
                               activeforeground='#FFFFFF')
        show_button.pack(pady=20)
    
    def show_highest_student(self):
        """Show student with highest overall mark"""
        if not self.students:
            messagebox.showinfo("No Students", "No student records available.")
            return
        
        highest_student = max(self.students, key=lambda x: x.total_score)
        
        self.display_student_record(highest_student)
        self.status_var.set(f"Displayed highest scoring student: {highest_student.name}")
    
    def show_lowest_student(self):
        """Show student with lowest overall mark"""
        if not self.students:
            messagebox.showinfo("No Students", "No student records available.")
            return
        
        lowest_student = min(self.students, key=lambda x: x.total_score)
        
        self.display_student_record(lowest_student)
        self.status_var.set(f"Displayed lowest scoring student: {lowest_student.name}")
    
    def sort_students(self):
        """Sort student records"""
        if not self.students:
            messagebox.showinfo("No Students", "No student records available.")
            return
        
        # Create dialog for sort options
        dialog = tk.Toplevel(self.root)
        dialog.title("Sort Students")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#1E3A8A')
        
        title_label = tk.Label(dialog, text="Sort by:", 
                              font=('Impact', 24, 'bold'),
                              bg='#1E3A8A', fg='#FFD700')
        title_label.pack(pady=20)
        
        sort_var = tk.StringVar(value="percentage")
        
        # Create colorful radio buttons with larger fonts
        colors = ['#FF6B6B', '#4ECDC4', '#FFD700']
        options = [
            ("Percentage (Descending)", "percentage"),
            ("Name (Ascending)", "name"),
            ("Student Code (Ascending)", "code")
        ]
        
        for i, (text, value) in enumerate(options):
            rb = tk.Radiobutton(dialog, text=text, variable=sort_var, value=value,
                               font=('Impact', 20),
                               bg='#1E3A8A', fg=colors[i],
                               activebackground='#1E3A8A',
                               selectcolor='#1E3A8A')
            rb.pack(anchor=tk.W, padx=40, pady=10)
        
        def perform_sort():
            if sort_var.get() == "percentage":
                self.students.sort(key=lambda x: x.percentage, reverse=True)
            elif sort_var.get() == "name":
                self.students.sort(key=lambda x: x.name)
            else:  # code
                self.students.sort(key=lambda x: x.code)
            
            self.view_all_students()
            self.status_var.set(f"Students sorted by {sort_var.get()}")
            dialog.destroy()
        
        sort_button = tk.Button(dialog, text="Sort", command=perform_sort,
                               font=('Impact', 20, 'bold'),
                               bg='#4A90E2', fg='#000000',
                               activebackground='#357ABD',
                               activeforeground='#FFFFFF')
        sort_button.pack(pady=20)
    
    def add_student(self):
        """Add a new student record"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#1E3A8A')
        
        # Form fields with colorful labels and larger fonts
        fields = [
            ("Student Code:", 0, '#FFD700'),
            ("Name:", 1, '#4ECDC4'),
            ("Coursework Mark 1 (out of 20):", 2, '#FF6B6B'),
            ("Coursework Mark 2 (out of 20):", 3, '#FF6B6B'),
            ("Coursework Mark 3 (out of 20):", 4, '#FF6B6B'),
            ("Exam Mark (out of 100):", 5, '#4ECDC4')
        ]
        
        entries = {}
        for label_text, row, color in fields:
            label = tk.Label(dialog, text=label_text, font=('Impact', 20),
                           bg='#1E3A8A', fg=color)
            label.grid(row=row, column=0, padx=10, pady=15, sticky=tk.W)
            
            entry = tk.Entry(dialog, font=('Impact', 20), bg='#E6F3FF')
            entry.grid(row=row, column=1, padx=10, pady=15, sticky=(tk.W, tk.E))
            entries[label_text] = entry
        
        dialog.columnconfigure(1, weight=1)
        
        def save_student():
            try:
                code = int(entries["Student Code:"].get())
                name = entries["Name:"].get()
                mark1 = int(entries["Coursework Mark 1 (out of 20):"].get())
                mark2 = int(entries["Coursework Mark 2 (out of 20):"].get())
                mark3 = int(entries["Coursework Mark 3 (out of 20):"].get())
                exam = int(entries["Exam Mark (out of 100):"].get())
                
                # Validate inputs
                if not (1000 <= code <= 9999):
                    messagebox.showerror("Error", "Student code must be between 1000 and 9999")
                    return
                
                if any(s.code == code for s in self.students):
                    messagebox.showerror("Error", "Student code already exists")
                    return
                
                if not name:
                    messagebox.showerror("Error", "Name cannot be empty")
                    return
                
                if not (0 <= mark1 <= 20) or not (0 <= mark2 <= 20) or not (0 <= mark3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20")
                    return
                
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                    return
                
                # Create and add new student
                new_student = Student(code, name, mark1, mark2, mark3, exam)
                self.students.append(new_student)
                
                if self.save_data():
                    messagebox.showinfo("Success", "Student added successfully!")
                    dialog.destroy()
                    self.status_var.set(f"Added new student: {name}")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding student: {str(e)}")
        
        save_button = tk.Button(dialog, text="Save", command=save_student,
                               font=('Impact', 20, 'bold'),
                               bg='#4A90E2', fg='#000000',
                               activebackground='#357ABD',
                               activeforeground='#FFFFFF')
        save_button.grid(row=6, column=0, columnspan=2, pady=20)
    
    def delete_student(self):
        """Delete a student record"""
        if not self.students:
            messagebox.showinfo("No Students", "No student records available.")
            return
        
        # Create dialog for student selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Student")
        dialog.geometry("600x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#1E3A8A')
        
        title_label = tk.Label(dialog, text="Select student to delete:", 
                              font=('Impact', 24, 'bold'),
                              bg='#1E3A8A', fg='#FFD700')
        title_label.pack(pady=20)
        
        student_var = tk.StringVar()
        student_names = [f"{student.code} - {student.name}" for student in self.students]
        student_combo = ttk.Combobox(dialog, textvariable=student_var, values=student_names, 
                                   state="readonly", font=('Impact', 20))
        student_combo.pack(pady=20, padx=40, fill=tk.X)
        
        def delete_selected():
            selection = student_combo.get()
            if selection:
                student_code = int(selection.split(" - ")[0])
                student_name = selection.split(" - ")[1]
                
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?"):
                    self.students = [s for s in self.students if s.code != student_code]
                    
                    if self.save_data():
                        messagebox.showinfo("Success", "Student deleted successfully!")
                        dialog.destroy()
                        self.status_var.set(f"Deleted student: {student_name}")
        
        delete_button = tk.Button(dialog, text="Delete", command=delete_selected,
                                 font=('Impact', 20, 'bold'),
                                 bg='#FF6B6B', fg='#000000',
                                 activebackground='#FF5252',
                                 activeforeground='#FFFFFF')
        delete_button.pack(pady=20)
    
    def update_student(self):
        """Update a student record"""
        if not self.students:
            messagebox.showinfo("No Students", "No student records available.")
            return
        
        # Create dialog for student selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Student")
        dialog.geometry("650x500")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#1E3A8A')
        
        title_label = tk.Label(dialog, text="Select student to update:", 
                              font=('Impact', 24, 'bold'),
                              bg='#1E3A8A', fg='#FFD700')
        title_label.pack(pady=20)
        
        student_var = tk.StringVar()
        student_names = [f"{student.code} - {student.name}" for student in self.students]
        student_combo = ttk.Combobox(dialog, textvariable=student_var, values=student_names, 
                                   state="readonly", font=('Impact', 20))
        student_combo.pack(pady=20, padx=40, fill=tk.X)
        
        # Update fields frame
        fields_frame = tk.Frame(dialog, bg='#1E3A8A')
        fields_frame.pack(pady=20, fill=tk.X, padx=40)
        
        field_configs = [
            ("Name:", 0, '#4ECDC4'),
            ("Coursework Mark 1 (out of 20):", 1, '#FF6B6B'),
            ("Coursework Mark 2 (out of 20):", 2, '#FF6B6B'),
            ("Coursework Mark 3 (out of 20):", 3, '#FF6B6B'),
            ("Exam Mark (out of 100):", 4, '#4ECDC4')
        ]
        
        entries = {}
        for label_text, row, color in field_configs:
            label = tk.Label(fields_frame, text=label_text, font=('Impact', 20),
                           bg='#1E3A8A', fg=color)
            label.grid(row=row, column=0, padx=10, pady=15, sticky=tk.W)
            
            entry = tk.Entry(fields_frame, font=('Impact', 20), bg='#E6F3FF')
            entry.grid(row=row, column=1, padx=10, pady=15, sticky=(tk.W, tk.E))
            entries[label_text] = entry
        
        fields_frame.columnconfigure(1, weight=1)
        
        def load_student_data():
            selection = student_combo.get()
            if selection:
                student_code = int(selection.split(" - ")[0])
                student = next((s for s in self.students if s.code == student_code), None)
                if student:
                    entries["Name:"].delete(0, tk.END)
                    entries["Name:"].insert(0, student.name)
                    entries["Coursework Mark 1 (out of 20):"].delete(0, tk.END)
                    entries["Coursework Mark 1 (out of 20):"].insert(0, str(student.mark1))
                    entries["Coursework Mark 2 (out of 20):"].delete(0, tk.END)
                    entries["Coursework Mark 2 (out of 20):"].insert(0, str(student.mark2))
                    entries["Coursework Mark 3 (out of 20):"].delete(0, tk.END)
                    entries["Coursework Mark 3 (out of 20):"].insert(0, str(student.mark3))
                    entries["Exam Mark (out of 100):"].delete(0, tk.END)
                    entries["Exam Mark (out of 100):"].insert(0, str(student.exam_mark))
        
        student_combo.bind('<<ComboboxSelected>>', lambda e: load_student_data())
        
        def update_selected():
            selection = student_combo.get()
            if selection:
                student_code = int(selection.split(" - ")[0])
                student = next((s for s in self.students if s.code == student_code), None)
                
                if student:
                    try:
                        student.name = entries["Name:"].get()
                        student.mark1 = int(entries["Coursework Mark 1 (out of 20):"].get())
                        student.mark2 = int(entries["Coursework Mark 2 (out of 20):"].get())
                        student.mark3 = int(entries["Coursework Mark 3 (out of 20):"].get())
                        student.exam_mark = int(entries["Exam Mark (out of 100):"].get())
                        
                        # Validate inputs
                        if not student.name:
                            messagebox.showerror("Error", "Name cannot be empty")
                            return
                        
                        if not (0 <= student.mark1 <= 20) or not (0 <= student.mark2 <= 20) or not (0 <= student.mark3 <= 20):
                            messagebox.showerror("Error", "Coursework marks must be between 0 and 20")
                            return
                        
                        if not (0 <= student.exam_mark <= 100):
                            messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                            return
                        
                        if self.save_data():
                            messagebox.showinfo("Success", "Student updated successfully!")
                            dialog.destroy()
                            self.status_var.set(f"Updated student: {student.name}")
                    
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid numeric values")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error updating student: {str(e)}")
        
        update_button = tk.Button(dialog, text="Update", command=update_selected,
                                 font=('Impact', 20, 'bold'),
                                 bg='#4A90E2', fg='#000000',
                                 activebackground='#357ABD',
                                 activeforeground='#FFFFFF')
        update_button.pack(pady=20)

def main():
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()