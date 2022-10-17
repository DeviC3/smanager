from core_commands import CoreCommands

__version__ = '0.1'

class SmanagerPrompt(CoreCommands):

    intro = f'SystemManager {__version__}'
    doc_header = ' List of commands '
    undoc_header = '--  --'
    ruler = '<?><?>'
    prompt = '$ '


if __name__ == '__main__':
    prompt = SmanagerPrompt()
    prompt.cmdloop()