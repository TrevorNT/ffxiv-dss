from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_engine = create_engine('sqlite:///dss.sqlite3.db')
_tableBase = declarative_base()

#class DutyCode(_tableBase):
#	__tablename__ = 'dutycodes'
#	
#	id = Column(String(16), primary_key = True)
#	dutyType = Column(String(16), nullable = False)
#	
#	def __repr__(self):
#		return "<DutyCode(id='%s', dutyType='%s')>" % (self.id, self.dutyType)
#	
#	def __str__(self):
#		return "<DutyCode: %s>" % self.id

class Duty(_tableBase):
	__tablename__ = 'duties'

#	id = Column(String(16), ForeignKey("dutycodes.id"), primary_key = True)
	id = Column(String(16), primary_key = True)
	type = Column(String(16), nullable = False)
	name = Column(String)
	description = Column(String)
	imageLocation = Column(String)
	receivedFromQuest = Column(String)
	isMainStory = Column(Boolean)
	expansion = Column(Integer)
	levelMin = Column(Integer)
	levelMax = Column(Integer)
	iLevelMin = Column(Integer)
	iLevelSync = Column(Integer)
	roulette = Column(String)
	tomestoneType = Column(String)
	tomestonesRewarded = Column(Integer)
	xpRewarded = Column(Integer)
	gilRewarded = Column(Integer)
	partySize = Column(Integer)
	
	def __repr__(self):
		return "<Duty(id='%s', name='%s', description='%s', imageLocation='%s', receivedFromQuest='%s', isMainStory='%s', expansion=%d, levelMin=%d, levelMax=%d, iLevelMin=%d, iLevelSync=%d, roulette='%s', tomestoneType='%s', tomestonesRewarded=%d, xpRewarded=%d, gilRewarded=%d, partySize=%d)>" % (self.id, self.name, self.description, self.imageLocation, self.receivedFromQuest, str(self.isMainStory), self.expansion, self.levelMin, self.levelMax, self.iLevelMin, self.iLevelSync, self.roulette, self.tomestoneType, self.tomestonesRewarded, self.xpRewarded, self.gilRewarded, self.partySize)
	
	def __str__(self):
		return "<Duty Name: %s, ID: %s>" % (self.name, self.id)



class DutyStrategy(_tableBase):
	__tablename__ = 'duty_strategies'
	
#	dutyId = Column(String(16), ForeignKey("dutycodes.id"), primary_key = True)
	dutyId = Column(String(16), ForeignKey("duties.id"), primary_key = True)
	role = Column(String(16), primary_key = True)
	strategy = Column(String)
	
	def __repr__(self):
		return "<DutyStrategy(dutyId='%s', role='%s', strategy='%s')>" % (self.dutyId, self.role, self.strategy)
	
	def __str__(self):
		return "<Duty Strategy for id %s, role %s>" % (self.dutyId, self.role)



def makeSession():
	return sessionmaker(bind = _engine)
