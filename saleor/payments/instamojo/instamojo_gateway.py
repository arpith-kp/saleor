from saleor.payments.instamojo import configuration


class InstaMojoGateway(object):
    def __init__(self, config=None, **kwargs):
        if isinstance(config, configuration.Configuration):
            self.config = config
        else:
            self.config = configuration.Configuration(
                client_id=kwargs.get("client_id"),
                client_secret=kwargs.get("client_secret"),
                access_token=kwargs.get("access_token"),
                http_strategy=kwargs.get("http_strategy")
            )
