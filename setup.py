from setuptools import setup, find_packages

setup(
    name="plix",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests','plotly','matplotlib','pycairo','kaleido','pybtex','hash_dict','msgpackr','watchdog'
    ],
      entry_points = {
     'console_scripts': ['plix=plix.plix_CLI:init']},

)
