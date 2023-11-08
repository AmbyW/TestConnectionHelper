from abc import abstractmethod
from http import HTTPStatus

from django.http import JsonResponse
from django.utils.module_loading import module_has_submodule

from .constants import NOT_IMPLEMENT_ERROR_MESSAGE


class BaseResponseHandler:

    url = ''

    def __init__(self, request):
        self.request = request

    @abstractmethod
    def handle(self):
        raise NotImplementedError(NOT_IMPLEMENT_ERROR_MESSAGE)


class DefaultResponseHandler(BaseResponseHandler):

    def handle(self):
        return JsonResponse(status=HTTPStatus.OK, data={})


class BaseResponseHandlerFactory:

    def __init__(self, request):
        self.request = request

    def get_class_based_handlers(self):
        response_handlers = []
        return response_handlers

    def get_database_handlers(self):
        response_handlers = []
        return response_handlers


    @abstractmethod
    def get_response_hanlder(self):
        raise NotImplementedError(NOT_IMPLEMENT_ERROR_MESSAGE)

    @abstractmethod
    def handle_reponse(self):
        raise NotImplementedError(NOT_IMPLEMENT_ERROR_MESSAGE)


class DefaultResponseHandlerFactory:

    def __init__(self, request):
        self.request = request
        self.response_handler = None

    @abstractmethod
    def get_response_hanlder(self):
        self.response_handler = None
        return self.response_handler

    @abstractmethod
    def handle_reponse(self):
        return self.response_handler.handle()

