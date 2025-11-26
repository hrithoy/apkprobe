# © 2024 Lucas Faudman.
# Licensed under the MIT License (see LICENSE for additional terms).
# For commercial use, see LICENSE for additional terms.
import sys
sys.path.insert(0, 'src')
from apkprobe import _compat
from setuptools import setup, find_namespace_packages
from setuptools.command.build_ext import build_ext

EXT_MODULES = []
try:
    from mypyc.build import mypycify

    EXT_MODULES.extend(
        mypycify(
            [
                "src/apkprobe/apkprobe.py",
                "src/apkprobe/concurrent_executor.py",
                "src/apkprobe/decompiler.py",
                "src/apkprobe/secret_scanner.py",
            ]
        )
    )
except Exception as e:
    print(f"Failed to compile with mypyc: {e}")

setup(
    name="apkprobe",
    version="0.4.0",
    use_scm_version=True,
    setup_requires=["setuptools>=42", "setuptools_scm>=8", "wheel"],
    description="APK decompiler and secrets scanner. Find leaked API keys, endpoints, credentials in Android apps.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="wadingporque",
    author_email="",
    url="https://github.com/wadingporque/apkprobe",
    packages=find_namespace_packages(where="src", exclude=["tests*"]),
    package_dir={"": "src"},
    package_data={
        "": ["LICENSE"],
        "apkprobe.secret_locators": ["*.json", "*.yaml", "*.yml", "*.toml"],
    },
    include_package_data=True,
    exclude_package_data={"": [".gitignore", ".pre-commit-config.yaml"]},
    install_requires=["enjarify-adapter", "pyyaml"],
    ext_modules=EXT_MODULES,
    cmdclass={"build_ext": build_ext},
    extras_require={
        "mypyc": [
            "mypy[mypyc]",
            "mypy_extensions",
        ]
    },
    entry_points={
        "console_scripts": [
            "apkprobe = apkprobe.main:main",
        ],
    },
    python_requires=">=3.10",
    license="LICENSE",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    keywords="secret scanner jadx decompile android java security mobile decompiler concurrency penetration-testing apktool security-tools fernflower cfr jadx procyon enjarify krakatau secret-scanning decompiler-java secret-scanner apk dex jar class smali zip aar arsc aab xapk jadx.kts ",
    project_urls={
        "Homepage": "https://github.com/wadingporque/apkprobe",
        "Repository": "https://github.com/wadingporque/apkprobe",
    },
)
