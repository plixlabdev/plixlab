Markdown
========

The tag ``text`` accepts Markdown syntax, e.g.

.. code-block:: python

  from plix import Slide
  
  Slide().text('<u> This </u> **text** is *really important*.',x=0.2,y=0.6,\
                 fontsize=0.1,color='orange').show()

.. import_example:: markdown

| The options ``x``, ``y`` and ``fontsize`` are all in fractional coordinates, normalized to the slide's dimension. If the ``x`` coordinate is not provided, the text will be centered horizontally. If the ``y`` coordinate is not provided, the text will be centered vertically. 
