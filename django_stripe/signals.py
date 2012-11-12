from django.dispatch import Signal

sSignal = Signal(providing_args=['message'])

upcoming_invoice_updated = sSignal
invoice_updated = sSignal

# Webhooks
sSignal = sSignal

recurring_payment_failed = sSignal

invoice_ready = sSignal

recurring_payment_succeeded = sSignal

subscription_trial_ending = sSignal

subscription_final_payment_attempt_failed = sSignal

ping = Signal()

stripe_broadcast_signal = sSignal

class StripeWebhook(object):
    pass
