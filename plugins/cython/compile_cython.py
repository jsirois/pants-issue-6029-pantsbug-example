import os
import shutil
import subprocess

from pants.backend.python.targets.python_library import PythonLibrary
from pants.backend.python.tasks.python_execution_task_base import PythonExecutionTaskBase
from pants.base.build_environment import get_buildroot
from pants.base.payload import Payload
from pants.build_graph.resources import Resources
from pants.task.simple_codegen_task import SimpleCodegenTask
from pants.util.dirutil import safe_mkdir_for
from pex.pex_info import PexInfo


class CompileCython(PythonLibrary):
    def __init__(self, inputs=None, payload=None, output=None, address=None, **kwargs):
        inputs = inputs.legacy_globs_class.create_fileset_with_spec(address.spec_path, *inputs.filespecs['globs'])
        payload = payload or Payload()
        payload.add_fields({
            'inputs': self.create_sources_field(inputs, sources_rel_path=address.spec_path, key_arg='sources')
        })
        self.output = output
        super(CompileCython, self).__init__(payload=payload, address=address, **kwargs)


class CompileCythonCreate(SimpleCodegenTask, PythonExecutionTaskBase):
    """
    This is both a SimpleCodegenTask because it generates a so and a PythonExecutionTaskBase because it needs to run python code in order
    to generate the so.
    """

    @classmethod
    def product_types(cls):
        return []

    @property
    def cache_target_dirs(self):
        return True

    @property
    def create_target_dirs(self):
        return True

    def __init__(self, context, workdir):
        super(CompileCythonCreate, self).__init__(context, workdir)

    def execute_codegen(self, target, results_dir):
        self.context.log.info("Processing target %s" % target)

        # Creating the pex can, as a side effect, change the location of the symbolic link pants creates
        result = self.create_pex(PexInfo.default())
        full_path = os.path.join(get_buildroot(), target.target_base)
        # subprocess.check_call(['cmake', full_path], cwd=results_dir)
        # subprocess.check_call(['make'], cwd=results_dir)

        result_code = result.run(
            with_chroot=True,
            blocking=True,
            args=(os.path.join(full_path, 'setup.py'), 'build_ext', '--inplace', '--verbose'),
            # Passing PATH helps cython find the correct c++ compiler
            env={'libraries': results_dir, 'PATH': os.getenv('PATH')}
        )

        if result_code != 0:
            raise ValueError('creating cython library failed')

        library_source_path = os.path.join(result.path(), target.output)

        library_output = os.path.join(results_dir, target.output)
        safe_mkdir_for(library_output)
        shutil.move(library_source_path, library_output)

        self.context.log.info('created library {}'.format(os.path.relpath(target.output, get_buildroot())))

    def synthetic_target_type_by_target(self, target):
        return Resources

    def synthetic_target_type(self, target):
        return Resources

    @property
    def validate_sources_present(self):
        # We don't actually have sources in this package that we want to copy. We just use the sources to compile the so
        return False

    gentarget_type = CompileCython

    def find_sources(self, target, target_workdir):
        return [target.output]

    @property
    def _copy_target_attributes(self):
        return []