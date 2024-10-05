from app import db

class datafilter(db.Model):
    __tablename__ = "artist"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"DataFilter(title={self.name})"