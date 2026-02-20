import pathlib
from setuptools import find_packages, setup

def requirements(filepath: str):
    path = pathlib.Path(filepath)
    if not path.exists():
        return []

    reqs: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith('-r '):
            nested = line.split(maxsplit=1)[1].strip()
            reqs.extend(requirements(nested))
            continue
        if line.startswith('--requirement '):
            nested = line.split(maxsplit=1)[1].strip()
            reqs.extend(requirements(nested))
            continue

        if line.startswith('-') or line.startswith('--'):
            continue

        reqs.append(line)
    return reqs

setup(
    name='ml_app',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.9',
    install_requires=requirements('requirements.txt'),
    extras_require={'dev': requirements('requirements-dev.txt')},
)