import uuid
import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User

print("___ adding admin __")
try:
    user = User(
        public_id=str(uuid.uuid4()),
        name='Admin',
        password=generate_password_hash('1234', method='sha256'),
        date_joined=dt.datetime.utcnow(),
        is_admin=True
    )

    db.session.add(user)
    db.session.commit()
    db.session.close()

    print("___ admin created __")

except:
    print("COULD NOT CREATE ADMIN")


