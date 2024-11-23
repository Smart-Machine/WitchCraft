import pygame
from abc import ABC, abstractmethod 

class Cutscene(ABC):
    def __init__(self, manager, settings):
        self.settings = settings
        self.manager = manager
        self.font = pygame.font.Font(None, 36)

        # size for background text (size: 840, 840)
        self.rect_size_footer = (100, self.settings.height - 100, self.settings.width - 200, self.settings.height - 700)
        # size for pager text (size: 840, 840)
        self.rect_size_pager = (50, 50, self.settings.width - 100, self.settings.height - 50)

    @property
    @abstractmethod
    def text(self):
        pass

    @property 
    @abstractmethod
    def font(self):
        pass

    @property
    @abstractmethod
    def rect(self):
        pass

    @abstractmethod
    def mainloop(self):
        pass

    def typewriter_effect(self, screen, rect, text, font, color, delay=50, background_color=None):
        """
        Animates the writing of text inside a rectangle.

        Args:
            screen: Pygame screen to render on.
            rect: pygame.Rect defining the rectangle for the text.
            text: String of text to animate.
            font: Pygame font object.
            color: Color of the text.
            delay: Delay in milliseconds between each character.
            background_color: Color to clear the rectangle, or None to keep the background transparent.
        """
        words = text.split(' ')
        x, y = rect.topleft
        line_spacing = font.get_linesize()
        # space_width = font.size(' ')[0]
        current_line = ""
        rendered_lines = []
        
        for word in words:
            # Check if adding the next word fits the line
            test_line = f"{current_line} {word}".strip()
            line_width, _ = font.size(test_line)
            
            if line_width > rect.width and current_line != "":
                # If the line is full, save it and start a new line
                rendered_lines.append(current_line)
                current_line = word
            else:
                # Otherwise, add the word to the current line
                current_line = test_line
        
        # Add the last line
        rendered_lines.append(current_line)

        # Animate line by line
        for line in rendered_lines:
            current_text = ""
            
            for char in line:
                current_text += char
                
                # Clear background if specified
                if background_color:
                    pygame.draw.rect(screen, background_color, rect, border_radius=20)
                
                # Render previously typed lines
                y_offset = 0
                for rendered_line in rendered_lines[:len(rendered_lines) - len(rendered_lines)]:
                    rendered_surface = font.render(rendered_line, True, color)
                    screen.blit(rendered_surface, (x, y + y_offset))
                    y_offset += line_spacing

                # Render current line as it types
                rendered_surface = font.render(current_text, True, color)
                screen.blit(rendered_surface, (x, y + y_offset))
                
                pygame.display.flip()  # Update display
                pygame.time.wait(delay)  # Delay between characters
            
def typewriter_effect(screen, rect, text, font, color, delay=50, background_color=None):
    """
    Animates the writing of text inside a rectangle.

    Args:
        screen: Pygame screen to render on.
        rect: pygame.Rect defining the rectangle for the text.
        text: String of text to animate.
        font: Pygame font object.
        color: Color of the text.
        delay: Delay in milliseconds between each character.
        background_color: Color to clear the rectangle, or None to keep the background transparent.
    """
    words = text.split(' ')
    x, y = rect.topleft
    line_spacing = font.get_linesize()
    # space_width = font.size(' ')[0]
    current_line = ""
    rendered_lines = []
    
    for word in words:
        # Check if adding the next word fits the line
        test_line = f"{current_line} {word}".strip()
        line_width, _ = font.size(test_line)
        
        if line_width > (rect.width - 10) and current_line != "":
            # If the line is full, save it and start a new line
            rendered_lines.append(current_line)
            current_line = word
        else:
            # Otherwise, add the word to the current line
            current_line = test_line
    
    # Add the last line
    rendered_lines.append(current_line)

    print(rendered_lines)

    # Animate line by line
    for line in rendered_lines:
        current_text = ""
        
        for char in line:
            current_text += char
            
            # Clear background if specified
            if background_color:
                pygame.draw.rect(screen, background_color, rect, border_radius=20)
            
            # Render previously typed lines
            x_offset = 20 
            y_offset = 10 
            for rendered_line in rendered_lines[:rendered_lines.index(line)]:
                print(f"previous: {rendered_line}")
                rendered_surface = font.render(rendered_line, True, color)
                screen.blit(rendered_surface, (x + x_offset, y + y_offset))
                y_offset += line_spacing

            # Render current line as it types
            rendered_surface = font.render(current_text, True, color)
            screen.blit(rendered_surface, (x + x_offset, y + y_offset))
            
            pygame.display.flip()  # Update display
            pygame.time.wait(delay)  # Delay between characters