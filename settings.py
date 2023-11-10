'''
Grady Landers
Demo Wheel - settings.py
Class to contain and verify all of the user settings.
'''

#imports
import configparser
import os
from PyQt6.QtGui import QColor

class Settings():
    def __init__(self):
        self.config = configparser.ConfigParser()
        #if the file doesn't exist, create it first with defaults
        if not os.path.isfile('settings.ini'):
            self.config['Wheel'] = {
                'size': '700',
                'bg_color': '224,98,54,255',
                'fg_color': '0,0,0,255',
                'bg_type': 'Multicolor'
            }
            self.config['Wheel_Colors'] = {
                'color0': '199,33,56,255',
                'color1': '224,98,54,255',
                'color2': '215,166,75,255',
                'color3': '48,76,122,255'
            }
            self.config['Text'] = {
                'font_size': '15',
                'text_color': '244,245,247,255',
                'shadow_bool': 'True',
                'shadow_color': '0,0,0,255'
            }
            self.config['Titles'] = {
                'title_0': 'Tony Hawk Pro Skater 2',
                'title_1': 'Star Wars: The Force Unleashed',
                'title_2': 'Borderlands',
                'title_3': 'Toe Jam and Earl',
                'title_4': 'Serious Sam',
                'title_5': 'PC Building Simulator',
                'title_6': 'Avatar',
                'title_7': 'Brothers in Arms',
                'title_8': 'Starfield',
                'title_9': 'Mario Kart'
            }
            self.config['Background'] = {
                'type': 'Solid',
                'color': '60,60,60,255',
                'image': ''
            }
            self.config['Button'] = {
                'bg_color': '224,98,54,255',
                'fg_color': '244,245,247,255',
                'bg_hover_color': '48,76,122,255',
                'fg_hover_color': '215,166,75,255',
                'bg_disable_color': '215,166,75,255',
                'fg_disable_color': '0,0,0,255'
            }
            self.save_config()
        
        #read the settings file and hold the configuration
        self.config.read('settings.ini')

        #get available themes
        self.themes = []
        self.load_themes()

    #save the current configuration to the settings file
    def save_config(self):
        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)
    
    #retrieve the requested setting value
    def get_value(self, section, setting):
        value = self.config[section][setting]
        if 'color' in setting:
            color = value.split(',')
            value = QColor(int(color[0]), int(color[1]), int(color[2]), int(color[3]))
        elif 'bool' in setting:
            if value.lower() == 'true':
                value = True
            else:
                value = False
        return value
    
    #retrieve the requested section tuple
    def get_section(self, section):
        return self.config[section]
    
    #retrieve the requested section as a list of its values
    def get_section_list(self, section):
        values = []
        for setting in self.config[section]:
            values.append(self.get_value(section, setting))
        return values
    
    #set the specified setting to the given value
    def set_value(self, section, setting, value):
        if isinstance(value, QColor):
            value = str(value.getRgb()).replace('(', '').replace(')', '').replace(' ', '')
        self.config[section][setting] = str(value)

    #change the settings of the specified section to the given list of values
    def set_section_list(self, section, setting, values):
        self.config[section] = {}
        for i in range(len(values)):
            self.set_value(section, setting+str(i), values[i])
    
    #load all the available themes
    def load_themes(self):
        files = os.scandir('./themes')
        for entry in files:
            if entry.is_file() and entry.name.endswith('.ini'):
                theme_config = configparser.ConfigParser()
                theme_config.read(entry.path)
                self.themes.append(theme_config)
    
    #get list of theme names
    def get_theme_list(self):
        theme_list = []
        for theme in self.themes:
            theme_list.append(theme['Theme']['title'])
        return theme_list

    #create and save a new theme with the current configuration
    def save_theme(self, title):
        #generate new config to capture settings, add Theme section
        theme_config = configparser.ConfigParser()
        theme_config['Theme'] = {'title': title}
        filename = title.lower().replace(' ', '_')

        #copy current config into theme config
        for section in self.config:
            theme_config[section] = {}
            for setting in self.config[section]:
                theme_config.set(section, setting, self.config[section][setting])
        
        #if there is an image file, copy it to the local image folder
        image = theme_config['Background']['image']
        if theme_config['Background']['type'] != 'Image':
            theme_config['Background']['image'] = ''
        elif image != '':
            ext = image.split('.')
            ext = ext[len(ext)-1]
            os.system('copy '+image.replace('/', '\\')+' images\\'+filename+'.'+ext)
            theme_config['Background']['image'] = 'images/'+filename+'.'+ext
        
        #save the new config as an ini file
        with open('./themes/'+filename+'.ini', 'w') as configfile:
            theme_config.write(configfile)
        
        #add to running themes list
        self.themes.append(theme_config)

    #set current config to chosen theme
    def apply_theme(self, index):
        #copy theme config into current config
        for section in self.themes[index]:
            if section != 'Theme':
                self.config[section] = {}
                for setting in self.themes[index][section]:
                    self.config.set(section, setting, self.themes[index][section][setting])
        
        #save
        self.save_config()
    
    #change the title of an existing theme
    def rename_theme(self, index, title):
        #update the title in the theme's config and generate new filename
        theme_config = self.themes[index]
        current_filename = theme_config['Theme']['title'].lower().replace(' ', '_')
        theme_config['Theme'] = {'title': title}
        filename = title.lower().replace(' ', '_')

        #if there is an image file, rename it in the local image folder
        image = theme_config['Background']['image']
        if image != '':
            ext = image.split('.')
            ext = ext[len(ext)-1]
            os.rename(image, 'images/'+filename+'.'+ext)
            theme_config['Background']['image'] = 'images/'+filename+'.'+ext

        #delete old file and save new one
        os.remove('./themes/'+current_filename+'.ini')
        with open('./themes/'+filename+'.ini', 'w') as configfile:
            theme_config.write(configfile)
    
    #duplicate a theme
    def duplicate_theme(self, index):
        #generate new config to capture settings, rename
        theme_config = configparser.ConfigParser()
        title = self.themes[index]['Theme']['title'] + ' Copy'
        theme_config['Theme'] = {'title': title}
        filename = title.lower().replace(' ', '_')

        #copy theme config into new config
        for section in self.themes[index]:
            if section != 'Theme':
                theme_config[section] = {}
                for setting in self.themes[index][section]:
                    theme_config.set(section, setting, self.themes[index][section][setting])

        #if there is an image file, copy it to the local image folder
        image = theme_config['Background']['image']
        if theme_config['Background']['type'] != 'Image':
            theme_config['Background']['image'] = ''
        elif image != '':
            ext = image.split('.')
            ext = ext[len(ext)-1]
            os.system('copy '+image.replace('/', '\\')+' images\\'+filename+'.'+ext)
            theme_config['Background']['image'] = 'images/'+filename+'.'+ext
        
        #save the new config as an ini file
        with open('./themes/'+filename+'.ini', 'w') as configfile:
            theme_config.write(configfile)
        
        #add to running themes list
        self.themes.append(theme_config)
    
    #delete a theme
    def delete_theme(self, index):
        filename = self.themes[index]['Theme']['title'].lower().replace(' ', '_')
        image = self.themes[index]['Background']['image']
        self.themes.remove(self.themes[index])
        os.remove('./themes/'+filename+'.ini')
        if image != '':
            os.remove(image)
