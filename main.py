from src.database import engine, Session
from src.models import Base, User, Certification, Topic
from src.ui import UI
import questionary
from rich import print as rprint
from rich.panel import Panel

def initialize_database():
    Base.metadata.create_all(engine)
    session = Session()
    
    # Add default certifications if they don't exist
    for cert_name in ["PMP", "ISTQB"]:
        if not session.query(Certification).filter_by(name=cert_name).first():
            cert = Certification(name=cert_name)
            session.add(cert)
    
    session.commit()
    return session

def main():
    session = initialize_database()
    
    rprint(Panel.fit(
        "[bold blue]Certification Study Assistant[/bold blue]\n"
        "Your personal certification prep companion",
        border_style="blue"
    ))
    
    # Simple user management
    username = questionary.text("Enter your username:").ask()
    user = session.query(User).filter_by(username=username).first()
    if not user:
        user = User(username=username)
        session.add(user)
        session.commit()
    
    ui = UI(session)
    ui.main_menu(user.id)

if __name__ == "__main__":
    main()
