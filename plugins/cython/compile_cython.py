import os
import shutil

from pants.backend.python.targets.python_library import PythonLibrary
from pants.backend.python.tasks import pex_build_util
from pants.backend.python.tasks.resolve_requirements import ResolveRequirements
from pants.base.build_environment import get_buildroot
from pants.base.exceptions import TaskError
from pants.base.payload import Payload
from pants.base.payload_field import PrimitiveField
from pants.build_graph.resources import Resources
from pants.task.simple_codegen_task import SimpleCodegenTask
from pants.util.contextutil import temporary_dir
from pants.util.dirutil import safe_mkdir_for
from pex.interpreter import PythonInterpreter
from pex.pex import PEX
from pex.pex_builder import PEXBuilder
from pex.pex_info import PexInfo


class CompileCython(PythonLibrary):
    def __init__(self, payload=None, address=None, output=None, **kwargs):
        payload = payload or Payload()
        payload.add_field('output', PrimitiveField(output))
        super(CompileCython, self).__init__(payload=payload, address=address, **kwargs)

    @property
    def output(self):
        return self.payload.output


class CompileCythonCreate(SimpleCodegenTask):

    @classmethod
    def prepare(cls, options, round_manager):
        round_manager.require_data(PythonInterpreter)
        round_manager.require_data(ResolveRequirements.REQUIREMENTS_PEX)

    @classmethod
    def product_types(cls):
        return []

    @property
    def cache_target_dirs(self):
        return True

    def execute_codegen(self, target, results_dir):
        self.context.log.info("Processing target {}".format(target))

        requirements_pex = self.context.products.get_data(ResolveRequirements.REQUIREMENTS_PEX)

        interpreter = self.context.products.get_data(PythonInterpreter)
        pex_info = PexInfo.default(interpreter)
        pex_info.pex_path = requirements_pex.path()
        with temporary_dir() as source_pex_chroot:
            sources_pex_builder = PEXBuilder(
                path=source_pex_chroot,
                interpreter=interpreter,
                copy=True,
                pex_info=pex_info
            )
            pex_build_util.dump_sources(sources_pex_builder, target, self.context.log)
            sources_pex_builder.freeze()
            codegen_pex = PEX(sources_pex_builder.path(), interpreter)

            setup_py_paths = []
            for source in target.sources_relative_to_source_root():
                if os.path.basename(source) == 'setup.py':
                    setup_py_paths.append(source)
            if len(setup_py_paths) != 1:
                raise TaskError(
                    'Expected target {} to own exactly one setup.py, found {}'.format(
                        setup_py_paths,
                        len(setup_py_paths)
                    )
                )
            setup_py_path = setup_py_paths[0]

            result_code = codegen_pex.run(
                with_chroot=True,
                blocking=True,
                args=(setup_py_path, 'build_ext', '--inplace', '--verbose'),
                # Passing PATH helps cython find the correct c++ compiler
                env={'libraries': results_dir, 'PATH': os.getenv('PATH')}
            )

            if result_code != 0:
                raise TaskError(
                    'creating cython library failed',
                    exit_code=result_code,
                    failed_targets=[target]
                )

            library_source_path = os.path.join(
                sources_pex_builder.path(),
                os.path.dirname(setup_py_path),
                target.output
            )

            library_output = os.path.join(results_dir, target.output)
            safe_mkdir_for(library_output)
            shutil.move(library_source_path, library_output)

            self.context.log.info(
                'created library {}'.format(os.path.relpath(library_output, get_buildroot()))
            )

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