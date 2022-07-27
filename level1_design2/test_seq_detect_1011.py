# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

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

    cocotb.log.info('#### TEST  FOR  SEQUENCE DETECTOR #####')

    dut.inp_bit.value=1

    dut._log.info(f'INP_BIT={1:03}  SEQ_SEEN={int(dut.seq_seen.value):03}')

    await FallingEdge(dut.clk)

    dut.inp_bit.value=1

    dut._log.info(f'INP_BIT={1:03} SEQ_SEEN={int(dut.seq_seen.value):03}')

    await FallingEdge(dut.clk)

    dut.inp_bit.value=0

    dut._log.info(f'INP_BIT={0:03} SEQ_SEEN={int(dut.seq_seen.value):03}')

    await FallingEdge(dut.clk)
    dut.inp_bit.value=1

    dut._log.info(f'INP_BIT={1:03} SEQ_SEEN={int(dut.seq_seen.value):03}')

    await FallingEdge(dut.clk)
    dut.inp_bit.value=1
    dut._log.info(f'INP_BIT={1:03} SEQ_SEEN={int(dut.seq_seen.value):03}')

    await FallingEdge(dut.clk)

    dut._log.info(f'SEQ_SEEN={int(dut.seq_seen.value):03}')

    assert dut.seq_seen.value == 1, "Test failed, because seq_seen output should be {B} but the output from DUT is {OUT} ".format(B=1, OUT=dut.seq_seen.value)

'''@cocotb.test()
async def test_seq_bug2(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### TEST  FOR  SEQUENCE DETECTOR #####')
    print(dut.inp_bit.value)
    print(dut.seq_seen.value)
    A=[1,0,1,1,0]

    for i in A:
        B=i
        dut.inp_bit.value=int(i)
        print(i)
        dut._log.info(f'SEQ_SEEN={int(dut.seq_seen.value):03}')
        
        await FallingEdge(dut.clk)
    print(dut.inp_bit.value)

    
    dut._log.info(f'SEQ_SEEN={int(dut.seq_seen.value):03}')

    assert dut.seq_seen.value == 1, "Test failed, because seq_seen output should be {B} but the output from DUT is {OUT} ".format(B=1, OUT=dut.seq_seen.value)'''