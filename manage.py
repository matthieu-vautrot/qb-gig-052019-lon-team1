# QUANTUMBLACK CONFIDENTIAL
#
# Copyright (c) 2016 - present QuantumBlack Visual Analytics Ltd. All
# Rights Reserved.
#
# NOTICE: All information contained herein is, and remains the property of
# QuantumBlack Visual Analytics Ltd. and its suppliers, if any. The
# intellectual and technical concepts contained herein are proprietary to
# QuantumBlack Visual Analytics Ltd. and its suppliers and may be covered
# by UK and Foreign Patents, patents in process, and are protected by trade
# secret or copyright law. Dissemination of this information or
# reproduction of this material is strictly forbidden unless prior written
# permission is obtained from QuantumBlack Visual Analytics Ltd.

""" Command line tools for manipulating a kernelai project.
Intended to be invoked via kernelai """

import sys
import os
import subprocess
import shutil
import shlex
from pathlib import Path

import click
from click import style, secho, ClickException

from kernelai.cli.utils import forward_command, call, python_call, \
    get_pkg_version
from kernelai.cli.docker import compose_docker_run_args, \
    check_docker_image_exists, make_container_name, copy_project_wheels


__kernel_version__ = '0.12.1'


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


NO_KERNELVIZ_MESSAGE = """
kernelviz is not installed. Please make sure kernelviz is in
src/python/requirements.txt and run `kernelai install`
"""


NO_PYTEST_MESSAGE = """
pytest is not installed. Please make sure pytest is in
src/python/requirements.txt and run `kernelai install`
"""


NO_NBSTRIPOUT_MESSAGE = """
nbstripout is not installed. Please make sure nbstripout is in
`src/python/requirements.txt` and run `kernelai install`
"""


NO_DOCKER_MESSAGE = """
Cannot connect to the Docker daemon. Is the Docker daemon running?
"""


DOCKER_DEFAULT_VOLUMES = ('conf/local', 'data', 'logs', 'notebooks',
                          'references', 'results')


IMAGE_ARG = click.option(
    '--image', type=str, default='', help='Docker image tag.')


NODE_TAG_ARG = click.option(
    '--tag', '-t', type=str, default=None, multiple=True,
    help="Construct the pipelines using only nodes which have this tag "
         "attached. Option can be used multiple times, what results in a "
         "pipelines constructed from nodes having any of those tags.")


root = Path(__file__).resolve().parent  # pylint: disable=invalid-name


def ipython_mesage():
    """ show a message saying how we have configured the ipython env """
    ipy_vars = ['proj_dir', 'proj_name', 'conf', 'io', 'parameters',
                'startup_error']
    secho('-' * 79, fg='cyan')
    secho(
        'Starting a KernelAI session with the following variables in scope',
    )
    secho(', '.join(ipy_vars), fg='green')
    secho('Use the line magicmagic {} to refresh them'.format(
        style('%reload_kernelai', fg='green'),
    ))
    secho('or to see the error message if they are undefined')
    secho('-' * 79, fg='cyan')


@click.group(context_settings=CONTEXT_SETTINGS, name=__file__)
def cli():
    """ Command line tools for manipulating a kernelai project """
    os.chdir(str(root))
    py_path = str(root / 'src' / 'python')
    sys.path.append(py_path)
    new_path = os.environ.get('PYTHONPATH', '') + os.pathsep + py_path
    os.environ['PYTHONPATH'] = new_path
    os.environ['IPYTHONDIR'] = str(root / '.ipython')


@cli.command()
@NODE_TAG_ARG
def run(tag):
    """ Run the pipelines """
    from project_irene.run import main
    main(pipeline_tags=tag, run_pipeline=True)


@forward_command(cli, forward_help=True)
def test(args):
    """ Run the test suite """
    try:
        import pytest  # pylint: disable=unused-import
    except ImportError:
        raise ClickException(NO_PYTEST_MESSAGE)
    else:
        python_call('pytest', args)


@cli.command()
def install():
    """ Install project dependencies from requirements.txt """
    python_call('pip', ['install', '-U', '-r', 'src/python/requirements.txt'])


@cli.command()
def lint():
    """ Check the Python code quality """
    python_call('pylint', [
        '-j', '0',
        '--disable=duplicate-code',
        'src/python/project_irene',
        'manage.py'
    ])
    python_call('pylint', [
        '-j', '0',
        '--disable=missing-docstring,redefined-outer-name,duplicate-code',
        'src/python/tests',
    ])


