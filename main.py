#!/usr/bin/env python3
"""
Law Maker - A Prolog Programming Game
Minimalist pastel aesthetic with quietly utopian undertones.
View-based navigation for immersive gameplay.
"""

import os
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import threading

try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import janus_swi as janus

    JANUS_AVAILABLE = True
except ImportError:
    JANUS_AVAILABLE = False


class GameResult(Enum):
    SUCCESS = "success"
    SYNTAX_ERROR = "syntax_error"
    WRONG_RESULTS = "wrong_results"
    PROLOG_ERROR = "prolog_error"


class GameView(Enum):
    """Different game views/screens"""
    INTRODUCTION = "introduction"
    TASK_OVERVIEW = "task_overview"
    TASK_WORKSPACE = "task_workspace"


@dataclass
class Query:
    """Represents a Prolog query with expected results"""
    query: str
    expected: List[str]
    description: str = ""


@dataclass
class Level:
    """Represents a game level with law implementation challenge"""
    id: str
    title: str
    description: str
    background_story: str
    given_facts: str
    law_description: str
    queries: List[Query]
    hints: List[str] = None
    difficulty: int = 1
    solution: List[str] = None
    completed: bool = False


class Theme:
    """Minimalist pastel theme"""
    COLORS = {
        'bg_primary': '#F5F5F0', 'bg_secondary': '#E8E4E0',
        'bg_panel': '#FAF8F5', 'bg_input': '#FEFEFE',
        'accent_primary': '#9BB5B0', 'accent_secondary': '#D4A5A5',
        'accent_tertiary': '#B5B0C9', 'success': '#A8C5A6',
        'text_primary': '#3A3A38', 'text_secondary': '#6B6B68',
        'text_accent': '#7A8B88', 'warning': '#D9A89F',
        'border': '#D5D0C8', 'hover': '#C8C3BB'
    }

    @staticmethod
    def configure_style():
        style = ttk.Style()
        c = Theme.COLORS

        style.configure('Pastel.TFrame', background=c['bg_primary'], relief='flat')
        style.configure('Panel.TFrame', background=c['bg_panel'], relief='flat')
        style.configure('Pastel.TLabel', background=c['bg_primary'],
                        foreground=c['text_primary'], font=('Helvetica Neue', 10))
        style.configure('Title.TLabel', background=c['bg_primary'],
                        foreground=c['text_primary'], font=('Helvetica Neue', 16))
        style.configure('Header.TLabel', background=c['bg_primary'],
                        foreground=c['text_accent'], font=('Helvetica Neue', 11))
        style.configure('Pastel.TButton', background=c['accent_primary'],
                        foreground=c['text_primary'], font=('Helvetica Neue', 9),
                        borderwidth=1, relief='flat', padding=(10, 5))
        style.map('Pastel.TButton', background=[('active', c['hover']), ('pressed', c['accent_secondary'])])
        style.configure('Pastel.TNotebook', background=c['bg_primary'], borderwidth=0)
        style.configure('Pastel.TNotebook.Tab', background=c['bg_secondary'],
                        foreground=c['text_secondary'], padding=[14, 6],
                        font=('Helvetica Neue', 9), borderwidth=0)
        style.map('Pastel.TNotebook.Tab',
                  background=[('selected', c['bg_primary']), ('active', c['hover'])],
                  foreground=[('selected', c['text_primary'])])
        return style


