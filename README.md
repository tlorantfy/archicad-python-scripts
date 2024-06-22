# Ready-to-go Python scripts for Archicad

[Download version 26.1](https://github.com/tlorantfy/archicad-python-scripts/archive/refs/tags/26.1.zip)

- [recurring_publish.py](#recurring_publish.py)
- [generate_building.py](#generate_building.py)
- [move_all_objects.py](#move_all_objects.py)
- [open_all_hotlinks.py](#open_all_hotlinks.py)
- [get_parameters_of_selected_GDLbased.py](#get_parameters_of_selected_GDLbased.py)
- [change_parameters_of_selected_GDLbased.py](#change_parameters_of_selected_GDLbased.py)

## recurring_publish.py

### Description
The script can schedule recurring publishing.  
The related Archicad project must be opened before executing the script, because the script retrieves the projectdata during the start-up of the script.

### Requirements
* **Requires Archicad 25 or later.**
* [Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands) (version 25.2 or later) is required to be loaded into Archicad.
  * [Download the Add-On for Archicad 26 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.26.apx)
  * [Download the Add-On for Archicad 25 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.25.apx)
  * [Download the Add-On for Archicad 25 for macOS platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/25.2/archicad-additional-json-commands.bundle.zip)

### Features

* Archicad will be shut down after each publishing and it will be restarted before each publishing, the project will be reloaded automatically.
* User can choose from the Publisher Sets. Only the selected sets will be published. Multiple choice is available.
* Recur time can be set in minutes.
* Continuous progress report, the remaining time till the next publishing countdown appears.
* Works for Teamwork (BIMcloud) projects also. A receive command is executed before each publishing.

### Usage

1. Running Archicad instance is required with an opened project and loaded [Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands/releases).
2. Run recurring_publish.py script from command line and with using python launcher.
3. Select Publisher Sets to publish.
4. Set time (in minutes) for recurring.
5. Click Start button.

### Demo video
Click to watch the demo video:
![recurring_publish.py](https://j.gifs.com/lRY80V.gif)

## generate_building.py

### Description
The script generates a skeleton building with slabs, columns and objects.

### Requirements
* **Requires Archicad 25 or later.**
* [Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands) (version 26.3 or later) is required to be loaded into Archicad.
  * [Download the Add-On for Archicad 26 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.26.apx)
  * [Download the Add-On for Archicad 25 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.25.apx)
  * [Download the Add-On for Archicad 25 for macOS platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/25.2/archicad-additional-json-commands.bundle.zip)

### Demo video
Click to watch the demo video:
![generate_building.py]https://s2.ezgif.com/tmp/ezgif-2-368597cfd4.gif)

## move_all_objects.py

### Description
The script moves all the elements with Object type to a new position.  

### Requirements
* **Requires Archicad 25 or later.**
* [Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands) (version 25.3 or later) is required to be loaded into Archicad.
  * [Download the Add-On for Archicad 26 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.26.apx)
  * [Download the Add-On for Archicad 25 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.25.apx)
  * [Download the Add-On for Archicad 25 for macOS platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/25.2/archicad-additional-json-commands.bundle.zip)

## open_all_hotlinks.py

### Description
The script retrieves the list of hotlinks in the currently active project, opens the hotlinks one-by-one and performs an operation for each of them.

### Requirements
* **Requires Archicad 25 or later.**
* [Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands) (version 25.4 or later) is required to be loaded into Archicad.
  * [Download the Add-On for Archicad 26 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.26.apx)
  * [Download the Add-On for Archicad 25 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.25.apx)
  * [Download the Add-On for Archicad 25 for macOS platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/25.2/archicad-additional-json-commands.bundle.zip)

## get_parameters_of_selected_GDLbased.py

### Description
The script lists the GDL parameters (name and value pairs) of the selected elements.

### Requirements
* **Requires Archicad 26 or later.**
* [Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands) (version 26.1 or later) is required to be loaded into Archicad.
  * [Download the Add-On for Archicad 26 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.26.apx)
  * [Download the Add-On for Archicad 25 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.25.apx)
  * [Download the Add-On for Archicad 25 for macOS platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/25.2/archicad-additional-json-commands.bundle.zip)

## change_parameters_of_selected_GDLbased.py

### Description
The script changes the values of given GDL parameters of the selected elements.
This examples changes the parameter with name 'gs_cont_pen' to pen with index 95.

### Requirements
* **Requires Archicad 26 or later.**
* [Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands) (version 26.1 or later) is required to be loaded into Archicad.
  * [Download the Add-On for Archicad 26 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.26.apx)
  * [Download the Add-On for Archicad 25 for Windows platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/26.3/archicad-additional-json-commands.25.apx)
  * [Download the Add-On for Archicad 25 for macOS platform](https://github.com/tlorantfy/archicad-additional-json-commands/releases/download/25.2/archicad-additional-json-commands.bundle.zip)