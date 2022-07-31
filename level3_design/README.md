# Verification for Elevator Controller
The Elevator Controller is a Mealy based finite state machine consisting of 3 states.<br>
<br>The inputs of the module are `requested_floor` which is of 4 bits, single bit `reset` and a clock('clk'). <br>The output from the module are `y` that shows the current floor, `door`,`Up`,`Down` and `wait_floor`.<br>
<br>The verification is done using [Vyoma's UpTickPro](https://vyomasystems.com).

![github_id](https://user-images.githubusercontent.com/84652232/181879292-9b0057a9-14a5-48eb-8640-1f4c2f89e669.png)



## Verification Environment

The process of verification is done using Python language with the help of [CoCoTb](https://www.cocotb.org/) library.
<br> <br>
Initially, the elevator is at ground floor(`y=0`).In the test, input `requested_floor` is given as 7(i.e. to move to the floor):


```
dut.requested_floor.value=7   
```
After this we wait for seven falling edge of the clock using a for loop:
```
    for i in (7):
        dut._log.info(f'UP={int(dut.Up.value):02} DOWN={int(dut.Down.value):02} DOOR={int(dut.door.value):02} WAITING={int(dut.wait_floor.value):02}             CURRENT_FLOOR={int(dut.y.value):04}')
        await FallingEdge(dut.clk)

```
The output from the DUT are seen during this time. At the end, it is checked whether the elevator have reached the requested floor i.e. the 7th floor. This is confirmed by an assert statement:
```
assert dut.y.value == 7, "Test failed, because it was expected to reach {B}th but DUT reached {OUT} ".format(B=7, OUT=dut.seq_seen.value)
```
When this test was done the bug got exopsed and the error message appeared:
```
 AssertionError: Test failed, because it was expected to reach 7th but DUT reached 01011
```




## Test Scenario ##

- The input given is `requested_floor=7`.
- Expected Output at the end of the test is `y=7`,`Up=0`,`Down=0`,`door=1` and `wait_floor=1`
- Observed Output in the DUT 

Output mismatches for the above inputs proving that there is a design bug


## Design Bug
Based on the above test input and analysing the design, we see the following bugs:

```
            begin
                if(requested_floor < current_floor)
                begin
                    current_floor=current_floor+1;              => BUG
                    door=1'd0;
                    wait_floor=4'd0;
                    Up=1'd0;
                    Down=1'd1;
                end                            
 
```
Here instead of `current_floor=current_floor+1` it should be `current_floor=current_floor-1`.


```
                else if(requested_floor == current_floor)
                begin
                    current_floor = current_floor+1;           => BUG
                    door=1'd1;
                    wait_floor=4'd1;
                    Up=1'd0;
                    Down=1'd0;                              
                end
```
Here, if the `inp_bit` is `1` then the next state should be `next_state = SEQ_1`.

## Design Fix
Updating the design and re-running the test makes the test pass.

![elevatorfix](https://user-images.githubusercontent.com/84652232/182021154-3483e47b-da5c-4fd3-888d-653341266986.png)


The updated design is checked in as Elevator_controller_fix.v

## Verification Strategy
The bug was inserted

## Is the verification complete ?
.

