# Verification for Elevator Controller
The Elevator Controller is a Mealy based finite state machine consisting of 3 states.<br>
<br>The inputs of the module are `requested_floor` which is of 4 bits, single bit `reset` and a clock('clk'). <br>The output from the module are `y` that shows the current floor, `door`,`Up`,`Down` and `wait_floor`.<br>
<br>The verification is done using [Vyoma's UpTickPro](https://vyomasystems.com).

![github_id](https://user-images.githubusercontent.com/84652232/181879292-9b0057a9-14a5-48eb-8640-1f4c2f89e669.png)



## Verification Environment

The process of verification is done using Python language with the help of [CoCoTb](https://www.cocotb.org/) library.
<br> <br>

#### Test 1 ####
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

#### Test 2 ####
A elevator should work in such a manner, that it should move to the firstly entered floor if two inputs are given in order. This property is verified here:
First the the input is given so as to move to 7th floor:
```
dut.requested_floor.value=7   
```
while this happens another input is given for moving to 2nd floor:
```
dut.requested_floor.value=2
```
Output from DUT is evaluated and the error message is generated with an assert statement:
```
assert dut.y.value == 7, "Test failed, because it was expected to reach {B}th but DUT reached {OUT} ".format(B=7, OUT=dut.seq_seen.value)
```

Failure of the design :
![bug_elevator](https://user-images.githubusercontent.com/84652232/182100071-03d81375-e128-41c4-8160-a0e26e314438.png)



## Test Scenario ##

#### Test 1 ####
- The input given is `requested_floor=7`.
- Expected Output at the end of the test is `y=7`,`Up=0`,`Down=0`,`door=1` and `wait_floor=1`
- Observed Output in the DUT `UP=00 DOWN=01 DOOR=00 WAITING=00 CURRENT_FLOOR=0011`

Output mismatches for the above inputs proving that there is a design bug

#### Test 2 ####
- The input given is `requested_floor=7` and while the elevator is moving another input is given `requested_floor=2`. The test ends in a time that is figured such that the elevator reaches the 7th floor
- Expected Output at the end of the test is `y=7`,`Up=0`,`Down=0`,`door=1` and `wait_floor=1`
- Observed Output in the DUT `UP=00 DOWN=01 DOOR=00 WAITING=00 CURRENT_FLOOR=0003`

Output mismatches for the above inputs proving that there is a design bug

## Design Bug

### From Test 1 ###
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
Here the line ``current_floor = current_floor+1`` should be removed.

## Design Fix
Updating the design and re-running the test makes the design pass test 1.

![ele](https://user-images.githubusercontent.com/84652232/182099769-f6d62a8c-1fa3-42fd-9503-2e8a27dc50a1.png)



The updated design is checked in as Elevator_controller_fix.v

## Verification Strategy
The bug was inserted for the hackathon purpose and the test cases were generated accordingly.

## Is the verification complete ?
In the design, there are some bugs that are related to the design. e.g.:
- If the an input is given during the movement of the elevator, instead of moving to the firstly entered floor it starts moving to the last entered floor.
- Speed of movement of the elevator. Instead of the design shown here, there should be a motor module that works according to the input and this motor controls the movement of the elevator.

