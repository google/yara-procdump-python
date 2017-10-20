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

import setuptools

_yara_procdump = setuptools.Extension('yara_procdump',
                                      sources=['yara_procdump_python.c'],
                                      libraries=['yara'])

description = 'A Python extension to wrap the Yara process memory access API.'

try:
  long_description = open('README.md').read()
except IOError:
  long_description = description


setuptools.setup(
    name='yara-procdump-python',
    version='0.1',
    description=description,
    long_description=long_description,
    license='Apache 2.0',
    author='Andreas Moser',
    author_email='amoser@google.com',
    url='https://github.com/google/yara-procdump-python',
    ext_modules=[_yara_procdump])
