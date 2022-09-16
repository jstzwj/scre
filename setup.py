
import setuptools
from Cython.Build import cythonize

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

extensions = [
    setuptools.Extension("*", ["scre/*/*.py"])
]

setuptools.setup(
    name="scre",
    version="0.0.1",
    author="Jun Wang",
    author_email="jstzwj@aliyun.com",
    description="SooChow Regular Expression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jstzwj/scre",
    project_urls={
        "Bug Tracker": "https://github.com/jstzwj/scre/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    ext_modules=cythonize(
        extensions,
        language_level = "3",
        annotate=True,
        compiler_directives={'language_level' : "3"},   # or "2" or "3str"
    ),
)