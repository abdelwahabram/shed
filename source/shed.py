import click
from pathlib import Path
from source.repository import Repository



@click.command
def create_repository():
    """create a shed repository if it doesn't exist in this directory or the parents
    """
    
    repository = Repository()
    repository.create()
    return

@click.command
@click.argument('files_list', type = click.Path(exists = True, dir_okay = False, path_type = Path), nargs = -1)
def add_file(files_list):
    """add updated file/s to the under construction area

    Args:
        file_path (Path): the relative path of the file
    """
    
    repository = Repository()
    
    for file_path in files_list:
        repository.add_file(file_path)
    
    return


@click.command
@click.argument('message', type = str)
def build(message):
    """ build a shell from the saved updates

    Args:
        message (str): build message to remember what have been built at this step
    """
    
    repository = Repository()
    
    repository.build(message)
    
    return


@click.command
def show_status():
    """ prints the current status of the repository
    """
    repository = Repository()
    repository.show_status()
    return

@click.command
def show_difference():
    """ prints the differences between files in under construction area and the working directory
    """
    repository = Repository()
    repository.show_difference()
    return

@click.command
def turn_into_git_repo():
    """ transform the repository into git repo to be easily pushed to gh"""
    repository = Repository()
    repository.turn_into_git_repository()
    return

# if __name__ == '__main__':
#     sss()