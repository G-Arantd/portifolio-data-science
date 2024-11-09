from app import db

class Database(db.Model):
    __tablename__ = 'data'

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(255), nullable=False) 
    date: str = db.Column(db.String(7), nullable=False)  # Format: YYYY-MM
    artist: str = db.Column(db.String(255), nullable=False)
    region: str = db.Column(db.String(255), nullable=False)
    streams: float = db.Column(db.Float, nullable=False)

    def __init__(self, title, date, artist, region, streams):
        self.title = title
        self.date = date[:7]
        self.artist = artist
        self.region = region
        self.streams = streams
        
    def __repr__(self):
        return f"{self.title} - {self.artist} - {self.region} - {self.streams}"