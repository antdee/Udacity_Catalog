#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Room, Base, Product, User

engine = create_engine('sqlite:///furniture.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

room1 = Room(name="Bedroom")
session.add(room1)
session.commit()

room1 = Room(name="Living_room")
session.add(room1)
session.commit()

room1 = Room(name="Kitchen")
session.add(room1)
session.commit()

room1 = Room(name="Dining")
session.add(room1)
session.commit()

room1 = Room(name="Bathroom")
session.add(room1)
session.commit()

room1 = Room(name="Outdoor")
session.add(room1)
session.commit()


product = Product(name="Bunk bed frame", 
				  description="Made of solid wood, which is a hardwearing and warm natural material.", 
				  price="130", 
				  room="Bedroom",
				  image="https://goo.gl/NV3kQZ",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Bed frame", 
				  description="16 slats of layer-glued birch adjust to your body weight and increase the suppleness of the mattress.", 
				  price="125", 
				  room="Bedroom",
				  image="https://goo.gl/JfbVnd",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Single Bed frame", 
				  description="Made of solid wood, which is a hardwearing and warm natural material. Adjustable bed sides allow you to use mattresses of different thicknesses.", 
				  price="165", 
				  room="Bedroom",
				  image="https://goo.gl/7PjGQT",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Underbed with storage", 
				  description="The underbed is perfect to roll out when a friend sleeps over and there's room for both bedlinens and toys in the 2 drawers.", 
				  price="175", 
				  room="Bedroom",
				  image="https://goo.gl/scxmQ7",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Mirror cab 2 door/built-in lighting", 
				  description="The LED lightsource consumes up to 85% less energy and lasts 20 times longer than incandescent bulbs.", 
				  price="250", 
				  room="Bathroom",
				  image="https://goo.gl/Ngb55c",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="High cabinet with mirror door", 
				  description="You can mount the door to open from the right or left.", 
				  price="120", 
				  room="Bathroom",
				  image="https://goo.gl/e53FNk",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Single wash-basin", 
				  description="10 year guarantee. Read about the terms in the guarantee brochure.", 
				  price="150", 
				  room="Bathroom",
				  image="https://goo.gl/MefysC",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()


product = Product(name="Wash-stand with 2 drawers", 
				  description="Drawers made of solid wood, with bottom in scratch-resistant melamine.", 
				  price="350", 
				  room="Bathroom",
				  image="https://goo.gl/EF891y",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Pendant lamp", 
				  description="You can easily switch between a brighter general light and a softer mood light by just pulling the strings.", 
				  price="110", 
				  room="Dining",
				  image="https://goo.gl/ZseYsw",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Storage combination w doors/drawers", 
				  description="The door's integrated dampers enable it to close slowly, silently and softly. The shelves are adjustable so you can customise your storage as needed.", 
				  price="795", 
				  room="Dining",
				  image="https://goo.gl/1CV87n",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Chair with armrests", 
				  description="Perfect for long dinners since the length and height of the armrests, the angle of the backrest and the extra thick seat make the chair comfortable to sit on.", 
				  price="95", 
				  room="Dining",
				  image="https://goo.gl/52kNSh",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Table and 4 chairs", 
				  description="Every table is unique, with varying grain pattern and natural colour shifts that are part of the charm of wood.", 
				  price="660", 
				  room="Dining",
				  image="https://goo.gl/dkVbd8",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="18-piece service", 
				  description="Dinnerware that combines a simple, rustic design with a soft ruffled edge. It allows you to coordinate ARV with other porcelain to get different characters in your table settings.", 
				  price="45", 
				  room="Kitchen",
				  image="https://goo.gl/sdeFf1",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Dish drainer", 
				  description="Holds large plates with a dia. up to 32 cm as well.", 
				  price="15", 
				  room="Kitchen",
				  image="https://goo.gl/x4wNRL",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Loose-base cake tin", 
				  description="Anodised aluminium gives the baking tin an extra durable and hard-wearing surface, so that you can keep baking for years.", 
				  price="10", 
				  room="Kitchen",
				  image="https://goo.gl/7YrHFn",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()

product = Product(name="Touch top bin", 
				  description="You open the waste bin easily by pressing lightly on the top of the lid.", 
				  price="30", 
				  room="Kitchen",
				  image="https://goo.gl/GMnQNY",
				  user_id="1",
				  user_picture="https://goo.gl/5BEJBs")
session.add(product)
session.commit()
