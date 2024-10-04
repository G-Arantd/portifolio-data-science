from app import db

class datafilter(db.Model):
    __tablename__ = "datafilter"
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(200), nullable=False)
    artist: str = db.Column(db.String(200), nullable=False)
    region: str = db.Column(db.String(200), nullable=False)
    streams: int = db.Column(db.Integer)

    def __init__(self, title: str, artist:str, region:str, streams:int) -> None:
        self.title = title
        self.artist = artist
        self.region = region
        self.streams = streams

    def __repr__(self) -> str:
        return f"DataFilter(title={self.title}, artist={self.artist}, region={self.region}, streams={self.streams})"