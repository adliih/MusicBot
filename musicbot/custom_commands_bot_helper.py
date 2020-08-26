import logging

log = logging.getLogger(__name__)

# Functio wrapper to load all custom command in custom_commands_bot.py
def load_custom_command(bot, reload=True):
    import types
    from . import custom_commands_bot
    from functools import partial

    if reload:
        import importlib
        importlib.reload(custom_commands_bot)

    # Listing all custom commands in custom_commands_bot
    for _custom_command in dir(custom_commands_bot):
        custom_command = getattr(custom_commands_bot, _custom_command, None)
        if isinstance(custom_command, types.FunctionType):
            function_name = custom_command.__name__
            if function_name.startswith('cmd_'):
                log.debug("[Custom Method] Binding custom method {}".format(function_name))
                # Add those method to this object
                setattr(bot, function_name, types.MethodType(custom_command, bot))

# Redownloading config from github configuration
def redownload_config():
    import os
    from dotenv import load_dotenv, find_dotenv
    allow_requests = True
    from github import Github

    load_dotenv(find_dotenv())

    if 'GITHUB_TOKEN' in os.environ and 'GITHUB_CONFIG_REPO' in os.environ:
        g = Github(os.getenv('GITHUB_TOKEN'))
        config_repo = g.get_repo(os.getenv('GITHUB_CONFIG_REPO'))
        for content in config_repo.get_contents(''):
            # Copying all except readme files to config folder
            if content.path != 'README.md':
                log.debug('copying ' + content.path)
                with open('config/' + content.path, 'wb') as config_file:
                    print(content.decoded_content)
                    config_file.write(content.decoded_content)