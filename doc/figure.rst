.. _plot2d_figure_styling:

Styling
-------

An example of how to style a Figure is like so:

.. code-block:: python

   import pylab
   import mplStyle as S

   # Get a figure
   fig = pylab.figure()

   # Create a style
   style = S.mgr.createStyle( 'Figure Style' )

   style.figure.width = 8
   style.figure.height = 8
   style.figure.bgColor = 'white'

   # Apply the style
   S.mgr.apply( fig, style )


Following is a list of possible Figure style properties:

      +--------------+-----------------------------+---------------------------------------------------------+
      | **Property** | **Type**                    | **Description**                                         |
      +==============+=============================+=========================================================+
      | axesPadX     | float                       | The pad to put between Axes in the x-direction.         |
      +--------------+-----------------------------+---------------------------------------------------------+
      | axesPadY     | float                       | The pad to put between Axes in the y-direction.         |
      +--------------+-----------------------------+---------------------------------------------------------+
      | bgColor      | `Color <color.rst>`__       | The background color value of the figure.               |
      +--------------+-----------------------------+---------------------------------------------------------+
      | bottomMargin | float                       | The bottom side margin of the figure (in figure coords).|
      +--------------+-----------------------------+---------------------------------------------------------+
      | dpi          | float                       | The resolution of the figure (in dots=per-inch).        |
      +--------------+-----------------------------+---------------------------------------------------------+
      | edgeColor    | `Color <color.rst>`__       | The color of the frame edge.                            |
      +--------------+-----------------------------+---------------------------------------------------------+
      | edgeStyle    | enum                        | The style to use for the edge line.  This can be one of |
      |              |                             | values:                                                 |
      |              |                             |                                                         |
      |              |                             |    +------+---------------+                             |
      |              |                             |    |  \-  | Solid line    |                             |
      |              |                             |    +------+---------------+                             |
      |              |                             |    | \-\- | Dashed line   |                             |
      |              |                             |    +------+---------------+                             |
      |              |                             |    |  -.  | Dash-Dot line |                             |
      |              |                             |    +------+---------------+                             |
      |              |                             |    |   :  | Dotted line   |                             |
      |              |                             |    +------+---------------+                             |
      |              |                             |    | None | No line       |                             |
      |              |                             |    +------+---------------+                             |
      +--------------+-----------------------------+---------------------------------------------------------+
      | edgeWidth    | float                       | The width (in pixels) of the edge line.                 |
      +--------------+-----------------------------+---------------------------------------------------------+
      | height       | float                       | The height (in inches) of the figure.                   |
      +--------------+-----------------------------+---------------------------------------------------------+
      | leftMargin   | float                       | The left-hand side margin of the figure (in figure coord|
      +--------------+-----------------------------+---------------------------------------------------------+
      | rightMargin  | float                       | The right-hand side margin of the figure (in figure coor|
      +--------------+-----------------------------+---------------------------------------------------------+
      | topMargin    | float                       | The top side margin of the figure (in figure coords).   |
      +--------------+-----------------------------+---------------------------------------------------------+
      | width        | float                       | The width (in inches) of the figure.                    |
      +--------------+-----------------------------+---------------------------------------------------------+

