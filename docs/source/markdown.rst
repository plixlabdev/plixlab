Markdown
========

The tag ``text`` accepts Markdown syntax, e.g.

.. code-block:: python

  from plix import Slide
  
  Slide().text('<u> This </u> **text** is *really important*.',x=0.2,y=0.6,\
                 fontsize=0.1,color='orange').show()


.. import_example:: markdown

Equations are supported via Mathjax. You can use latex format between the dollar signs, i.e.


.. code-block:: python

  from plix import Slide
  
  Slide().text(r'''$\frac{1}{2}$''').show()


