Hot reload
===========

When you show a presentation, any change to the document is immediately applied to the live presentation, as long as the local server is still running. To disable this option, you can use ``hot_reload``


.. code-block:: python

   from plixlab import Slide

   Slide.text('Example Hot Reload').show(hot_reload=False)
