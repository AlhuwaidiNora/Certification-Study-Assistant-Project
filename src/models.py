from database import Base, engine
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    study_sessions = relationship("StudySession", back_populates="user")
    quiz_results = relationship("QuizResult", back_populates="user")

class Certification(Base):
    __tablename__ = 'certifications'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    topics = relationship("Topic", back_populates="certification")

class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    certification_id = Column(Integer, ForeignKey('certifications.id'))
    title = Column(String)
    content = Column(String)
    importance = Column(String)
    certification = relationship("Certification", back_populates="topics")
    flashcards = relationship("Flashcard", back_populates="topic")

class Flashcard(Base):
    __tablename__ = 'flashcards'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    question = Column(String)
    answer = Column(String)
    topic = relationship("Topic", back_populates="flashcards")

class StudySession(Base):
    __tablename__ = 'study_sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    duration = Column(Float)  # in minutes
    comprehension_rating = Column(Integer)  # 1-5
    notes = Column(String)
    user = relationship("User", back_populates="study_sessions")

class QuizResult(Base):
    __tablename__ = 'quiz_results'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    score = Column(Float)
    total_questions = Column(Integer)
    certification_id = Column(Integer, ForeignKey('certifications.id'))
    user = relationship("User", back_populates="quiz_results")
