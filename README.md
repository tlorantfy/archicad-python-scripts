# Ready-to-go Python scripts for Archicad

[Download version 25.1](https://github.com/tlorantfy/archicad-python-scripts/archive/refs/tags/25.1.zip)

## recurring_publish.py

### Description
The script can schedule recurring publishing.  
The related Archicad project must be opened before executing the script, because the script retrieves the projectdata during the start-up of the script.

[Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands/releases) (version 25.1 or later) is required to run.

### Features

* Archicad will be shut down after each publishing and it will be restarted before each publishing, the project will be reloaded automatically.
* User can choose from the Publisher Sets. Only the selected sets will be published. Multiple choice is available.
* Recur time can be set in minutes.
* Continuous progress report, the remaining time till the next publishing countdown appears.
* Works for Teamwork (BIMcloud) projects also.

### Usage

1. Running Archicad instance is required with an opened project and loaded [Additional JSON/Python Commands Add-On](https://github.com/tlorantfy/archicad-additional-json-commands/releases).
2. Run recurring_publish.py script from command line and with using python launcher.
3. Select Publisher Sets to publish.
4. Set time (in minutes) for recurring.
5. Click Start button.

### Demo video
Click to watch the demo video:
[![recurring_publish.py](https://j.gifs.com/lRY80V.gif)](https://ttprivatenew.s3.amazonaws.com/pulse/lorantfyt/attachments/16911630/archicad_recurring_publish_demo.mp4)
