# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux1(dut):
    """Test for mux2"""

    cocotb.log.info('##### Testing whether sel works for all values, bug when sel is 12  ########')

    i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19,i20,i21,i22,i23,i24,i25,i26,i27,i28,i29,i30 = (random.randint(0, 3) for x in range(31))

    print(i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19,i20,i21,i22,i23,i24,i25,i26,i27,i28,i29,i30)
    
    for i in range(31):

        A=(i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19,i20,i21,i22,i23,i24,i25,i26,i27,i28,i29,i30)[i]

        inp_sel=i
        
        dut.inp0.value=i0
        dut.inp1.value=i1
        dut.inp2.value=i2
        dut.inp3.value=i3
        dut.inp4.value=i4
        dut.inp5.value=i5
        dut.inp6.value=i6
        dut.inp7.value=i7
        dut.inp8.value=i8
        dut.inp9.value=i9
        dut.inp10.value=i10
        dut.inp11.value=i11
        dut.inp12.value=i12
        dut.inp13.value=i13
        dut.inp14.value=i14
        dut.inp15.value=i15
        dut.inp16.value=i16
        dut.inp17.value=i17
        dut.inp18.value=i18
        dut.inp19.value=i19
        dut.inp20.value=i20
        dut.inp21.value=i21
        dut.inp22.value=i22
        dut.inp23.value=i23
        dut.inp24.value=i24
        dut.inp25.value=i25
        dut.inp26.value=i26
        dut.inp27.value=i27
        dut.inp28.value=i28
        dut.inp29.value=i29
        dut.inp30.value=i30
        
        dut.sel.value=inp_sel

        print("Test for selection of inp"+str(i))

        await Timer(2, units='ns')

        dut._log.info(f'A={A:03} B={inp_sel:05} EXPECT={A:03} DUT={int(dut.out.value):05}')

        assert dut.out.value == A, "Randomised test failed with, because, selected input was inp{B} and expected output was {A} but the output from DUT is {OUT} ".format(B=dut.sel.value,A='{0:03b}'.format(A), OUT=dut.out.value)


@cocotb.test()
async def test_mux2(dut):
    
    cocotb.log.info('##### Exopsing bug in sel when selecting the inp13 ########')

    A=2
    B=3 
    inp_sel=13 

    dut.inp12.value=A
    dut.inp13.value=B
    dut.sel.value=inp_sel

    await Timer(2, units='ns')

    dut._log.info(f'A={A:03} B={B:03} SEL={inp_sel:05} EXPECT={B:03} DUT={int(dut.out.value):05}')

    assert dut.out.value == B, "Test failed, because selected input was inp13 and expected output was {B} but the output from DUT is {OUT} ".format(B=dut.inp13.value, OUT=dut.out.value)


@cocotb.test()
async def test_mux3(dut):
    
    cocotb.log.info('##### Bug when giving sel=30 ########')

    A=3
    inp_sel=30

    dut.inp30.value=A
    dut.sel.value=inp_sel

    await Timer(2, units='ns')

    dut._log.info(f'A={A:03}  SEL={inp_sel:05}  EXPECT={A:03}  DUT={int(dut.out.value):05}')

    assert dut.out.value == A, "Test failed, because selected input was inp30 and expected output was {A} but the output from DUT is {OUT} ".format(A=dut.inp30.value, OUT=dut.out.value)



