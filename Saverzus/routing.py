from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path

from chat.consumers import ChatConsumer
from public_chat.consumers import PublicChatConsumer



application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
            
			URLRouter([
				re_path(r'public_chat/(?P<room_id>\w+)/$', PublicChatConsumer),
				re_path(r'chat/(?P<room_id>\w+)/$', ChatConsumer),
			])
            
		)
	),
})