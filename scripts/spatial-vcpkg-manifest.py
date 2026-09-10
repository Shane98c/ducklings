"""Derive a Worker-specific manifest from the pinned spatial dependency manifest."""
import json
import sys
from pathlib import Path

source, output = map(Path, sys.argv[1:3])
with_gdal = sys.argv[3] == '1'
manifest = json.loads((source / 'vcpkg.json').read_text())
# Workers use fetch-backed httpfs. Keep OpenSSL for httpfs' crypto headers/library.
omit = {'curl'} | (set() if with_gdal else {'gdal'})
manifest['dependencies'] = [
    dependency for dependency in manifest['dependencies']
    if (dependency if isinstance(dependency, str) else dependency['name']) not in omit
]
manifest['vcpkg-configuration']['overlay-ports'] = [str(source / 'vcpkg_ports')]
output.mkdir(parents=True, exist_ok=True)
(output / 'vcpkg.json').write_text(json.dumps(manifest, indent=2) + '\n')
