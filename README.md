# symptom
We have a plugin to compile cython files into an .so that exposes some extension objects. We'd like to use those extension objects in other python build targets, and also use them in unit tests.
Exposing the so for other targets works, in that the .so appears in the pex. However unit tests don't work. The test runner can't find the .so.

Perhaps there something we are not doing in the plugin code to expose the .so to py.test? Do we need to add something to the pythonpath?

# environment
pants: 1.8.0rc0
ubuntu 17.04
target python for the build artifacts: 3.6.3


# Repro
In [pantsbug.zip](https://github.com/pantsbuild/pants/files/2138427/pantsbug.zip) is a small toy project that demonstrates the issue. To repro:

```bash
mkdir repro
cd repro
cp ~/Downloads/pantsbug.zip .
unzip pantsbug.zip

# clean slate
rm -rf dist lib/*.h lib/*.so lib/*.cpp /tmp/pantscache && ./pants clean-all

# create pex for app that depends on the cython lib
./pants binary apps/gardener:

# run the pex, this works
dist/gardener.pex

# same thing for the lib itself, also works
dist/shrubbery-lib.pex


# verify the .so are in the pex (they have to be, otherwise running the pex above would not work
unzip -l dist/shrubbery-lib.pex | grep shrubberylib
unzip -l dist/gardener.pex | grep shrubberylib


# running tests does not work sadly, because test runner does not find the .so
./pants test libraries/shrubbery-lib:

# same fail here
./pants test apps/gardener:

```

Here is the output of doing what's above
```
$ ls
3rdparty  apps  libraries  pants  pants.ini  plugins


$ rm -rf dist lib/*.h lib/*.so lib/*.cpp /tmp/pantscache && ./pants clean-all
fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

11:18:41 00:00 [main]
               (To run a reporting server: ./pants server)
11:18:41 00:00   [setup]
11:18:41 00:00     [parse]fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

               Executing tasks in goals: clean-all
11:18:41 00:00   [clean-all]
11:18:41 00:00     [ng-killall]
11:18:41 00:00     [kill-pantsd]
11:18:41 00:00     [clean-all]INFO] For async removal, run `./pants clean-all --async`

11:18:41 00:00   [complete]
               SUCCESS


$ ./pants binary apps/gardener:
fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

11:18:48 00:00 [main]
               (To run a reporting server: ./pants server)
11:18:48 00:00   [setup]
11:18:48 00:00     [parse]fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

               Executing tasks in goals: jvm-platform-validate -> bootstrap -> imports -> unpack-jars -> deferred-sources -> gen -> pyprep -> resolve -> resources -> compile -> binary
11:18:48 00:00   [jvm-platform-validate]
11:18:48 00:00     [jvm-platform-validate]
11:18:48 00:00   [bootstrap]
11:18:48 00:00     [substitute-aliased-targets]
11:18:48 00:00     [jar-dependency-management]
11:18:48 00:00     [bootstrap-jvm-tools]
11:18:48 00:00     [provide-tools-jar]
11:18:48 00:00   [imports]
11:18:48 00:00     [ivy-imports]
11:18:48 00:00   [unpack-jars]
11:18:48 00:00     [unpack-jars]
11:18:48 00:00   [deferred-sources]
11:18:48 00:00     [deferred-sources]
11:18:48 00:00   [gen]
11:18:48 00:00     [antlr-java]
11:18:48 00:00     [antlr-py]
11:18:48 00:00     [jaxb]
11:18:48 00:00     [protoc]
11:18:48 00:00     [ragel]
11:18:48 00:00     [thrift-java]
11:18:48 00:00     [thrift-py]
11:18:48 00:00     [wire]
11:18:48 00:00   [pyprep]
11:18:48 00:00     [interpreter]
11:18:53 00:05     [build-local-dists]
11:18:53 00:05     [requirements]
11:18:53 00:05       [cache] 
                   No cached artifacts for 1 target.
                   Invalidated 1 target.
11:18:55 00:07     [sources]
11:18:55 00:07       [cache]     
                   No cached artifacts for 5 targets.
                   Invalidated 5 targets.
11:18:55 00:07   [resolve]
11:18:55 00:07     [ivy]
11:18:55 00:07     [coursier]
11:18:55 00:07     [node]
11:18:55 00:07   [resources]
11:18:55 00:07     [prepare]
11:18:55 00:07     [services]
11:18:55 00:07   [compile]
11:18:55 00:07     [node]
11:18:55 00:07     [compile-jvm-prep-command]
11:18:55 00:07       [jvm_prep_command]
11:18:55 00:07     [compile-prep-command]
11:18:55 00:07     [compile]
11:18:55 00:07     [zinc]
11:18:55 00:07     [javac]
11:18:55 00:07     [compile-cython]
11:18:55 00:07       [cache] 
                   No cached artifacts for 1 target.
                   Invalidated 1 target.
                     Processing target CompileCython(BuildFileAddress(libraries/shrubbery-lib/BUILD, compile-plugins)).      
                     No cached artifacts for 6 targets.
                     Invalidated 6 targets.running build_ext
building 'shrubberylib' extension
creating build
creating build/temp.linux-x86_64-3.6
creating build/temp.linux-x86_64-3.6/home
creating build/temp.linux-x86_64-3.6/home/jhersch
creating build/temp.linux-x86_64-3.6/home/jhersch/repro
creating build/temp.linux-x86_64-3.6/home/jhersch/repro/libraries
creating build/temp.linux-x86_64-3.6/home/jhersch/repro/libraries/shrubbery-lib
gcc -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -I/usr/local/include/python3.6m -c /home/jhersch/repro/libraries/shrubbery-lib/shrubbery.cpp -o build/temp.linux-x86_64-3.6/home/jhersch/repro/libraries/shrubbery-lib/shrubbery.o
cc1plus: warning: command line option '-Wstrict-prototypes' is valid for C/ObjC but not for C++
g++ -pthread -shared build/temp.linux-x86_64-3.6/home/jhersch/repro/libraries/shrubbery-lib/shrubbery.o -L/usr/local/lib -lpython3.6m -o /home/jhersch/repro/.pants.d/compile/compile-cython/CPython-3.6.3/b27d189021791fc2a8efad10052d56e808756e1a/shrubberylib.cpython-36m-x86_64-linux-gnu.so

                     created library shrubberylib.cpython-36m-x86_64-linux-gnu.so
11:18:57 00:09   [binary]
11:18:57 00:09     [binary-jvm-prep-command]
11:18:57 00:09       [jvm_prep_command]
11:18:57 00:09     [binary-prep-command]
11:18:57 00:09     [py]
11:18:57 00:09       [cache]  
                   No cached artifacts for 2 targets.
                   Invalidated 2 targets.
                   created pex dist/gardener.pex
                   created pex dist/shrubbery-lib.pex
11:18:59 00:11     [py-wheels]
11:18:59 00:11     [jvm]
11:18:59 00:11     [dup]
               Waiting for background workers to finish.
11:19:00 00:12   [complete]
               SUCCESS


$ dist/gardener.pex
creating a 10x20 shrub
area is: 200
perimeter is: 60


$ dist/shrubbery-lib.pex
<module 'shrubberylib' from '/home/jhersch/.pex/code/79fe3c9b25b21953f7ee78aa6bbc3b4528c8e63a/shrubberylib.cpython-36m-x86_64-linux-gnu.so'>
<shrubberylib.Shrubbery object at 0x7f8fc73930c0>
This shrubbery is 1 by 2 cubits I think.
area is: 2
perimeter is: 6


$ unzip -l dist/shrubbery-lib.pex | grep shrubberylib
warning [dist/shrubbery-lib.pex]:  25 extra bytes at beginning or within zipfile
  (attempting to process anyway)
   247200  2018-06-26 11:18   shrubberylib.cpython-36m-x86_64-linux-gnu.so


$ unzip -l dist/gardener.pex | grep shrubberylib
warning [dist/gardener.pex]:  25 extra bytes at beginning or within zipfile
  (attempting to process anyway)
   247200  2018-06-26 11:18   shrubberylib.cpython-36m-x86_64-linux-gnu.so



$ ./pants test libraries/shrubbery-lib:
fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

11:19:27 00:00 [main]
               (To run a reporting server: ./pants server)
11:19:27 00:00   [setup]
11:19:27 00:00     [parse]fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

               Executing tasks in goals: bootstrap -> imports -> unpack-jars -> deferred-sources -> gen -> jvm-platform-validate -> resolve -> resources -> pyprep -> compile -> test
11:19:27 00:00   [bootstrap]
11:19:27 00:00     [substitute-aliased-targets]
11:19:27 00:00     [jar-dependency-management]
11:19:27 00:00     [bootstrap-jvm-tools]
11:19:27 00:00     [provide-tools-jar]
11:19:27 00:00   [imports]
11:19:27 00:00     [ivy-imports]
11:19:27 00:00   [unpack-jars]
11:19:27 00:00     [unpack-jars]
11:19:27 00:00   [deferred-sources]
11:19:27 00:00     [deferred-sources]
11:19:27 00:00   [gen]
11:19:27 00:00     [antlr-java]
11:19:27 00:00     [antlr-py]
11:19:27 00:00     [jaxb]
11:19:27 00:00     [protoc]
11:19:27 00:00     [ragel]
11:19:27 00:00     [thrift-java]
11:19:27 00:00     [thrift-py]
11:19:27 00:00     [wire]
11:19:27 00:00   [jvm-platform-validate]
11:19:27 00:00     [jvm-platform-validate]
11:19:27 00:00   [resolve]
11:19:27 00:00     [ivy]
11:19:27 00:00     [coursier]
11:19:27 00:00     [node]
11:19:27 00:00   [resources]
11:19:27 00:00     [prepare]
11:19:27 00:00     [services]
11:19:27 00:00   [pyprep]
11:19:27 00:00     [interpreter]
11:19:27 00:00     [build-local-dists]
11:19:27 00:00     [requirements]
11:19:28 00:01     [sources]
11:19:28 00:01       [cache] 
                   No cached artifacts for 1 target.
                   Invalidated 1 target.
11:19:28 00:01   [compile]
11:19:28 00:01     [node]
11:19:28 00:01     [compile-jvm-prep-command]
11:19:28 00:01       [jvm_prep_command]
11:19:28 00:01     [compile-prep-command]
11:19:28 00:01     [compile]
11:19:28 00:01     [zinc]
11:19:28 00:01     [javac]
11:19:28 00:01     [compile-cython]
11:19:28 00:01   [test]
11:19:28 00:01     [test-jvm-prep-command]
11:19:28 00:01       [jvm_prep_command]
11:19:28 00:01     [test-prep-command]
11:19:28 00:01     [test]
11:19:28 00:01     [pytest-prep]
11:19:28 00:01       [cache]     
                   No cached artifacts for 5 targets.
                   Invalidated 5 targets.
11:19:30 00:03     [pytest]
11:19:30 00:03       [cache] 
                   No cached artifacts for 1 target.
                   Invalidated 1 target.
11:19:30 00:03       [run]
                     ============== test session starts ===============
                     platform linux -- Python 3.6.3, pytest-3.0.6, py-1.5.3, pluggy-0.4.0
                     rootdir: /home/jhersch/repro/.pants.d, inifile: /home/jhersch/repro/.pants.d/test/pytest-prep/CPython-3.6.3/8a0011cf88c12b5115d1bc6b6c573067ab912ddc/pytest.ini
                     plugins: cov-2.4.0, timeout-1.2.0
                     collected 0 items / 1 errors
                     
                      generated xml file: /home/jhersch/repro/.pants.d/test/pytest/libraries.shrubbery-lib.test/junitxml/TEST-libraries.shrubbery-lib.test.xml 
                     ===================== ERRORS =====================
                      ERROR collecting pyprep/sources/37ab7c1e7cfdc7bb743989b78701f6b8ec4dbb16/test_shrubbery.py 
                     ImportError while importing test module '/home/jhersch/repro/.pants.d/pyprep/sources/37ab7c1e7cfdc7bb743989b78701f6b8ec4dbb16/test_shrubbery.py'.
                     Hint: make sure your test modules/packages have valid Python names.
                     Traceback:
                     .pants.d/pyprep/sources/37ab7c1e7cfdc7bb743989b78701f6b8ec4dbb16/test_shrubbery.py:2: in <module>
                         import shrubberylib
                     E   ModuleNotFoundError: No module named 'shrubberylib'
                     ============ 1 error in 0.05 seconds =============
                     
                   libraries/shrubbery-lib:test                                                    .....   FAILURE
FAILURE: FAILURE


               Waiting for background workers to finish.
11:19:31 00:04   [complete]
               FAILURE



$ ./pants test apps/gardener:
fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

11:19:36 00:00 [main]
               (To run a reporting server: ./pants server)
11:19:36 00:00   [setup]
11:19:37 00:01     [parse]fatal: Not a git repository (or any parent up to mount point /home/jhersch)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).

               Executing tasks in goals: bootstrap -> imports -> unpack-jars -> deferred-sources -> gen -> jvm-platform-validate -> resolve -> resources -> pyprep -> compile -> test
11:19:37 00:01   [bootstrap]
11:19:37 00:01     [substitute-aliased-targets]
11:19:37 00:01     [jar-dependency-management]
11:19:37 00:01     [bootstrap-jvm-tools]
11:19:37 00:01     [provide-tools-jar]
11:19:37 00:01   [imports]
11:19:37 00:01     [ivy-imports]
11:19:37 00:01   [unpack-jars]
11:19:37 00:01     [unpack-jars]
11:19:37 00:01   [deferred-sources]
11:19:37 00:01     [deferred-sources]
11:19:37 00:01   [gen]
11:19:37 00:01     [antlr-java]
11:19:37 00:01     [antlr-py]
11:19:37 00:01     [jaxb]
11:19:37 00:01     [protoc]
11:19:37 00:01     [ragel]
11:19:37 00:01     [thrift-java]
11:19:37 00:01     [thrift-py]
11:19:37 00:01     [wire]
11:19:37 00:01   [jvm-platform-validate]
11:19:37 00:01     [jvm-platform-validate]
11:19:37 00:01   [resolve]
11:19:37 00:01     [ivy]
11:19:37 00:01     [coursier]
11:19:37 00:01     [node]
11:19:37 00:01   [resources]
11:19:37 00:01     [prepare]
11:19:37 00:01     [services]
11:19:37 00:01   [pyprep]
11:19:37 00:01     [interpreter]
11:19:37 00:01     [build-local-dists]
11:19:37 00:01     [requirements]
11:19:37 00:01     [sources]
11:19:37 00:01   [compile]
11:19:37 00:01     [node]
11:19:37 00:01     [compile-jvm-prep-command]
11:19:37 00:01       [jvm_prep_command]
11:19:37 00:01     [compile-prep-command]
11:19:37 00:01     [compile]
11:19:37 00:01     [zinc]
11:19:37 00:01     [javac]
11:19:37 00:01     [compile-cython]
11:19:37 00:01   [test]
11:19:37 00:01     [test-jvm-prep-command]
11:19:37 00:01       [jvm_prep_command]
11:19:37 00:01     [test-prep-command]
11:19:37 00:01     [test]
11:19:37 00:01     [pytest-prep]
11:19:37 00:01       [cache]   
                   No cached artifacts for 3 targets.
                   Invalidated 3 targets.
11:19:37 00:01     [pytest]
11:19:37 00:01       [cache] 
                   No cached artifacts for 1 target.
                   Invalidated 1 target.
11:19:38 00:02       [run]
                     ============== test session starts ===============
                     platform linux -- Python 3.6.3, pytest-3.0.6, py-1.5.3, pluggy-0.4.0
                     rootdir: /home/jhersch/repro/.pants.d, inifile: /home/jhersch/repro/.pants.d/test/pytest-prep/CPython-3.6.3/e9f6783c89fd0426d1c750e0263b13c6f6569ee4/pytest.ini
                     plugins: timeout-1.2.0, cov-2.4.0
                     collected 0 items / 1 errors
                     
                      generated xml file: /home/jhersch/repro/.pants.d/test/pytest/apps.gardener.test/junitxml/TEST-apps.gardener.test.xml 
                     ===================== ERRORS =====================
                      ERROR collecting pyprep/sources/7f177550d8bf3e8ceb7efe047d482bf955fb5d34/test_app.py 
                     ImportError while importing test module '/home/jhersch/repro/.pants.d/pyprep/sources/7f177550d8bf3e8ceb7efe047d482bf955fb5d34/test_app.py'.
                     Hint: make sure your test modules/packages have valid Python names.
                     Traceback:
                     .pants.d/pyprep/sources/7f177550d8bf3e8ceb7efe047d482bf955fb5d34/test_app.py:1: in <module>
                         import shrubberylib
                     E   ModuleNotFoundError: No module named 'shrubberylib'
                     ============ 1 error in 0.03 seconds =============
                     
                   apps/gardener:test                                                              .....   FAILURE
FAILURE: FAILURE


               Waiting for background workers to finish.
11:19:38 00:02   [complete]
               FAILURE

```
