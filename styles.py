from pygui import Style, Colors

DEFAULT = Style(Colors(background=(20, 20, 20),
                       fill=(37, 120, 157),
                       hovered=(25, 104, 139),
                       border=(15, 60, 80),
                       clicked=(15, 60, 80),
                       focused=(170, 170, 193),
                       text=(191, 191, 203)), 
                       border=2,
                       rounding=5,
                       padding=10,
                       spacing=15)

BORDERLESS = Style(Colors(background=(20, 20, 20),
                       fill=(37, 120, 157),
                       hovered=(25, 104, 139),
                       border=(15, 60, 80),
                       clicked=(15, 60, 80),
                       focused=(170, 170, 193),
                       text=(191, 191, 203)), 
                       border=2,
                       rounding=5,
                       padding=0,
                       spacing=10)
