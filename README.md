# edutainment_emdb

e-MDB implementation of the WP8 Edutainmet use case for the PILLAR project.

## Installation

- Install the e-MDB: <https://github.com/pillar-robots/wp5_gii>
- Clone this repo inside the e-MDB folder:

```bash
cd ~/eMDB_ws/src/wp5_gii
git clone https://github.com/pillar-robots/edutainment_emdb.git
````

- Build and source the experiment:

```bash
source /opt/ros/humble/setup.bash
cd ~/eMDB_ws/
colcon build --packages-select edutainment_emdb --symlink-install
source install/setup.bash
```

## Launch the edutainment experiment

```bash
cd ~/eMDB_ws/
source install/setup.bash
ros2 launch edutainment_emdb edutainment_launch.py |& tee ~/edutainment_output.log
```