@forward_command(cli, forward_help=True)
def ipython(args):
    """ Open ipython with project specific variables loaded """
    if '-h' not in args and '--help' not in args:
        ipython_mesage()
    call(['ipython'] + list(args))


@cli.command()
def package():
    """ Package the project as a Python egg and wheel """
    call([sys.executable, 'setup.py', 'bdist_egg'], cwd='src/python')
    call([sys.executable, 'setup.py', 'bdist_wheel'], cwd='src/python')


@forward_command(cli, forward_help=True)
@NODE_TAG_ARG
def viz(tag, args):
    """Visualize the pipelines using kernelviz"""
    try:
        import kernelviz  # pylint: disable=unused-import
    except ImportError:
        raise ClickException(NO_KERNELVIZ_MESSAGE)
    from project_irene.run import main
    main(pipeline_tags=tag, run_pipeline=False)
    python_call('kernelviz', ['--logdir', 'logs/visualization'] + list(args))


@cli.command('build-docs')
def build_docs():
    """ Build the project documentation """
    python_call('pip', ['install', 'src/python[docs]'])
    python_call('pip', ['install', '-r', 'src/python/requirements.txt'])
    python_call('ipykernel', ['install', '--user',
                              '--name=project_irene'])
    if Path('docs/build').exists():
        shutil.rmtree('docs/build')
    call(['sphinx-apidoc', '--module-first', '-o', 'docs/source',
          'src/python/project_irene'])
    call(['sphinx-build', '-M', 'html', 'docs/source', 'docs/build', '-a'])


@cli.command('activate-nbstripout')
def activate_nbstripout():
    """ Install the nbstripout git hook to automatically clean notebooks """
    secho((
        'Notebook output cells will be automatically cleared before commiting'
        ' to git.'
    ), fg='yellow')

    try:
        import nbstripout  # pylint: disable=unused-import
    except ImportError:
        raise ClickException(NO_NBSTRIPOUT_MESSAGE)

    try:
        res = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if res.returncode:
            raise ClickException('Not a git repository. Run `git init` first.')
    except FileNotFoundError:
        raise ClickException('Git executable not found. Install Git first.')

    call(['nbstripout', '--install'])


@cli.group()
def jupyter():
    """ Open jupyter notebook / lab with project specific variables loaded """


@forward_command(jupyter, 'notebook', forward_help=True)
@click.option('--ip', type=str, default='127.0.0.1')
def jupyter_notebook(ip, args):
    """ Open jupyter notebook with project specific variables loaded """
    if '-h' not in args and '--help' not in args:
        ipython_mesage()
    call(['jupyter-notebook', '--ip=' + ip] + list(args))


@forward_command(jupyter, 'lab', forward_help=True)
@click.option('--ip', type=str, default='127.0.0.1')
def jupyter_lab(ip, args):
    """ Open jupyter lab with project specific variables loaded """
    if '-h' not in args and '--help' not in args:
        ipython_mesage()
    call(['jupyter-lab', '--ip=' + ip] + list(args))


@cli.group(name='docker')
def docker_group():
    """ Dockerize project """
    # check that docker is running
    try:
        res = subprocess.run(['docker', 'version'],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL).returncode
    except FileNotFoundError:
        raise ClickException(NO_DOCKER_MESSAGE)
    if res:
        raise ClickException(NO_DOCKER_MESSAGE)


@forward_command(docker_group, 'build')
@click.option('--wheel-dir', default=None,
              help='Path to a directory containing kernelai '
                   'and kernelviz wheel files. All other files are ignored.',
              type=click.Path(exists=True, file_okay=False,
                              dir_okay=True, resolve_path=True))
def docker_build(args, wheel_dir):
    """Build a Docker image for the project. Any extra arguments
    unspecified in this help are passed to `docker build` as is."""
    pkg_offline = root / 'python-pkg-offline'

    try:
        # re-create python-pkg-offline directory
        shutil.rmtree(str(pkg_offline), ignore_errors=True)
        pkg_offline.mkdir(parents=True, exist_ok=True)

        if wheel_dir:
            # use provided package wheels, don't download via pip
            copy_project_wheels(wheel_dir, pkg_offline)
        else:
            reqs_path = root / 'src' / 'python' / 'requirements.txt'
            # download kernelai
            _kai_version = get_pkg_version(reqs_path, 'kernelai')
            python_call('pip', ['download', '--no-deps',
                                '-d', str(pkg_offline), _kai_version])

            # download kernelviz
            _kviz_version = get_pkg_version(reqs_path, 'kernelviz')
            python_call('pip', ['download', '--no-deps',
                                '-d', str(pkg_offline), _kviz_version])

        # build docker image
        # add image tag if only it is not already supplied by the user
        combined_args = compose_docker_run_args(
            optional_args=[('-t', str(root.name))],
            user_args=list(args))
        command = ['docker', 'build'] + combined_args + [str(root)]
        msg = 'Running build:\n{}'.format(style(' '.join(command), fg='green'))
        secho(msg)
        call(command)
    finally:
        # remove python-pkg-offline
        shutil.rmtree(str(pkg_offline), ignore_errors=True)


