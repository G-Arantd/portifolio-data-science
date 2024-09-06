from app import db

class DataFilter(db.Model):
    __tablename__ = "data_filter"
    id: int = db.Column(db.Integer, primary_key=True)
    rank: int = db.Column(db.Integer, nullable=False)
    title: str = db.Column(db.String(100), nullable=False)
    artist: str = db.Column(db.String(100), nullable=False)
    region: str = db.Column(db.String(100), nullable=False)
    streams: int = db.Column(db.Integer)

    def __init__(self, rank: int, title: str, artist:str, region:str, streams:int) -> None:
        self.rank = rank
        self.title = title
        self.artist = artist
        self.region = region
        self.streams = streams

    def __repr__(self) -> str:
        return f"DataFilter(rank={self.rank}, title={self.title}, artist={self.artist}, region={self.region}, streams={self.streams})"