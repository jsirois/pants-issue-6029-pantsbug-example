compile_cython(
  name='compile-plugins',
  sources=rglobs('*.*'),
  output='shrubberylib.cpython-36m-x86_64-linux-gnu.so',
  dependencies=['3rdparty:cython'],
)

python_binary(
  name='shrubbery-lib',
  source='run_shrubbery.py',
  dependencies=[':compile-plugins'],
  zip_safe=False,
)

python_tests(
  name='test',
  sources=['test_shrubbery.py'],
  dependencies=[':compile-plugins'],
)