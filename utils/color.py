"""
Color and Pixel Detection Module
Handles screen pixel color detection for visual triggers
"""

try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class PixelDetector:
    """Detects pixel colors on screen for conditional execution"""

    def __init__(self):
        """Initialize pixel detector"""
        if not PIL_AVAILABLE:
            print("Warning: PIL (Pillow) not available. Pixel detection disabled.")

    def get_pixel_color(self, x, y):
        """
        Get the color of a pixel at screen coordinates

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Color as hex string #RRGGBB, or None if PIL unavailable
        """
        if not PIL_AVAILABLE:
            return None

        try:
            # Grab a 1x1 pixel screenshot at the specified position
            screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
            r, g, b = screenshot.getpixel((0, 0))[:3]  # Get RGB, ignore alpha if present
            return f"#{r:02X}{g:02X}{b:02X}"
        except Exception as e:
            print(f"Error detecting pixel color at ({x}, {y}): {e}")
            return None

    def check_pixel(self, x, y, expected_color, tolerance=10):
        """
        Check if pixel at (x, y) matches expected color within tolerance

        Args:
            x: X coordinate
            y: Y coordinate
            expected_color: Expected color as hex string #RRGGBB
            tolerance: Color difference tolerance (0-255)

        Returns:
            True if pixel matches within tolerance, False otherwise
        """
        if not PIL_AVAILABLE:
            return False

        actual_color = self.get_pixel_color(x, y)
        if actual_color is None:
            return False

        # Calculate color distance
        distance = self.color_distance(actual_color, expected_color)
        return distance <= tolerance

    def color_distance(self, color1, color2):
        """
        Calculate Euclidean distance between two colors

        Args:
            color1: First color as hex string #RRGGBB
            color2: Second color as hex string #RRGGBB

        Returns:
            Color distance (0-441, where 0 is identical)
        """
        # Parse hex colors
        r1, g1, b1 = self._parse_hex_color(color1)
        r2, g2, b2 = self._parse_hex_color(color2)

        # Euclidean distance in RGB space
        distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        return distance

    def _parse_hex_color(self, hex_color):
        """
        Parse hex color string to RGB tuple

        Args:
            hex_color: Color as #RRGGBB

        Returns:
            Tuple of (r, g, b)
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)
