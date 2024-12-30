import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Callable
from models import User, Certification, Topic
from quiz_generator import QuizGenerator
from study_tracker import StudyTracker

class UI:
    def __init__(self, db_session):
        self.console = Console()
        self.session = db_session
        self.quiz_generator = QuizGenerator(db_session)
        self.study_tracker = StudyTracker(db_session)

    def main_menu(self, user_id: int):
        while True:
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "Study Topics",
                    "Take Quiz",
                    "Review Flashcards",
                    "View Progress",
                    "Add Study Notes",
                    "Manage Content",
                    "Exit"
                ]
            ).ask()

            actions = {
                "Study Topics": lambda: self.study_topics(user_id),
                "Take Quiz": lambda: self.take_quiz(user_id),
                "Review Flashcards": lambda: self.review_flashcards(user_id),
                "View Progress": lambda: self.view_progress(user_id),
                "Add Study Notes": lambda: self.add_study_notes(user_id),
                "Manage Content": lambda: self.manage_content(user_id),
                "Exit": lambda: "exit"
            }

            result = actions[action]()
            if result == "exit":
                break

    def study_topics(self, user_id: int):
        cert = self._select_certification()
        if not cert:
            return

        topics = self.session.query(Topic).filter_by(certification_id=cert.id).all()
        topic = questionary.select(
            "Select topic to study:",
            choices=[t.title for t in topics]
        ).ask()

        selected_topic = next(t for t in topics if t.title == topic)
        self.console.print(Panel(f"[bold]{selected_topic.title}[/bold]\n\n{selected_topic.content}"))
        
        duration = questionary.text("Study duration (minutes):").ask()
        comprehension = questionary.select(
            "How well did you understand this topic?",
            choices=["1 - Poor", "2 - Fair", "3 - Good", "4 - Very Good", "5 - Excellent"]
        ).ask()

        self.study_tracker.log_study_session(
            user_id=user_id,
            topic_id=selected_topic.id,
            duration=float(duration),
            comprehension=int(comprehension[0]),
            notes=""
        )

    def take_quiz(self, user_id: int):
        cert = self._select_certification()
        if not cert:
            return

        num_questions = questionary.text(
            "How many questions would you like?",
            default="5"
        ).ask()

        topics = self.session.query(Topic).filter_by(certification_id=cert.id).all()
        questions = []
        for topic in topics:
            questions.extend(self.quiz_generator.generate_questions(
                topic.id, 
                num_questions=int(num_questions) // len(topics)
            ))

        score = 0
        for i, q in enumerate(questions, 1):
            self.console.print(f"\n[bold]Question {i}:[/bold] {q['question']}")
            answer = questionary.text("Your answer:").ask()
            
            if answer.lower() == q['answer'].lower():
                self.console.print("[green]Correct![/green]")
                score += 1
            else:
                self.console.print(f"[red]Incorrect. The answer was: {q['answer']}[/red]")

        final_score = (score / len(questions)) * 100
        self.console.print(f"\n[bold]Final Score:[/bold] {final_score:.1f}%")

    def _select_certification(self):
        certs = self.session.query(Certification).all()
        if not certs:
            self.console.print("[red]No certifications available[/red]")
            return None

        cert_name = questionary.select(
            "Select certification:",
            choices=[c.name for c in certs]
        ).ask()

        return next(c for c in certs if c.name == cert_name)
