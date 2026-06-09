from setuptools import find_packages, setup
from glob import glob

package_name = 'cmd_vel_to_pixhawk'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rover',
    maintainer_email='fujiwara.t@s.okayama-u.ac.jp',
    description='cmd_vel to Pixhawk',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'cmd_vel_to_pixhawk = cmd_vel_to_pixhawk.cmd_vel_to_pixhawk:main',
        ],
    },
)
