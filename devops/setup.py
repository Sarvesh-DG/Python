from setuptools import setup, find_packages

setup(
    name='dg_atulya_pkg',
    version='0.0.1',
    author='Atulya Kumar Pandey',
    author_email='atul3015@gmail.com',
    description='Test package deployment to pypi using gitlab',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)