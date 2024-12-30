from datetime import datetime, timedelta
from typing import List, Dict
from models import User, StudySession, Topic, QuizResult
from sqlalchemy.orm import Session
import matplotlib.pyplot as plt
import io

class StudyTracker:
    def __init__(self, db_session: Session):
        self.session = db_session

    def log_study_session(self, user_id: int, topic_id: int, 
                         duration: float, comprehension: int, notes: str = ""):
        session = StudySession(
            user_id=user_id,
            topic_id=topic_id,
            duration=duration,
            comprehension_rating=comprehension,
            notes=notes
        )
        self.session.add(session)
        self.session.commit()

    def get_study_statistics(self, user_id: int) -> Dict:
        user = self.session.query(User).get(user_id)
        sessions = user.study_sessions
        
        total_time = sum(session.duration for session in sessions)
        avg_comprehension = sum(session.comprehension_rating for session in sessions) / len(sessions) if sessions else 0
        
        return {
            'total_study_time': total_time,
            'average_comprehension': avg_comprehension,
            'total_sessions': len(sessions),
            'topics_covered': len(set(session.topic_id for session in sessions))
        }

    def generate_progress_chart(self, user_id: int) -> bytes:
        user = self.session.query(User).get(user_id)
        quiz_results = user.quiz_results
        
        dates = [result.date for result in quiz_results]
        scores = [result.score for result in quiz_results]
        
        plt.figure(figsize=(10, 6))
        plt.plot(dates, scores, marker='o')
        plt.title('Quiz Performance Over Time')
        plt.xlabel('Date')
        plt.ylabel('Score (%)')
        plt.grid(True)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf.getvalue()
