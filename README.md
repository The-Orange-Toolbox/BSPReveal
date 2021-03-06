# BSPReveal
Reveal various BSP elements previously unable to be visualised. BSPReveal is a map compile tool that add in-game functionality to your map. Some features are powered by existing console commands, others are new commands. Improved visualization allows for better debugging but note that BSPReveal is also relevant for your released maps. Players can now provide better feedback with more powerful screenshots and learn about various invisible elements to increase their mastery of your map. 

Download: [see the release page](https://github.com/The-Orange-Toolbox/BSPReveal/releases)
<!--- start txt omit -->

## Feature overview
Using `r_drawclipbrushes 2`

![alt text](https://github.com/The-Orange-Toolbox/BSPReveal/blob/master/docs/bspreveal_infographic_clip.jpg?raw=true "r_drawclipbrushes 2")

Using `ent_fire vis_disp toggle`

![alt text](https://github.com/The-Orange-Toolbox/BSPReveal/blob/master/docs/bspreveal_infographic_disp.jpg?raw=true "ent_fire vis_disp toggle")

Using `map_showspawnpoints`

![alt text](https://github.com/The-Orange-Toolbox/BSPReveal/blob/master/docs/bspreveal_infographic_spawns.jpg?raw=true "map_showspawnpoints")

Using `showtriggers_toggle`

![alt text](https://github.com/The-Orange-Toolbox/BSPReveal/blob/master/docs/bspreveal_infographic_trigger.jpg?raw=true "showtriggers_toggle")
<!--- end txt omit -->
## Installation

### Using with CompilePal
BSPReveal is packaged as ready to be used in CompilePal. Follow these quick steps to install it:
- Copy the BSPReveal folder into "Compile Pal 02x.xx/Parameters"
- Restart CompilePal.
- From the CompilePal UI, use the "Add..." button to add BSPReveal to your list of executables.
- Tick the checkmark to have it run on your next compile.

### Using with Hammer (expert compile)
The executable can be used standalone without any of the other files it is bundled with. Follow these quick steps to add it to your hammer compile:
- Copy the BSPReveal.exe from BSPReveal/ to "Team Fortress 2/bin" (or any prefered folder).
- In Hammer's expert compile window, use the "New" button to add a new command.
- For the command, click the "Cmds" button, select "executable", select the location of the BSPReveal.exe.
- For the parameters, add `$bspdir\$file.bsp` into the text field.
- Use the "Move Up"/"Move Down" buttons to order the command properly (recommended to be placed after the copy command).
- Hit "Go!" and compile away!

### Using with command line
Run the executable with `BSPReveal --help` for complete information about its usage.
