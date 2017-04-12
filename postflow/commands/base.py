import os
import click

from flask.cli import FlaskGroup, ScriptInfo, pass_script_info

from postflow import create_app

def make_app(script_info):
    config_file = getattr(script_info, "config_file")
    return create_app(config_file)


def set_config(ctx, param, value):
    """This will pass the config file to the create_app function."""
    ctx.ensure_object(ScriptInfo).config_file = value


@click.group(cls=FlaskGroup, create_app=make_app, add_version_option=False)
@click.option('--config', expose_value=False, callback=set_config,
              required=False, is_flag=False, is_eager=True, metavar="CONFIG",
              help="Specify the config to use")
@pass_script_info
def postflow(info, **params):
    os.environ["FLASK_DEBUG"] = str(info.load_app().config['DEBUG'])
