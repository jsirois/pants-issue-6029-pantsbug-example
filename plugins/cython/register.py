from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.goal.task_registrar import TaskRegistrar as task
from compile_cython import CompileCythonCreate, CompileCython


def build_file_aliases():
    return BuildFileAliases(
        targets={
            'compile_cython': CompileCython,
        }
    )


def register_goals():
    task(name='compile-cython', action=CompileCythonCreate).install('compile')
