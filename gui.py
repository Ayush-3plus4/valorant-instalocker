import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk

# Palette Setup: Dark Slate (#0F1923), Crimson Accent (#FF4655), Off-White (#ECE8E1), Card Gray (#1F2326)
BG_DARK = "#0F1923"
CRIMSON = "#FF4655"
TEXT_WHITE = "#ECE8E1"
CARD_GRAY = "#1F2326"
CYAN_LOCKED = "#00F0FF"
YELLOW_SEARCH = "#FFD700"

class ValorantHUDGUI(ctk.CTk):
    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        self.detector.status_callback = self.on_status_change
        self.selected_agent = "Jett"

        self.title("VALORANT // TACTICAL INSTALOCKER")
        self.geometry("520x680")
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)

        ctk.set_appearance_mode("dark")

        self.build_ui()

    def build_ui(self):
        # Header Container
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="VALORANT // INSTALOCKER",
            font=ctk.CTkFont(family="Impact", size=26, weight="bold"),
            text_color=CRIMSON
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="ULTRA-FAST MSS DETECTION ENGINE • SYSTEM READY",
            font=ctk.CTkFont(family="Consolas", size=10, weight="normal"),
            text_color="#8B9B9E"
        )
        subtitle_label.pack(anchor="w")

        # Status Badge Frame
        status_card = ctk.CTkFrame(self, fg_color=CARD_GRAY, corner_radius=8, border_width=1, border_color="#2A2F33")
        status_card.pack(fill="x", padx=25, pady=10)

        status_header = ctk.CTkLabel(
            status_card,
            text="STATUS OVERRIDE",
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color="#8B9B9E"
        )
        status_header.pack(anchor="w", padx=15, pady=(10, 0))

        self.status_badge = ctk.CTkLabel(
            status_card,
            text="[IDLE]",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color="#8B9B9E"
        )
        self.status_badge.pack(anchor="w", padx=15, pady=(0, 10))

        # Agent Grid Title
        grid_title = ctk.CTkLabel(
            self,
            text="// SELECT TARGET AGENT",
            font=ctk.CTkFont(family="Impact", size=14),
            text_color=TEXT_WHITE
        )
        grid_title.pack(anchor="w", padx=25, pady=(15, 5))

        # Agent Grid Frame (Scrollable)
        self.grid_frame = ctk.CTkScrollableFrame(self, fg_color=CARD_GRAY, corner_radius=8, scrollbar_button_color=CRIMSON, scrollbar_button_hover_color="#D13644")
        self.grid_frame.pack(fill="both", expand=True, padx=25, pady=5)

        agents = [
            "Astra", "Breach", "Brimstone", "Chamber", "Clove", "Cypher",
            "Deadlock", "Fade", "Gekko", "Harbor", "Iso", "Jett",
            "Kayo", "Killjoy", "Neon", "Omen", "Phoenix", "Raze",
            "Reyna", "Sage", "Skye", "Sova", "Viper", "Vyse",
            "Waylay", "Yoru"
        ]
        self.agent_buttons = {}

        cols = 4
        for idx, agent in enumerate(agents):
            r = idx // cols
            c = idx % cols
            btn = ctk.CTkButton(
                self.grid_frame,
                text=agent.upper(),
                font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                fg_color="#181B1E",
                hover_color=CRIMSON,
                text_color=TEXT_WHITE,
                border_width=2,
                border_color=CRIMSON if agent == self.selected_agent else "#2A2F33",
                corner_radius=6,
                height=45,
                command=lambda a=agent: self.select_agent(a)
            )
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            self.agent_buttons[agent] = btn

        for i in range(cols):
            self.grid_frame.columnconfigure(i, weight=1)


        # Action Button Frame
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=25, pady=15)

        self.start_btn = ctk.CTkButton(
            action_frame,
            text="ACTIVATE LOCK-IN [F8 ABORT]",
            font=ctk.CTkFont(family="Impact", size=16),
            fg_color=CRIMSON,
            hover_color="#D13644",
            text_color=TEXT_WHITE,
            height=45,
            corner_radius=6,
            command=self.toggle_lock
        )
        self.start_btn.pack(fill="x")

        # Footer Attribution Frame
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=25, pady=(0, 15))

        footer_link = ctk.CTkLabel(
            footer_frame,
            text="Developer: Ayush-3plus4",
            font=ctk.CTkFont(family="Consolas", size=11, underline=True),
            text_color=CRIMSON,
            cursor="hand2"
        )
        footer_link.pack(side="right")
        footer_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Ayush-3plus4"))

        hotkey_notice = ctk.CTkLabel(
            footer_frame,
            text="Press F8 to Abort • 1920x1080 Native",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#5D6C6F"
        )
        hotkey_notice.pack(side="left")

    def select_agent(self, agent):
        self.selected_agent = agent
        self.detector.set_agent(agent)
        for name, btn in self.agent_buttons.items():
            if name == agent:
                btn.configure(border_color=CRIMSON, fg_color="#26191B")
            else:
                btn.configure(border_color="#2A2F33", fg_color="#181B1E")

    def toggle_lock(self):
        if not self.detector.running:
            self.detector.start_instalock()
            self.start_btn.configure(text="STOP SEARCHING", fg_color="#5A6266", hover_color="#454B4E")
        else:
            self.detector.stop_instalock()
            self.start_btn.configure(text="ACTIVATE LOCK-IN [F8 ABORT]", fg_color=CRIMSON, hover_color="#D13644")

    def on_status_change(self, state, message=""):
        if state == "IDLE":
            self.status_badge.configure(text=f"[IDLE] {message}", text_color="#8B9B9E")
            self.start_btn.configure(text="ACTIVATE LOCK-IN [F8 ABORT]", fg_color=CRIMSON, hover_color="#D13644")
        elif state == "SEARCHING":
            self.status_badge.configure(text=f"[SEARCHING...] {message}", text_color=YELLOW_SEARCH)
        elif state == "LOCKED":
            self.status_badge.configure(text=f"[LOCKED] {message}", text_color=CYAN_LOCKED)
            self.start_btn.configure(text="ACTIVATE LOCK-IN [F8 ABORT]", fg_color=CRIMSON, hover_color="#D13644")
