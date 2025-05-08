import tkinter as tk
import subprocess
import webbrowser
import os
import tkinter.messagebox
import datetime
from tkinter import colorchooser

def open_app(app_path):
    """Opens a specified application using subprocess."""
    try:
        subprocess.Popen(app_path)
        dev_print(settings, f"Opened app: {app_path}")
    except FileNotFoundError:
        dev_print(settings, f"Error: Application not found at {app_path}")
        print(f"Error: Application not found at {app_path}")
    except Exception as e:
        dev_print(settings, f"An error occurred: {e}")
        print(f"An error occurred: {e}")

def open_website(url):
    """Opens a specified website using the default web browser."""
    dev_print(settings, f"Opening website: {url}")
    webbrowser.open_new(url)

def create_button(master, text, command, **kwargs):
    """Creates a button with specified text and command."""
    button = tk.Button(master, text=text, command=command, **kwargs)
    return button

def open_start_menu():
    """Opens the Windows Start Menu."""
    try:
        subprocess.Popen("explorer shell:AppsFolder")
        dev_print(settings, "Opened Start Menu")
    except Exception as e:
        dev_print(settings, f"Could not open Start Menu: {e}")
        tk.messagebox.showerror("Error", f"Could not open Start Menu: {e}")

def open_run_dialog():
    """Opens the Windows Run dialog."""
    try:
        # Use os.startfile to open the Run dialog (works for 'explorer.exe')
        # But there is no official way to open Win+R Run dialog programmatically.
        # As a workaround, open explorer as a neutral action:
        subprocess.Popen("explorer")
        dev_print(settings, "Opened Run Dialog (workaround: opened Explorer)")
    except Exception as e:
        dev_print(settings, f"Could not open Run dialog: {e}")
        tk.messagebox.showerror("Error", f"Could not open Run dialog: {e}")

def close_window(window):
    """Closes the specified window."""
    dev_print(settings, "Window closed")
    window.destroy()

def load_username():
    """Load username from file if it exists, else return default."""
    try:
        with open("username.txt", "r", encoding="utf-8") as f:
            return f.read().strip() or "User"  # Changed default username to "User"
    except Exception:
        return "User"  # Changed default username to "User"

def save_username(name):
    """Save username to file."""
    try:
        with open("username.txt", "w", encoding="utf-8") as f:
            f.write(name)
    except Exception as e:
        print(f"Could not save username: {e}")

