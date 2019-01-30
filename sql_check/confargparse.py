import sys
from argparse import ArgumentParser


class ConfArgParser(ArgumentParser):
    """
    Extends argparse.ArgumentParser to make it able to take in values from a configuration file.
    It inserts values from the configuration files before CLI provided values into sys.argv.
    """

    def __init__(self, *args, config=None, **kwargs):
        """
        :param args: ArgumentParser args
        :param config: a dict containing the configuration
        :param kwargs: ArgumentParser kwargs
        """
        self.__config = config if config is not None else dict()
        self.__key_opts = {}
        super(ConfArgParser, self).__init__(*args, **kwargs)

    def add_argument(self, *args, conf_key=None, **kwargs):
        """
        :param args:  ArgumentParser.add_argument args
        :param conf_key: dot style path to the corresponding configuration item for the config dict
        :param kwargs: ArgumentParser kwargs.add_argument kwargs
        :return: ArgumentParser.add_argument result
        """
        if conf_key is not None:
            self.__key_opts[conf_key] = args[0]

        return super(ConfArgParser, self).add_argument(*args, **kwargs)

    def parse_args(self, **kwargs):
        config_as_opts = []
        for key, opt in self.__key_opts.items():
            conf_value = self.__resolve_conf(key.split("."), self.__config)
            if conf_value is not None:
                config_as_opts.append(opt)
                config_as_opts.append(str(conf_value))
        sys.argv = sys.argv[0:1] + config_as_opts + sys.argv[1:]

        return super(ConfArgParser, self).parse_args(**kwargs)

    def __resolve_conf(self, key_frags, node):
        if key_frags[0] not in node:
            return None
        elif len(key_frags) == 1:
            return node[key_frags[0]]
        else:
            return self.__resolve_conf(key_frags[1:], node[key_frags[0]])
