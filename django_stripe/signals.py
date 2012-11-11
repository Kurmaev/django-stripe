from django.dispatch import Signal

upcoming_invoice_updated = Signal(providing_args=['customer'])
invoice_updated = Signal(providing_args=['invoice'])

# Webhooks
recurring_payment_failed = Signal(providing_args=[
    'customer',
    'attempt',
    'invoice',
    'payment',
    'livemode',
])

invoice_ready = Signal(providing_args=[
    'customer',
    'invoice'
])

recurring_payment_succeeded = Signal(providing_args=[
    'customer',
    'invoice',
    'payment',
    'livemode',
])

subscription_trial_ending = Signal(providing_args=[
    'customer',
    'subscription',
])

subscription_final_payment_attempt_failed = Signal(providing_args=[
    'customer',
    'subscription',
])

ping = Signal()

stripe_broadcast_signal = Signal(providing_args=['message'])

class StripeWebhook(object):
    pass
