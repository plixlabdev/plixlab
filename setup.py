from setuptools import setup, find_packages

setup(
    name="plix",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',\
         'plotly',\
         'matplotlib',\
         'pycairo',\
         'pybtex',\
         'hash_dict',\
         'jsonpointer',\
         'msgpack',\
         'watchdog',\
         'tornado',\
         'jsonpatch',\
         'dict_hash',\
         'pandas',\
         'bokeh',\
         'requests',\
         'matplotlib',\
         'numpy'
    ],
      entry_points = {
     'console_scripts': ['plix=plix.plix_CLI:init']},

)
