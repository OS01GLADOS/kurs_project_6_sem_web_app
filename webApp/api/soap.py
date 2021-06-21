from spyne import  Application, rpc, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
from spyne.service import Service

from webApp.models import Message


class NewFeedbackService(Service):
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def create_feedback_fom_soap(ctx, email, title, message):
        message = Message(Email=email, header=title, Message=message)
        message.save()
        print(email, title, message, sep=" _ ")
        return "message created"

app = Application([NewFeedbackService],
    'spyne.django',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11(),
                  )

hello_world_service = csrf_exempt(DjangoApplication(app))