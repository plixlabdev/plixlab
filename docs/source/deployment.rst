Deployment
================================

To share a PlixLab presentation, you first need to get the `credentials <plix_web>`_. After registration, the file ``plixlab.json`` will be saved. Plix will first look in ``~/.plixlab/``, and then in the current directory. After you obtain the credentials, use ``share``


.. code-block:: python

   from plixlab import Slide

   Slide().text('Example Sharing').share()

A URL will be displayed. The visibility of this URL depends on the `plan <plix_plans>`_ you subscribed to. 
   

.. _plotly_web: https://plix.com
.. _plotly_plans: https://plix.com
