from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

user1 = User(first_name="Bob", last_name="Beltcher")
user2 = User(
    first_name="Rick",
    last_name="Sanchez",
    img_url="https://cdn.dribbble.com/users/5592443/screenshots/14279501/media/03a05059cbfbc4ed313162fff2476111.png?compress=1&resize=800x600",
)
user3 = User(
    first_name="Stewie",
    last_name="Griffin",
    img_url="https://www.thefactsite.com/wp-content/uploads/2012/11/stewie-griffin-facts.webp",
)
user4 = User(
    first_name="Michael",
    last_name="Scott",
    img_url="https://miro.medium.com/max/500/1*xDIevNE7HEMiJQVTYg0qDQ.png",
)
user5 = User(first_name="Jim", last_name="Halpert")


db.session.add_all([user1, user2, user3, user4, user5])
db.session.commit()
