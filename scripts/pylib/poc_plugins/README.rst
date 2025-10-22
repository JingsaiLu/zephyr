.. _integration_with_pytest:

Integration with pytest test framework
######################################

Introduction
************

This pytest plugin feature introduces 3 pytest fixtures for multi-device testing feature:
1. harness_build_dirs
2. harness_devices
3. harness_shells

To use this feature, you need to have map.yaml for dut as usual, 
but with fixture, 
then write pytest test cases for your sample/test apps.
1. overwrite harness_build_dirs fixture in test suite to return the build_dirs for each harness devices.
2. depends on harness_devices, or harness_shells fixtures in your test function, 
if you need interact with multi-devices, 
then the harness_devices fixutre will flash the build_dirs for each harness devices,
and initialize the devices for test cases.

@pytest.fixture(scope=determine_scope)
def harness_build_dirs(request: pytest.FixtureRequest, required_build_dirs: list[str]) -> list[str]:
    """
    Return a list of build directories for each harness device.
    """
    logger.info(f'required_build_dirs: {required_build_dirs}')
    return required_build_dirs

map.yml
- connected: true
  fixtures: 
    - multi_instance_harness:C:/Users/97014/zephyrproject/harness_boards_for_001061256778.yml
  id: 001061256778
  platform: frdm_mcxw72/mcxw727c/cpu0
  product: J-Link
  runner: jlink
  serial: COM3

harness_boards_for_001061256778.yml
- connected: true
  id: 001063989196
  platform: frdm_mcxw72/mcxw727c/cpu0
  product: J-Link
  runner: jlink
  serial: COM4


Fixtures
********

harness_build_dirs
==================
    return [build_dir] for one harness devices as default.
    if there are multiple harness devices, need to be overridden in test suite.

    such as, flash differernt build dirs for harness devices, 
    the harness_build_dirs should be set as: [build_dir_1, build_dir_2, ...],
    build_dir_1 could be build_dir, or from required_build_dirs fixture.
    """

.. code-block:: python

   import pytest
   from typing import List
   from twister_harness import DeviceAdapter, harness_devices

   def harness_build_dirs(request: pytest.FixtureRequest) -> List[str]:
    build_dir = request.config.getoption('--build-dir')
    return [build_dir, build_dir]

harness_devices
===============
This pytest fixture is designed for multi-device testing in connectivity test, such as BLE, etc.
This pytest fixture will load harness devices info from 
multi_instance_harness Twister fixture (defined in test yaml and hardware map),
then flash and initialize the devices as dut fixture,
Give access to a list of `DeviceAdapter`_ type objects (has to be same platform).
To use this pytest fixture, ``harness_build_dirs`` fixture must to be defined in test suite.
which should return the buid_dirs for each harness devices.

.. code-block:: yaml

   multi_harness_devices_for_one_dut:
      - connected: true
        id: 001063989196
        platform: frdm_mcxw72/mcxw27c/cpu0
        product: J-Link
        runner: jlink
        serial: COM4
      - connected: true
        id: 001063989178
        platform: frdm_mcxw72/mcxw27c/cpu0
        product: J-Link
        runner: jlink
        serial: COM5

.. code-block:: python

   import pytest
   from typing import List
   from twister_harness import DeviceAdapter, harness_devices

   def harness_build_dirs(request: pytest.FixtureRequest) -> List[str]:
    build_dir = request.config.getoption('--build-dir')
    return [build_dir, build_dir]

   def test_sample(harness_devices: list[DeviceAdapter]):
      for harness_device in harness_devices:
         harness_device.readlines_until(regex=r'Bluetooth initialized', timeout=3)

harness_shells
==============
This fixture is designed with harness_devices, just like shell fixture with dut.
give access to a list of `Shell`_ type objects for each harness device.

.. code-block:: python

   from twister_harness import Shell

   def test_sample(harness_shells: list[Shell]):
      for shell in harness_shells:
        shell.exec_command('help')


Limitations
***********

* Not every platform type is supported in the plugin (yet).
