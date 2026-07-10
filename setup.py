import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'edutainment_emdb'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*launch.[pxy][yma]*')),
        (os.path.join('share', package_name, 'experiments'), glob('experiments/*.[yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='AntonioLeis',
    maintainer_email='antonio.leis@udc.es',
    description='Edutainment experiment for the PILLAR project',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'edutainment_simulator = edutainment_emdb.edutainment_simulator:main',
            'test_sim = edutainment_emdb.test_sim:main',
            'manual_publisher = edutainment_emdb.manual_publisher:main',
            'manual_publisher_og = edutainment_emdb.manual_publisher_og:main'
        ],
    },
)