class LevelLoader:
    """Loads level configurations from JSON files"""

    @staticmethod
    def load_levels_from_directory(directory: str) -> List[Level]:
        """Load all levels from a directory containing JSON files"""
        levels = []

        if not os.path.exists(directory):
            LevelLoader.create_sample_levels(directory)

        try:
            level_files = [f for f in os.listdir(directory) if f.endswith('.json')]
            level_files.sort()

            for filename in level_files:
                filepath = os.path.join(directory, filename)
                level = LevelLoader.load_level_from_file(filepath)
                if level:
                    levels.append(level)
        except Exception as e:
            print(f"Error loading levels: {e}")
            return LevelLoader.get_sample_levels()

        return levels if levels else LevelLoader.get_sample_levels()

    @staticmethod
    def load_level_from_file(filepath: str) -> Optional[Level]:
        """Load a single level from a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'content' in data:
                data = data['content']

            queries = []
            for q_data in data.get('queries', []):
                query = Query(
                    query=q_data['query'],
                    expected=q_data['expected'],
                    description=q_data.get('description', '')
                )
                queries.append(query)

            level = Level(
                id=data['id'],
                title=data['title'],
                description=data['description'],
                background_story=data['background_story'],
                given_facts=data['given_facts'],
                law_description=data['law_description'],
                queries=queries,
                hints=data.get('hints', []),
                difficulty=data.get('difficulty', 1),
                solution=data.get('solution', [])
            )

            return level

        except Exception as e:
            print(f"Error loading level from {filepath}: {e}")
            return None

    @staticmethod
    def create_sample_levels(directory: str):
        """Create sample level files in the specified directory"""
        os.makedirs(directory, exist_ok=True)

        level1_data = {
            "id": "student_meal_subsidy",
            "title": "Student Meal Subsidy Law",
            "description": "Implement the new student meal subsidy law for Solarfurt",
            "background_story": "Welcome to Solarfurt, civil servant! Our eco-friendly city council has passed the Student Meal Subsidy Law. Your job is to implement this law in our legal database system.\n\nThe law supports sustainable living: students under 25 are eligible for meal subsidies. Base rate is 50 credits, with a 30-credit bonus for low-income students.\n\nThis is your first assignment in our rusty-but-reliable legal tech system. Code with care!",
            "given_facts": "person(alice).\nperson(bob).\nperson(charlie).\nperson(diana).\n\nage(alice, 22).\nage(bob, 26).\nage(charlie, 19).\nage(diana, 23).\n\nincome(alice, low).\nincome(bob, medium).\nincome(charlie, low).\nincome(diana, high).\n\nstudent(alice).\nstudent(charlie).",
            "law_description": "Student Meal Subsidy Law (Solarfurt Ordinance 2024-001):\n\n1. Eligibility: Must be a student AND under 25 years old\n2. Base subsidy: 50 credits per month for eligible students\n3. Low-income bonus: Additional 30 credits (total 80)\n4. Implementation: Create eligible(Person) and subsidy_amount(Person, Amount)\n5. Non-eligible persons should make subsidy_amount fail",
            "queries": [
                {"query": "eligible(X)", "expected": ["alice", "charlie"], "description": "Find all eligible students"},
                {"query": "subsidy_amount(alice, Amount)", "expected": ["80"],
                 "description": "Alice: student + low income = 80"},
                {"query": "subsidy_amount(charlie, Amount)", "expected": ["80"],
                 "description": "Charlie: student + low income = 80"},
                {"query": "subsidy_amount(diana, Amount)", "expected": [],
                 "description": "Diana: not a student, should fail"},
                {"query": "subsidy_amount(bob, Amount)", "expected": [], "description": "Bob: too old, should fail"}
            ],
            "hints": [
                "Check BOTH student(Person) AND age < 25",
                "Low-income students get 80 credits (50 + 30 bonus)",
                "Non-eligible people should make subsidy_amount fail"
            ],
            "difficulty": 1
        }

        with open(os.path.join(directory, '01_student_meal_subsidy.json'), 'w') as f:
            json.dump(level1_data, f, indent=2)

    @staticmethod
    def get_sample_levels() -> List[Level]:
        """Return hardcoded sample levels as fallback"""
        query1 = [
            Query("eligible(X)", ["alice", "charlie"], "Find all eligible students"),
            Query("subsidy_amount(alice, Amount)", ["80"], "Alice: student + low income = 80"),
            Query("subsidy_amount(charlie, Amount)", ["80"], "Charlie: student + low income = 80"),
            Query("subsidy_amount(diana, Amount)", [], "Diana: not a student, should fail"),
        ]

        level1 = Level(
            id="student_meal_subsidy",
            title="Student Meal Subsidy Law",
            description="Implement the new student meal subsidy law for Solarfurt",
            background_story="Welcome to Solarfurt, civil servant! Our eco-friendly city council has passed the Student Meal Subsidy Law.",
            given_facts="person(alice).\nperson(bob).\nperson(charlie).\nperson(diana).\n\nage(alice, 22).\nage(bob, 26).\nage(charlie, 19).\nage(diana, 23).\n\nincome(alice, low).\nincome(bob, medium).\nincome(charlie, low).\nincome(diana, high).\n\nstudent(alice).\nstudent(charlie).",
            law_description="Student Meal Subsidy Law:\n1. Must be student AND under 25\n2. Base: 50 credits\n3. Low-income bonus: +30 credits",
            queries=query1,
            hints=["Check both conditions", "Use income facts", "Make predicate fail for non-eligible"]
        )

        return [level1]


class JanusPrologRunner:
    """Enhanced Prolog runner using janus_swi for better integration"""

    def __init__(self):
        self.janus_available = JANUS_AVAILABLE
        if self.janus_available:
            try:
                janus.query_once("writeln('Prolog available!')")
                self.prolog_available = True
            except Exception as e:
                print(f"Error initializing janus_swi: {e}")
                self.prolog_available = False
                self.janus_available = False
        else:
            self.prolog_available = False

    def run_queries(self, prolog_code: str, queries: List[Query]) -> Tuple[GameResult, Dict[str, Any]]:
        """Run Prolog queries using janus_swi"""
        if not self.prolog_available:
            return GameResult.PROLOG_ERROR, {
                "error": "Janus SWI-Prolog not available. Install with: pip install janus_swi"}

        try:
            janus.consult("temp_rules", prolog_code)
            results = {}
            all_correct = True

            for i, query in enumerate(queries):
                try:
                    actual_results = []
                    found_solutions = False

                    for solution in janus.query(query.query):
                        found_solutions = True
                        if solution:
                            if isinstance(solution, dict) and solution:
                                for var, value in solution.items():
                                    if value not in [True, False, 'True', 'False', None, 'None'] and str(value) not in [
                                        'True', 'False', 'None']:
                                        actual_results.append(str(value))
                            elif not isinstance(solution, dict):
                                if (solution not in [True, False, 'True', 'False', None, 'None'] and
                                        str(solution) not in ['True', 'False', 'None']):
                                    actual_results.append(str(solution))

                    if found_solutions and not actual_results:
                        if not query.expected or (len(query.expected) == 1 and query.expected[0] in ['true', True]):
                            actual_results.append("true")

                    if not found_solutions:
                        try:
                            result = janus.query_once(query.query)
                            if result is not None:
                                if isinstance(result, dict) and result:
                                    for var, value in result.items():
                                        if value not in [True, False, 'True', 'False', None, 'None']:
                                            actual_results.append(str(value))
                                elif result is True:
                                    if not any(c.isupper() for c in query.query):
                                        actual_results.append("true")
                        except:
                            pass

                    if not query.expected or query.expected == ['false']:
                        correct = len(actual_results) == 0
                    else:
                        expected_set = set(str(e) for e in query.expected)
                        actual_set = set(str(r) for r in actual_results)
                        correct = actual_set == expected_set

                    results[f"query_{i}"] = {
                        "query": query.query,
                        "expected": query.expected,
                        "actual": actual_results,
                        "correct": correct
                    }

                    if not correct:
                        all_correct = False

                except Exception as e:
                    results[f"query_{i}"] = {
                        "query": query.query,
                        "expected": query.expected,
                        "actual": [],
                        "error": str(e),
                        "correct": False
                    }
                    all_correct = False

            if all_correct:
                return GameResult.SUCCESS, results
            else:
                return GameResult.WRONG_RESULTS, results

        except Exception as e:
            return GameResult.PROLOG_ERROR, {"error": f"Prolog error: {str(e)}"}


class PrologTemplateButton(tk.Button):
    """A button that inserts Prolog template code into the editor"""

    def __init__(self, parent, template_text, label, code_widget, **kwargs):
        self.template_text = template_text
        self.code_widget = code_widget

        super().__init__(parent, text=label, command=self.insert_template,
                         bg=Theme.COLORS['bg_secondary'], fg=Theme.COLORS['text_primary'],
                         font=('Helvetica Neue', 8), relief=tk.FLAT, bd=1,
                         padx=5, pady=4, wraplength=70, justify=tk.CENTER, **kwargs)

    def insert_template(self):
        cursor_pos = self.code_widget.index(tk.INSERT)
        self.code_widget.insert(cursor_pos, self.template_text + '\n')
        new_pos = self.code_widget.index(f"{cursor_pos}+{len(self.template_text)} chars")
        self.code_widget.mark_set(tk.INSERT, new_pos)
        self.code_widget.see(tk.INSERT)
        self.code_widget.focus()


class LawMakerGUI:
    """View-based GUI for the Law Maker game"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Law Maker")
        self.root.geometry("1200x900")

        self.style = Theme.configure_style()
        self.root.configure(bg=Theme.COLORS['bg_primary'])

        self.levels_directory = "levels"
        self.levels = []
        self.current_level_index = 0
        self.current_level = None
        self.prolog_runner = JanusPrologRunner()
        self.attempts_remaining = 3
        self.current_view = GameView.INTRODUCTION

        # Main container
        self.main_container = tk.Frame(self.root, bg=Theme.COLORS['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.load_levels()
        self.show_introduction()

    def load_levels(self):
        """Load levels from directory"""
        self.levels = LevelLoader.load_levels_from_directory(self.levels_directory)
        if not self.levels:
            messagebox.showerror("Error", "No levels could be loaded!")
            self.root.quit()

    def clear_view(self):
        """Clear the current view"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_introduction(self):
        """Show the introduction view"""
        self.current_view = GameView.INTRODUCTION
        self.clear_view()

        intro_frame = tk.Frame(self.main_container, bg=Theme.COLORS['bg_primary'], padx=50, pady=40)
        intro_frame.pack(fill=tk.BOTH, expand=True)

        # Image
        try:
            if PIL_AVAILABLE and os.path.exists("sprites/cityscape-background-illustration.jpg"):
                image = Image.open("sprites/cityscape-background-illustration.jpg")
                image = image.resize((800, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(intro_frame, image=photo, bg=Theme.COLORS['bg_primary'])
                img_label.image = photo
                img_label.pack(pady=(0, 30))
        except:
            pass

        # Welcome text
        welcome_msg = """Welcome to Solarfurt.

The year is 2028. The civil service is aging—predictably, without drama.

To address this, laws are being transformed into processable logic. A new device assists: the Pocket-Inferer, a logical calculator which translates ordinances into executable code. Your role involves learning this system and formalizing municipal regulations.

The work is precise. Occasionally tedious. Somehow satisfying. The question who buys new coffee remains unresolved.
"""

        text_widget = tk.Text(intro_frame, height=10, width=80, wrap=tk.WORD,
                              font=('Helvetica Neue', 11),
                              bg=Theme.COLORS['bg_panel'],
                              fg=Theme.COLORS['text_primary'],
                              relief=tk.FLAT, bd=0, padx=25, pady=25)
        text_widget.insert(tk.END, welcome_msg)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 30))

        # Button
        btn = tk.Button(intro_frame, text="Ok then.",
                        command=self.show_task_overview,
                        font=('Helvetica Neue', 11),
                        bg=Theme.COLORS['accent_primary'],
                        fg=Theme.COLORS['text_primary'],
                        relief=tk.FLAT, bd=0,
                        padx=40, pady=12)
        btn.pack()

    def show_task_overview(self):
        """Show the task overview view"""
        self.current_view = GameView.TASK_OVERVIEW
        self.clear_view()

        overview_frame = tk.Frame(self.main_container, bg=Theme.COLORS['bg_primary'])
        overview_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Header
        header = ttk.Frame(overview_frame, style='Panel.TFrame')
        header.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(header, text="Department of Administrative Logic",
                  style='Title.TLabel').pack(pady=8)
        ttk.Label(header, text="Task Assignment Board · Solarfurt B Wing",
                  style='Header.TLabel').pack(pady=(0, 8))

        # Instructions
        ttk.Label(overview_frame, text="Available Ordinances",
                  style='Header.TLabel').pack(pady=(10, 5))
        ttk.Label(overview_frame, text="Select a regulation to formalize:",
                  style='Pastel.TLabel').pack(pady=5)

        # Task list
        list_frame = ttk.Frame(overview_frame, style='Panel.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        self.task_listbox = tk.Listbox(
            list_frame, height=15, font=('Helvetica Neue', 11),
            bg=Theme.COLORS['bg_input'], fg=Theme.COLORS['text_primary'],
            selectbackground=Theme.COLORS['accent_tertiary'],
            selectforeground=Theme.COLORS['text_primary'],
            relief=tk.FLAT, borderwidth=1
        )
        self.task_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.task_listbox.bind('<Double-Button-1>', lambda e: self.select_task())

        self.populate_task_list()

        # Status
        status_frame = ttk.Frame(overview_frame, style='Pastel.TFrame')
        status_frame.pack(fill=tk.X, pady=10)

        completed_count = sum(1 for level in self.levels if level.completed)
        status_text = f"Progress: {completed_count}/{len(self.levels)} ordinances formalized"
        ttk.Label(status_frame, text=status_text, style='Pastel.TLabel').pack()

        # Buttons
        button_frame = ttk.Frame(overview_frame, style='Pastel.TFrame')
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Open Selected Task", command=self.select_task,
                   style='Pastel.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_and_show_overview,
                   style='Pastel.TButton').pack(side=tk.LEFT, padx=5)

    def populate_task_list(self):
        """Populate the task list"""
        self.task_listbox.delete(0, tk.END)
        for i, level in enumerate(self.levels):
            status = "✓" if level.completed else " "
            self.task_listbox.insert(tk.END, f"[{status}] Ordinance {i + 1}: {level.title}")

    def select_task(self):
        """Select a task and show the workspace"""
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("", "Please select a task first.")
            return

        self.load_level(selection[0])
        self.show_task_workspace()

    def load_level(self, level_index: int):
        """Load a specific level"""
        if 0 <= level_index < len(self.levels):
            self.current_level_index = level_index
            self.current_level = self.levels[level_index]
            self.attempts_remaining = 3

    def show_task_workspace(self):
        """Show the task workspace view"""
        if not self.current_level:
            messagebox.showwarning("", "No task selected.")
            return

        self.current_view = GameView.TASK_WORKSPACE
        self.clear_view()

        workspace_frame = tk.Frame(self.main_container, bg=Theme.COLORS['bg_primary'])
        workspace_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header with back button
        header = ttk.Frame(workspace_frame, style='Panel.TFrame')
        header.pack(fill=tk.X, pady=(0, 10))

        back_btn = ttk.Button(header, text="← Back to Tasks", command=self.show_task_overview,
                              style='Pastel.TButton')
        back_btn.pack(side=tk.LEFT, padx=10, pady=8)

        ttk.Label(header, text=f"Ordinance {self.current_level_index + 1}: {self.current_level.title}",
                  style='Title.TLabel').pack(side=tk.LEFT, padx=20)

        # Notebook for different sections
        self.notebook = ttk.Notebook(workspace_frame, style='Pastel.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Setup tabs
        self.setup_workspace_tabs()

    def setup_workspace_tabs(self):
        """Setup the workspace tabs"""
        # Brief tab
        self.brief_frame = ttk.Frame(self.notebook, style='Pastel.TFrame')
        self.notebook.add(self.brief_frame, text="Brief")
        self.setup_brief_tab()

        # Pocket-Inferer tab
        self.editor_frame = ttk.Frame(self.notebook, style='Pastel.TFrame')
        self.notebook.add(self.editor_frame, text="Pocket-Inferer")
        self.setup_editor_tab()

        # Results tab
        self.results_frame = ttk.Frame(self.notebook, style='Pastel.TFrame')
        self.notebook.add(self.results_frame, text="Results")
        self.setup_results_tab()

    def setup_brief_tab(self):
        """Setup the brief/description tab"""
        brief_notebook = ttk.Notebook(self.brief_frame, style='Pastel.TNotebook')
        brief_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        tabs = [
            ("Context", "story_text", self.current_level.background_story),
            ("Data", "facts_text", self.current_level.given_facts, ('Menlo', 9)),
            ("Requirements", "law_text", self.current_level.law_description),
            ("Tests", "queries_text", self.format_queries_text()),
            ("Notes", "hints_text", self.format_hints_text()),
        ]

        for tab_info in tabs:
            name, attr_name, content = tab_info[0], tab_info[1], tab_info[2]
            font = tab_info[3] if len(tab_info) > 3 else None

            frame = ttk.Frame(brief_notebook, style='Pastel.TFrame')
            brief_notebook.add(frame, text=name)

            kwargs = {'state': tk.DISABLED, 'height': 20}
            if font:
                kwargs['font'] = font

            text_widget = self.create_styled_text(frame, **kwargs)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            text_widget.config(state=tk.NORMAL)
            text_widget.insert(1.0, content)
            text_widget.config(state=tk.DISABLED)

            setattr(self, attr_name, text_widget)

    def format_queries_text(self):
        """Format queries for display"""
        text = "Test specifications:\n\n"
        for i, query in enumerate(self.current_level.queries, 1):
            text += f"{i}. {query.query}\n"
            text += f"   Expected: {query.expected if query.expected else 'fail'}\n"
            if query.description:
                text += f"   {query.description}\n"
            text += "\n"
        return text

    def format_hints_text(self):
        """Format hints for display"""
        if self.current_level.hints:
            return "Implementation notes:\n\n" + "\n".join(
                f"{i}. {h}" for i, h in enumerate(self.current_level.hints, 1))
        return "No additional notes."

    def setup_editor_tab(self):
        """Setup the code editor tab"""
        # Pocket-Inferer header
        pocket_header = ttk.Frame(self.editor_frame, style='Panel.TFrame')
        pocket_header.pack(fill=tk.X, padx=10, pady=8)

        header_content = ttk.Frame(pocket_header, style='Panel.TFrame')
        header_content.pack(fill=tk.X, padx=10, pady=8)

        left_header = ttk.Frame(header_content, style='Panel.TFrame')
        left_header.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_header, text="Pocket-Inferer",
                  style='Header.TLabel').pack(anchor=tk.W)
        ttk.Label(left_header, text="Logical Calculator · Model Tadashi-B-2028",
                  font=('Helvetica Neue', 8),
                  foreground=Theme.COLORS['text_secondary'],
                  background=Theme.COLORS['bg_panel']).pack(anchor=tk.W, pady=(2, 0))

        # Try to load device image
        try:
            if PIL_AVAILABLE and os.path.exists("sprites/pocket-inferer.png"):
                pocket_image = Image.open("sprites/pocket-inferer.png")
                pocket_image = pocket_image.resize((60, 80), Image.Resampling.LANCZOS)
                pocket_photo = ImageTk.PhotoImage(pocket_image)
                img_label = tk.Label(header_content, image=pocket_photo, bg=Theme.COLORS['bg_panel'])
                img_label.image = pocket_photo
                img_label.pack(side=tk.RIGHT, padx=10)
        except:
            pass

        # Display (live results)
        display_label = ttk.Label(self.editor_frame, text="Display",
                                  font=('Helvetica Neue', 9),
                                  foreground=Theme.COLORS['text_secondary'],
                                  background=Theme.COLORS['bg_primary'])
        display_label.pack(pady=(5, 2), padx=10, anchor=tk.W)

        self.live_results_text = self.create_styled_text(self.editor_frame, height=6)
        self.live_results_text.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0, 10))

        # Code input area
        editor_header = ttk.Frame(self.editor_frame, style='Pastel.TFrame')
        editor_header.pack(fill=tk.X, padx=10, pady=(8, 4))

        ttk.Label(editor_header, text="Input",
                  font=('Helvetica Neue', 9),
                  foreground=Theme.COLORS['text_secondary'],
                  background=Theme.COLORS['bg_primary']).pack(side=tk.LEFT)

        self.attempts_label = ttk.Label(editor_header, text="", style='Pastel.TLabel')
        self.attempts_label.pack(side=tk.RIGHT)
        self.update_attempts_display()

        self.code_text = self.create_styled_text(self.editor_frame, height=8, font=('Menlo', 10))
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Template buttons
        button_panel = ttk.Frame(self.editor_frame, style='Panel.TFrame')
        button_panel.pack(fill=tk.X, padx=10, pady=8)

        ttk.Label(button_panel, text="Function Keys",
                  font=('Helvetica Neue', 9),
                  foreground=Theme.COLORS['text_secondary'],
                  background=Theme.COLORS['bg_panel']).pack(anchor=tk.W, padx=10, pady=(5, 8))

        templates_frame = ttk.Frame(button_panel, style='Pastel.TFrame')
        templates_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        templates = [
            ("Fact", "predicate(arg)."), ("Rule", "head :- body."),
            ("Query", "?- pred(X)."), ("AND", "cond1, cond2"),
            ("OR", "(c1 ; c2)"), ("NOT", "\\+ pred(X)"),
            ("Unify", "X = value"), ("< ", "X < Y"),
            ("> ", "X > Y"), ("= ", "X = Y"),
            ("List", "[H|T]"), ("Findall", "findall(X, p(X), L)"),
            ("Member", "member(X, [1,2])"), ("Length", "length(L, N)"),
            ("Append", "append(L1, L2, R)"), ("Comment", "% note"),
        ]

        for i, (label, template) in enumerate(templates):
            btn = PrologTemplateButton(templates_frame, template, label, self.code_text)
            btn.grid(row=i // 4, column=i % 4, padx=3, pady=3, sticky="nsew")

        for i in range(4):
            templates_frame.grid_columnconfigure(i, weight=1)

        # Control buttons
        control_frame = ttk.Frame(button_panel, style='Pastel.TFrame')
        control_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(control_frame, text="Controls",
                  font=('Helvetica Neue', 9),
                  foreground=Theme.COLORS['text_secondary'],
                  background=Theme.COLORS['bg_panel']).pack(anchor=tk.W, pady=(0, 5))

        action_frame = ttk.Frame(control_frame, style='Pastel.TFrame')
        action_frame.pack(fill=tk.X)

        self.go_button = ttk.Button(action_frame, text="Compute", command=self.execute_code,
                                    style='Pastel.TButton')
        self.go_button.pack(side=tk.LEFT, padx=3)

        self.submit_button = ttk.Button(action_frame, text="Submit", command=self.test_solution,
                                        style='Pastel.TButton')
        self.submit_button.pack(side=tk.LEFT, padx=3)

        ttk.Button(action_frame, text="Clear", command=self.clear_code,
                   style='Pastel.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(action_frame, text="Example", command=self.load_example,
                   style='Pastel.TButton').pack(side=tk.LEFT, padx=3)

        self.prolog_status = ttk.Label(action_frame, text="",
                                       font=('Helvetica Neue', 8),
                                       foreground=Theme.COLORS['text_secondary'],
                                       background=Theme.COLORS['bg_primary'])
        self.prolog_status.pack(side=tk.RIGHT, padx=10)
        self.update_prolog_status()

    def setup_results_tab(self):
        """Setup the results display tab"""
        ttk.Label(self.results_frame, text="Compliance Report",
                  style='Header.TLabel').pack(pady=12)

        self.results_text = self.create_styled_text(self.results_frame, height=25, state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        results_buttons = ttk.Frame(self.results_frame, style='Pastel.TFrame')
        results_buttons.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(results_buttons, text="Clear", command=self.clear_results,
                   style='Pastel.TButton').pack(side=tk.LEFT, padx=5)

    def create_styled_text(self, parent, **kwargs):
        """Create a styled text widget"""
        return scrolledtext.ScrolledText(
            parent, bg=Theme.COLORS['bg_input'], fg=Theme.COLORS['text_primary'],
            insertbackground=Theme.COLORS['text_accent'], selectbackground=Theme.COLORS['accent_tertiary'],
            relief='flat', borderwidth=1, **kwargs
        )

    def update_attempts_display(self):
        """Update the attempts display"""
        dots = "●" * self.attempts_remaining + "○" * (3 - self.attempts_remaining)
        self.attempts_label.config(text=f"Attempts: {dots}")

    def update_prolog_status(self):
        """Update the Prolog status indicator"""
        if self.prolog_runner.prolog_available:
            self.prolog_status.config(text="Prolog: active", foreground=Theme.COLORS['success'])
        else:
            self.prolog_status.config(text="Prolog: unavailable", foreground=Theme.COLORS['warning'])

    def clear_code(self):
        """Clear the code editor"""
        self.code_text.delete(1.0, tk.END)

    def clear_results(self):
        """Clear the results display"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)

    def clear_live_results(self):
        """Clear the live results display"""
        self.live_results_text.config(state=tk.NORMAL)
        self.live_results_text.delete(1.0, tk.END)
        self.live_results_text.config(state=tk.DISABLED)

    def load_example(self):
        """Load an example solution"""
        if not self.current_level:
            return

        example_code = "% Implementation goes here\n% Define required predicates\n\n"

        if self.current_level.id == "student_meal_subsidy":
            example_code = """% Student meal subsidy implementation

% Eligibility: student status and age below 25
eligible(Person) :-
    student(Person),
    age(Person, Age),
    Age < 25.

% Low-income eligible students: 80 credits (base + supplement)
subsidy_amount(Person, Amount) :-
    eligible(Person),
    income(Person, low),
    Amount = 80.

% Other eligible students: 50 credits (base only)
subsidy_amount(Person, Amount) :-
    eligible(Person),
    \\+ income(Person, low),
    Amount = 50."""

        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(1.0, example_code)

    def execute_code(self):
        """Execute code for testing (without counting attempts)"""
        if not self.current_level:
            messagebox.showwarning("", "Please select a task first.")
            return

        user_code = self.code_text.get(1.0, tk.END).strip()
        if not user_code:
            messagebox.showwarning("", "Editor is empty.")
            return

        self.go_button.config(state=tk.DISABLED, text="Computing...")

        def run_code():
            try:
                full_code = self.current_level.given_facts + '\n' + user_code
                result, details = self.prolog_runner.run_queries(full_code, self.current_level.queries)
                self.root.after(0, lambda: self.display_live_results(result, details))
            except Exception as e:
                self.root.after(0, lambda: self.display_live_error(str(e)))

        threading.Thread(target=run_code, daemon=True).start()

    def display_live_results(self, result: GameResult, details: Dict):
        """Display live results from computation"""
        self.go_button.config(state=tk.NORMAL, text="Compute")

        results_text = ""
        if result == GameResult.SUCCESS:
            results_text = "All tests passed.\n" + "─" * 40 + "\n"
            for query_id, query_result in details.items():
                if query_id.startswith('query_'):
                    results_text += f"✓ {query_result['query']}\n  → {query_result['actual']}\n"

        elif result == GameResult.PROLOG_ERROR:
            results_text = f"Syntax error detected.\n{'─' * 40}\n{details.get('error', 'Unknown error')}\n"

        elif result == GameResult.WRONG_RESULTS:
            results_text = "Test failures detected.\n" + "─" * 40 + "\n"
            for query_id, query_result in details.items():
                if query_id.startswith('query_'):
                    if query_result['correct']:
                        results_text += f"✓ {query_result['query']}\n"
                    else:
                        results_text += f"✗ {query_result['query']}\n"
                        results_text += f"  Expected: {query_result['expected']}\n"
                        results_text += f"  Got: {query_result['actual']}\n"

        self.live_results_text.config(state=tk.NORMAL)
        self.live_results_text.delete(1.0, tk.END)
        self.live_results_text.insert(1.0, results_text)
        self.live_results_text.config(state=tk.DISABLED)

    def display_live_error(self, error_msg: str):
        """Display error from computation"""
        self.go_button.config(state=tk.NORMAL, text="Compute")
        error_text = f"Error occurred.\n{'─' * 40}\n{error_msg}"
        self.live_results_text.config(state=tk.NORMAL)
        self.live_results_text.delete(1.0, tk.END)
        self.live_results_text.insert(1.0, error_text)
        self.live_results_text.config(state=tk.DISABLED)

    def test_solution(self):
        """Test the solution (counts as an attempt)"""
        if not self.current_level:
            messagebox.showwarning("", "Please select a task first.")
            return

        if self.attempts_remaining <= 0:
            messagebox.showinfo("", "No attempts remaining for this task.")
            return

        user_code = self.code_text.get(1.0, tk.END).strip()
        if not user_code:
            messagebox.showwarning("", "Editor is empty.")
            return

        self.submit_button.config(state=tk.DISABLED, text="Evaluating...")

        def run_test():
            try:
                full_code = self.current_level.given_facts + '\n' + user_code
                result, details = self.prolog_runner.run_queries(full_code, self.current_level.queries)
                self.root.after(0, lambda: self.display_test_results(result, details))
            except Exception as e:
                self.root.after(0, lambda: self.display_error(str(e)))

        threading.Thread(target=run_test, daemon=True).start()

    def display_test_results(self, result: GameResult, details: Dict):
        """Display test results after submission"""
        self.submit_button.config(state=tk.NORMAL, text="Submit")

        results_text = "Compliance Report\n" + "=" * 50 + "\n"
        results_text += f"Task: {self.current_level.title}\n"
        results_text += f"Attempt: {4 - self.attempts_remaining}/3\n" + "=" * 50 + "\n\n"

        if result == GameResult.SUCCESS:
            results_text += "Task completed successfully.\nAll requirements satisfied.\n\n"

            for query_id, query_result in details.items():
                if query_id.startswith('query_'):
                    results_text += f"[pass] {query_result['query']}\n"
                    results_text += f"       Expected: {query_result['expected'] if query_result['expected'] else 'fail'}\n"
                    results_text += f"       Result: {query_result['actual']}\n\n"

            # Mark level as completed
            self.current_level.completed = True

            # Show completion message and return to overview
            self.root.after(100, lambda: self.show_completion_and_return())

        elif result == GameResult.PROLOG_ERROR:
            results_text += f"Syntax error.\nIssue: {details.get('error', 'Unknown error')}\n\nPlease review and resubmit.\n"

        elif result == GameResult.WRONG_RESULTS:
            results_text += "Compliance issues detected.\n\n"

            for query_id, query_result in details.items():
                if query_id.startswith('query_'):
                    status = "[pass]" if query_result['correct'] else "[fail]"
                    results_text += f"{status} {query_result['query']}\n"
                    results_text += f"       Expected: {query_result['expected'] if query_result['expected'] else 'fail'}\n"
                    results_text += f"       Result: {query_result['actual']}\n"

                    if 'error' in query_result and query_result['error']:
                        results_text += f"       Note: {query_result['error']}\n"
                    results_text += "\n"

        self.attempts_remaining -= 1
        self.update_attempts_display()

        if result != GameResult.SUCCESS and self.attempts_remaining == 0:
            results_text += "\nAttempts exhausted.\nConsider reviewing the task or selecting another.\n"
        elif result != GameResult.SUCCESS and self.attempts_remaining > 0:
            dots = "●" * self.attempts_remaining
            results_text += f"\n{dots} attempts remaining.\n"

            if self.attempts_remaining == 2 and self.current_level.hints:
                results_text += "\nConsult the Notes tab for guidance.\n"

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results_text)

        self.results_text.tag_configure("success", foreground=Theme.COLORS['success'])
        self.results_text.tag_configure("error", foreground=Theme.COLORS['warning'])
        self.results_text.tag_configure("header", foreground=Theme.COLORS['text_accent'])

        content = self.results_text.get(1.0, tk.END)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_start = f"{i + 1}.0"
            line_end = f"{i + 1}.end"

            if "[pass]" in line or "successfully" in line:
                self.results_text.tag_add("success", line_start, line_end)
            elif "[fail]" in line or "error" in line.lower() or "issues" in line:
                self.results_text.tag_add("error", line_start, line_end)
            elif "Report" in line or "Task:" in line:
                self.results_text.tag_add("header", line_start, line_end)

        self.results_text.config(state=tk.DISABLED)
        self.notebook.select(self.results_frame)

    def show_completion_and_return(self):
        """Show completion message and return to task overview"""
        messagebox.showinfo("Task Complete",
                            f"Ordinance {self.current_level_index + 1} successfully formalized!\n\n"
                            "Implementation verified and archived.\n\n"
                            "Returning to assignment board...")
        self.show_task_overview()

    def display_error(self, error_msg: str):
        """Display error message"""
        self.submit_button.config(state=tk.NORMAL, text="Submit")
        messagebox.showerror("Error", f"Compilation issue:\n\n{error_msg}")

    def refresh_and_show_overview(self):
        """Refresh levels and show overview"""
        try:
            self.levels = LevelLoader.load_levels_from_directory(self.levels_directory)
            self.show_task_overview()
        except Exception as e:
            messagebox.showerror("Error", f"Refresh failed:\n{e}")

    def run(self):
        """Start the application"""
        self.root.mainloop()


def create_sample_levels():
    """Create sample level files"""
    LevelLoader.create_sample_levels("levels")
    print("Sample tasks created in 'levels' directory")


def main():
    """Main entry point"""
    print("Initializing Law Maker...")

    if not os.path.exists("levels") or not os.listdir("levels"):
        print("Setting up task database...")
        create_sample_levels()

    if not JANUS_AVAILABLE:
        print("Warning: janus_swi not available")
        print("Install with: pip install janus_swi")

    try:
        print("Launching interface...")
        app = LawMakerGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nShutdown initiated.")
    except Exception as e:
        print(f"System error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()