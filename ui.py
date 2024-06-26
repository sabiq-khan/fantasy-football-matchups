#!/usr/bin/env python3
import tkinter as tk
from tkinter import scrolledtext
from typing import List
from matchups import MatchupCreator
from tkinter import messagebox
from tkinter import ttk


class MatchupUi:
    def clear(self):
        self.window.destroy()
        self.window: tk.Tk = self.create_ui()
        self.window.mainloop()

    def create_matchups(self):
        west_division: List[str] = self.west_division_input.get(
            "1.0", tk.END).strip().split('\n')
        east_division: List[str] = self.east_division_input.get(
            "1.0", tk.END).strip().split('\n')
        south_division: List[str] = self.south_division_input.get(
            "1.0", tk.END).strip().split('\n')
        intradivisional_weeks: List[int] = [int(
            week) for week in self.divisional_week_input.get("1.0", tk.END).strip().split('\n')]
        interdivisional_weeks: List[int] = [int(
            week) for week in self.nondivisional_week_input.get("1.0", tk.END).strip().split('\n')]
        playoff_weeks: List[int] = [int(week) for week in self.playoff_week_input.get(
            "1.0", tk.END).strip().split('\n')]

        matchup_creator: MatchupCreator = MatchupCreator(
            west_division=west_division,
            east_division=east_division,
            south_division=south_division,
            interdivisional_weeks=interdivisional_weeks,
            intradivisional_weeks=intradivisional_weeks,
            playoff_weeks=playoff_weeks
        )
        matchup_creator.create_all_seasonal_matchups()
        matchup_creator.write_matchups_to_csv()

        messagebox.showinfo("Success", "Created matchups in matchups.csv.")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_ui(self):
        window = tk.Tk()
        window.title("Fantasy Football Matchups")
        window.geometry("1000x1700")
        window.tk.call("tk", "scaling", 1.5)

        # Create canvas
        self.canvas = tk.Canvas(window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Add scrollbar to the canvas
        # Create and configure a custom style for the scrollbar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Vertical.TScrollbar", width=20, arrowsize=20, borderwidth=3)
        self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview, style="Vertical.TScrollbar", cursor="hand1")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create main frame inside the canvas
        self.frame = tk.Frame(self.canvas)

        # Add the frame to the canvas
        self.canvas.create_window((170, 0), window=self.frame, anchor="nw")
        # Configure the canvas scrolling
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.label = tk.Label(
            self.frame, text="Fantasy Football Matchups", font=("Arial", 14))
        self.label.pack(pady=20)

        # West division input
        tk.Label(self.frame, text="Enter west division teams (one per line):").pack(
            pady=(10, 0))
        self.west_division_input = scrolledtext.ScrolledText(
            self.frame, width=40, height=5)
        self.west_division_input.pack(pady=(0, 10))

        # East division input
        tk.Label(self.frame, text="Enter east division teams (one per line):").pack(
            pady=(10, 0))
        self.east_division_input = scrolledtext.ScrolledText(
            self.frame, width=40, height=5)
        self.east_division_input.pack(pady=(0, 10))

        # South division input
        tk.Label(self.frame, text="Enter south division teams (one per line):").pack(
            pady=(10, 0))
        self.south_division_input = scrolledtext.ScrolledText(
            self.frame, width=40, height=5)
        self.south_division_input.pack(pady=(0, 10))

        # Non-divisional weeks input
        tk.Label(
            self.frame, text="Enter non-divisional weeks (one per line):").pack(pady=(10, 0))
        self.nondivisional_week_input = scrolledtext.ScrolledText(
            self.frame, width=40, height=5)
        self.nondivisional_week_input.pack(pady=(0, 10))

        # Divisional weeks input
        tk.Label(self.frame, text="Enter divisional weeks (one per line):").pack(
            pady=(10, 0))
        self.divisional_week_input = scrolledtext.ScrolledText(
            self.frame, width=40, height=5)
        self.divisional_week_input.pack(pady=(0, 10))

        # Playoff weeks input
        tk.Label(self.frame, text="Enter playoff weeks (one per line):").pack(
            pady=(10, 0))
        self.playoff_week_input = scrolledtext.ScrolledText(
            self.frame, width=40, height=5)
        self.playoff_week_input.pack(pady=(0, 10))

        # Button for creating matchups
        button = tk.Button(self.frame, text="Create matchups",
                           command=lambda: self.create_matchups())
        button.pack(pady=10)

        # Button for clearing the window
        button = tk.Button(self.frame, text="Clear",
                           command=lambda: self.clear())
        button.pack(pady=10)

        return window

    def __init__(self):
        self.window = self.create_ui()
        self.window.mainloop()


def main():
    matchup_ui: MatchupUi = MatchupUi()


if __name__ == "__main__":
    main()
