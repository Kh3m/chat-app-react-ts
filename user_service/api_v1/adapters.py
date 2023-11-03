"""
Defines a customized Account Adapter for allauth
https://github.com/pennersr/django-allauth/blob/main/allauth/account/adapter.py#L174
"""

from allauth.account.adapter import DefaultAccountAdapter

from api_v1.events import publishers


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        """
        The default behavior of this function is to send an email.
        It is now overridden to publish an event instead.

        Instead of sending an email, this function publishes an event based on
        the context data provided. The specific event published depends on the
        content of the 'context' dictionary.

        If the 'context' dictionary includes an 'activate_url', nothing is done

        If the 'context' dictionary includes a 'password_reset_url', an event
            related to a password reset is published. This event contains the
            reset token and user ID.

        For other cases, where neither activation nor password reset is
        detected, the function sends the message using the default email
        sending mechanism.

        """
        if 'activate_url' in context:
            # Don't send email; email confirmation is handled
            # in signals
            pass

        elif 'password_reset_url' in context:
            reset_url_parts = context.get('password_reset_url').split('/')
            if reset_url_parts[-1] == '':
                reset_url_parts.pop()

            email = str(context['user'].email)
            token, uidb64 = reset_url_parts[-1], reset_url_parts[-2]
            publishers.publish_password_reset(email, token, uidb64)

        else:
            msg = self.render_mail(template_prefix, email, context)
            msg.send()
