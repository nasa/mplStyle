
.. _plot2d_marker_styling:

Styling
-------

Following is a list of possible edge style properties:

      +--------------+------------------------+-------------------------------------+
      | **Property** | **Type**               | **Description**                     |
      +==============+========================+=====================================+
      | color        | `Color <color.html>`__ | The color value of the marker.      |
      +--------------+------------------------+-------------------------------------+
      | edgeColor    | `Color <color.html>`__ | The color value of the edge.        |
      +--------------+------------------------+-------------------------------------+
      | edgeWidth    | float                  | The width of the edge line (in      |
      |              |                        | pixels).                            |
      +--------------+------------------------+-------------------------------------+
      | fill         | enum                   | For marker styles that can be       |
      |              |                        | filled this specifies a fill        |
      |              |                        | pattern.                            |
      |              |                        | This can be one of the following:   |
      |              |                        |                                     |
      |              |                        |    * 'full'                         |
      |              |                        |    * 'left'                         |
      |              |                        |    * 'right'                        |
      |              |                        |    * 'top'                          |
      |              |                        |    * 'bottom'                       |
      |              |                        |    * 'none'                         |
      +--------------+------------------------+-------------------------------------+
      | size         | float                  | The size of the marker (in pixels). |
      +--------------+------------------------+-------------------------------------+
      | style        | string                 | The MPL style of the marker.  This  |
      |              |                        | determines the actual marker shape. |
      |              |                        | See above for a list of possible    |
      |              |                        | marker values.                      |
      +--------------+------------------------+-------------------------------------+

