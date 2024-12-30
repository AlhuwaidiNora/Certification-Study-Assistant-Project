# Certification Study Assistant

A Python-based study assistant to help prepare for professional certifications like PMP and ISTQB.

## Features
- Study material management
- Quiz generation
- Progress tracking
- Flashcard system
- Performance analytics

## Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`

## Usage
Run `python main.py` to start the application.

## Project Structure
```
certification_assistant/
├── src/
│   ├── database.py - Database configuration
│   ├── models.py - Data models
│   ├── quiz_generator.py - Quiz functionality
│   ├── study_tracker.py - Progress tracking
│   └── ui.py - User interface
├── data/
│   ├── pmp_content.json - PMP study content
│   └── istqb_content.json - ISTQB study content
└── main.py - Main application entry
```
