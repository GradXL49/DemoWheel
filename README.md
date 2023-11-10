# DemoWheel
Desktop app for facilitating the random selection process of the Funhaus Demo Wheel show.

Through this project I wanted to provide a free and standalone implentation for a wheel-based random selector.
For the fun of it this was done with little help from online sources. This is probably not the most elegant or
efficient solution!

This app was designed to provide easy use and customization of your wheel-based random selector from the comfort
of a laptop or desktop PC without connecting to a webpage that's going to serve you ads and steal your data.

THIS APP IS INTENDED TO WORK ONLY ON WINDOWS; SUPPORT FOR OTHER OPERATING SYSTEMS IS NOT PLANNED

How to Operate:
1) Start the program
2) Click the SPIN button
3) Hope it lands on the disk with a Star Trek game

Modifying Settings:
1) Click the 'Settings' menu on the tool bar (top left corner)
2) Change the options to your liking
3) Make the background whatever nasty rule 34 picture you want

Notes About the Settings:
1) In the Wheel tab, Line color controls the outline for a solid colored wheel and the color of the pointer
2) In the Wheel Colors and Titles lists you can't edit an entry, just delete and add what you want
   Also note that these lists won't let you delete the last remaining entry, this prevents crashes
3) The Shadow option in the Text tab consistently tanks the framerate. Unfortunately it can't be improved,
   this seems to be a limitation of the PyQt library
4) Large image files (2k+) take longer to load and there is no loading bar, be patient (or use reasonable images)
5) If a settings file is not present a default one will be created; Do not modify this file directly

Using Themes:
1) Your current configuration can be saved as a theme in the Themes tab of the settings
2) The way settings are implemented I do not recommend modifying the ini files directly
3) The name of your theme must not contain special characters and has to be unique from the other themes
   installed in your operating directory, otherwise they won't load properly (or at all potentially)
4) The 'Save Theme' button lets you save your current settings as a unique theme
5) The 'Apply' button changes your current settings to those of the theme selected in the list
   THIS WILL OVERWRITE YOUR CURRENT SETTINGS WITHOUT SAVING THEM AND WITHOUT WARNING
6) The 'Rename' button lets you change the name of the selected theme if you want
7) The 'Duplicate' button lets you create a copy of the selected theme so you can use it as a baseline
   WARNING: This will also duplicate that theme's background image if one is set
8) The 'Delete' button lets you delete the selected theme WITHOUT WARNING

Sharing Themes:
1) To share your themes with others send them your 'images' and 'themes' folders (they're next to the exe)
2) To add others' themes copy their 'images' and 'themes' folders to your operating directory (where the exe is)
3) Make sure copied themes are uniquely named or they will overwrite your existing theme with the same name
