.. _plot2d_patches_styling:

Styling
-------

Following is a list of possible Patch style properties:

      +--------------+-----------------------------+-------------------------------------+
      | **Property** | **Type**                    | **Description**                     |
      +==============+=============================+=====================================+
      | alpha        | float   [ 0.0 -> 1.0 ]      | The transparency value of the       |
      |              |                             | patch.                              |
      +--------------+-----------------------------+-------------------------------------+
      | antialiased  | bool                        | Whether or not the Patch element    |
      |              |                             | will be antialiased when rendered.  |
      +--------------+-----------------------------+-------------------------------------+
      | clip         | bool                        | Is this clipped by the axes         |
      |              |                             | boundaries?                         |
      +--------------+-----------------------------+-------------------------------------+
      | color        | `Color <color.rst>`__       | The color value of the patch.       |
      +--------------+-----------------------------+-------------------------------------+
      | edgeColor    | `Color <color.rst>`__       | The color value of the edge.        |
      +--------------+-----------------------------+-------------------------------------+
      | edgeStyle    | enum                        | The style to use for the edge line. |
      |              |                             | This can be one of the              |
      |              |                             | following values:                   |
      |              |                             |                                     |
      |              |                             | +-----------+---------------+       |
      |              |                             | |    '\-'   | Solid line    |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | |  'solid'  | Solid line    |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | |   '\-\-'  | Dashed line   |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | |  'dashed' | Dashed line   |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | |    '-.'   | Dash-Dot line |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | | 'dashdot' | Dash-Dot line |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | |    ':'    | Dotted line   |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | |  'dotted' | Dotted line   |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | |    None   | No line       |       |
      |              |                             | +-----------+---------------+       |
      |              |                             | |   'none'  | No line       |       |
      |              |                             | +-----------+---------------+       |
      +--------------+-----------------------------+-------------------------------------+
      | edgeWidth    | float                       | The width (in pixels) of the edge   |
      |              |                             | line.                               |
      +--------------+-----------------------------+-------------------------------------+
      | filled       | bool                        | If True, then the patch will be     |
      |              |                             | filled with the 'color' value.      |
      +--------------+-----------------------------+-------------------------------------+
      | snap         | bool                        | Snap vertices to the nearest pixel  |
      |              |                             | center.                             |
      +--------------+-----------------------------+-------------------------------------+
      | visible      | bool                        | Is this to be drawn?                |
      +--------------+-----------------------------+-------------------------------------+
      | zOrder       | float                       | The z-order value is used for depth |
      |              |                             | sorting.                            |
      +--------------+-----------------------------+-------------------------------------+

