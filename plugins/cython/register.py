from pants.backend.python.tasks.gather_sources import GatherSources
from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.goal.error import GoalError
from pants.goal.goal import Goal
from pants.goal.task_registrar import TaskRegistrar as task
from compile_cython import CompileCythonCreate, CompileCython


def build_file_aliases():
    return BuildFileAliases(
        targets={
            'compile_cython': CompileCython,
        }
    )


def _find_gather_sources():
    for goal in Goal.all():
        for task_name, task_type in goal.task_items():
            if issubclass(task_type, GatherSources):
                yield goal.name, task_name

def register_goals():
    gather_sources_registrations = list(_find_gather_sources())
    if len(gather_sources_registrations) == 0:
        raise GoalError(
            'Failed to find a registration for the %s task to install %s before.'
            % (GatherSources, CompileCythonCreate)
        )

    for gather_sources_goal, gather_sources_task in gather_sources_registrations:
        task(name='compile-cython', action=CompileCythonCreate).install(
            goal=gather_sources_goal,
            before=gather_sources_task
        )
