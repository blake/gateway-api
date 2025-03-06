# Copyright 2023 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import shutil
import logging
from mkdocs import plugins
from mkdocs.structure.files import File
from pathlib import Path

log = logging.getLogger(f'mkdocs.plugins.{__name__}')


@plugins.event_priority(100)
def on_files(files, config, **kwargs):
    log.info("adding geps")

    # Remove previous site-src/geps path
    site_src_geps = Path('site-src/geps')
    if site_src_geps.exists() and site_src_geps.is_dir():
      log.info("Found gep/ directory in site-src/. Deleting...")
      shutil.rmtree(site_src_geps)

    for root, _, gep_files, in Path('geps').walk():

      # Iterate over the all the files in the GEP folder and add them to the site
      for filename in gep_files:
        file_path = str(root / filename)

        if files.get_file_from_path(file_path) is None:
          new_file = File(
            path=file_path,
            src_dir='./',
            dest_dir=config['site_dir'],
            use_directory_urls=config['use_directory_urls']
          )
          new_file.generated_by = f'{__name__}'

          files.append(new_file)

    return files
