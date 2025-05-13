Installing PLIX
================

   
PLIX can be installed as a PIP package

.. code-block:: bash

   python3 -m venv plix-env

   source plix-env/bin/activate

   pip install --upgrade pip

   pip install -U --no-cache  git+https://github.com/ComputoLab/plix.git


Test:

.. code-block:: bash

   python -c 'import plix; plix.Slide().text(r"Welcome to Plix!").show()'




