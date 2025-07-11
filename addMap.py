import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

# --- Style Guide ---
# Colors inspired by Minecraft's UI
COLOR_BACKGROUND = "#212121"  # A dark, stone-like background
COLOR_FRAME = "#3E3E3E"       # A slightly lighter frame color, like an inventory slot
COLOR_TEXT = "#FFFFFF"        # White text for high contrast
COLOR_BUTTON = "#7A7A7A"       # Standard button grey
COLOR_BUTTON_ACTIVE = "#696969" # Button color when pressed
COLOR_BUTTON_HOVER = "#8C8C8C"  # Button color on hover

# Font configuration
# Make sure you have installed the "Minecraftia" font on your system
FONT_NORMAL = ("Minecraftia", 14)
FONT_BOLD = ("Minecraftia", 16, "bold")


class MinecraftUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Basic Window Setup ---
        self.title("Minecraft Map Installer")
        self.geometry("600x450")

        # --- Load Background Image ---
        # Ensure 'background.jpg' is in the same directory
        self.bg_image_pil = Image.open("background.jpg")
        self.bg_image = ImageTk.PhotoImage(self.bg_image_pil)
        
        # Create a label to hold the background image
        # This label will be the base for all other widgets
        self.background_label = tk.Label(self, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Create Widgets ---
        self.create_widgets()

        # --- Language Setup (Example) ---
        self.languages = {
            "en": {"title": "Map Installer", "label_text": "Drag and Drop Map File Here:"},
            "pl": {"title": "Instalator Map", "label_text": "Przeciągnij i Upuść Plik Mapy Tutaj:"}
        }
        self.current_language = "en"
        
        # --- FIX: Populate UI on startup ---
        self.switch_language(self.current_language)

    def create_widgets(self):
        # A main frame to hold the content, giving it a semi-transparent look
        # by using a solid color that fits the theme.
        self.main_frame = tk.Frame(self, bg=COLOR_FRAME, bd=2, relief="solid")
        # Use .place() to position it over the background image
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=250)

        # --- Create Styled Widgets inside the frame ---
        # Main instruction label
        self.instruction_label = tk.Label(
            self.main_frame,
            text="",  # Text will be set by switch_language
            font=FONT_BOLD,
            bg=COLOR_FRAME,
            fg=COLOR_TEXT
        )
        self.instruction_label.pack(pady=(20, 10))

        # Drag-and-drop area (using a Label)
        self.dnd_area = tk.Label(
            self.main_frame,
            text="...",
            font=("Minecraftia", 24),
            bg=COLOR_BACKGROUND,
            fg=COLOR_BUTTON,
            relief="solid",
            bd=2,
            padx=20,
            pady=40
        )
        self.dnd_area.pack(pady=10, padx=20, fill="x")

        # Language selection buttons
        button_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        button_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        common_button_options = {
            "font": FONT_NORMAL,
            "bg": COLOR_BUTTON,
            "fg": COLOR_TEXT,
            "activebackground": COLOR_BUTTON_ACTIVE,
            "relief": "raised",
            "borderwidth": 2,
            "width": 5,
        }

        self.en_button = tk.Button(button_frame, text="EN", **common_button_options, command=lambda: self.switch_language("en"))
        self.en_button.pack(side="left", padx=5)
        
        self.pl_button = tk.Button(button_frame, text="PL", **common_button_options, command=lambda: self.switch_language("pl"))
        self.pl_button.pack(side="left")
        
    def switch_language(self, lang):
        self.current_language = lang
        lang_data = self.languages[self.current_language]
        
        # Update widget texts
        self.title(lang_data["title"])
        self.instruction_label.config(text=lang_data["label_text"])


# To run this example:
if __name__ == "__main__":
    app = MinecraftUI()
    app.mainloop()
