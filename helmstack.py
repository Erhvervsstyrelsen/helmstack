import click
import ruamel.yaml as yaml
import pprint


class Config(object):
    def __init__(self):
        self.environment = None
        self.context = None
        self.helm_binary = None
        self.file = None
        self.debug = False
        self.stack = None
        self.recreate_pods = False
        self.force = False


config = Config()


@click.command()
@click.option('--environment', '-e', default=None, help='Specify target environment')
@click.option('--context', '-c', default=None, help='kubectl context')
@click.option('--helm-binary', '-b', default='helm', help='Path to helm binary')
@click.option('--file', '-f', type=click.File('r'), default='helmstack.yaml', help='Specify stack file')
@click.option('--debug', is_flag=True, help='Enable debug')
def cli(environment, context, helm_binary, file, debug):
    """This script run helm commands"""

    config.environment = environment
    config.context = context
    config.helm_binary = helm_binary
    config.file = file
    config.debug = debug

    if config.stack['helmDefaults']:
        if config.stack['helmDefaults']['recreatePods']:
            config.recreate_pods = config.stack['helmDefaults']['recreatePods']

    print("Environment: %s" % environment)
    print("Context: %s" % context)
    print("Stack file: %s" % file.name)

    try:
        stack = yaml.safe_load(file)
        if debug:
            pprint.pprint(stack)
        config.stack = stack
    except yaml.YAMLError as exc:
        print(exc)

    handle_repositories()


def handle_repositories():
    stack = config.stack
    if stack['repositories']:
        for repository in stack['repositories']:
            sh_exec("helm repo add %s %s" % (repository['name'], repository['url']))
        sh_exec("helm repo update")


def sh_exec(cmd):
    print(cmd)


def helm(cmd):
    context = "--kube-context %s" % config.context if config.context else ""
    recreate_pods = "--recreate-pods" if config.recreate_pods else ""
    force = "--force" if config.recreate_pods else ""
    sh_exec("%s %s %s %s %s" % (config.helm_binary, context, cmd, recreate_pods, force))
