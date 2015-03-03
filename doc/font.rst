.. _plot2d_font_styling:

Styling
-------

Following is a list of possible font style properties:

      +--------------+--------------+-------------------------------------+
      | **Property** | **Type**     | **Description**                     |
      +==============+==============+=====================================+
      | family       | str          | This can be either a font family or |
      |              |              | the name of any font                |
      |              |              | (as found by the 'fontconfig'       |
      |              |              | package).                           |
      +--------------+--------------+-------------------------------------+
      | scale        | float / enum | A multiplicative factor applied to  |
      |              |              | the base font size to determine the |
      |              |              | final size of the rendered font.    |
      |              |              | The base size is determined by the  |
      |              |              | resolved valued of the 'size'       |
      |              |              | property.  This can also be one of  |
      |              |              | the following strings:              |
      |              |              |                                     |
      |              |              |    * 'xx-small'                     |
      |              |              |    * 'x-small'                      |
      |              |              |    * 'small'                        |
      |              |              |    * 'medium'                       |
      |              |              |    * 'large'                        |
      |              |              |    * 'x-large'                      |
      |              |              |    * 'xx-large'                     |
      |              |              |    * 'larger'                       |
      |              |              |    * 'smaller'                      |
      +--------------+--------------+-------------------------------------+
      | size         | float        | The size of the font (in points).   |
      +--------------+--------------+-------------------------------------+
      | style        | enum         | The style defines the 'slant' of    |
      |              |              | the font.  This can be one of       |
      |              |              | the following:                      |
      |              |              |                                     |
      |              |              |    * 'normal'                       |
      |              |              |    * 'italic'                       |
      |              |              |    * 'oblique'                      |
      +--------------+--------------+-------------------------------------+
      | weight       | float        | This can be a float of an enum      |
      |              |              | describing the 'boldness' of the    |
      |              |              | font.                               |
      +--------------+--------------+-------------------------------------+

