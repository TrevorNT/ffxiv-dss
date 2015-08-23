from spyne.protocol.json import JsonDocument
from spyne.application import Application
from spyne.server.wsgi import WsgiApplication

from dsservice.service import DSService

application = WsgiApplication(
	Application([DSService],
		tns = 'com.toryktech.dsservice',
		in_protocol = JsonDocument(validator = "soft"),
		out_protocol = JsonDocument(),
	)
)
