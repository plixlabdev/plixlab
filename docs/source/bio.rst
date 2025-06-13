Bio
==========

Bio plots are based on `Dash-bio`_ and can be created with the ``plotly`` module. Currently, only Volcano plots are supported:

.. code-block:: python

  from plix import Slide
  import dash_bio as dashbio
  import pandas as pd

  df = pd.read_csv('https://git.io/volcano_data1.csv')
  
  fig=dashbio.VolcanoPlot(dataframe=df)

  Slide().plotly(fig).show()

.. import_example:: volcano


.. _Dash-bio: https://dash.plotly.com/dash-bio
