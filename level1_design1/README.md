# Multiplexer Design Verification
The inputs of the multiplexer module are 31 two bit inputs( inp0,inp1,inp2,...inp30) and a four bit 'sel'. The output from the module is 'out' which is in two bits. A properly designed multiplexer selects one of the 31 inputs from inp0,inp1,inp2,...inp30 based on the value given to input 'sel' and gives that input as the 'out' value.

The verification is done using [Vyoma's UpTickPro](https://vyomasystems.com).

![github_id](https://user-images.githubusercontent.com/84652232/181879292-9b0057a9-14a5-48eb-8640-1f4c2f89e669.png)



## Verification Environment

The process of verification is done using Python language with the help of [CoCoTb](https://www.cocotb.org/) library.
<br> All the inputs among inp0,inp1,...inp30 are assigned random 2 bit valued integers (ie. numbers from 0 t0 3) using:

```
i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19,i20,i21,i22,i23,i24,i25,i26,i27,i28,i29,i30 = (random.randint(0, 3) for x in range(31))
```
```
dut.inp0.value=i0
dut.inp1.value=i1
dut.inp2.value=i2
```
.<br>.<br>.<br>
```
dut.inp30.value=i30
```
The input 'sel' is given different values in the different tests conducted.

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
AssertionError: Randomised test failed with, because, selected input was inp01100 and expected output was 001 but the output from DUT is 00 
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
AssertionError: Test failed, because selected input was inp13 and expected output was 11 but the output from DUT is 10 
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
    AssertionError: Test failed, because selected input was inp30 and expected output was 11 but the output from DUT is 00 
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

![muxfix](https://user-images.githubusercontent.com/84652232/181877909-8c4ccec6-17c6-4edd-87c8-4edbf05c74e7.png)


The updated design is checked in as mux_fix.v

## Verification Strategy
Analysis of the verilog code given for the design, helped to understand possible bugs. These bug were then confirmed through three tests.

## Is the verification complete ?
Yes, the multiplexer design code is completely verified and three bugs were found.
