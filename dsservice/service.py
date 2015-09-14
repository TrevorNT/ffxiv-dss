import logging
logging.basicConfig(level = logging.WARNING)

from spyne.service import ServiceBase
from spyne.decorator import rpc
from spyne.model.primitive import Unicode
from spyne.model.complex import Iterable, Array
from spyne.model.fault import Fault

from dsservice.types import DutyFilter, DutyInfo, DutyAllStrategies
from dsservice.database import Duty, DutyStrategy, makeSession

from hashlib import sha256

_duties = {}	# A dict with the prime key as the DutyCode.
				# The values of these keys are dicts that
				# map to the many values of the duty.  When
				# using AddDuty or any of the Set methods,
				# these entries must be updated as well as
				# the SQLite DB.

_dutyStrategies = {}	# A dict with the prime key as the DutyCode.
						# The values of these keys are dicts that
						# map to the four roles ('dps', 'tank',
						# 'healer' and 'misc') and their strategies.

_version = "0.0.1"

class DSService(ServiceBase):
	@rpc(_returns = Unicode)
	def alive(request):
		global _version
		return "FFX|V Duty Strategy Service, Version %s" % _version


##########


	@rpc(Array(DutyFilter), _returns = Iterable(Unicode))
	def FilterDutyCodes(request, dutyFilters):
		"""Filters the database of duties based on the given parameters.  The filtering is actually quite complex and will be documented in a separate...docstring.  You can pass it a blank array to just send everything back."""
		raise Fault("Not implemented.")


##########


	@rpc(Unicode, _returns = DutyInfo)
	def GetDutyInfo(request, dutyCode):
		"""Performs a lookup using the given dutyCode and returns all the miscellaneous (non-strategy) information it knows about that duty.  Throws an error if the code is not found."""
		raise Fault("Not implemented.")


##########


	@rpc(Unicode, Unicode, _returns = Unicode)
	def GetDutyStrategy(request, dutyCode, role):
		"""Gets the strategy for a single duty and role.  Throws an error if the dutyCode or role is not found.  Possible roles: "dps", "healer", "tank", "misc" (where misc returns data universal to all three jobs)."""
		raise Fault("Not implemented.")


##########


	@rpc(Unicode, _returns = DutyAllStrategies)
	def GetAllDutyStragegies(request, dutyCode):
		"""Gets strategies for all three roles for the given dutyCode.  Throws an error if the dutyCode is not found."""
		raise Fault("Not implemented.")


