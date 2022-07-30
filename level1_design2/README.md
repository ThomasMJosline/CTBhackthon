# Verification for 1011 Sequence Detector 
The 1011 Sequence detector is a Mealy based finite state machine consisting of 5 states.<br>
<br>The inputs of the Sequence detector module are single bit 'inp_bit', single bit 'reset' and a clock('clk'). <br>The output from the module is 'seq_seen' which is also single bit. A bug free 1011 Sequence detector is used to identify whether, the input given through 'inp_bit' is in the order 1,0,1,1. When this happens the 'seq_seen' output goes high. The Sequence detector also finds valid sequences, that are overlapped with non-sequences.<br>
<br>The verification is done using [Vyoma's UpTickPro](https://vyomasystems.com).
![github_id](https://user-images.githubusercontent.com/84652232/181879292-9b0057a9-14a5-48eb-8640-1f4c2f89e669.png)



## Verification Environment

The process of verification is done using Python language with the help of [CoCoTb](https://www.cocotb.org/) library.
<br> <br>
The bugs in the design arises when there are situations when valid sequences comes overlapping with the non-sequences.<br>
- 1,1,0,1,1 
- 1,0,1,0,1,1  <br>

These are the cases where, bugs in the design are seen.


#### Test 1 ####
This test, is for checking whether the design can identify the sequence ``1,0,1,1`` from `` 1,1,0,1,1 ``.<br>
Initially 'reset' is set to 1 so that the system moves to 'IDLE' state and after this 'reset' is set 0 and inputs are given. These happen along the running of the clock.
```
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

```
The output from the DUT is compared with the inp13 as the 'sel' was given value equal to 13. If the values don't match a error message is thrown by the assert statement:
```
assert dut.out.value == B, "Test failed, because selected input was inp13 and expected output was {B} but the output from DUT is {OUT} ".format(B=dut.inp13.value, OUT=dut.out.value)
```
When this test was done the bug got exopsed:
```

```

#### Test 2 ####
Instead of a randomised test, here the the test specifically aims for capturing the bug when 'sel' becomes 13.<br>
Values are assigned to inp12, inp13 and sel :
```
A=2
B=3 
inp_sel=13 

dut.inp12.value=A
dut.inp13.value=B
dut.sel.value=inp_sel
```
The output from the DUT is compared with the inp13 as the 'sel' was given value equal to 13. If the values don't match a error message is thrown by the assert statement:
```
assert dut.out.value == B, "Test failed, because selected input was inp13 and expected output was {B} but the output from DUT is {OUT} ".format(B=dut.inp13.value, OUT=dut.out.value)
```
When this test was done the bug got exopsed:
```

```





## Test Scenario ##
#### Test1
- It is a randomised test covering conditions where sel is given different values
- Expected Output when 'sel' was equal to : 
- Observed Output in the DUT dut.sum=2

Output mismatches for the above inputs proving that there is a design bug

#### Test2
- Testing with value of 'sel' = 13, inp12=2 and inp13=3
- Expected Output: out=3
- Observed Output in the DUT dut.out=2

Output mismatches for the above inputs proving that there is a design bug

#### Test3
- Testing with value of 'sel'=30 and inp30=3
- Expected Output: out=12
- Observed Output in the DUT dut.out=0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following bugs:

### From Test1 and Test2
```
      5'b01101: out = inp12;
      5'b01101: out = inp13;        => for the case of 'sel'=12, nothing is defined so it goes to 
                                       default case when 'sel'=12 and when 'sel'=13 the output becomes equal to inp12.
 
```
Here, the first line should be ``5'b01100: out = inp12;`` instead of ``5'b01101: out = inp12;`` as in the design code.

### From Test3
```
      5'b11101: out = inp29;                
      default: out = 0;
    endcase                         =>Here the case where 'sel'=30 is not included, so it gets directed to default case.
```
Here, ``5'b11110: out = inp30;`` should be added after ``5'b11101: out = inp29;``.

## Design Fix
Updating the design and re-running the test makes the test pass.

$$$$image$$$$$

The updated design is checked in as mux_fix.v

## Verification Strategy
Analysis of the verilog code given for the design, helped to understand possible bugs. These bug were then confirmed through three tests.

## Is the verification complete ?
Yes, the multiplexer design code is completely verified and three bugs were found.
