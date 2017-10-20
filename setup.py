# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup.py for yara-procdump-python."""

from distutils.command import build
from distutils.command import build_ext
import setuptools

_yara_procdump = setuptools.Extension('yara_procdump',
                                      sources=['yara_procdump_python.c'],
                                      include_dirs=['yara/libyara',
                                                    'yara/libyara/include'])

OPTIONS = [
    ('dynamic-linking', None, 'link dynamically against libyara'),
]

BOOLEAN_OPTIONS = [
    'dynamic-linking',
]

description = 'A Python extension to wrap the Yara process memory access API.'

try:
  long_description = open('README.md').read()
except IOError:
  long_description = description


class BuildCommand(build.build):

  user_options = build.build.user_options + OPTIONS
  boolean_options = build.build.boolean_options + BOOLEAN_OPTIONS

  def initialize_options(self):
    build.build.initialize_options(self)
    self.dynamic_linking = None


class BuildExtCommand(build_ext.build_ext):
  """A custom command to build the extension."""

  user_options = build_ext.build_ext.user_options + OPTIONS
  boolean_options = build_ext.build_ext.boolean_options + BOOLEAN_OPTIONS

  def initialize_options(self):
    build_ext.build_ext.initialize_options(self)
    self.dynamic_linking = None

  def finalize_options(self):
    build_ext.build_ext.finalize_options(self)
    self.set_undefined_options('build',
                               ('dynamic_linking', 'dynamic_linking'))

  def run(self):
    """Execute the build command."""

    module = self.distribution.ext_modules[0]

    building_for_windows = self.plat_name in ['win32', 'win-amd64']
    if building_for_windows:
      module.define_macros.append(('_CRT_SECURE_NO_WARNINGS', '1'))
      module.libraries.append('advapi32')

    if self.dynamic_linking:
      module.libraries.append('yara')
    else:
      module.sources.append('yara/libyara/arena.c')
      module.sources.append('yara/libyara/hash.c')
      module.sources.append('yara/libyara/hex_grammar.c')
      module.sources.append('yara/libyara/hex_lexer.c')
      module.sources.append('yara/libyara/libyara.c')
      module.sources.append('yara/libyara/mem.c')
      module.sources.append('yara/libyara/modules.c')
      module.sources.append('yara/libyara/object.c')
      module.sources.append('yara/libyara/proc.c')
      module.sources.append('yara/libyara/re.c')
      module.sources.append('yara/libyara/re_grammar.c')
      module.sources.append('yara/libyara/re_lexer.c')
      module.sources.append('yara/libyara/sizedstr.c')
      module.sources.append('yara/libyara/stream.c')
      module.sources.append('yara/libyara/strutils.c')
      module.sources.append('yara/libyara/threading.c')
      module.sources.append('yara/libyara/modules/elf.c')
      module.sources.append('yara/libyara/modules/math.c')
      module.sources.append('yara/libyara/modules/pe.c')
      module.sources.append('yara/libyara/modules/pe_utils.c')
      module.sources.append('yara/libyara/modules/time.c')
      module.sources.append('yara/libyara/modules/tests.c')

    build_ext.build_ext.run(self)


setuptools.setup(
    name='yara-procdump-python',
    version='0.1.0.post2',
    description=description,
    long_description=long_description,
    license='Apache 2.0',
    author='Andreas Moser',
    author_email='amoser@google.com',
    url='https://github.com/google/yara-procdump-python',
    cmdclass={
        'build': BuildCommand,
        'build_ext': BuildExtCommand,
    },
    ext_modules=[_yara_procdump])
