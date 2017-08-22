from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Exercise, User

engine = create_engine('sqlite:///exercisecatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="Buff Dude", email="strongone@gmail.com", picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="Strong Chick", email="strongtwo@gmail.com", picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

#Catalog for Fat Loss Category
category1 = Category(name="Fat Loss")
session.add(category1)
session.commit()

exercise1 = Exercise(name="Walking", description="Something you do every day. Do it right!", url="https://www.youtube.com/embed/-fD2TSL2s7I", category=category1)
session.add(exercise1)
session.commit()

exercise2 = Exercise(name="Elliptical", description="A great machine to transition from walking to running.", url="https://www.youtube.com/embed/gpxUeHJ-Ps0", category=category1)
session.add(exercise2)
session.commit()

exercise3 = Exercise(name="Rowing", description="Perfect for cardio while using the back and hips.", url="https://www.youtube.com/embed/H0r_ZPXJLtg", category=category1)
session.add(exercise3)
session.commit()

exercise4 = Exercise(name="Running", description="Classic exercise that few know with proper technique.", url="https://www.youtube.com/embed/8XiwtiDTlYU", category=category1)
session.add(exercise4)
session.commit()

#Catalog for Muscle Gain Category
category2 = Category(name="Muscle Gain")
session.add(category2)
session.commit()

exercise1 = Exercise(name="Kettlebell Swings", description="A simple tool to add strength and build the posterior chain.", url="https://www.youtube.com/embed/-KqxcDijOyA", category=category2)
session.add(exercise1)
session.commit()

exercise2 = Exercise(name="Myotatic Crunch", description="Killer ab exercise that full stretches muscles for maximum gain.", url="https://www.youtube.com/embed/p7SnVdkx9do", category=category2)
session.add(exercise2)
session.commit()

exercise3 = Exercise(name="Side Plank", description="Balance the body by working the oblique abs.", url="https://www.youtube.com/embed/HgaRSh7pLro", category=category2)
session.add(exercise3)
session.commit()

exercise4 = Exercise(name="Glute Bridge", description="Active the glutes to strength the posterior chain.", url="https://www.youtube.com/embed/WowARnE-p0s", category=category2)
session.add(exercise4)
session.commit()

exercise5 = Exercise(name="Front Squat to Push Press", description="Develop explosive motion in hips while strengthen entire body.", url="https://www.youtube.com/embed/dP4SjMwFIRk", category=category2)
session.add(exercise5)
session.commit()

#Catalog for Strength Gain Category
category3 = Category(name="Strength Gain")
session.add(category3)
session.commit()

exercise1 = Exercise(name="Deadlift", description="Lift something heavy from the ground.", url="https://www.youtube.com/embed/UyRiw2b8yI4", category=category3)
session.add(exercise1)
session.commit()

exercise2 = Exercise(name="Push Up", description="Another classic exercise. Let's dust it off with good form.", url="https://www.youtube.com/embed/zF0jbubK_jU", category=category3)
session.add(exercise2)
session.commit()

exercise3 = Exercise(name="The Torture Twist", description="Isometric strength in abs while working obliques as well.", url="https://www.youtube.com/embed/g_16Gp01zZM", category=category3)
session.add(exercise3)
session.commit()

exercise4 = Exercise(name="Sprints", description="Run. Run real fast.", url="https://www.youtube.com/embed/kQfXgIAcl0M", category=category3)
session.add(exercise4)
session.commit()

#Catalog for Well Being Category
category4 = Category(name="Well Being")
session.add(category4)
session.commit()

exercise1 = Exercise(name="Downward Dog", description="Foundational Yoga movement you will do over and over. Get it right.", url="https://www.youtube.com/embed/W12PdhF5AuE", category=category4)
session.add(exercise1)
session.commit()

exercise2 = Exercise(name="Relaxed Breathing", description="Reduce anxiety and find calm.", url="https://www.youtube.com/embed/Apkg1cKDyyA", category=category4)
session.add(exercise2)
session.commit()

print("exercises have been added :)")
