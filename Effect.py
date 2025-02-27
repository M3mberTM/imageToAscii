from enum import Enum


class Effect(Enum):
    """Simple enum class to be used by other Ascii Generator Classes

    Attributes
    ----------
    RAINBOW_HORIZONTAL
        makes the image have a rainbow gradient from left to right
    RAINBOW_VERTICAL
        makes the image have a rainbow gradient from top to bottom
    RAINBOW_RADIAL
        makes the image have a rainbow gradient from center to the edges
    RAINBOW_HORIZONTAL_REV
        makes the image have a rainbow gradient from right to left
    RAINBOW_VERTICAL_REV
        makes the image have a rainbow gradient from bottom to top
    RAINBOW_RADIAL_REV
        makes the image have a rainbow gradient from the edges to the center
    VIDEO_RAINBOW_RADIAL
        makes the video slowly change color over time
    """

    RAINBOW_HORIZONTAL = 0
    RAINBOW_VERTICAL = 1
    RAINBOW_RADIAL = 2
    RAINBOW_HORIZONTAL_REV = 3
    RAINBOW_VERTICAL_REV = 4
    RAINBOW_RADIAL_REV = 5
    ORIGINAL_COLOR = 6

    VIDEO_RAINBOW_GRADUAL = 100  # works only on video
