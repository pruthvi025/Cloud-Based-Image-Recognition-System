"""
Cloud Image Recognition System - GUI Application with Firebase Auth and GCS
A Tkinter-based GUI for image upload, analysis, and cloud storage
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from PIL import Image, ImageTk
import os
from google.cloud import vision, storage
import io
import json
import datetime
import pyrebase
import threading


class CloudImageRecognitionApp:
    """Main application class for the Cloud Image Recognition System"""
    
    def __init__(self, root):
        """
        Initialize the application
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.root.title("Cloud Image Recognition System")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        # Configure root window background
        self.root.config(bg="#f0f0f0")
        
        # Variable to store the current image path and user info
        self.current_image_path = None
        self.current_photo = None
        self.current_user = None
        self.user_email = None
        
        # Firebase configuration
        firebase_config = {
            "apiKey": "AIzaSyCxfqrP0UlAx6yOuHhjyecf9LXXagSxrUw",
            "authDomain": "python-project-ee581.firebaseapp.com",
            "projectId": "python-project-ee581",
            "storageBucket": "python-project-ee581.appspot.com",
            "messagingSenderId": "94884040561",
            "appId": "1:94884040561:web:YOUR_APP_ID",
            "databaseURL": ""
        }
        
        # Initialize Firebase
        try:
            self.firebase = pyrebase.initialize_app(firebase_config)
            self.auth = self.firebase.auth()
            print("Firebase initialized successfully")
        except Exception as e:
            print(f"Firebase initialization error: {str(e)}")
            self.auth = None
        
        # Initialize Google Cloud Vision client
        try:
            # Set the credentials file path
            credentials_path = os.path.join(os.path.dirname(__file__), 
                                           'python-project-476206-c40e283fa576.json')
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            
            # Create Vision API client
            self.vision_client = vision.ImageAnnotatorClient()
            
            # Create GCS client
            self.storage_client = storage.Client()
            self.bucket_name = "image-recognition-storage-project"
            self.bucket = self.storage_client.bucket(self.bucket_name)
            
            self.api_initialized = True
            
        except Exception as e:
            self.vision_client = None
            self.storage_client = None
            self.api_initialized = False
            print(f"Warning: Google Cloud API initialization failed: {str(e)}")
        
        # Setup the GUI components
        self.setup_login_ui()
        
    def setup_login_ui(self):
        """Setup login/signup UI"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=40, pady=40)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Cloud Image Recognition System",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 30))
        
        # Login/Signup Frame
        auth_frame = tk.LabelFrame(
            main_frame,
            text="Authentication",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2c3e50",
            padx=30,
            pady=30
        )
        auth_frame.pack()
        
        # Email
        tk.Label(auth_frame, text="Email:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.email_entry = tk.Entry(auth_frame, font=("Arial", 12), width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Password
        tk.Label(auth_frame, text="Password:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.password_entry = tk.Entry(auth_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(auth_frame, bg="white")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        login_btn = tk.Button(
            button_frame,
            text="Login",
            command=self.login,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        login_btn.pack(side=tk.LEFT, padx=10)
        
        signup_btn = tk.Button(
            button_frame,
            text="Sign Up",
            command=self.signup,
            font=("Arial", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        signup_btn.pack(side=tk.LEFT, padx=10)
        
        # Bind Enter key to login
        self.email_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
    def login(self):
        """Handle user login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
        
        try:
            # Authenticate with Firebase
            user = self.auth.sign_in_with_email_and_password(email, password)
            self.current_user = user
            self.user_email = email
            
            messagebox.showinfo("Success", f"Welcome back, {email}!")
            self.setup_main_ui()
            
        except Exception as e:
            error_msg = str(e)
            if "INVALID_PASSWORD" in error_msg or "INVALID_LOGIN_CREDENTIALS" in error_msg:
                messagebox.showerror("Error", "Invalid email or password!")
            elif "EMAIL_NOT_FOUND" in error_msg:
                messagebox.showerror("Error", "Email not found. Please sign up first!")
            else:
                messagebox.showerror("Error", f"Login failed: {error_msg}")
    
    def signup(self):
        """Handle user signup"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters!")
            return
        
        try:
            # Create new user with Firebase
            user = self.auth.create_user_with_email_and_password(email, password)
            self.current_user = user
            self.user_email = email
            
            messagebox.showinfo("Success", f"Account created successfully!\nWelcome, {email}!")
            self.setup_main_ui()
            
        except Exception as e:
            error_msg = str(e)
            if "EMAIL_EXISTS" in error_msg:
                messagebox.showerror("Error", "This email is already registered. Please login!")
            elif "WEAK_PASSWORD" in error_msg:
                messagebox.showerror("Error", "Password is too weak. Use at least 6 characters!")
            else:
                messagebox.showerror("Error", f"Signup failed: {error_msg}")
    
    def setup_main_ui(self):
        """Setup main application UI after authentication"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container frame with padding
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top bar with title and logout
        top_bar = tk.Frame(main_frame, bg="#f0f0f0")
        top_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Title Label
        title_label = tk.Label(
            top_bar,
            text="Cloud Image Recognition System",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(side=tk.LEFT)
        
        # User info and logout
        user_frame = tk.Frame(top_bar, bg="#f0f0f0")
        user_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            user_frame,
            text=f"User: {self.user_email}",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#7f8c8d"
        ).pack(side=tk.LEFT, padx=10)
        
        logout_btn = tk.Button(
            user_frame,
            text="Logout",
            command=self.logout,
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        logout_btn.pack(side=tk.LEFT)
        
        # Button Frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Upload Image Button
        self.upload_btn = tk.Button(
            button_frame,
            text="📁 Upload Image",
            command=self.upload_image,
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        # Analyze Image Button
        self.analyze_btn = tk.Button(
            button_frame,
            text="🔍 Analyze & Save",
            command=self.analyze_and_save,
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            activeforeground="white",
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # View History Button
        self.history_btn = tk.Button(
            button_frame,
            text="📜 View History",
            command=self.view_history,
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.history_btn.pack(side=tk.LEFT, padx=5)
        
        # Content Frame (holds image preview and output side by side)
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Image Preview
        preview_frame = tk.LabelFrame(
            content_frame,
            text="Image Preview",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.image_label = tk.Label(
            preview_frame,
            text="No image uploaded\n\nClick 'Upload Image' to begin",
            font=("Arial", 10),
            bg="white",
            fg="#7f8c8d",
            width=40,
            height=20
        )
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Output
        output_frame = tk.LabelFrame(
            content_frame,
            text="Analysis Results",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#2c3e50",
            height=20
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        self.log_message("Welcome to Cloud Image Recognition System!")
        self.log_message(f"Logged in as: {self.user_email}")
        self.log_message("Upload an image to begin analysis.\n")
    
    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.user_email = None
        self.current_image_path = None
        self.current_photo = None
        self.setup_login_ui()
    
    def upload_image(self):
        """Handle image upload functionality"""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.current_image_path = file_path
                self.display_image(file_path)
                self.analyze_btn.config(state=tk.NORMAL)
                
                filename = os.path.basename(file_path)
                self.log_message(f"✓ Image uploaded: {filename}\n")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
                self.log_message(f"✗ Error loading image: {str(e)}\n")
    
    def display_image(self, image_path):
        """Display the selected image in the preview area"""
        try:
            image = Image.open(image_path)
            orig_width, orig_height = image.size
            
            # Scale to fit preview (max 400x500)
            max_width = 400
            max_height = 500
            
            width_ratio = max_width / orig_width
            height_ratio = max_height / orig_height
            scale_ratio = min(width_ratio, height_ratio, 1.0)
            
            new_width = int(orig_width * scale_ratio)
            new_height = int(orig_height * scale_ratio)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.current_photo = ImageTk.PhotoImage(image)
            
            self.image_label.config(image=self.current_photo, text="")
            self.image_label.image = self.current_photo
            
        except Exception as e:
            raise Exception(f"Error displaying image: {str(e)}")
    
    def analyze_and_save(self):
        """Analyze image and save results to GCS"""
        if not self.current_image_path:
            messagebox.showwarning("No Image", "Please upload an image first!")
            return
        
        if not self.api_initialized:
            messagebox.showerror("API Error", "Google Cloud services are not initialized.")
            return
        
        # Run analysis in a separate thread to avoid freezing UI
        threading.Thread(target=self._perform_analysis, daemon=True).start()
    
    def _perform_analysis(self):
        """Perform the actual analysis (runs in separate thread)"""
        try:
            filename = os.path.basename(self.current_image_path)
            self.log_message(f"\n{'='*50}")
            self.log_message(f"🔍 Analyzing: {filename}")
            self.log_message(f"{'='*50}\n")
            
            # Read image
            with io.open(self.current_image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Perform analysis
            results = {}
            
            # Label Detection
            self.log_message("📌 Detecting labels...")
            response_labels = self.vision_client.label_detection(image=image)
            labels = response_labels.label_annotations
            results['labels'] = [{'description': label.description, 'score': label.score} for label in labels[:10]]
            
            if labels:
                for label in labels[:5]:
                    self.log_message(f"   • {label.description}: {label.score*100:.2f}%")
            
            # Object Detection
            self.log_message("\n🎯 Detecting objects...")
            response_objects = self.vision_client.object_localization(image=image)
            objects = response_objects.localized_object_annotations
            results['objects'] = [{'name': obj.name, 'score': obj.score} for obj in objects[:5]]
            
            if objects:
                for obj in objects[:3]:
                    self.log_message(f"   • {obj.name}: {obj.score*100:.2f}%")
            
            # Text Detection
            self.log_message("\n📝 Detecting text...")
            response_text = self.vision_client.text_detection(image=image)
            texts = response_text.text_annotations
            results['text'] = texts[0].description if texts else ""
            
            if texts:
                detected_text = texts[0].description.strip()
                if detected_text:
                    lines = detected_text.split('\n')[:3]
                    for line in lines:
                        self.log_message(f"   • {line}")
            
            # Face Detection
            self.log_message("\n👤 Detecting faces...")
            response_faces = self.vision_client.face_detection(image=image)
            faces = response_faces.face_annotations
            results['faces'] = len(faces)
            
            if faces:
                self.log_message(f"   • Found {len(faces)} face(s)")
            
            # Save to GCS
            self.log_message(f"\n{'='*50}")
            self.log_message("☁️  Saving to Google Cloud Storage...")
            self.log_message(f"{'='*50}\n")
            
            uid = self.current_user['localId']
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = os.path.splitext(filename)[0]
            
            # Upload image
            image_blob_name = f"{uid}/images/{timestamp}_{filename}"
            image_blob = self.bucket.blob(image_blob_name)
            image_blob.upload_from_filename(self.current_image_path)
            self.log_message(f"✓ Image saved: {image_blob_name}")
            
            # Save results as JSON
            results['timestamp'] = timestamp
            results['original_filename'] = filename
            results['image_path'] = image_blob_name
            
            result_blob_name = f"{uid}/results/{timestamp}_{base_filename}.json"
            result_blob = self.bucket.blob(result_blob_name)
            result_blob.upload_from_string(json.dumps(results, indent=2), content_type='application/json')
            self.log_message(f"✓ Results saved: {result_blob_name}")
            
            self.log_message(f"\n{'='*50}")
            self.log_message("✅ Analysis complete and saved to cloud!")
            self.log_message(f"{'='*50}\n")
            
        except Exception as e:
            self.log_message(f"\n✗ Error: {str(e)}\n")
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def view_history(self):
        """View user's analysis history from GCS"""
        if not self.api_initialized:
            messagebox.showerror("API Error", "Google Cloud services are not initialized.")
            return
        
        # Create history window
        history_window = tk.Toplevel(self.root)
        history_window.title("Analysis History")
        history_window.geometry("800x600")
        history_window.config(bg="#f0f0f0")
        
        # Title
        tk.Label(
            history_window,
            text="Your Analysis History",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=10)
        
        # Frame for listbox and scrollbar
        list_frame = tk.Frame(history_window, bg="#f0f0f0")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 10),
            yscrollcommand=scrollbar.set,
            height=15
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Button frame
        btn_frame = tk.Frame(history_window, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        # View Details Button
        view_btn = tk.Button(
            btn_frame,
            text="View Details",
            command=lambda: self.view_result_details(history_window),
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        view_btn.pack(side=tk.LEFT, padx=5)
        
        # Delete Button
        delete_btn = tk.Button(
            btn_frame,
            text="Delete",
            command=lambda: self.delete_history_item(history_window),
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh Button
        refresh_btn = tk.Button(
            btn_frame,
            text="Refresh",
            command=lambda: self.load_history(history_window),
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Load history
        self.load_history(history_window)
    
    def load_history(self, history_window):
        """Load user's history from GCS"""
        try:
            self.history_listbox.delete(0, tk.END)
            
            uid = self.current_user['localId']
            prefix = f"{uid}/results/"
            
            # List all result files
            blobs = list(self.bucket.list_blobs(prefix=prefix))
            
            if not blobs:
                self.history_listbox.insert(tk.END, "No history found")
                return
            
            # Store blob references
            self.history_blobs = []
            
            for blob in blobs:
                if blob.name.endswith('.json'):
                    # Download and parse JSON
                    json_data = json.loads(blob.download_as_string())
                    
                    timestamp = json_data.get('timestamp', 'Unknown')
                    filename = json_data.get('original_filename', 'Unknown')
                    
                    display_text = f"{timestamp} - {filename}"
                    self.history_listbox.insert(tk.END, display_text)
                    self.history_blobs.append((blob, json_data))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load history: {str(e)}")
    
    def view_result_details(self, history_window):
        """View details of selected result"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to view!")
            return
        
        try:
            idx = selection[0]
            if idx >= len(self.history_blobs):
                return
            
            blob, json_data = self.history_blobs[idx]
            
            # Create details window
            details_window = tk.Toplevel(history_window)
            details_window.title("Analysis Details")
            details_window.geometry("700x600")
            details_window.config(bg="#f0f0f0")
            
            # Title
            tk.Label(
                details_window,
                text=f"Analysis: {json_data.get('original_filename', 'Unknown')}",
                font=("Arial", 14, "bold"),
                bg="#f0f0f0",
                fg="#2c3e50"
            ).pack(pady=10)
            
            # Details text area
            details_text = scrolledtext.ScrolledText(
                details_window,
                wrap=tk.WORD,
                font=("Consolas", 10),
                bg="#ffffff",
                fg="#2c3e50"
            )
            details_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Display formatted results
            details_text.insert(tk.END, f"Timestamp: {json_data.get('timestamp', 'N/A')}\n")
            details_text.insert(tk.END, f"Original File: {json_data.get('original_filename', 'N/A')}\n")
            details_text.insert(tk.END, f"Image Path: {json_data.get('image_path', 'N/A')}\n\n")
            
            details_text.insert(tk.END, "="*50 + "\n")
            details_text.insert(tk.END, "LABELS DETECTED\n")
            details_text.insert(tk.END, "="*50 + "\n")
            labels = json_data.get('labels', [])
            if labels:
                for label in labels[:10]:
                    details_text.insert(tk.END, f"• {label['description']}: {label['score']*100:.2f}%\n")
            else:
                details_text.insert(tk.END, "No labels detected\n")
            
            details_text.insert(tk.END, "\n" + "="*50 + "\n")
            details_text.insert(tk.END, "OBJECTS DETECTED\n")
            details_text.insert(tk.END, "="*50 + "\n")
            objects = json_data.get('objects', [])
            if objects:
                for obj in objects:
                    details_text.insert(tk.END, f"• {obj['name']}: {obj['score']*100:.2f}%\n")
            else:
                details_text.insert(tk.END, "No objects detected\n")
            
            details_text.insert(tk.END, "\n" + "="*50 + "\n")
            details_text.insert(tk.END, "TEXT DETECTED\n")
            details_text.insert(tk.END, "="*50 + "\n")
            text = json_data.get('text', '')
            if text:
                details_text.insert(tk.END, text + "\n")
            else:
                details_text.insert(tk.END, "No text detected\n")
            
            details_text.insert(tk.END, "\n" + "="*50 + "\n")
            details_text.insert(tk.END, "FACES DETECTED\n")
            details_text.insert(tk.END, "="*50 + "\n")
            faces = json_data.get('faces', 0)
            details_text.insert(tk.END, f"Number of faces: {faces}\n")
            
            details_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view details: {str(e)}")
    
    def delete_history_item(self, history_window):
        """Delete selected history item"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to delete!")
            return
        
        try:
            idx = selection[0]
            if idx >= len(self.history_blobs):
                return
            
            blob, json_data = self.history_blobs[idx]
            
            # Confirm deletion
            result = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete:\n{json_data.get('original_filename', 'Unknown')}?"
            )
            
            if not result:
                return
            
            # Delete result JSON
            blob.delete()
            
            # Delete associated image
            image_path = json_data.get('image_path', '')
            if image_path:
                try:
                    image_blob = self.bucket.blob(image_path)
                    image_blob.delete()
                except Exception as e:
                    print(f"Error deleting image: {str(e)}")
            
            messagebox.showinfo("Success", "Item deleted successfully!")
            
            # Refresh the list
            self.load_history(history_window)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete item: {str(e)}")
    
    def log_message(self, message):
        """Add a message to the output text area"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)


def main():
    """Main function to run the application"""
    # Create the root window
    root = tk.Tk()
    
    # Create the application instance
    app = CloudImageRecognitionApp(root)
    
    # Run the application
    root.mainloop()


if __name__ == "__main__":
    main()
