.. _plot2d_styles:

Plotting Styles
===============

.. toctree::
   :hidden:

   doc/*

The style system allow you to customize the look of your plots easily
and to maintain a consistent style on a large number of plots.  Styles
are used to control how plot elements look (color, marker style, line
style, font, etc.) and not how the plot is structured (line
vs. marker, which tick formatter to use, etc.).

They can be combined and chained together hierarchically.  They can be
edited programmaticaly via the python shell, or in a text editor.

All of these examples assume that you have imported the plot and style
manager into your script:

.. code-block:: python

   import pylab
   from mplStyle import mgr as smgr


Background and Problems
=======================

This style system was extracted from a much larger Python project and
so the current naming conventions, coding style, and package structure
is not ideal.  The conventions were those of the larger project and
have not been updated yet to be PEP8/MPL compliant.  The various
internal dependencies were extracted from the larger system as well so
the current package structure could be made a lot simpler.  This
overview document was also extracted from a larger custom Sphinx
documentation project and needs to be updated to work properly as a
standalone RST document.

If there is sufficient interest in this kind of style system, the hope
is that it can modified into a standard MPL package and delivered with
MPL.  At that point these style, documentation, and test conventions
can be addressed.

------------------------------------------------------------------------

.. _plot2d_styles_overview:

Overview
--------

The style system has two primary user interfaces: the style manager class,
and the style class.  The style manager is responsible for creating styles,
applying styles to plots, saving and loading styles, and remembering
which styles were applied to which plots so they can be automatically
updated.

The style class is responsible for storing the set of properties to
change in the plot.  Styles have a variety of display parameters,
applying to different parts of the plot.  Each parameter can be set or
unset.  When the style is applied to a plot, those parameters which
are set will be implemented; those parameters which are unset will be
ignored.

The structure of a style reflects the structure of a figure: in a figure,
there are usually  several contained objects (for example, an Axes object, 
a Line object, etc.).  Likewise, in a style the parameters are organized by
the type of object they affect: there are portions that affect only Axes
objects, only Line objects, etc.

The main style structure has some default attributes (bgColor,
fgColor, line, patch, text) which apply to any appropriate plot
element.  If you set a property in the text attribute of a style, it
will apply to any text in the plot (which is a nice way to control
fonts, colors, etc).  The figure and axes attributes are used to
control specific parts of the plot (e.g. axes.xAxes applies just to
the X axis and axes.yAxes applies just to the Y axes).

The basic MplStyle structure looks like this:

      +--------------+-----------------------------+-------------------------------------+
      | **Property** | **Type**                    | **Description**                     |
      +==============+=============================+=====================================+
      | axes         | `Axes <doc/axes.rst>`__     | Controls how to style an Axes and   |
      |              |                             | all it's components.                |
      +--------------+-----------------------------+-------------------------------------+
      | bgColor      | `Color <doc/color.rst>`__   | The default background color to use |
      |              |                             | for a sub-style if none is          |
      |              |                             | is specified (i.e. the default      |
      |              |                             | background color).                  |
      +--------------+-----------------------------+-------------------------------------+
      | fgColor      | `Color <doc/color.rst>`__   | The default foreground color to use |
      |              |                             | for a sub-style if none is          |
      |              |                             | is specified (i.e. the default      |
      |              |                             | foreground color).                  |
      +--------------+-----------------------------+-------------------------------------+
      | figure       | `Figure <doc/figure.rst>`__ | Controls how to style a Figure.     |
      +--------------+-----------------------------+-------------------------------------+
      | line         | `Line <doc/line.rst>`__     | This specifies the style properties |
      |              |                             | for line elements plotted on an     |
      |              |                             | Axes.                               |
      +--------------+-----------------------------+-------------------------------------+
      | patch        | `Patch <doc/patch.rst>`__   | This specifies the style properties |
      |              |                             | for patch elements plotted on an    |
      |              |                             | Axes.                               |
      +--------------+-----------------------------+-------------------------------------+
      | text         | `Text <doc/text.rst>`__     | The default text style to use.      |
      |              |                             | Sub-style elements may override for |
      |              |                             | specific pieces of text.            |
      +--------------+-----------------------------+-------------------------------------+

.. note::

   The full list of available parameters can be found here:
   `Full List <doc/style_all.rst>`__ 

------------------------------------------------------------------------

.. _plot2d_styles_create:

Style Creation
--------------

Styles are created by calling the manager create method with the name
of the style.  Once the style has been created, set the parameters on
the style using the names of the style attributes (see the top level
style structure above for the possible names)

.. code-block:: python

   # Create the style
   style = smgr.create( "Big Title" )

   # Change the axes title font.
   style.axes.title.font.family = "sans-serif"
   style.axes.title.font.size = 24

You can also pass a dictionary of style attributes to the create
method to create and initialize the style in one call.  The keys of
the dictionary are the string form of the variable path: so the
variable style.this.parameter.path becomes the dictionary key
'this.parameter.path'.  The value associated with each key needs to be
of the proper type for the parameter; some require floating point
values, integers, booleans, or other strings.

.. code-block:: python

   # Create the style
   style = smgr.create( "Big Title", {
                        "axes.title.font.family" : "sans-serif",
                        "axes.title.font.size" : 24,
                        } )


When defining a style, you can optionally name a parent style.  When the 
style is applied, the parent style is automatically applied first.  This
means that a child style will overwrite the settings contained in the
parent style, if and when those styles conflict.

.. code-block:: python

   # Create the style to make fonts larger and easier to read.
   s1 = smgr.create( "Big Text" )
   s1.text.font.scale = 1.5

   # Create a new style, with a parent style   
   s2 = smgr.create( 'Presentation', parent='Big Text' )

   # Set something particular to the child style
   s2.figure.width = 800
   s2.figure.height = 600

   # Big Text will be applied before the other parts of Presentation
   smgr.apply( fig, 'Presentation' )

It should be noted that in the above example the 'Big Text' style is
*not* overwritten when we create the 'Presentation' style.  This is
because when we create styles in this manner, they are automatically
registered and stored in a style manager class.  They can then be
access later by name.


Setting Attributes
------------------

Each Style object has a set of parameters affecting how plots are
displayed.  The parameters are unset by default; they will not affect
the display of a plot unless they are set.  In an existing style
object, you can use Python's dot syntax to access and set parameters.

To access an already defined style, use the find() method on the manager

.. code-block:: python

   # Find a previous define dstyle
   style = smgr.find( "Big Text" )

   # Change some of the style attributes
   style.text.font.size = 16


Applying Styles to a Plot
-------------------------

Styles can be applied to any matplotlib plot element (figures, axes,
axis, lines, etc).  Applying the style to the figure is most common
use case.  When you apply a style to a figure, it will search the
figure for various plot elements and axes and recursively apply the
same style to them (the same is true when calling apply only on the
axes).

The style attributes dictate which matplotlib elements are modified.
So the attribute axes.bgColor will only change the color of the axes
while the attribute figure.bgColor will change the background for the
figure.

Style are applied using the apply method on the manager.  You can pass
in the style object or the name of the style to apply.

.. code-block:: python

   fig, ax = pylab.subplots()
   lines = ax.plot( [1, 2, 3, 4, 5], [2, 1, 0, 1, 2] )
   ax.set_title( "This is the Title" )
   
   # Create the style and set some fields
   style = smgr.create( "Big Title" )
   style.axes.title.font.family = "sans-serif"
   style.axes.title.font.size = 24

   # Apply the style to the figure.
   smgr.apply( fig, style )

   # Apply a list of styles to just the lines.
   smgr.apply( lines, [ "Dashed Lines", "Blue Lines", "Bold Lines" ] )

The style manager will recursively walk down through the input plot
element and apply the style.  So if a plot contains four subplots, the
axes style will be applied to each of the four subplots and the text
style will apply to all the text in the plot.  If you want to apply
the style only the input object (say an input figure), pass
recurse=False to the apply method.

.. code-block:: python

   # Apply the style only to the figure
   smgr.apply( fig, 'Figure Style', recurse=False )


Updating and Re-applying Styles
-------------------------------

When the manager applyes a style to the figure (or to any other other
plotting element), the manager will remember what style was applied to
which element, so if you later modify any styles, the changes can be
automatically applied to the plot elements by calling the reapply
method.

.. code-block:: python

   # Modify the style
   style.axes.title.font.size = 16

   # Apply the update to everything that is currently using it.
   smgr.reapply()

This will change the fonts from size 24 (the original "Big Title"
size) to the new size of 16 and update the plot.  The reapply() method
will update any and all plots that have styes applied to them.


Saving & Loading
----------------

The style manager can be used to save and load styles to a persistent
form.  Each style is saved into a file with the form
'Style_Name.mplstyle'.  Style files are human readable, Python files
and may be edited by the user.  Styles are NOT automatically saved and
loaded by the manager (though that could change based on user
feedback).

.. note::

   Style names including a space ' ' will be changed to use an
   underscore '_' when saved as a .mplstyle file.  For Example, 
   a style named "DSS 16" will be saved as "DSS_16.mplstyle".

To save the current set of styles, use the manager save method.  To
load all the available styles, use the load method.

.. code-block:: python

   # Save the current styles to $HOME/.masar/styles
   smgr.save()

   # Save the current styles to the local directory.
   smgr.save( "." )

   # Load all available styles.
   smgr.load()

When loading styles, the manager will use a search path that looks for
styles in the following order (high priority to low priority):

#. The current directory.
#. The user's home directory: $HOME/.matplotlib/styles/

Styles that are defined in more than one of these locations will use
the first definition.  This way, each user can override and customize
certain Monte styles to their liking; they can also use different
directories to try out different style options in parallel.  You can
change the list of directories to look in by modifying your STYLEPATH
environment variable.

You can also manipulate the loading and saving of styles in your
Python script directly.  The "path" variable on the style manager is a
simple Python list of directory names.  By changing the path, you can
change what styles are loaded:

.. code-block:: python

   # Add a search path and load the styles.
   smgr.path.append( "/proj/scripts/styles" )
   smgr.load()


Tagging Plot Elements
---------------------

.. _plot2d_styles_tags:

Tagging or style tags are way to filter which plot elements (figure,
axes, lines, etc) a style is applied to by setting a tag (string name)
to a plot element.  The script that creates the plot tags each element
with a name.  When a style is applied to an element, the tag input can
be specified to limit which elements get changed.

Let's say you have a plot that shows two lines for each DSN complex
(Goldstone, Canberra, and Madrid).  The plotting script has access to
those lines and knows which complex they are a part of but the lines
are hard to get to after the plotting script is finished.  If the
plotting script tags the lines with the complex name like this:

.. code-block:: python

   def createPlot():
      fig, ax = pylab.subplots()
      # create data to plot, layout plot, etc.

      l = ax.plot( gldX, gldY )
      smgr.tag( l, "Goldstone" )

      l = ax.plot( madX, madY )
      smgr.tag( l, "Madrid" )

      l = ax.plot( canX, canY )
      smgr.tag( l, "Canberra" )

      return fig

The calling script can use those tags to apply styles to the
individual lines without having direct access to them.  Both the
apply() and set() functions can use the tag keyword to filter which
elements are used.

.. code-block:: python

   fig = createPlot()

   # Apply the 'Goldstone Style' to elements tagged Goldstone
   smgr.apply( fig, "Goldstone Style", tag="Goldstone" )

   # Change every line tagged Canberra to be blue.
   smgr.set( fig, { 'line.color' : 'blue' }, tag="Canberra" )

Tags are a powerful tool that allows you to write complicated plotting
scripts and then control individual elements in those plots using
styles from outside the plotting script.


.. _plot2d_styles_unmanaged:

Setting Attributes and Unmanaged Styles
---------------------------------------

The style system can also be used to quickly set plot attributes
without creating a style by calling the manager set() method.  This
method can accept either a single style attribute or a dictionary of
style attributes and can use the tag system to filter which plot
elements are set.

.. code-block:: python

   # Change the background color to black.
   smgr.set( fig, "bgColor", "black" )

   # Change the multiple attributes.
   smgr.set( fig, { "bgColor" : "black",
                    "fgColor" : "white",
                    "text.font.scale" : 1.25 } )

   # Change lines tagged 'DSS 14' to gold.
   smgr.set( fig, "line.color", "gold", tag="DSS 14" )

An "unmanaged" style can be created using the style constructor and
applied directly to a plot.  The style manager will have no knowlege
of this style and so reapply will not work, and the style will not be
saved.

.. code-block:: python

   import mpy.plot.style as S

   # Unmanaged style - won't be saved.
   style = S.MplStyle( 'dummy' )

   # Must use style.apply(), smgr.apply() won't work.
   style.apply( fig )


------------------------------------------------------------------------

.. _plot2d_styles_example:

An Example
----------

Following is a more complete example on how to make the plot at the top of
this page:

.. code-block:: python

   # import some modules
   import pylab
   from mplStyle import mgr as smgr

   # create the plot
   fig, ax = pylab.subplots()

   xdata = [ 1, 1.5,  2, 2.5,  3, 3.5,  4, 4.5,  4.75, 5 ]
   ydata = [ 1, 1.75, 2, 2.75, 3, 2.75, 2, 2.25, 2.75, 3 ]
   line = ax.plot( xdata, ydata )

   rect = mpylab.Rectangle( (2.8, 1.0), 0.4, 1.2 )
   ax.add_patch( rect )

   figTitle = fig.suptitle( "Figure Title" )
   axTitle = ax.set_title( "Axes Title" )
   xLabel = ax.set_xlabel( "X-Axis Label" )
   yLabel = ax.set_ylabel( "Y-Axis Label" )

   figText = fig.text( 0.02, 0.02, "FigureText" )
   txt = ax.text( 4.2, 1.1, "Text" )

   # Create the style
   style = smgr.create( "My Style" )
   style.bgColor = 'white'
   style.fgColor = 'black'
   # Figure
   style.figure.width = 10
   style.figure.height = 10
   # Axes
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
   # Lines
   style.line.color = "blue"
   style.line.style = 'dash-dot'
   style.line.width = 1.5
   style.line.marker.color = 'red'
   style.line.marker.edgeColor = 'green'
   style.line.marker.edgeWidth = 3
   style.line.marker.size = 20
   style.line.marker.style = 'circle'
   style.line.marker.fill = 'bottom'
   # Patches
   style.patch.color = 'gold'
   style.patch.filled = True
   style.patch.edgeColor = 'purple'
   style.patch.edgeWidth = 5
   # Text
   style.text.lineSpacing = 1.0
   style.text.font.size = 12
   style.text.font.family = 'monospace'

   # apply the style
   smgr.apply( fig, style )


                    |
      +--------------+----------------------------------------+-------------------------------------+
      | bgColor      | :ref:`color <plot2d_color>`            | The background color of the axes.   |
      +--------------+----------------------------------------+-------------------------------------+
      | bottomEdge   | :ref:`Sub-Style <plot2d_edge_styling>` | The style properties for the bottom |
      |              |                                        | axes edge.                          |
      +--------------+----------------------------------------+-------------------------------------+
      | fgColor      | :ref:`fgColor <plot2d_color>`          | The forground color for axes        |
      |              |                                        | components.                         |
      +--------------+----------------------------------------+-------------------------------------+
      | frameWidth   | float                                  | The with of the axes border frame.  |
      +--------------+----------------------------------------+-------------------------------------+
      | labels       | :ref:`Sub-Style <plot2d_text_styling>` | Set this to influence tick labels   |
      |              |                                        | and axis labels.                    |
      +--------------+----------------------------------------+-------------------------------------+
      | leftEdge     | :ref:`Sub-Style <plot2d_edge_styling>` | The style properties for the left   |
      |              |                                        | axes edge.                          |
      +--------------+----------------------------------------+-------------------------------------+
      | rightEdge    | :ref:`Sub-Style <plot2d_edge_styling>` | The style properties for the right  |
      |              |                                        | axes edge.                          |
      +--------------+----------------------------------------+-------------------------------------+
      | showFrame    | bool                                   | The visibility of the axes frame    |
      +--------------+----------------------------------------+-------------------------------------+
      | title        | :ref:`Sub-Style <plot2d_text_styling>` | This controls how title text looks  |
      |              |                                        | for a given axes.                   |
      +--------------+----------------------------------------+-------------------------------------+
      | topEdge      | :ref:`Sub-Style <plot2d_edge_styling>` | The style properties for the top    |
      |              |                                        | axes edge.                          |
      +--------------+----------------------------------------+-------------------------------------+
      | visible      | bool                                   | Is the axes (and all components)    |
      |              |                                        | visible or not.                     |
      +--------------+----------------------------------------+-------------------------------------+
      | xAxis        | :ref:`Sub-Style <plot2d_axis_styling>` | The style properties for the        |
      |              |                                        | x-axis.                             |
      +--------------+----------------------------------------+-------------------------------------+
      | yAxis        | :ref:`Sub-Style <plot2d_axis_styling>` | The style properties for the        |
      |              |                                        | y-axis.                             |
      +--------------+----------------------------------------+-------------------------------------+
      | zOrder       | float                                  | The z-order value is used for depth |
      |              |                                        | sorting.                            |
      +--------------+----------------------------------------+-------------------------------------+

