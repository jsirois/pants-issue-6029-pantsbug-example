python_library(
  name='impl',
  sources=rglobs('*.py'),
  dependencies=[
    'libraries/shrubbery-lib:shrubbery-lib'
  ]
)

python_binary(
  name='gardener',
  source='main.py',
  dependencies=[':impl'],
  zip_safe=False,
)

python_tests(
  name='test',
  sources=['test_app.py'],
  dependencies=[':impl'],
)

