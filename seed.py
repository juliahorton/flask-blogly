"""Seed file to make sample data for Blogly database."""

from app import app
from models import db, User

# Create all tables within the application context
app.app_context().push()
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
user_1 = User(first_name="Vic", last_name="Fuentes", image_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmn2s-content.s3.eu-west-2.amazonaws.com%2Fwp-content%2Fuploads%2F2020%2F11%2F27170246%2Fvic-fuentes-MN2S.jpg&f=1&nofb=1&ipt=3fe491922e4d9dd205d23923e1ec074f826805326cfa2cbb44d96d74a354d8ab&ipo=images")
user_2 = User(first_name="Dasha", last_name="Redscare", image_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstarktimes.com%2Fwp-content%2Fuploads%2F2022%2F04%2FDasha-Nekrasova1-1024x786.jpg&f=1&nofb=1&ipt=20059db6838d2ae994e842e4328aa56fc28aa6f8ef8ff6759790fbe0bf6b6ec8&ipo=images")
user_3 = User(first_name="Chet", last_name="Hoemath")
user_4 = User(first_name="Mitski", last_name="Genius", image_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flastfm.freetls.fastly.net%2Fi%2Fu%2F770x0%2F46122caa7b21d80faa8a3f1c021fee9b.jpg%2346122caa7b21d80faa8a3f1c021fee9b&f=1&nofb=1&ipt=39e4fd0ebdd5e0c9c1fb08415d3a08640dd50390185b6a19f2d239c054c9c4d5&ipo=images")
user_5 = User(first_name="Kellin", last_name="Quinn", image_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.genius.com%2F87b00efc13e0fc58b334b2c38679f5d5.1000x1000x1.jpg&f=1&nofb=1&ipt=32b9df125139d6c161e289d38bda96497771183b4b787515b2cff1a1f3269b02&ipo=images")


# Add new objects to session
db.session.add(user_1)
db.session.add(user_2)
db.session.add(user_3)
db.session.add(user_4)
db.session.add(user_5)

# Commit
db.session.commit()
