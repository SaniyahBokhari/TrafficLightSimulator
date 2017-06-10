import curses
import time
import signal


"""
Set up traffic light frame object.
It is in string format to represent ascii art.
"""
class Frame:
    def __init__(self):
        self.bulb_frame =  "|     .====.     |\n"+\
                           "|    /      \    |\n"+\
                           "|   [        ]   |\n"+\
                           "|    \      /    |\n"+\
                           "|     .====.     |\n"
       
        self.top =         "        ##\n"+\
                           "       _[]_\n"+\
                           "      [____]\n"+\
                           ".-----'    '-----.\n"
        
       
        self.bottom =      "'-----.____.-----'" 

	
    """
    Combine the strings to get traffic light frame string as ascii art.
    Return string to be displayed on screen.
    """
    def frame_string(self, num_colors): 
       ascii_frame = self.top
       # Number of colors determines number of bulbs in traffic light
       for i in range(num_colors):         
           ascii_frame = ascii_frame + self.bulb_frame
       ascii_frame += self.bottom
       return ascii_frame


"""
Class to turn colors of the traffic light on and off until time expires
""" 
class Signals:
    def __init__(self, screen, color, curses_color, coordinates, color_pair_index):
        self.screen = screen
        self.color = color
        self.curses_color = curses_color
        self.coordinates = coordinates
        self.color_pair_index = color_pair_index
        curses.use_default_colors() 

     
    """
    Curses adding color to bulbs when ON and adding default color of 
    background when OFF 
    """
    def on_off_pattern(self, pattern1, pattern2, pattern3): 
        self.screen.addstr(self.coordinates[0], self.coordinates[1], 
                           pattern1,curses.color_pair(self.color_pair_index)|curses.A_BOLD)  
        self.screen.addstr(self.coordinates[0]+1, self.coordinates[1]-1, pattern2, curses.color_pair(self.color_pair_index)|curses.A_BOLD)
        self.screen.addstr(self.coordinates[0]+2, self.coordinates[1], pattern3, curses.color_pair(self.color_pair_index)|curses.A_BOLD)  


    """
    Turn the color ON for traffic light bulb and keep it on for user inputed time
    """
    def ON(self, time_on): 
        # -1 is the default background color of terminal
        curses.init_pair(self.color_pair_index, eval(self.curses_color),-1)
        self.on_off_pattern("#"*6,"#"*8,"#"*6)
        self.screen.refresh()
        time.sleep(time_on)


    """ 
    Turn the color OFF for the traffic light bulb
    """
    def OFF(self, num_colors): 
        # -1 is the default color of terminal
        curses.init_pair(self.color_pair_index, -1, -1)    
        self.on_off_pattern(" "*6," "*8," "*6)
        self.screen.refresh()
        if (num_colors==1):
            time.sleep(1)

"""
Class methods to:
- assign each color with appropriate coordinate for displaying color
- assign each color with corresponding curses defined color
- assign each color with curses color pair number to distinguish between colors 
"""
class colorAttributes:

    coordinates = {}
    curses_colors = {}
    color_pair_index = {}

    
    """
    Assign coordinates for colors of the bulbs and store it in a dictionary
    """
    def coordinates_assign(self, colors_list): 
        x,y = 8,7
        for color in colors_list:         
            self.coordinates[color] = y,x
            y += 5

     
    """
    Assign curses color for the bulb e.g. curses.COLOR_RED for red. Store key-values in a dictionary
    """
    def assign_curses_colors(self, colors_list): 
        for color in colors_list:
            self.curses_colors[color]="curses.COLOR_"+color.upper()


    """
    Assign curses color index number for each color and store in dictionary 
    """
    def assign_color_pair_index(self, colors_list):
        num=1
        for color in colors_list:
            self.color_pair_index[color] = num
            num+=1

    def __init__(self, colors_list):
        self.coordinates_assign(colors_list)
        self.assign_curses_colors(colors_list)
        self.assign_color_pair_index(colors_list)
   

"""
Object to capture Control-C and set terminate variable
""" 
class controlC_catcher:
    terminate = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.die)

    def die(self, signum, frame):
        self.terminate = True


"""
Class to display and simulate traffic light
"""
class TrafficLight:
    def __init__(self, colors_list, times_dict):
        self.colors_list = colors_list
        self.times_dict = times_dict
        curses.wrapper(self.display_frame)


    def display_frame(self, screen):
        catcher = controlC_catcher()
        frame_str = Frame().frame_string(len(self.colors_list))
        curses.curs_set(False)           
        screen.addstr(0,2,"PRESS CONTROL-C TO EXIT")
        while(True):
            for z, line in enumerate(frame_str.splitlines(), 2):
                screen.addstr(z, 2, line)
            screen.refresh()
            self.displayColors(screen)           
            # If Control-C is entered exit at end of color cycle
            if catcher.terminate:
                screen.addstr(16,25,"Exiting Traffic Light Simulator.....")
                screen.refresh()
                time.sleep(1)                
                break


    def displayColors(self, screen):
        attr = colorAttributes(self.colors_list)
        new_color = self.colors_list[0]
        for color in self.colors_list:
           signal = Signals(screen, new_color, attr.curses_colors[new_color], attr.coordinates[new_color], attr.color_pair_index[new_color])
           signal.ON(self.times_dict[new_color])
           signal.OFF(len(self.colors_list))
           new_color = self.next_state(new_color)
        screen.timeout(10)


    """
    If state is red, the next_state is green for standard classic traffic light.
    """
    def next_state(self, color):
       if color == "red":
          return "green"
       elif color == "green":
          return "yellow"
       else: 
          return "red"



def main():
    colors_list = ["red","yellow","green"]
    times_colors_on_dict = {"red":4,"yellow":2,"green":4}
    TrafficLight(colors_list, times_colors_on_dict) 

    
if __name__ == "__main__":
    main()  
