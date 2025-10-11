from typing import List, Optional
from src.level import Level
import os
import json
from src.query import Query

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
