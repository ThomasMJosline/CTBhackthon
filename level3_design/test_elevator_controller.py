import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### TEST  FOR  ELEVATOR CONTROLLER #####')

    dut._log.info(f'UP={int(dut.Up.value):02} DOWN={int(dut.Down.value):02} DOOR={int(dut.door.value):02} WAITING={int(dut.wait_floor.value):02} CURRENT_FLOOR={int(dut.y.value):04}')
    dut.requested_floor.value=7

    dut._log.info(f'REQUESTED_FLOOR={7:04}')

    await FallingEdge(dut.clk)

    for i in range (10):
        dut._log.info(f'UP={int(dut.Up.value):02} DOWN={int(dut.Down.value):02} DOOR={int(dut.door.value):02} WAITING={int(dut.wait_floor.value):02} CURRENT_FLOOR={int(dut.y.value):04}')
        await FallingEdge(dut.clk)

    dut._log.info(f'UP={int(dut.Up.value):02} DOWN={int(dut.Down.value):02} DOOR={int(dut.door.value):02} WAITING={int(dut.wait_floor.value):02} CURRENT_FLOOR={int(dut.y.value):04}')
    assert dut.y.value == 7, "Test failed, because it was expected to reach {B}th but DUT reached {OUT} ".format(B=7, OUT=dut.y.value)
