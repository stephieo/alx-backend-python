from sqlalchemy import create_engine, Column, String, 
from sqlalchemy.dialects.mysql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker


def connect_db():
    """ connects  to a a myssql databases server
    returns:

    """
    engine = create_engine(mysql+mysqldb://ife:deputy@localhost:3306/ALX_prodev)
    Session = sessionmaker(bind=engine)
    session = Session()
    return sessions



def create_database(connection):
    """ creates the ALX_prodev database"""
   
    

def connect_to_prodev():
    """connects to the ALX_prodev database
    returns:
            """

def create_table(connection):
    """creates a table 'user_data' if not existing"""
    Base = declarative_base()
     class UserData(Base):
        """the user_data table in the datatbase"""
        __tablename__ = 'user_data'
        user_id = Column(UUID, primary_key=True, index=True)
        name = Column(String, nullable=false)
        email = Column(String, nullable=false)
        age = Column(Decimal(10,2))
    
    Base.metadata.create_all(engine)
    

def insert_data(connection, data):
    """inserts data inthe database if non-existent"""