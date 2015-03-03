
.. _plot2d_text_styling:

Styling
-------

Any text that appears on a plot will have (at a minimum) the
properties described here.  Following is a list of possible Text
style properties:

      +--------------+----------------------------------------+-------------------------------------+
      | **Property** | **Type**                               | **Description**                     |
      +==============+========================================+=====================================+
      | alpha        | float    [0.0 -> 1.0]                  | The transparency value of the text. |
      +--------------+----------------------------------------+-------------------------------------+
      | bgColor      | `Color <color.html>`__                 | The background color for the        |
      |              |                                        | bounding box containing the text.   |
      +--------------+----------------------------------------+-------------------------------------+
      | clip         | bool                                   | Should the text be clipped by the   |
      |              |                                        | Axes bounds.                        |
      +--------------+----------------------------------------+-------------------------------------+
      | color        | `Color <color.html>`__                 | The color of the text.              |
      +--------------+----------------------------------------+-------------------------------------+
      | fgColor      | `Color <color.html>`__                 | The color of the text.  This is the |
      |              |                                        | same as 'color'.                    |
      +--------------+----------------------------------------+-------------------------------------+
      | font         | `Font <font.html>`__                   | The properties for setting the font |
      |              |                                        | used for this text.                 |
      +--------------+----------------------------------------+-------------------------------------+
      | horizAlign   | enum                                   | The horizontal alignment of the     |
      |              |                                        | text bounding box.                  |
      |              |                                        | Can be one of the following values: |
      |              |                                        |                                     |
      |              |                                        |    * 'center'                       |
      |              |                                        |    * 'left'                         |
      |              |                                        |    * 'right'                        |
      +--------------+----------------------------------------+-------------------------------------+
      | lineSpacing  | float                                  | The space between lines (as a       |
      |              |                                        | multiple of the font size).         |
      +--------------+----------------------------------------+-------------------------------------+
      | multiAlign   | enum                                   | The alignment of the text within    |
      |              |                                        | the bounding box.                   |
      |              |                                        | Can be one of the following values: |
      |              |                                        |                                     |
      |              |                                        |    * 'center'                       |
      |              |                                        |    * 'left'                         |
      |              |                                        |    * 'right'                        |
      +--------------+----------------------------------------+-------------------------------------+
      | rotation     | float                                  | The rotation of the text (in        |
      |              |                                        | degrees).                           |
      +--------------+----------------------------------------+-------------------------------------+
      | snap         | bool                                   | Snap vertices to the nearest pixel  |
      |              |                                        | center.                             |
      +--------------+----------------------------------------+-------------------------------------+
      | vertAlign    | enum                                   | The vertical alignment of the text  |
      |              |                                        | bounding box.                       |
      |              |                                        | Can be one of the following values: |
      |              |                                        |                                     |
      |              |                                        |    * 'center'                       |
      |              |                                        |    * 'top'                          |
      |              |                                        |    * 'bottom'                       |
      |              |                                        |    * 'baseline'                     |
      +--------------+----------------------------------------+-------------------------------------+
      | visible      | bool                                   | Is this to be drawn?                |
      +--------------+----------------------------------------+-------------------------------------+
      | zOrder       | float                                  | The z-order value is used for depth |
      |              |                                        | sorting.                            |
      +--------------+----------------------------------------+-------------------------------------+

