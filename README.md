# edutainment_emdb

e-MDB experiment for the edutainment use case for the PILLAR project.

## Installation

- Install the e-MDB: <https://github.com/pillar-robots/wp8_emdb.git>
- Clone this repo inside the e-MDB folder:

```bash
cd ~/wp8_emdb/src/
git clone https://github.com/pillar-robots/edutainment_emdb.git
````

- Build and source the experiment:

```bash
source /opt/ros/humble/setup.bash
cd ~/wp8_emdb/
colcon build --packages-select edutainment_emdb --symlink-install
source install/setup.bash
```

## Launch the edutainment experiment

```bash
cd ~/wp8_emdb/
source install/setup.bash
ros2 launch edutainment_emdb edutainment_launch.py |& tee ~/edutainment_output.log
```
