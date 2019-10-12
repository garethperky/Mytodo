from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

from .models import Todo

def send_push_function(token, message, extra=None):
    try:
        response = PushClient().publish(PushMessage(to=token, body=message, data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        rollbar.report_exc_info(
            extra_data={
                "token": token,
                "message": message,
                "extra": extra,
                "errors": exc.errors,
                "response_data": exc.response_data,
            }
        )
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        rollbar.report_exc_info(
            extra_data={"token": token, "message": message, "extra": extra}
        )
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken

        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        rollbar.report_exc_info(
            extra_data={
                "token": token,
                "message": message,
                "extra": extra,
                "push_response": exc.push_response._asdict(),
            }
        )
        raise self.retry(exc=exc)


class PushTokenAdmin(admin.ModelAdmin):  # add this
      list_display = ('title', 'description', 'completed')
      actions = ['send_out_push']

      def send_out_push(self, request, queryset):
        if 'apply' in request.POST:
          for pushtoken in queryset:
            token = "ExponentPushToken[vc0tz-PHnUdm6R07miyPzF]"
            push_message = request.POST['your_message']
            message = request.POST['your_message']
            queryset.update(description=push_message)
            send_push_function(token, message, extra=None)

            self.message_user(request,
                              "Changed status on {} orders".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request,
                      'order_intermediate.html',
                      context={'users':queryset})
      send_out_push.short_description = "Send Push Notifications"




admin.site.register(Todo, PushTokenAdmin)
