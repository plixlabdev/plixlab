Deployment
================================

To share a Plix presentation, you first need to get the `credentials <plix_web>`_. After registration, the file ``plix.json`` will be saved. Plix will first look in ``~/.plix/``, and then in the current directory. After you obtain the credentials, use ``share``


.. code-block:: python

   from plix import Slide

   Slide().text('Example Sharing').share()

A URL will be displayed. The visibility of this URL depends on the `plan <plix_plans>`_ you subscribed to. 
   

.. _plotly_web: https://plix.com
.. _plotly_plans: https://plix.com
