import logging
logging.basicConfig(level = logging.WARNING)

from spyne.service import ServiceBase
from spyne.decorator import rpc
from spyne.model.primitive import Unicode
from spyne.model.complex import Iterable, Array
from spyne.model.fault import Fault

from dsservice.types import DutyFilter, DutyInfo, DutyAllStrategies

_version = "0.0.1"

class DSService(ServiceBase):
	@rpc(_returns = Unicode)
	def alive(request):
		global _version
		return "FFX|V Duty Strategy Service, Version %s" % _version



	@rpc(Array(DutyFilter), _returns = Iterable(Unicode))
	def FilterDutyCodes(request, dutyFilters):
		"""Filters the database of duties based on the given parameters.  The filtering is actually quite complex and will be documented in a separate...docstring.  You can pass it a blank array to just send everything back."""
		raise Fault("Not implemented.")



	@rpc(Unicode, _returns = DutyInfo)
	def GetDutyInfo(request, dutyCode):
		"""Performs a lookup using the given dutyCode and returns all the miscellaneous (non-strategy) information it knows about that duty.  Throws an error if the code is not found."""
		raise Fault("Not implemented.")



	@rpc(Unicode, Unicode, _returns = Unicode)
	def GetDutyStrategy(request, dutyCode, role):
		"""Gets the strategy for a single duty and role.  Throws an error if the dutyCode or role is not found.  Possible roles: "dps", "healer", "tank", "misc" (where misc returns data universal to all three jobs)."""
		raise Fault("Not implemented.")



	@rpc(Unicode, _returns = DutyAllStrategies)
	def GetAllDutyStragegies(request, dutyCode):
		"""Gets strategies for all three roles for the given dutyCode.  Throws an error if the dutyCode is not found."""
		raise Fault("Not implemented.")



	@rpc(Unicode, Unicode, Unicode, _returns = Unicode)
	def AddDuty(request, magicHash, dutyCode, dutyType):
		"""If you know the magicHash, allows you to add a duty to the database."""
		raise Fault("Not implemented.")



	@rpc(Unicode, Unicode, Unicode, Unicode, _returns = Unicode)
	def SetDutyProperty(request, magicHash, dutyCode, propertyName, propertyValue):
		"""If you know the magicHash, allows you to set a duty's property (any of the miscellaneous fields, not strategy information)."""
		raise Fault("Not implemented.")



	@rpc(Unicode, Unicode, Unicode, Unicode, _returns = Unicode)
	def SetDutyStrategy(request, magicHash, dutyCode, role, strategy):
		"""If you know the magicHash, allows you to set strategy information for a given duty and job."""
		raise Fault("Not implemented.")
