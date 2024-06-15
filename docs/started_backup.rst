PLIX Quickstart
===============

A minimal single-slide presentation can be created with two lines of code

.. code-block:: python

  from plix import Slide
  
  Slide().text('Welcome to Plix!').show()


.. import_example:: plix.pkl

Plix features several interactive data-oriented components. Here is an example for embedding plotly data


.. code-block:: python

  from plix import Slide
  import plotly.express as px

  df = px.data.iris()

  fig = px.scatter(df, x="sepal_width", \
                     y="sepal_length", \
                     color="species")

  Slide().plotly(fig).show()


.. import_example:: plotly_example.pkl

.. code-block:: python

  from plix import Slide
 
  Slide().img('assets/image.png').show()

.. import_example:: example_2.pkl

To add multiple objects:

   .. code-block:: python

  from plix import Slide
 
  Slide().img('assets/image.png',w=0.4,x=0.2,y=0.4).\
          text('Hello, World!',x=0.7,y=0.5,fontsize=0.05).show()

.. import_example:: example_3.pkl

The coordinates, width and fontsize are all normalized to the slide's size.

To add animation:

.. code-block:: python

  from plix import Slide
 
  Slide().img('assets/image.png',w=0.4,x=0.2,y=0.4,animation=0).\
          text('Hello, World!',x=0.7,y=0.5,fontsize=0.05,animation=1).show()

.. import_example:: example_4.pkl

Animations, which are activated with arrows, are only shown in full mode.
To have multiple slides:

.. code-block:: python

  from plix import Slide,Presentation
 
  S1 = Slide().text('Slide 1')
  S2 = Slide().text('Slide 2')

  Presentation([S1,S2]).show()
..

.. import_example:: example_5.pkl

To deploy to the cloud:

.. code-block:: python

  from plix import Slide
 
  Slide().img('assets/image.png',w=0.4,x=0.2,y=0.4,animation=0).\
          text('Hello, World!',x=0.7,y=0.5,fontsize=0.05,animation=1).share()

Note that to deploy a presentation you need to get the token first.

  




