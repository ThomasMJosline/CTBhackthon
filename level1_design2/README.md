# Verification for 1011 Sequence Detector 
The 1011 Sequence detector is a Mealy based finite state machine consisting of 5 states.<br>
<br>The inputs of the Sequence detector module are single bit 'inp_bit', single bit 'reset' and a clock('clk'). <br>The output from the module is 'seq_seen' which is also single bit. A bug free 1011 Sequence detector is used to identify whether, the input given through 'inp_bit' is in the order 1,0,1,1. When this happens the 'seq_seen' output goes high. The Sequence detector also finds valid sequences, that are overlapped with non-sequences.<br>
<br>The verification is done using [Vyoma's UpTickPro](https://vyomasystems.com).

![hackmux](https://user-images.githubusercontent.com/84652232/181822344-6db71373-f658-43a5-b73d-d7427a1ee080.png)


## Verification Environment

The process of verification is done using Python language with the help of [CoCoTb](https://www.cocotb.org/) library.
<br> <br>
The bugs in the design arises when there are situations when valid sequences comes overlapping with the non-sequences.<br>
- 1,1,0,1,1 
- 1,0,1,0,1,1  <br>

These are the cases where, bugs in the design are seen.



#### Test1 ####

Here the inputs other than 'sel' is driven as seen above.<br>
In this test the input 'sel' is given all posiible values (ie. 0 to 30 ) by using a 'for' loop:
```
for i in range(31):
```
```
inp_sel=i
```
```
 dut.sel.value=inp_sel
 ```
 The values of 'sel', current input being selected, expected output and the output from the DUT are displayed
 ```
 dut._log.info(f'INPUT={A:03} SEL={inp_sel:05} EXPECT={A:03} DUT={int(dut.out.value):05}')
 ```
 For each value of 'sel' the comparison between the expected output and the output from DUT is done using the assert statement.

The following error is seen if expected result is not acheived
```
assert dut.out.value == A, "Randomised test failed because, selected input was inp{B} and expected output was {A} but the output from DUT is {OUT} ".format(B=dut.sel.value,A='{0:03b}'.format(A), OUT=dut.out.value)
```
When the test is run bug is found at 'sel'=12 :
```

```

#### Test2 ####
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

#### Test3 ####
This test is for capturing the bug when the 'sel' is equal to 30<br> Values assigned to inp30 and sel:

```
A=3
inp_sel=30

dut.inp30.value=A
dut.sel.value=inp_sel

```
The output from the DUT is compared with the inp30 as the 'sel' was given value equal to 30. If the values don't match a error message is thrown by the assert statement:


```
assert dut.out.value == A, "Test failed, because selected input was inp30 and expected output was {A} but the output from DUT is {OUT} ".format(A=dut.inp30.value, OUT=dut.out.value)

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
