
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from pathlib import Path
from datetime import datetime
import random

# ─────────────────────────────────────────────
# NOVA PLANNER
# ─────────────────────────────────────────────

APP = Path.home() / "nova_planner"
APP.mkdir(exist_ok=True)
DB = APP / "nova.db"

BG = "#0B0D17"
PANEL = "#141827"
CARD = "#1B2032"
PURPLE = "#8B5CF6"
TEXT = "#F4F5FF"
MUTED = "#929AB5"
GREEN = "#34D399"
BLUE = "#60A5FA"


class NovaPlanner:

    def __init__(self, root):
        self.root = root
        self.root.title("NOVA Planner")
        self.root.geometry("1250x800")
        self.root.minsize(1000, 650)
        self.root.configure(bg=BG)

        self.db = sqlite3.connect(DB)
        self.setup_database()

        self.style()
        self.build_shell()
        self.dashboard()

        self.root.bind("<Control-n>", lambda e: self.add_task())
        self.root.bind("<Control-q>", lambda e: self.root.destroy())

    # ─────────────────────────────────────────
    # DATABASE
    # ─────────────────────────────────────────

    def setup_database(self):
        c = self.db.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            title TEXT,
            priority TEXT,
            completed INTEGER DEFAULT 0,
            created TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            id INTEGER PRIMARY KEY,
            title TEXT,
            completed INTEGER DEFAULT 0
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS moods(
            id INTEGER PRIMARY KEY,
            mood TEXT,
            date TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS achievements(
            name TEXT PRIMARY KEY,
            unlocked INTEGER DEFAULT 0
        )
        """)

        for name in [
            "First Task",
            "Task Master",
            "Focus Starter",
            "Habit Builder",
            "Mood Explorer"
        ]:
            c.execute(
                "INSERT OR IGNORE INTO achievements(name) VALUES(?)",
                (name,)
            )

        self.db.commit()

    # ─────────────────────────────────────────
    # STYLING
    # ─────────────────────────────────────────

    def style(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            rowheight=36,
            borderwidth=0
        )

        s.configure(
            "Treeview.Heading",
            background=PANEL,
            foreground=MUTED,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )

        s.map(
            "Treeview",
            background=[("selected", PURPLE)],
            foreground=[("selected", "white")]
        )

    # ─────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────

    def label(self, parent, text, size=11, color=TEXT, bold=False):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal")
        )

    def card(self, parent, bg=CARD):
        return tk.Frame(
            parent,
            bg=bg,
            highlightbackground="#252B40",
            highlightthickness=1,
            bd=0
        )

    def button(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=PURPLE if primary else CARD,
            fg="white",
            activebackground="#7044D6",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ─────────────────────────────────────────
    # MAIN LAYOUT
    # ─────────────────────────────────────────

    def build_shell(self):
        self.sidebar = tk.Frame(self.root, bg=PANEL, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="✦ NOVA",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", padx=25, pady=(30, 5))

        self.label(
            self.sidebar,
            "YOUR PERSONAL WORKSPACE",
            8,
            MUTED
        ).pack(anchor="w", padx=27, pady=(0, 35))

        nav = [
            ("⌂   Dashboard", self.dashboard),
            ("✓   Tasks", self.tasks_page),
            ("◉   Habits", self.habits_page),
            ("♡   Mood", self.mood_page),
            ("◆   Achievements", self.achievement_page),
            ("⚙   Settings", self.settings_page)
        ]

        for text, command in nav:
            tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg=PANEL,
                fg=TEXT,
                activebackground=CARD,
                activeforeground=TEXT,
                anchor="w",
                relief="flat",
                bd=0,
                padx=25,
                pady=15,
                cursor="hand2",
                font=("Segoe UI", 11)
            ).pack(fill="x")

        self.label(
            self.sidebar,
            "NOVA • PERSONAL EDITION",
            9,
            MUTED
        ).pack(side="bottom", pady=20)

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="right", fill="both", expand=True)

        self.header = tk.Frame(self.main, bg=BG)
        self.header.pack(fill="x", padx=35, pady=(25, 10))

        self.clock = tk.Label(
            self.header,
            text=datetime.now().strftime("%A, %d %B %Y"),
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        )
        self.clock.pack(side="left")

        self.button(
            self.header,
            "+ New task",
            self.add_task,
            True
        ).pack(side="right")

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

    # ─────────────────────────────────────────
    # DASHBOARD
    # ─────────────────────────────────────────

    def dashboard(self):
        self.clear_content()

        self.label(
            self.content,
            "Your space. Your progress.",
            26,
            TEXT,
            True
        ).pack(anchor="w")

        self.label(
            self.content,
            "A fresh start begins with one small step.",
            11,
            MUTED
        ).pack(anchor="w", pady=(5, 25))

        welcome = self.card(self.content)
        welcome.pack(fill="x", pady=(0, 20))

        tk.Label(
            welcome,
            text="WELCOME TO NOVA ✦",
            bg=CARD,
            fg=PURPLE,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 8))

        tk.Label(
            welcome,
            text=random.choice([
                "Small steps create big progress.",
                "You don't need to be perfect. Just begin.",
                "Your future is built one day at a time.",
                "Make today a little better than yesterday."
            ]),
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 17, "bold"),
            wraplength=700,
            justify="left"
        ).pack(anchor="w", padx=25)

        self.button(
            welcome,
            "Create your first task →",
            self.add_task,
            True
        ).pack(anchor="w", padx=25, pady=25)

        # Statistics
        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", pady=(0, 20))

        total = self.db.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]

        completed = self.db.execute(
            "SELECT COUNT(*) FROM tasks WHERE completed=1"
        ).fetchone()[0]

        habits = self.db.execute(
            "SELECT COUNT(*) FROM habits"
        ).fetchone()[0]

        self.stat_card(stats, "TOTAL TASKS", total, PURPLE)
        self.stat_card(stats, "COMPLETED", completed, GREEN)
        self.stat_card(stats, "YOUR HABITS", habits, BLUE)

        # Quick actions
        self.label(
            self.content,
            "QUICK ACTIONS",
            12,
            TEXT,
            True
        ).pack(anchor="w", pady=(10, 12))

        actions = tk.Frame(self.content, bg=BG)
        actions.pack(fill="x")

        self.button(
            actions, "＋  Add task", self.add_task
        ).pack(side="left", padx=(0, 10))

        self.button(
            actions, "◉  Add habit", self.add_habit
        ).pack(side="left", padx=10)

        self.button(
            actions, "♡  Check in", self.mood_page
        ).pack(side="left", padx=10)

        self.button(
            actions, "⏱  Focus session", self.focus
        ).pack(side="left", padx=10)

        # Today's tasks
        self.label(
            self.content,
            "YOUR TASKS",
            12,
            TEXT,
            True
        ).pack(anchor="w", pady=(25, 10))

        self.show_tasks(self.content, limit=5)

    def stat_card(self, parent, title, value, color):
        c = self.card(parent)
        c.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            c,
            text=title,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 5))

        tk.Label(
            c,
            text=str(value),
            bg=CARD,
            fg=color,
            font=("Segoe UI", 26, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 18))

    # ─────────────────────────────────────────
    # TASKS
    # ─────────────────────────────────────────

    def add_task(self):
        title = simpledialog.askstring(
            "New task",
            "What would you like to accomplish?",
            parent=self.root
        )

        if not title or not title.strip():
            return

        priority = simpledialog.askstring(
            "Priority",
            "Priority: Low, Medium or High",
            initialvalue="Medium",
            parent=self.root
        )

        priority = priority or "Medium"

        self.db.execute(
            "INSERT INTO tasks(title,priority,created) VALUES(?,?,?)",
            (
                title.strip(),
                priority.title(),
                datetime.now().strftime("%Y-%m-%d")
            )
        )

        self.db.commit()

        self.unlock("First Task")
        self.dashboard()

    def complete_task(self, task_id):
        self.db.execute(
            "UPDATE tasks SET completed=1 WHERE id=?",
            (task_id,)
        )

        self.db.commit()

        completed = self.db.execute(
            "SELECT COUNT(*) FROM tasks WHERE completed=1"
        ).fetchone()[0]

        if completed >= 5:
            self.unlock("Task Master")

        self.dashboard()

    def show_tasks(self, parent, limit=None):
        tasks = self.db.execute(
            "SELECT id,title,priority,completed FROM tasks ORDER BY completed,id"
        ).fetchall()

        if limit:
            tasks = tasks[:limit]

        if not tasks:
            empty = self.card(parent)
            empty.pack(fill="x", pady=5)

            tk.Label(
                empty,
                text="Nothing here yet.",
                bg=CARD,
                fg=MUTED,
                font=("Segoe UI", 12)
            ).pack(pady=20)

            return

        for task_id, title, priority, completed in tasks:
            row = self.card(parent)
            row.pack(fill="x", pady=4)

            symbol = "✓" if completed else "○"

            tk.Label(
                row,
                text=symbol,
                bg=CARD,
                fg=GREEN if completed else PURPLE,
                font=("Segoe UI", 15)
            ).pack(side="left", padx=15, pady=12)

            tk.Label(
                row,
                text=title,
                bg=CARD,
                fg=MUTED if completed else TEXT,
                font=("Segoe UI", 11)
            ).pack(side="left", padx=5)

            if not completed:
                self.button(
                    row,
                    "Complete",
                    lambda tid=task_id: self.complete_task(tid)
                ).pack(side="right", padx=10, pady=5)

    def tasks_page(self):
        self.clear_content()

        self.label(
            self.content, "Tasks", 26, TEXT, True
        ).pack(anchor="w")

        self.label(
            self.content, "Turn intentions into progress.", 11, MUTED
        ).pack(anchor="w", pady=5)

        self.button(
            self.content, "+ Add task", self.add_task, True
        ).pack(anchor="w", pady=20)

        self.show_tasks(self.content)

    # ─────────────────────────────────────────
    # HABITS
    # ─────────────────────────────────────────

    def add_habit(self):
        title = simpledialog.askstring(
            "New habit",
            "What habit would you like to build?",
            parent=self.root
        )

        if title and title.strip():
            self.db.execute(
                "INSERT INTO habits(title) VALUES(?)",
                (title.strip(),)
            )
            self.db.commit()
            self.habits_page()

    def habits_page(self):
        self.clear_content()

        self.label(
            self.content, "Habits", 26, TEXT, True
        ).pack(anchor="w")

        self.label(
            self.content, "Build consistency one day at a time.", 11, MUTED
        ).pack(anchor="w", pady=5)

        self.button(
            self.content, "+ New habit", self.add_habit, True
        ).pack(anchor="w", pady=20)

        habits = self.db.execute(
            "SELECT id,title,completed FROM habits"
        ).fetchall()

        if not habits:
            self.label(
                self.content,
                "Your habit journey starts here.",
                12,
                MUTED
            ).pack(anchor="w", pady=20)

        for hid, title, done in habits:
            row = self.card(self.content)
            row.pack(fill="x", pady=5)

            tk.Label(
                row, text=title, bg=CARD, fg=TEXT,
                font=("Segoe UI", 12)
            ).pack(side="left", padx=20, pady=15)

            self.button(
                row,
                "✓ Done" if done else "Mark done",
                lambda h=hid: self.complete_habit(h)
            ).pack(side="right", padx=15)

    def complete_habit(self, hid):
        self.db.execute(
            "UPDATE habits SET completed=1 WHERE id=?",
            (hid,)
        )
        self.db.commit()

        self.unlock("Habit Builder")
        self.habits_page()

    # ─────────────────────────────────────────
    # MOOD
    # ─────────────────────────────────────────

    def mood_page(self):
        self.clear_content()

        self.label(
            self.content, "Mood check-in", 26, TEXT, True
        ).pack(anchor="w")

        self.label(
            self.content,
            "Take a moment to notice how you're feeling.",
            11,
            MUTED
        ).pack(anchor="w", pady=10)

        moods = [
            ("😊", "Happy"),
            ("😌", "Calm"),
            ("😐", "Okay"),
            ("😟", "Worried"),
            ("😴", "Tired")
        ]

        for emoji, mood in moods:
            self.button(
                self.content,
                f"{emoji}  {mood}",
                lambda m=mood: self.save_mood(m)
            ).pack(fill="x", pady=5)

        self.label(
            self.content, "YOUR RECENT CHECK-INS", 12, TEXT, True
        ).pack(anchor="w", pady=(30, 10))

        records = self.db.execute(
            "SELECT mood,date FROM moods ORDER BY id DESC LIMIT 7"
        ).fetchall()

        for mood, date in records:
            self.label(
                self.content, f"{date}  •  {mood}", 11, MUTED
            ).pack(anchor="w", pady=4)

    def save_mood(self, mood):
        self.db.execute(
            "INSERT INTO moods(mood,date) VALUES(?,?)",
            (mood, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        self.db.commit()

        self.unlock("Mood Explorer")

        messagebox.showinfo(
            "Check-in saved",
            "Thanks for checking in with yourself."
        )

        self.mood_page()

    # ─────────────────────────────────────────
    # ACHIEVEMENTS
    # ─────────────────────────────────────────

    def unlock(self, name):
        self.db.execute(
            "UPDATE achievements SET unlocked=1 WHERE name=?",
            (name,)
        )
        self.db.commit()

    def achievement_page(self):
        self.clear_content()

        self.label(
            self.content, "Achievements", 26, TEXT, True
        ).pack(anchor="w")

        self.label(
            self.content, "Celebrate the progress you make.", 11, MUTED
        ).pack(anchor="w", pady=10)

        achievements = self.db.execute(
            "SELECT name,unlocked FROM achievements"
        ).fetchall()

        descriptions = {
            "First Task": "Create your first task",
            "Task Master": "Complete five tasks",
            "Focus Starter": "Finish a focus session",
            "Habit Builder": "Create your first habit",
            "Mood Explorer": "Complete your first mood check-in"
        }

        for name, unlocked in achievements:
            row = self.card(self.content)
            row.pack(fill="x", pady=5)

            icon = "🏆" if unlocked else "🔒"

            tk.Label(
                row,
                text=f"{icon}  {name}",
                bg=CARD,
                fg=GREEN if unlocked else TEXT,
                font=("Segoe UI", 12, "bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))

            tk.Label(
                row,
                text=descriptions.get(name, ""),
                bg=CARD,
                fg=MUTED,
                font=("Segoe UI", 10)
            ).pack(anchor="w", padx=20, pady=(0, 15))

    # ─────────────────────────────────────────
    # FOCUS TIMER
    # ─────────────────────────────────────────

    def focus(self):
        window = tk.Toplevel(self.root)
        window.title("NOVA Focus")
        window.geometry("350x350")
        window.configure(bg=BG)
        window.transient(self.root)

        seconds = 15 * 60
        running = False
        after_id = None

        timer_label = tk.Label(
            window,
            text="15:00",
            bg=BG,
            fg=PURPLE,
            font=("Segoe UI", 42, "bold")
        )
        timer_label.pack(pady=40)

        status = tk.Label(
            window,
            text="15-minute focus session",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 11)
        )
        status.pack()

        def tick():
            nonlocal seconds, after_id

            if seconds <= 0:
                timer_label.config(text="00:00")
                status.config(text="Session complete!")
                self.unlock("Focus Starter")
                messagebox.showinfo(
                    "Focus complete",
                    "Great work completing your focus session!"
                )
                return

            seconds -= 1

            timer_label.config(
                text=f"{seconds // 60:02}:{seconds % 60:02}"
            )

            after_id = window.after(1000, tick)

        def start():
            nonlocal running

            if not running:
                running = True
                tick()

        def pause():
            nonlocal running

            running = False

            if after_id:
                window.after_cancel(after_id)

        self.button(window, "Start", start, True).pack(pady=15)
        self.button(window, "Pause", pause).pack()

    # ─────────────────────────────────────────
    # SETTINGS
    # ─────────────────────────────────────────

    def settings_page(self):
        self.clear_content()

        self.label(
            self.content, "Settings", 26, TEXT, True
        ).pack(anchor="w")

        self.label(
            self.content,
            "Your NOVA workspace.",
            11,
            MUTED
        ).pack(anchor="w", pady=10)

        self.button(
            self.content,
            "Export tasks",
            self.export_tasks
        ).pack(anchor="w", pady=10)

        self.label(
            self.content,
            "NOVA Planner • Personal Edition",
            10,
            MUTED
        ).pack(anchor="w", pady=20)

    def export_tasks(self):
        tasks = self.db.execute(
            "SELECT title,priority,completed FROM tasks"
        ).fetchall()

        path = APP / "tasks_export.txt"

        with open(path, "w", encoding="utf-8") as file:
            for title, priority, completed in tasks:
                file.write(
                    f"{title} | {priority} | Completed: {completed}\n"
                )

        messagebox.showinfo(
            "Export complete",
            f"Tasks saved to:\n{path}"
        )


# ─────────────────────────────────────────────
# START APPLICATION
# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = NovaPlanner(root)
    root.mainloop()
