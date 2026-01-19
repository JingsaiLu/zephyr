# Copyright 2025 NXP
#
# SPDX-License-Identifier: Apache-2.0

import logging
import random
import re
import time

import pytest
from twister_harness import Shell
from twister_harness.fixtures import determine_scope

logger = logging.getLogger(__name__)


@pytest.fixture(scope=determine_scope)
def harness_build_dirs(request: pytest.FixtureRequest, required_build_dirs: list[str]) -> list[str]:
    """
    Return a list of build directories for each harness device.
    """
    logger.info(f'required_build_dirs: {required_build_dirs}')
    return required_build_dirs

def test_os_boot(dut, harness_devices):
    dut.reset()
    harness_devices[0].reset()
    dut.readlines_until('Booting Zephyr OS build', timeout=5)
    harness_devices[0].readlines_until('Booting Zephyr OS build', timeout=5)


def test_bluetooth_boot(dut, harness_devices):
    dut.readlines_until('AD evt type', timeout=5)
    # harness_devices[0].readlines_until('AD evt type', timeout=5)
    harness_devices[0].readlines_until('Advertising successfully started', timeout=5)


def test_bluetooth_connection(dut, harness_devices):
    dut.readlines_until('Connected', timeout=5)


def test_match_temp_value_over_ble(dut, harness_devices):
    dut.readlines_until(r'Temperature \d{1,2}C', timeout=5)