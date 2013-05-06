from stripe import convert_to_stripe_object

from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, FormView

from .settings import STRIPE_SECRET_KEY
from .forms import CardTokenForm
from .signals import (recurring_payment_failed, invoice_ready, \
    recurring_payment_succeeded, subscription_trial_ending, \
    subscription_final_payment_attempt_failed, ping, StripeWebhook, \
    stripe_broadcast_signal, sSignal)

class BaseCardTokenFormView(FormView):
    template_name = 'django_stripe/card_form.html'
    form_class = CardTokenForm

    def get_last4(self):
        return None

    def get_form_kwargs(self):
        kwargs = super(BaseCardTokenFormView, self).get_form_kwargs()
        kwargs.update({
            'initial': {
                'last4': self.get_last4(),
            }
        })

        return kwargs

class WebhookSignalView(View):
    http_method_names = ['post']
    event_signals = {
        'invoice.payment_failed': recurring_payment_failed,
        'invoice.payment_succeeded': recurring_payment_succeeded,
        'invoice.created': invoice_ready,
        'customer.subscription.trial_will_end': subscription_trial_ending,
        'charge.failed': subscription_final_payment_attempt_failed,
        'ping': ping,
    }

    def post(self, request, *args, **kwargs):

        #View accepts only POST, so:
        post = request.raw_post_data

        try:
            message = json.loads(post)
        except Exception:
            # writting to logs wrong json
            f = open('/tmp/err_log', 'w+')
            f.write(request.body)
            f.write('\n')
            f.write(str(request.POST))
            f.write('\n')
            f.write(str(post))
            f.write('\nend\n')
            f.close()
            #Make that admins know about err
            raise

        event = message.get('type')
        del message['type']

        if event not in self.event_signals:
            return HttpResponse()

        msg = {'type':event}
        for key, value in message.iteritems():
            if isinstance(value, dict) and 'object' in value:
                msg[key] = convert_to_stripe_object(value, STRIPE_SECRET_KEY)
        msg = {'message':msg}
        signal = self.event_signals.get(event, sSignal)
        signal.send_robust(sender=StripeWebhook, **msg)
        stripe_broadcast_signal.send_robust(sender=StripeWebhook, **msg)

        return HttpResponse()

webhook_to_signal = csrf_exempt(WebhookSignalView.as_view())