def load_settings():
    """Load settings from file if it exists, else return defaults."""
    settings = {"username": "User", "bgcolor": "skyblue", "devmode": "off"}  # Changed default username to "User"
    try:
        with open("settings.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    settings[key] = value
    except Exception:
        pass
    return settings

def save_settings(settings):
    """Save settings to file."""
    try:
        with open("settings.txt", "w", encoding="utf-8") as f:
            for k, v in settings.items():
                f.write(f"{k}={v}\n")
    except Exception as e:
        print(f"Could not save settings: {e}")

def dev_print(settings, *args, **kwargs):
    if settings.get("devmode", "off") == "on":
        print(*args, **kwargs)

def open_settings(window, greeting_label, name_label, settings, update_bgcolor):
    """Open a dialog to change the username and background color."""
    def pick_color():
        color_code = colorchooser.askcolor(title="Choose background color")[1]
        if color_code:
            settings["bgcolor"] = color_code
            update_bgcolor(settings["bgcolor"])
            dev_print(settings, f"Background color changed to {color_code}")
    def save_and_update():
        new_name = entry.get().strip()
        if new_name:
            settings["username"] = new_name
            dev_print(settings, f"Username changed to {new_name}")
        settings["devmode"] = "on" if devmode_var.get() else "off"
        save_settings(settings)
        update_greeting(greeting_label, name_label, settings["username"])
        dev_print(settings, f"Dev Mode set to {settings['devmode']}")
        settings_win.destroy()
    settings_win = tk.Toplevel(window)
    settings_win.title("Settings")
    settings_win.geometry("340x250")
    tk.Label(settings_win, text="Enter your name:").pack(pady=5)
    entry = tk.Entry(settings_win)
    entry.pack(pady=5)
    entry.insert(0, settings["username"])
    tk.Label(settings_win, text="Background color:").pack(pady=5)
    tk.Button(settings_win, text="Change background color", command=pick_color).pack(pady=2)
    devmode_var = tk.BooleanVar(value=(settings.get("devmode", "off") == "on"))
    devmode_check = tk.Checkbutton(settings_win, text="Dev Mode", variable=devmode_var)
    devmode_check.pack(pady=8)
    tk.Button(settings_win, text="Save", command=save_and_update).pack(pady=10)

def update_greeting(greeting_label, name_label, user_name):
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = f"Good morning "
    elif 12 <= hour < 18:
        greeting = f"Good afternoon "
    else:
        greeting = f"Good evening "
    greeting_label.config(text=greeting)
    name_label.config(text=user_name + "!")

if __name__ == "__main__":
    settings = load_settings()
    window = tk.Tk()
    window.title("App/Website Launcher")
    window.geometry("400x300")  # Set initial window size
    window.configure(bg=settings["bgcolor"])  # Set background color

    # Make window borderless and not appear on the taskbar
    window.overrideredirect(True)
    window.attributes("-toolwindow", True)  # Hint to not show in taskbar (Windows only)
    window.attributes("-topmost", True)     # Always on top

    # Center the window on the screen
    window.update_idletasks()
    w = 400
    h = 300
    # Place window in the bottom right corner
    x = window.winfo_screenwidth() - w - 10
    y = window.winfo_screenheight() - h - 50
    window.geometry(f"{w}x{h}+{x}+{y}")

    # --- Draggable window ---
    def start_move(event):
        window.x = event.x
        window.y = event.y

    def do_move(event):
        x = window.winfo_pointerx() - window.x
        y = window.winfo_pointery() - window.y
        window.geometry(f"+{x}+{y}")

    window.bind("<Button-1>", start_move)
    window.bind("<B1-Motion>", do_move)

    # Settings button in the top left
    def update_bgcolor(bg):
        window.configure(bg=bg)
        greeting_frame.configure(bg=bg)
        greeting_label.configure(bg=bg)
        name_label.configure(bg=bg)
        heading_label.configure(bg=bg)
        content_frame.configure(bg=bg)
        bottom_frame.configure(bg=bg)

    # Greeting
    user_name = settings["username"]
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = f"Good morning "
    elif 12 <= hour < 18:
        greeting = f"Good afternoon "
    else:
        greeting = f"Good evening "

    # Use two labels to bold the name
    greeting_frame = tk.Frame(window, bg=settings["bgcolor"])
    greeting_frame.pack(pady=(10, 0))
    greeting_label = tk.Label(greeting_frame, text=greeting, font=("Arial", 12), bg=settings["bgcolor"])
    greeting_label.pack(side=tk.LEFT)
    name_label = tk.Label(greeting_frame, text=user_name + "!", font=("Arial", 12, "bold"), bg=settings["bgcolor"])
    name_label.pack(side=tk.LEFT)

    settings_button = create_button(
        window,
        "Settings",
        command=lambda: open_settings(window, greeting_label, name_label, settings, update_bgcolor),
        width=10,
        height=1
    )
    settings_button.place(x=10, y=10)

    # Heading Label
    heading_label = tk.Label(window, text="Startup Launchpad", font=("Arial", 16), bg=settings["bgcolor"])
    heading_label.pack(pady=10)

    # Main content frame for all buttons except Finish
    content_frame = tk.Frame(window, bg=settings["bgcolor"])
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Example applications and websites
    apps = {
        "Notepad": "notepad.exe",
        "Calculator": "calc.exe",
    }
    websites = {
        "Bing": "https://www.bing.com",  # Changed label and URL to Bing
        "YouTube": "https://www.youtube.com",
    }

    # Remove "See More Apps" from the grid buttons
    buttons = []
    for app_name, app_path in apps.items():
        buttons.append(create_button(content_frame, f"Open {app_name}", lambda path=app_path: open_app(path)))
    for website_name, url in websites.items():
        buttons.append(create_button(content_frame, f"Open {website_name}", lambda u=url: open_website(u)))
    buttons.append(create_button(content_frame, "Open Start Menu", open_start_menu))
    buttons.append(create_button(content_frame, "Open Windows Explorer", open_run_dialog))

    # --- Extra row of buttons ---
    def open_edge():
        # Try to open Microsoft Edge
        try:
            subprocess.Popen("msedge")
        except FileNotFoundError:
            try:
                subprocess.Popen(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not open Microsoft Edge: {e}")

    def open_vscode():
        # Try to open Visual Studio Code
        try:
            subprocess.Popen("code")
        except FileNotFoundError:
            try:
                subprocess.Popen(r"C:\Program Files\Microsoft VS Code\Code.exe")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not open Visual Studio Code: {e}")

    def open_defender():
        # Open Windows Security (Defender)
        try:
            subprocess.Popen("windowsdefender:")
        except Exception:
            try:
                subprocess.Popen(["start", "windowsdefender:"], shell=True)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not open Windows Security: {e}")

    extra_buttons_frame = tk.Frame(window, bg=settings["bgcolor"])
    extra_buttons_frame.pack(pady=(0, 10))

    edge_btn = create_button(extra_buttons_frame, "Open Edge", open_edge, width=14, height=1)
    vscode_btn = create_button(extra_buttons_frame, "Open Visual Studio", open_vscode, width=14, height=1)
    defender_btn = create_button(extra_buttons_frame, "Open Defender", open_defender, width=14, height=1)

    edge_btn.grid(row=0, column=0, padx=8, pady=4, sticky="ew")
    vscode_btn.grid(row=0, column=1, padx=8, pady=4, sticky="ew")
    defender_btn.grid(row=0, column=2, padx=8, pady=4, sticky="ew")

    for col in range(3):
        extra_buttons_frame.grid_columnconfigure(col, weight=1)

    # Place buttons in a 3-column grid, centered
    for idx, btn in enumerate(buttons):
        row, col = divmod(idx, 3)
        btn.grid(row=row, column=col, padx=10, pady=8, sticky="ew")

    # --- Date and Time Display ---
    info_frame = tk.Frame(window, bg=settings["bgcolor"])
    info_frame.pack(pady=(0, 5))

    # Date
    date_label = tk.Label(
        info_frame,
        text=datetime.datetime.now().strftime("%A, %d %B %Y"),
        font=("Arial", 11),
        bg=settings["bgcolor"]
    )
    date_label.pack(side=tk.LEFT, padx=10)

    # Time (12-hour, updates every second)
    time_label = tk.Label(
        info_frame,
        font=("Arial", 11),
        bg=settings["bgcolor"]
    )
    time_label.pack(side=tk.LEFT, padx=10)

    def update_time():
        now = datetime.datetime.now()
        time_label.config(text=now.strftime("%I:%M:%S %p"))
        date_label.config(text=now.strftime("%A, %d %B %Y"))  # <-- update date as well
        time_label.after(1000, update_time)

    update_time()

    # Bottom frame for "See More Apps", "Close", and "Settings" buttons
    bottom_frame = tk.Frame(window, bg=settings["bgcolor"])
    bottom_frame.pack(pady=20, side=tk.BOTTOM)

    see_more_apps_button = create_button(
        bottom_frame,
        "See More Apps",
        command=open_start_menu,
        width=20,  # Increased width
        height=2
    )
    see_more_apps_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

    close_button = create_button(
        bottom_frame,
        "Close",
        command=lambda: close_window(window),
        width=20,  # Increased width
        height=2
    )
    close_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

    window.mainloop()