import os
import inspect


class Environment(object):
    """
    A class representing which environment the client library is using.
    Pass in one of the following values as the first argument to
    :class:`Instamojo.Configuration.configure() <Instamojo.configuration.Configuration>` ::

        Instamojo.Environment.Sandbox
        Instamojo.Environment.Production
    """

    def __init__(self, name, server, port, auth_url, is_ssl=None, ssl_certificate=None):
        self.__name__ = name
        self.__server = server
        self.__port = port
        self.is_ssl = is_ssl
        self.ssl_certificate = ssl_certificate
        self.__auth_url = auth_url

    @property
    def base_url(self):
        return "%s%s:%s" % (self.protocol, self.server, self.port)

    @property
    def port(self):
        return int(self.__port)

    @property
    def auth_url(self):
        return self.__auth_url

    @property
    def protocol(self):
        return self.__port == "443" and "https://" or "http://"

    @property
    def server(self):
        return self.__server

    @property
    def server_and_port(self):
        return self.__server + ":" + self.__port


    @staticmethod
    def instamojo_root():
        return os.path.dirname(inspect.getfile(Environment))

    def __str__(self):
        return self.__name__


Environment.Sandbox = Environment("sandbox", "test.instamojo.com", "443", "https:/test.instamojo.com/api/1.1/")
Environment.Production = Environment("production", "instamojo.com", "443", "https://instamojo.com/api/1.1/")
Environment.All = {
    "sandbox": Environment.Sandbox,
    "production": Environment.Production
}
