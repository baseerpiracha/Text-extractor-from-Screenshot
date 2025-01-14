import os
import time
from tkinter import Tk, Label, Button, Entry, Text, Canvas, PhotoImage, messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import pytesseract
import pyautogui
import threading

# Configure Tesseract path (Update the path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update if Tesseract is installed elsewhere

class ScreenshotTextExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduled Screenshot Text Extractor")
        self.root.geometry("800x650")
        self.root.config(bg="#f4f7fb")  # Light background color
        self.screenshot_path = None

        # Title Label
        self.label = Label(root, text="Scheduled Screenshot Text Extractor", font=("Arial", 18, "bold"), bg="#f4f7fb", fg="#333")
        self.label.pack(pady=20)

        # Timer input
        self.timer_label = Label(root, text="Enter Timer (in seconds):", font=("Arial", 12), bg="#f4f7fb", fg="#333")
        self.timer_label.pack(pady=5)
        self.timer_entry = Entry(root, font=("Arial", 12), width=15, borderwidth=2, relief="solid", fg="#333", justify="center")
        self.timer_entry.pack(pady=10)

        # Start Button
        self.start_button = Button(root, text="Start Timer", command=self.start_timer, font=("Arial", 12, "bold"), fg="white", bg="#007BFF", width=15, relief="flat")
        self.start_button.pack(pady=15)

        # Canvas for displaying the screenshot
        self.canvas_frame = ttk.Frame(root)
        self.canvas_frame.pack(pady=15)

        self.canvas = Canvas(self.canvas_frame, width=600, height=300, bg="gray", bd=0, highlightthickness=0)
        self.canvas.pack()

        # Text widget for displaying and copying extracted text
        self.text_label = Label(root, text="Extracted Text:", font=("Arial", 12), bg="#f4f7fb", fg="#333")
        self.text_label.pack(pady=5)
        self.text_widget = Text(root, height=10, width=80, font=("Arial", 12), wrap="word", relief="solid", bd=1, fg="#333", bg="#fff")
        self.text_widget.pack(pady=15)

        # Save Button
        self.save_button = Button(root, text="Save Extracted Text", command=self.save_text, font=("Arial", 12, "bold"), fg="white", bg="#28a745", width=20, relief="flat")
        self.save_button.pack(pady=15)

    def start_timer(self):
        """Start the timer to take a screenshot after the specified time."""
        try:
            delay = int(self.timer_entry.get())
            if delay < 0:
                raise ValueError("Time cannot be negative.")
            messagebox.showinfo("Timer Started", f"Screenshot will be taken in {delay} seconds.")
            threading.Thread(target=self.capture_screenshot_after_delay, args=(delay,)).start()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the timer.")

    def capture_screenshot_after_delay(self, delay):
        """Wait for the delay and capture a screenshot."""
        time.sleep(delay)
        self.screenshot_path = "screenshot.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(self.screenshot_path)

        # Display the screenshot on the canvas
        img = Image.open(self.screenshot_path)
        img.thumbnail((600, 500))  # Resize for display
        img_tk = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.image = img_tk  # Keep a reference to avoid garbage collection

        self.extract_text()

    def extract_text(self):
        """Extract text from the screenshot and display it."""
        try:
            if self.screenshot_path and os.path.exists(self.screenshot_path):
                # Use Tesseract to extract text
                text = pytesseract.image_to_string(Image.open(self.screenshot_path))
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", text)
            else:
                messagebox.showerror("Error", "No screenshot available for text extraction.")
        except Exception as e:
            messagebox.showerror("Error", f"Error extracting text: {e}")

        # Optionally, clean up the screenshot file
        if os.path.exists(self.screenshot_path):
            os.remove(self.screenshot_path)
            self.screenshot_path = None

    def save_text(self):
        """Open a file dialog to save the extracted text to a .txt file."""
        try:
            # Get the text from the text widget
            extracted_text = self.text_widget.get("1.0", "end-1c")  # Remove trailing newline

            if not extracted_text:
                messagebox.showerror("Error", "No text to save.")
                return

            # Open a file dialog to select the save location
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

            if file_path:  # If the user selected a file location
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(extracted_text)
                messagebox.showinfo("Success", f"Text saved successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving text: {e}")


if __name__ == "__main__":
    # Create the GUI window
    root = Tk()
    app = ScreenshotTextExtractor(root)
    root.mainloop()
