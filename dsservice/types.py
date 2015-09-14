from spyne.model.complex import ComplexModel
from spyne.model.primitive import Unicode, Integer, Boolean, Decimal

class DutyFilter(ComplexModel):
	dutyProperty = Unicode
	propertyValue = Unicode

class DutyInfo(ComplexModel):
	code = Unicode					# aka dutyCode
	name = Unicode
	description = Unicode
	imageLocation = Unicode			# for if/when the site starts serving images?
	receivedFromQuest = Unicode		# name of quest
	isMainStory = Boolean
	expansion = Integer				# currently either 2 or 3; the filter accepts (case-insensitively) any of the following: "v2", "2.0", "v2.0", "2", "ARR", "RR", "Realm Reborn", or "A Realm Reborn"; or "v3", "3.0", "v3.0", "3", "HVN", or "Heavensward"
	levelMin = Integer				# below this level, you can't get in
	levelMax = Integer				# above this level, you sync to this level
	iLevelMin = Integer
	iLevelSync = Integer			# not iLevelMax because any gear above the *min* suddenly becomes this sync amount
	roulette = Unicode				# values are "Leveling", "High Level", "Expert", "Trials", "Guildhests", "Main Scenario", or just leaving it blank for none
	tomestoneType = Unicode			# values are "Poetics", "Law", "Esoterics", or whatever...you know how often they change; or leave blank for none
	tomestonesRewarded = Integer
	xpRewarded = Integer			# guildhests
	gilRewarded = Integer			# still guildhests
	partySize = Integer				# 4 == light party, 8 == full party, 24 == full raid
	
	def __init__(self, code, info):
		self.code = code
		self.name = info["name"]
		self.description = info["description"]
		self.imageLocation = info["imageLocation"]
		self.receivedFromQuest = info["receivedFromQuest"]
		self.isMainStory = info["isMainStory"]
		self.expansion = info["expansion"]
		self.levelMin = info["levelMin"]
		self.levelMax = info["levelMax"]
		self.iLevelMin = info["iLevelMin"]
		self.iLevelSync = info["iLevelSync"]
		self.roulette = info["roulette"]
		self.tomestoneType = info["tomestoneType"]
		self.tomestonesRewarded = info["tomestonesRewarded"]
		self.xpRewarded = info["xpRewarded"]
		self.gilRewarded = info["gilRewarded"]
		self.partySize = info["partySize"]

class DutyAllStrategies(ComplexModel):
	tank = Unicode
	dps = Unicode
	healer = Unicode
	misc = Unicode
	
	def __init__(self, info):
		if "tank" in info:
			self.tank = info["tank"]
		if "dps" in info:
			self.dps = info["dps"]
		if "healer" in info:
			self.healer = info["healer"]
		if "misc" in info:
			self.misc = info["misc"]
