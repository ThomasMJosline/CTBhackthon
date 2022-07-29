# Multiplexer Design Verification
The inputs of the multiplexer module are 31 two bit inputs( inp0,inp1,inp2,...inp30) and a four bit 'sel'. The output from the module is 'out' which is in two bits. A properly designed multiplexer selects one of the 31 inputs from inp0,inp1,inp2,...inp30 based on the value given to input 'sel' and gives that input as the 'out' value.

The verification is done using [Vyoma's UpTickPro](https://vyomasystems.com).

<img src="challenges-ThomasMJosline/level1_design1/hackmux.png">

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

## Test Scenario **(Important)**
- Test Inputs: a=7 b=5
- Expected Output: sum=12
- Observed Output in the DUT dut.sum=2

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
 always @(a or b) 
  begin
    sum = a - b;             ====> BUG
  end
```
For the adder design, the logic should be ``a + b`` instead of ``a - b`` as in the design code.

## Design Fix
Updating the design and re-running the test makes the test pass.

![](https://i.imgur.com/5XbL1ZH.png)

The updated design is checked in as adder_fix.v

## Verification Strategy

## Is the verification complete ?
