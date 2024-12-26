import peewee
from datetime import datetime

db = peewee.SqliteDatabase("data.db")


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    id = peewee.AutoField(primary_key=True)
    secret_key = peewee.CharField(unique=True, index=True)
    created_at = peewee.DateTimeField(default=datetime.now, index=True)
    is_active = peewee.BooleanField(default=True)

    def __str__(self):
        return f"User(id={self.id})"

    class Meta:
        table_name = "users"


class ImageProcessingResult(BaseModel):
    user = peewee.ForeignKeyField(
        User, backref="processing_results", on_delete="CASCADE"
    )
    openai_response = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.now, index=True)

    class Meta:
        table_name = "image_processing_results"


def create_tables():
    db.create_tables([User, ImageProcessingResult])

create_tables()
