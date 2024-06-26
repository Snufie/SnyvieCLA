# SnyvieCLA
<hr>
text goes here...

<hr>
<details>
<summary>Click to see changelogs</summary>

# v1.0.32

## TL;DR
Trying to create an auto-updater. so the CLA can be updated by the user with built-in functions.

## New Features
- README added
-  Update checker added
-  Admin panel added

## Known Issues
Auto-updater doesn't work

# v1.0.33

## TL;DR
Added an automatic way to create a changelog and add it to the README.md file when setting an update as an admin.

## New Features
- Automatic changelogs
- Fully functional release creator for admins

## Known Issues
- Version variable doesn't update with each update
- Admin input does not get validated correctly

# v1.0.34

## TL;DR
Updated changelog functionality to accomodate the changelogs being in "details" tags now

## New Features
- Changelog adder now appends inside the "details" tags

## Known Issues
- None found

<hr>

# v1.0.4

## TL;DR
Added the functionality for checking for updates, downloading the update and installing the update.

## New Features
- Add updater.py
- Add update checker in snyvie.py
- Add version control in admin.py

## Known Issues
- Snyvie's PyCLI does not work and may give errors
- Code still has print statements
- Updater may not work correctly as is prone to fail a lot. Keep a backup of your agenda items!
        
<hr>

# v1.0.41

## TL;DR
Add version info to AppInit

## New Features
- Added version display

## Known Issues
- Unknown error occurs after updating where old script still runs
        
<hr>

# v1.0.42

## TL;DR
Add version info to an isolated class so that it won't keep spamming you with update notifs.

## New Features
- Removed AppInit.Version
- Added Version.version
- Fixed README updating after creating a release

## Known Issues
- Update installs in nested folder
- Old script doesn't stop running after updating
        
<hr>

# v1.0.43

## TL;DR
Fixed the README file having to be committed separately and the old script continuing to run.

## New Features
- Add sys.exit(0) after updating
- Added subprocesses to commit README.md
- Added update rollout feedback in admin.py

## Known Issues
- Snyvie's PyCLI doesn't work and may give errors when used
- Updates install in a nested folder
        
<hr>

# v1.0.5

## TL;DR
Fixed the updates installing in a nested folder, now everything works as expected. I still need to manually change the CURRENT_VERSION variable but that'll be fixed soon aswell.

## New Features
- Fixed updater.py
- Emptied RELEASE-NOTES.md; no more random changelogs!

## Known Issues
- Snyvie's PyCLI doesn't work and gives an error when used
        
<hr>

# v1.0.51

## TL;DR
Update current version

## New Features
- Updated current version

## Known Issues
- Snyvie's PyCLI doesn't work and gives an error when used
        
<hr>

# v1.1.0

## TL;DR
Added repeating function and consequently fixed all code.

## New Features
- Add repeater function
- Add due date updater
- Fixed nearing and passed functions
- Updated current_version variable

## Known Issues
- Repeat_after_days is still required when repeat is `False`
- Debug prints still present
- Obsolete prints
- Update alert displays if version is higher than latest release
        
<hr>

# v1.1.8

## TL;DR
File tree is organized and repeating agenda items work

## New Features
- Fixed repeater resetting date
- New directory structure

## Known Issues
- Repeater is not aware of more than expected days passed
        </details>        