@forward_command(docker_group, 'run')
@IMAGE_ARG
@click.option('--run-args', type=str, default='',
              help='These arguments get appended to `docker run` command '
                   'after the image tag.')
def docker_run(image, run_args, args):
    """Run the pipelines in Docker container.
    Any extra arguments unspecified in this help
    are passed to `docker run` as is."""
    run_args = shlex.split(run_args)
    image = image or str(root.name)

    # check that the image exists
    check_docker_image_exists(image)
    # default container name
    container_name = make_container_name(image, "run")

    _docker_run_args = compose_docker_run_args(
        host_root=str(root),
        container_root='/home/kernelai/project_irene',
        mount_volumes=DOCKER_DEFAULT_VOLUMES,
        optional_args=[("--rm", None), ("--name", container_name)],
        user_args=list(args))
    command = ["docker", "run"] + _docker_run_args + [image] + run_args
    call(command)


@forward_command(docker_group, 'ipython')
@IMAGE_ARG
@click.option('--run-args', type=str, default='',
              help='Optional arguments `ipython` to be called with.')
def docker_ipython(image, run_args, args):
    """Run ipython in Docker container.
    Any extra arguments unspecified in this help
    are passed to `docker run` as is."""
    run_args = shlex.split(run_args)
    image = image or str(root.name)

    # check that the image exists
    check_docker_image_exists(image)
    # default container name
    container_name = make_container_name(image, "ipython")

    _docker_run_args = compose_docker_run_args(
        host_root=str(root),
        container_root='/home/kernelai/project_irene',
        mount_volumes=DOCKER_DEFAULT_VOLUMES,
        optional_args=[('--rm', None),
                       ('-it', None),
                       ('--name', container_name)],
        user_args=list(args))
    command = ['docker', 'run'] + _docker_run_args \
        + [image, 'ipython'] + run_args
    call(command)


@docker_group.group(name='jupyter')
def docker_jupyter():
    """Run jupyter lab / notebook in Docker container."""


@forward_command(docker_jupyter, 'notebook')
@IMAGE_ARG
@click.option('--port', type=int, default=8888,
              help='Host port to publish to.')
def docker_jupyter_notebook(port, image, args):
    """Run jupyter notebook in Docker container.
    Any extra arguments unspecified in this help
    are passed to `docker run` as is."""
    image = image or str(root.name)

    # check that the image exists
    check_docker_image_exists(image)
    # default container name
    container_name = make_container_name(image, "jupyter-notebook")

    _docker_run_args = compose_docker_run_args(
        host_root=str(root),
        container_root='/home/kernelai/project_irene',
        mount_volumes=DOCKER_DEFAULT_VOLUMES,
        required_args=[("-p", "{}:8888".format(port))],
        optional_args=[("--rm", None),
                       ("-it", None),
                       ("--name", container_name)],
        user_args=list(args))
    command = ["docker", "run"] + _docker_run_args \
        + [image, "jupyter", "notebook", "--ip", "0.0.0.0", "--no-browser"]
    call(command)


@forward_command(docker_jupyter, 'lab')
@IMAGE_ARG
@click.option('--port', type=int, default=8888,
              help='Host port to publish to.')
def docker_jupyter_lab(port, image, args):
    """Run jupyter lab in Docker container.
    Any extra arguments unspecified in this help
    are passed to `docker run` as is."""
    image = image or str(root.name)

    # check that the image exists
    check_docker_image_exists(image)
    # default container name
    container_name = make_container_name(image, "jupyter-lab")

    _docker_run_args = compose_docker_run_args(
        host_root=str(root),
        container_root='/home/kernelai/project_irene',
        mount_volumes=DOCKER_DEFAULT_VOLUMES,
        required_args=[("-p", "{}:8888".format(port))],
        optional_args=[("--rm", None),
                       ("-it", None),
                       ("--name", container_name)],
        user_args=list(args))
    command = ["docker", "run"] + _docker_run_args \
        + [image, "jupyter", "lab", "--ip", "0.0.0.0", "--no-browser"]
    call(command)


if __name__ == '__main__':
    cli()
