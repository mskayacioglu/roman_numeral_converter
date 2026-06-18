# gui.py
import tkinter as tk
import tkinter.font as tkfont
from converter import int_to_roman, roman_to_int


MAROON = "#7d0000"
GOLD = "#d4af37"
MAX_ROMAN_LENGTH = 15
MAX_DECIMAL_LENGTH = 4

def center_window(window, width=600, height=400):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

class RomanConverterApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=MAROON, padx=10, pady=10)
        self.master = master
        self.master.configure(bg=MAROON)

        # Fonts
        families = set(tkfont.families())
        preferred = (
            "Times New Roman"
            if "Times New Roman" in families
            else ("Times" if "Times" in families else None)
        )
        self.entry_font = (preferred or "Times New Roman", 14)
        self.label_font = (preferred or "Times New Roman", 14, "bold")

        # Vars & guards
        self.var_roman = tk.StringVar()
        self.var_decimal = tk.StringVar()
        self.var_status = tk.StringVar()
        self._updating_from = None
        self._normalizing_roman = False  # prevent recursive trace during uppercase normalize

        # Root grid stretch
        self.grid(sticky="nsew")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Container (all maroon)
        container = tk.Frame(self, bg=MAROON)
        container.grid(row=0, column=0, sticky="nsew")
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        # SPQR banner (top)
        self._build_spqr_banner(container)

        # Inputs block (center area, maroon)
        inputs = tk.Frame(container, bg=MAROON, padx=10, pady=10)
        inputs.grid(row=1, column=0, sticky="n")
        inputs.columnconfigure(1, weight=1)

        # Validation commands
        vcmd_roman = (self.register(self._validate_roman), "%P")
        vcmd_decimal = (self.register(self._validate_decimal), "%P")

        # Labels
        tk.Label(
            inputs, text="Roman:", font=self.label_font, fg=GOLD, bg=MAROON
        ).grid(row=0, column=0, padx=8, pady=8, sticky="e")

        tk.Label(
            inputs, text="Decimal:", font=self.label_font, fg=GOLD, bg=MAROON
        ).grid(row=1, column=0, padx=8, pady=8, sticky="e")

        # Entries (gold text, maroon bg, gold border)
        self.entry_roman = tk.Entry(
            inputs,
            textvariable=self.var_roman,
            width=20,
            font=self.entry_font,
            validate="key",
            validatecommand=vcmd_roman,
            fg=GOLD,
            bg=MAROON,
            insertbackground=GOLD,       
            highlightthickness=2,        
            highlightbackground=GOLD,    
            highlightcolor=GOLD,         
        )
        self.entry_roman.grid(row=0, column=1, pady=8)

        self.entry_decimal = tk.Entry(
            inputs,
            textvariable=self.var_decimal,
            width=20,
            font=self.entry_font,
            validate="key",
            validatecommand=vcmd_decimal,
            fg=GOLD,
            bg=MAROON,
            insertbackground=GOLD,
            highlightthickness=2,
            highlightbackground=GOLD,
            highlightcolor=GOLD,
        )
        self.entry_decimal.grid(row=1, column=1, pady=8)

        self.status_label = tk.Label(
            inputs,
            textvariable=self.var_status,
            font=self.entry_font,
            fg=GOLD,
            bg=MAROON,
            wraplength=360,
        )
        self.status_label.grid(
            row=2, column=0, columnspan=2, padx=8, pady=(8, 0)
        )

        # Traces
        self.var_roman.trace_add("write", self._on_roman_change)
        self.var_decimal.trace_add("write", self._on_decimal_change)

        self.entry_roman.focus_set()

    # -------------------------
    # Validation
    # -------------------------
    def _validate_roman(self, proposed: str) -> bool:
        # Only allow I,V,X,L,C,D,M (upper/lower). Uppercasing is done in trace.
        return len(proposed) <= MAX_ROMAN_LENGTH and all(
            ch in "IVXLCDMivxlcdm" for ch in proposed
        )

    def _validate_decimal(self, proposed: str) -> bool:
        # str.isdigit() also accepts characters such as ²; accept ASCII digits only.
        return len(proposed) <= MAX_DECIMAL_LENGTH and all(
            ch in "0123456789" for ch in proposed
        )

    # -------------------------
    # Banner
    # -------------------------
    def _build_spqr_banner(self, parent):
        canvas = tk.Canvas(parent, height=120, bg=MAROON, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        parent.columnconfigure(0, weight=1)

        def redraw(_event=None):
            canvas.delete("all")
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            margin = 10

            # Flag rectangle
            canvas.create_rectangle(
                margin, margin, w - margin, h - margin,
                fill=MAROON, outline=GOLD, width=4
            )

            # SPQR text
            font_size = max(16, int(h * 0.5))
            canvas.create_text(
                w // 2, h // 2,
                text="SPQR",
                fill=GOLD,
                font=("Times New Roman", font_size, "bold"),
            )

        canvas.bind("<Configure>", redraw)
        redraw()

    # -------------------------
    # Event handlers
    # -------------------------
    def _on_roman_change(self, *_):
        if self._updating_from == "decimal":
            return
        if self._normalizing_roman:
            return

        text = self.var_roman.get()
        if text == "":
            self._set_decimal("")
            self._set_status("")
            return
        
        # Normalize to uppercase without moving the cursor
        upper = text.upper()
        if text != upper:
            try:
                idx = self.entry_roman.index("insert")
            except Exception:
                idx = None
            self._normalizing_roman = True
            self.var_roman.set(upper)
            self._normalizing_roman = False
            if idx is not None:
                self.entry_roman.icursor(idx)

        # Convert or warn
        try:
            value = roman_to_int(upper)
            self._set_decimal(str(value))
            self._set_status("")
        except ValueError:
            self._set_decimal("")
            self._set_status("Invalid Roman numeral")

    def _on_decimal_change(self, *_):
        if self._updating_from == "roman":
            return
        s = self.var_decimal.get().strip()
        if not s:
            self._set_roman("")
            self._set_status("")
            return
        
        try:
            n = int(s)
            self._set_roman(int_to_roman(n))
            self._set_status("")
        except ValueError:
            self._set_roman("")
            self._set_status("Decimal value must be between 1 and 3999")


    # -------------------------
    # Helpers
    # -------------------------
    def _set_roman(self, val: str):
        self._updating_from = "decimal"
        try:
            self.var_roman.set(val)
        finally:
            self._updating_from = None

    def _set_decimal(self, val: str):
        self._updating_from = "roman"
        try:
            self.var_decimal.set(val)
        finally:
            self._updating_from = None

    def _set_status(self, val: str):
        self.var_status.set(val)
