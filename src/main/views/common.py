import logging

from django.shortcuts import render
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


def server_error_view(request):
    """When a server error is encountered (code 500), the error gets logged and users see an error id
    :param request: HTTP request
    :return:
    """
    error_code = get_random_string(length=8)
    context = {'error_code': error_code}
    logger.exception("An unknown application error (500) has been encountered", extra={'error_code': error_code})
    return render(request, template_name='500.html', context=context, status=500)


def permission_denied_view(request, exception):
    logger.warning(str(exception), extra={'user': request.user.username, 'path': request.get_full_path_info()})
    return render(request, template_name='403.html', status=403)
