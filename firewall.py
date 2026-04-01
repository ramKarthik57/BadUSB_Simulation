import keyboard
import tkinter as tk
import datetime


# ============================================================
# CONFIG MODULE
# ============================================================

class Config:

    WINDOW_WIDTH = 340
    WINDOW_HEIGHT = 240

    COLOR_BG = "#1e1e1e"
    COLOR_TEXT = "white"
    COLOR_GREEN = "#00ff88"
    COLOR_RED = "#ff4d4d"
    COLOR_BUTTON = "#333333"

    TITLE = "KEYSTROKE FIREWALL"
    FOOTER = "BadUSB Protection Module"

    FONT_TITLE = ("Segoe UI", 14, "bold")
    FONT_STATUS = ("Segoe UI", 16, "bold")
    FONT_BUTTON = ("Segoe UI", 11, "bold")
    FONT_FOOTER = ("Segoe UI", 8)


# ============================================================
# LOGGER MODULE
# ============================================================

class Logger:

    def __init__(self):

        self.enabled = True

    def log(self, message):

        if not self.enabled:
            return

        time = datetime.datetime.now().strftime("%H:%M:%S")

        print(f"[{time}] {message}")

    def info(self, message):

        self.log("[INFO] " + message)

    def warn(self, message):

        self.log("[WARN] " + message)

    def error(self, message):

        self.log("[ERROR] " + message)


logger = Logger()


# ============================================================
# FIREWALL MODULE
# ============================================================

class Firewall:

    def __init__(self):

        self.enabled = False
        self.hook = None

        logger.info("Firewall initialized")

    # ----------------------------------------

    def blocker(self, event):

        return False

    # ----------------------------------------

    def install_hook(self):

        if self.hook is None:

            logger.info("Installing hook")

            self.hook = keyboard.hook(
                self.blocker,
                suppress=True
            )

    # ----------------------------------------

    def remove_hook(self):

        if self.hook is not None:

            logger.info("Removing hook")

            keyboard.unhook(self.hook)

            self.hook = None

    # ----------------------------------------

    def enable(self):

        logger.info("Enable firewall")

        self.enabled = True

        self.install_hook()

    # ----------------------------------------

    def disable(self):

        logger.info("Disable firewall")

        self.enabled = False

        self.remove_hook()

    # ----------------------------------------

    def toggle(self):

        logger.info("Toggle firewall")

        if self.enabled:

            self.disable()

        else:

            self.enable()

    # ----------------------------------------

    def is_enabled(self):

        return self.enabled


# ============================================================
# UI MODULE
# ============================================================

class UI:

    def __init__(self, firewall):

        self.firewall = firewall

        self.root = None

        self.status_var = None
        self.status_label = None

        logger.info("UI created")

    # ----------------------------------------

    def create_window(self):

        self.root = tk.Tk()

        self.root.title("Keystroke Firewall")

        self.root.geometry(
            str(Config.WINDOW_WIDTH)
            + "x"
            + str(Config.WINDOW_HEIGHT)
        )

        self.root.configure(bg=Config.COLOR_BG)

        self.root.resizable(False, False)

    # ----------------------------------------

    def create_title(self):

        title = tk.Label(

            self.root,

            text=Config.TITLE,

            font=Config.FONT_TITLE,

            fg=Config.COLOR_TEXT,

            bg=Config.COLOR_BG

        )

        title.pack(pady=(15, 5))

    # ----------------------------------------

    def create_status(self):

        self.status_var = tk.StringVar()

        self.status_var.set("ALLOW")

        self.status_label = tk.Label(

            self.root,

            textvariable=self.status_var,

            font=Config.FONT_STATUS,

            fg=Config.COLOR_GREEN,

            bg=Config.COLOR_BG

        )

        self.status_label.pack(pady=10)

    # ----------------------------------------

    def create_button(self):

        btn = tk.Button(

            self.root,

            text="TOGGLE",

            command=self.on_toggle,

            font=Config.FONT_BUTTON,

            bg=Config.COLOR_BUTTON,

            fg="white",

            activebackground="#555555",

            activeforeground="white",

            width=15,

            height=1,

            bd=0

        )

        btn.pack(pady=10)

    # ----------------------------------------

    def create_footer(self):

        footer = tk.Label(

            self.root,

            text=Config.FOOTER,

            font=Config.FONT_FOOTER,

            fg="#888888",

            bg=Config.COLOR_BG

        )

        footer.pack(side="bottom", pady=5)

    # ----------------------------------------

    def set_allow(self):

        self.status_var.set("ALLOW")

        self.status_label.config(
            fg=Config.COLOR_GREEN
        )

    # ----------------------------------------

    def set_block(self):

        self.status_var.set("BLOCKING")

        self.status_label.config(
            fg=Config.COLOR_RED
        )

    # ----------------------------------------

    def on_toggle(self):

        logger.info("Button pressed")

        self.firewall.toggle()

        if self.firewall.is_enabled():

            self.set_block()

        else:

            self.set_allow()

    # ----------------------------------------

    def build(self):

        self.create_window()

        self.create_title()

        self.create_status()

        self.create_button()

        self.create_footer()

    # ----------------------------------------

    def run(self):

        logger.info("UI started")

        self.root.mainloop()


# ============================================================
# APPLICATION MODULE
# ============================================================

class App:

    def __init__(self):

        logger.info("App starting")

        self.firewall = Firewall()

        self.ui = UI(self.firewall)

    # ----------------------------------------

    def setup(self):

        logger.info("Setup")

        self.ui.build()

    # ----------------------------------------

    def run(self):

        logger.info("Run")

        self.ui.run()


# ============================================================
# MAIN
# ============================================================

def main():

    logger.info("Main")

    app = App()

    app.setup()

    app.run()


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":

    main()