from sqlalchemy.orm import sessionmaker
from dbmodel import *

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

user1 = Users(name='Augustin', login='augus', password='qwe123QWE', email='ap@gmail.com',userStatus = "admin",locationId=1)
user2 = Users(name='Lfd', login='lav', password='pirate', email='gaskjglasf@gmail.com', userStatus="user",locationId=2)
session.add(user1)
session.add(user2)
session.flush()

advertisement1 = Advertisement(name = "fadas",protectedStatus = 0,)
advertisement2 = Advertisement(name = "fadafgs",protectedStatus = 1,)
session.add(advertisement2)
session.add(advertisement1)
session.flush()

message1 = Message(text = " 31fsadfsf",advertisement_id=advertisement1.id)
message2 = Message(text = " 7fsadfsf",advertisement_id=advertisement2.id)
# message3 = Message(text = " 5fsadfsf",advertisement_id=advertisement1.id)
# message4 = Message(text = " 4fsadfsf",advertisemnt_id =advertisement2.id)
#message5 = Message(text = " 2fsadfsf",advertisemnt_id =advertisement2.id)
session.add(message1)
session.add(message2)
# session.add(message3)
# session.add(message4)
#session.add(message5)
session.flush()

location1 = Location(location_id = user1.id,advertisement_id = advertisement1.id)
location2 = Location(location_id = user2.id,advertisement_id = advertisement2.id)
session.add(location1)
session.add(location2)
session.flush()

session.commit()