##########


	@rpc(Unicode, Unicode, Unicode, _returns = Unicode)
	def AddDuty(request, magicHash, dutyCode, dutyType):
		"""If you know the magicHash, allows you to add a duty to the database."""
		# Verification of the data
		if len(dutyCode) > 16:
			raise Fault(faultcode = "Client.DutyCode", faultstring = "Code is too long (must be <16 chars).")
		
		if not (dutyType == "dungeon" or dutyType == "trial" or dutyType == "raid" or dutyType == "guildhest" or dutyType == "roulette":
			raise Fault(faultcode = "Client.DutyType", faultstring = "Only the following values are allowed: 'dungeon', 'trial', 'raid', 'guildhest', 'roulette'.")
		
		# Verification of the hash
		if sha256(magicHash).hexdigest() == 'f43e52381d33c58a4362ebc646a4924b81448e4383dff916ebce8b4c1a4627bc':
			# Try to connect to the database
			try:
				sesh = makeSession()
			except:
				raise Fault(faultcode = "Server.SessionError", faultstring = "Database session creation failed.")
			
			# Try to add the duty
			try:
				newDuty = Duty(id = dutyCode, type = dutyType)
				sesh.add(newDuty)
			except:
				sesh.close()
				raise Fault(faultcode = "Server.DataError", faultstring = "Database was unable to create the new duty.")
			
			# Try to commit the data
			try:
				sesh.commit()
			except:
				sesh.rollback()
				sesh.close()
				raise Fault(faultcode = "Server.CommitError", faultstring = "Database was unable to commit the new duty.")
			
			# Add the duty to the master dict
			global _duties, _dutyStrategies
			_duties[dutyCode] = {}
			_dutyStrategies[dutyCode] = {}
			
			sesh.close()
			return "OK"
		else:
			raise Fault(faultcode = "Client.BadHash", faultstring = "Access denied due to incorrect magicHash.")


##########


	@rpc(Unicode, Unicode, Unicode, Unicode, _returns = Unicode)
	def SetDutyProperty(request, magicHash, dutyCode, propertyName, propertyValue):
		"""If you know the magicHash, allows you to set a duty's property (any of the miscellaneous fields, not strategy information)."""
		# Verification of the data
		if not dutyCode in _duties:
			raise Fault(faultcode = "Client.DutyCodeDoesNotExist", faultstring = "The given duty code does not exist.")
		
		if not propertyName in ["name", "description", "imageLocation", "receivedFromQuest", "isMainStory", "expansion", "levelMin", "levelMax", "iLevelMin", "iLevelSync", "roulette", "tomestoneType", "tomestonesAwarded", "xpRewarded", "gilRewarded", "partySize"]:
			raise Fault(faultcode = "Client.PropertyNameInvalid", faultstring = "The given property name is invalid.")
		
		# Verification of the hash
		if sha256(magicHash).hexdigest() == '17f7bd1bcd476d65105fd7cf4695a9bb608eaa37f2a213c34963b8d6511457af':
			# Try to connect to the database
			try:
				sesh = makeSession()
			except:
				raise Fault(faultcode = "Server.SessionError", faultstring = "Database session creation failed.")
			
			# Try to get the duty and change the property
			try:
				thisDuty = sesh.query(DutyCode).get(dutyCode)
				setattr(thisDuty, propertyName, propertyValue)
			except:
				sesh.close()
				raise Fault(faultcode = "Server.DataError", faultstring = "Database was unable to retrieve or update the duty.")
			
			# Try to commit the data
			try:
				sesh.commit()
			except:
				sesh.rollback()
				sesh.close()
				raise Fault(faultcode = "Server.CommitError", faultstring = "Database was unable to commit the new duty information.")
			
			# Change the property data in the local dict
			global _duties
			_duties[dutyCode][propertyName] = propertyValue
			
			sesh.close()
			return "OK"
		else:
			raise Fault(faultcode = "Client.BadHash", faultstring = "Access denied due to incorrect magicHash.")


##########


	@rpc(Unicode, Unicode, Unicode, Unicode, _returns = Unicode)
	def SetDutyStrategy(request, magicHash, dutyCode, role, strategy):
		"""If you know the magicHash, allows you to set strategy information for a given duty and job."""
		# Verification of the data
		if not dutyCode in _duties:
			raise Fault(faultcode = "Client.DutyCodeDoesNotExist", faultstring = "The given duty code does not exist.")
		
		if not role in ["tank", "healer", "dps", "misc"]:
			raise Fault(faultcode = "Client.RoleNameInvalid", faultstring = "The given role name is invalid.")
		
		# Verification of the hash
		if sha256(magicHash).hexdigest() == 'feb3de6cf791db25e757b1b89b99a990ee218b29da5e09afe2ae60dea869e84f':
			# Try to connect to the database
			try:
				sesh = makeSession()
			except:
				raise Fault(faultcode = "Server.SessionError", faultstring = "Database session creation failed.")
			
			# Try to add the duty strategy
			try:
				existingStrategy = sesh.query(DutyStrategy).get((dutyCode, dutyRole))
				if not existingStrategy:
					newStrategy = sesh.add(DutyStrategy(dutyId = dutyCode, role = dutyRole, strategy = strategy))
				else:
					setattr(existingStrategy, dutyRole, strategy)
			except:
				sesh.close()
				raise Fault(faultcode = "Server.DataError", faultstring = "Database was unable to create the new duty.")
			
			# Try to commit the data
			try:
				sesh.commit()
			except:
				sesh.rollback()
				sesh.close()
				raise Fault(faultcode = "Server.CommitError", faultstring = "Database was unable to commit the new duty.")
			
			# Add the duty to the master dict
			global _dutyStrategies
			_dutyStrategies[dutyCode][role] = strategy
			
			sesh.close()
			return "OK"
		else:
			raise Fault(faultcode = "Client.BadHash", faultstring = "Access denied due to incorrect magicHash.")
