
.. _plot2d_axes_styling:

Styling
-------

An axes can be styled by itself or as part of a figure.  An example of
how to style an Axes is like so:

.. MPY_GUI_TEST:
.. code-block:: python

   import pylab
   import mplStyle as S

   # Get some axes
   ax = pylab.axes()

   # Create a style
   style = S.mgr.createStyle( 'Axes Style' )

   # Set some properties
   style.axes.axisBelow = True
   style.axes.leftEdge.color = 'magenta'
   style.axes.leftEdge.width = 5
   style.axes.leftEdge.style = '--'
   style.axes.bottomEdge.color = 'magenta'
   style.axes.bottomEdge.width = 5
   style.axes.bottomEdge.style = 'dashed'
   style.axes.topEdge.visible = False
   style.axes.rightEdge.visible = False
   style.axes.title.font.scale = 2.0
   style.axes.title.font.family = 'sans-serif'
   # X-Axis
   style.axes.xAxis.autoscale = True
   style.axes.xAxis.dataMargin = 0.1
   style.axes.xAxis.label.font.scale = 1.2
   style.axes.xAxis.majorTicks.labels.font.scale = 0.75
   style.axes.xAxis.majorTicks.marks.visible = True
   style.axes.xAxis.majorTicks.grid.visible = True
   style.axes.xAxis.majorTicks.grid.color = '#B0B0B0'
   style.axes.xAxis.majorTicks.grid.width = 1.5
   style.axes.xAxis.majorTicks.grid.style = ':'
   style.axes.xAxis.majorTicks.length = 15.0
   style.axes.xAxis.majorTicks.width = 1.5
   style.axes.xAxis.minorTicks.marks.visible = True
   style.axes.xAxis.minorTicks.grid.visible = True
   style.axes.xAxis.minorTicks.grid.color = '#B0B0B0'
   style.axes.xAxis.minorTicks.grid.width = 0.5
   style.axes.xAxis.minorTicks.grid.style = ':'
   style.axes.xAxis.minorTicks.length = 5.0
   style.axes.xAxis.minorTicks.width = 0.5
   # Y-Axis
   style.axes.yAxis = style.axes.xAxis.copy()

   # Apply the style
   S.mgr.apply( ax, style )

In the above example, we set the yAxis properties to be the same as the
xAxis properties, but since we do not want a change in one to affect the
other, we copy xAxis before setting yAxis.

Following is a list of possible Axes style properties:

      +--------------+----------------------------------------+-------------------------------------+
      | **Property** | **Type**                               | **Description**                     |
      +==============+========================================+=====================================+
      | alpha        | float     [0.0 -> 1.0]                 | The transparency value of the axes. |
      +--------------+----------------------------------------+-------------------------------------+
      | axisBelow    | bool                                   | Should the axis lines be below the  |
      |              |                                        | plot elements                       |
      +--------------+----------------------------------------+-------------------------------------+
      | bgColor      | `Color <color.rst>`__                  | The background color of the axes.   |
      +--------------+----------------------------------------+-------------------------------------+
      | bottomEdge   | `Edge <edge.rst>`__                    | The style properties for the bottom |
      |              |                                        | axes edge.                          |
      +--------------+----------------------------------------+-------------------------------------+
      | fgColor      | `Color <doc/color.rst>`__              | The forground color for axes        |
      |              |                                        | components.                         |
      +--------------+----------------------------------------+-------------------------------------+
      | frameWidth   | float                                  | The with of the axes border frame.  |
      +--------------+----------------------------------------+-------------------------------------+
      | labels       | `Text <text.rst>`__                    | Set this to influence tick labels   |
      |              |                                        | and axis labels.                    |
      +--------------+----------------------------------------+-------------------------------------+
      | leftEdge     | `Edge <edge.rst>`__                    | The style properties for the left   |
      |              |                                        | axes edge.                          |
      +--------------+----------------------------------------+-------------------------------------+
      | rightEdge    | `Edge <edge.rst>`__                    | The style properties for the right  |
      |              |                                        | axes edge.                          |
      +--------------+----------------------------------------+-------------------------------------+
      | showFrame    | bool                                   | The visibility of the axes frame    |
      +--------------+----------------------------------------+-------------------------------------+
      | title        | `Text <text.rst>`__                    | This controls how title text looks  |
      |              |                                        | for a given axes.                   |
      +--------------+----------------------------------------+-------------------------------------+
      | topEdge      | `Edge <edge.rst>`__                    | The style properties for the top    |
      |              |                                        | axes edge.                          |
      +--------------+----------------------------------------+-------------------------------------+
      | visible      | bool                                   | Is the axes (and all components)    |
      |              |                                        | visible or not.                     |
      +--------------+----------------------------------------+-------------------------------------+
      | xAxis        | `Axis <axis.rst>`__                    | The style properties for the        |
      |              |                                        | x-axis.                             |
      +--------------+----------------------------------------+-------------------------------------+
      | yAxis        | `Axis <axis.rst>`__                    | The style properties for the        |
      |              |                                        | y-axis.                             |
      +--------------+----------------------------------------+-------------------------------------+
      | zOrder       | float                                  | The z-order value is used for depth |
      |              |                                        | sorting.                            |
      +--------------+----------------------------------------+-------------------------------------+

