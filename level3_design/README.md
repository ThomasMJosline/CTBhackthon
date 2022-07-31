# Verification for Elevator Controller
The Elevator Controller is a Mealy based finite state machine consisting of 3 states.<br>
<br>The inputs of the module are `requested_floor` which is of 4 bits, single bit `reset` and a clock('clk'). <br>The output from the module are `y` that shows the current floor, `door`,`Up`,`Down` and `wait_floor`.<br>
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
The output from the DUT `seq_seen` should be equal to `1` at the end of the test. This is confirmed by an assert statement:
```
assert dut.seq_seen.value == 1, "Test failed, because seq_seen output should be {B} but the output from DUT is {OUT} ".format(B=1, OUT=dut.seq_seen.value)
```
When this test was done the bug got exopsed and the error message appeared:
```
AssertionError: Test failed, because seq_seen output should be 1 but the output from DUT is 0 
```




## Test Scenario ##
#### Test 1
- It tests whether the design can detect the sequence `1,0,1,1` from `1,1,0,1,1`
- Expected Output is `seq_seen = 1` atthe end of the test.
- Observed Output in the DUT ``dut.seq_seen=0``

Output mismatches for the above inputs proving that there is a design bug



## Design Bug
Based on the above test input and analysing the design, we see the following bugs:

### From Test 1
```
    SEQ_1:
    begin
        if(inp_bit == 1)
        next_state = IDLE;
        else
        next_state = SEQ_10;
      end                                => Here if the ``inp_bit`` is `1` the next state is `IDLE`. That is a bug.
 
```
Here, if the `inp_bit` is `1` then the next state should be `next_state = SEQ_1`.

## Design Fix
Updating the design and re-running the test makes the test pass.

![seq_fix](https://user-images.githubusercontent.com/84652232/181933584-5933a1a5-2d48-4167-8563-f147700a19c2.png)


The updated design is checked in as 

## Verification Strategy
.

## Is the verification complete ?
.

