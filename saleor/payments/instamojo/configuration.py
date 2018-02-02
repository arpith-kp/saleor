import os
import sys
import braintree
from braintree.exceptions.configuration_error import ConfigurationError
from braintree.credentials_parser import CredentialsParser
from braintree.environment import Environment

class Configuration(object):
    """
    A class representing the configuration of your Braintree account.
    You must call configure before any other Braintree operations. ::

        instamojo.Configuration.configure(
            instamojo.Environment.Sandbox,
            "your_public_key",
            "your_private_auth_token"
        )
    """
    @staticmethod
    def configure(environment, public_key, private_auth_token, **kwargs):
        Configuration.environment = Environment.parse_environment(environment)
        Configuration.public_key = public_key
        Configuration.private_key = private_auth_token
        Configuration.default_http_strategy = kwargs.get("http_strategy", None)
        Configuration.timeout = kwargs.get("timeout", 60)
        Configuration.wrap_http_exceptions = kwargs.get("wrap_http_exceptions", False)

    @staticmethod
    def gateway():
        return braintree.braintree_gateway.BraintreeGateway(config=Configuration.instantiate())

    @staticmethod
    def instantiate():
        return Configuration(
            environment=Configuration.environment,
            public_key=Configuration.public_key,
            private_auth_token=Configuration.private_auth_token,
            http_strategy=Configuration.default_http_strategy,
            timeout=Configuration.timeout,
            wrap_http_exceptions=Configuration.wrap_http_exceptions
        )

    @staticmethod
    def api_version():
        return "1.1"

    def __init__(self, environment=None, public_key=None, private_auth_token=None,
                 client_id=None, client_secret=None, access_token=None, *args, **kwargs):
        if len(args) == 2:
            public_key, private_auth_token = args

        parser = CredentialsParser(client_id=client_id, client_secret=client_secret, access_token=access_token)
        if parser.access_token is not None:
            parser.parse_access_token()
            self.environment = parser.environment
            self.merchant_id = parser.merchant_id
        elif parser.client_id is not None or parser.client_secret is not None:
            parser.parse_client_credentials()
            self.environment = parser.environment
        else:
            self.environment = Environment.parse_environment(environment)

            if public_key == "":
                raise ConfigurationError("Missing public_key")
            else:
                self.public_key = public_key

            if private_auth_token == "":
                raise ConfigurationError("Missing private_key")
            else:
                self.private_key = private_auth_token

        self.client_id = parser.client_id
        self.client_secret = parser.client_secret
        self.access_token = parser.access_token
        self.timeout = kwargs.get("timeout", 60)
        self.wrap_http_exceptions = kwargs.get("wrap_http_exceptions", False)
        self.http_strategy = kwargs.get("http_strategy", None)

    def base_url(self):
        return self.environment.protocol + self.environment.server_and_port

    def has_client_credentials(self):
        return self.client_secret is not None and self.client_id is not None

    def assert_has_client_credentials(self):
        if not self.has_client_credentials():
            raise ConfigurationError("client_id and client_secret are required")

    def has_access_token(self):
        return self.access_token is not None
