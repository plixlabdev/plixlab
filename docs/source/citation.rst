Citation
=========

Citations can be imported with the tag ``cite``


.. code-block:: python

  from plix import Slide

  Slide().cite('einstein1935').show()

.. import_example:: citation

| where a file named ``biblio.bib`` is first searched in the current directory, then in the ``assets`` directory, and finally in the ``~/.plix`` folder. Multiple citations, which can be added using a list of keys, will be stacked vertically. You can adjust the fontsize with ``fontsize``. To further format the text and change its position, use the ``Bibliography`` utility, combined with ``tag``

.. code-block:: python

  from plix import Slide,Bibliography

  Slide().text(Bibliography.format('einstein1935'),fotsize=0.2,x=0.3,y=0.6).show()

.. import_example:: citation_text

| where we used general styling.   

