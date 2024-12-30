import random
from typing import List, Dict
from models import Topic, Flashcard
from sqlalchemy.orm import Session

class QuizGenerator:
    def __init__(self, db_session: Session):
        self.session = db_session

    def generate_questions(self, topic_id: int, num_questions: int = 5) -> List[Dict]:
        topic = self.session.query(Topic).get(topic_id)
        flashcards = topic.flashcards
        
        if len(flashcards) < num_questions:
            return self._generate_from_content(topic, num_questions)
        
        selected_cards = random.sample(flashcards, num_questions)
        return [{'question': card.question, 'answer': card.answer} 
                for card in selected_cards]

    def _generate_from_content(self, topic: Topic, num_questions: int) -> List[Dict]:
        sentences = topic.content.split('.')
        questions = []
        
        for _ in range(min(num_questions, len(sentences))):
            sentence = random.choice(sentences)
            words = sentence.split()
            if len(words) < 3:
                continue
            
            key_word = random.choice(words)
            question = sentence.replace(key_word, '_____')
            questions.append({
                'question': question,
                'answer': key_word
            })
        
        return questions
