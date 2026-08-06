import sys
import os
import json
import threading
import webbrowser
import customtkinter as ctk
from PIL import Image, ImageTk
from detector import InstalockDetector

# Visual Palette: Dark Slate (#0F1923), Crimson Accent (#FF4655), Off-White (#ECE8E1), Card Background (#1F2326)
COLOR_BG_DARK = "#0F1923"
COLOR_CRIMSON = "#FF4655"
COLOR_TEXT_WHITE = "#ECE8E1"
COLOR_CARD_GRAY = "#1F2326"
COLOR_CYAN_LOCKED = "#00F0FF"
COLOR_YELLOW_SEARCH = "#FFD700"
COLOR_TEXT_SUBTLE = "#8B9B9E"

class ValorantInstalockerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize core detector instance
        self.detector = InstalockDetector(status_callback=self.on_status_change)
        self.selected_agent = "Jett"

        # Window configuration
        self.title("VALORANT // TACTICAL INSTALOCKER")
        self.geometry("540x700")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_DARK)

        ctk.set_appearance_mode("dark")

        # Build GUI Layout
        self._create_header()
        self._create_status_card()
        self._create_agent_selection_card()
        self._create_action_controls()
        self._create_footer()

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="VALORANT // INSTALOCKER",
            font=ctk.CTkFont(family="Impact", size=28, weight="bold"),
            text_color=COLOR_CRIMSON
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="HIGH-PRECISION MSS DETECTION • DIRECTINPUT AUTOMATION",
            font=ctk.CTkFont(family="Consolas", size=10, weight="normal"),
            text_color=COLOR_TEXT_SUBTLE
        )
        subtitle_label.pack(anchor="w")

    def _create_status_card(self):
        status_card = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_GRAY,
            corner_radius=8,
            border_width=1,
            border_color="#2A2F33"
        )
        status_card.pack(fill="x", padx=25, pady=10)

        status_header = ctk.CTkLabel(
            status_card,
            text="SYSTEM STATUS",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color=COLOR_TEXT_SUBTLE
        )
        status_header.pack(anchor="w", padx=15, pady=(10, 2))

        self.status_badge = ctk.CTkLabel(
            status_card,
            text="[IDLE] Ready to launch",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=COLOR_TEXT_SUBTLE
        )
        self.status_badge.pack(anchor="w", padx=15, pady=(0, 12))

    def _create_agent_selection_card(self):
        section_title = ctk.CTkLabel(
            self,
            text="// TARGET AGENT SELECT",
            font=ctk.CTkFont(family="Impact", size=14),
            text_color=COLOR_TEXT_WHITE
        )
        section_title.pack(anchor="w", padx=25, pady=(12, 6))

        # Agent Scrollable Card Grid
        self.grid_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLOR_CARD_GRAY,
            corner_radius=8,
            scrollbar_button_color=COLOR_CRIMSON,
            scrollbar_button_hover_color="#D13644"
        )
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
                hover_color=COLOR_CRIMSON,
                text_color=COLOR_TEXT_WHITE,
                border_width=2,
                border_color=COLOR_CRIMSON if agent == self.selected_agent else "#2A2F33",
                corner_radius=6,
                height=42,
                command=lambda a=agent: self.select_agent(a)
            )
            btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
            self.agent_buttons[agent] = btn

        for i in range(cols):
            self.grid_frame.columnconfigure(i, weight=1)

    def _create_action_controls(self):
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=25, pady=15)

        self.start_btn = ctk.CTkButton(
            action_frame,
            text="START INSTALOCK [F8 TO STOP]",
            font=ctk.CTkFont(family="Impact", size=17),
            fg_color=COLOR_CRIMSON,
            hover_color="#D13644",
            text_color=COLOR_TEXT_WHITE,
            height=48,
            corner_radius=6,
            command=self.toggle_instalock
        )
        self.start_btn.pack(fill="x")

    def _create_footer(self):
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=25, pady=(0, 15))

        # Hotkey / Resolution notice
        hotkey_notice = ctk.CTkLabel(
            footer_frame,
            text="Press F8 to Abort • 1920x1080 Native",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#5D6C6F"
        )
        hotkey_notice.pack(side="left")

        # Clickable Developer Credit Link
        footer_link = ctk.CTkLabel(
            footer_frame,
            text="Developer: Ayush-3plus4",
            font=ctk.CTkFont(family="Consolas", size=11, underline=True, weight="bold"),
            text_color=COLOR_CRIMSON,
            cursor="hand2"
        )
        footer_link.pack(side="right")
        footer_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Ayush-3plus4"))

    def select_agent(self, agent_name):
        self.selected_agent = agent_name
        self.detector.set_agent(agent_name)
        for name, btn in self.agent_buttons.items():
            if name == agent_name:
                btn.configure(border_color=COLOR_CRIMSON, fg_color="#26191B")
            else:
                btn.configure(border_color="#2A2F33", fg_color="#181B1E")

    def toggle_instalock(self):
        if not self.detector.running:
            self.detector.start_instalock()
            self.start_btn.configure(text="STOP SEARCHING [F8]", fg_color="#5A6266", hover_color="#454B4E")
        else:
            self.detector.stop_instalock()
            self.start_btn.configure(text="START INSTALOCK [F8 TO STOP]", fg_color=COLOR_CRIMSON, hover_color="#D13644")

    def on_status_change(self, state, message=""):
        if state == "IDLE":
            self.status_badge.configure(text=f"[IDLE] {message}", text_color=COLOR_TEXT_SUBTLE)
            self.start_btn.configure(text="START INSTALOCK [F8 TO STOP]", fg_color=COLOR_CRIMSON, hover_color="#D13644")
        elif state == "SEARCHING":
            self.status_badge.configure(text=f"[SEARCHING...] {message}", text_color=COLOR_YELLOW_SEARCH)
        elif state == "LOCKED":
            self.status_badge.configure(text=f"[LOCKED] {message}", text_color=COLOR_CYAN_LOCKED)
            self.start_btn.configure(text="START INSTALOCK [F8 TO STOP]", fg_color=COLOR_CRIMSON, hover_color="#D13644")

def main():
    app = ValorantInstalockerGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
