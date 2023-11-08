from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator


class ResponseHandler(models.Model):

    URL_MAX_LENGTH = 2000
    NAME_MAX_LENGTH = 200

    url = models.CharField(max_length=URL_MAX_LENGTH,
                           verbose_name=_('URL'),
                           help_text=_('Url which the response handler will answer, this can be valid url with no FQDN,'
                                       'regular expresions are allowed due to this url will be interpreted as it'
                                       'max length allowed its 2k characters'),
                           validators=[MinLengthValidator(1), MaxLengthValidator(URL_MAX_LENGTH)])
    json_response = models.JSONField(verbose_name=_('Response'),
                                     default='{}',
                                     help_text=_('Response to be send when the url it\'s requested using AJAX'))
    html_response = models.TextField(verbose_name=_("Response HTML"),
                                     default='',
                                     help_text=_('Response to be send when the url receive a normal HTTP request'))
    name = models.CharField(verbose_name=_('Name'),
                            default='',
                            max_length=NAME_MAX_LENGTH,
                            help_text=_('Name to identify the request handler, should be unique'),
                            validators=[MinLengthValidator(3), MaxLengthValidator(NAME_MAX_LENGTH)])
    created_on = models.DateTimeField(verbose_name=_('Created On'), auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name=_('Updated On'), auto_now=True)

    class Meta:
        ordering = ('url', )
        verbose_name = _('Response Handler')
        verbose_name_plural = _('Response Handlers')
