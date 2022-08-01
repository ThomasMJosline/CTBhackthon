
# Verification for Bitmanipulation co-processor

<br>The verification is done using [Vyoma's UpTickPro](https://vyomasystems.com).

![github_id](https://user-images.githubusercontent.com/84652232/181879292-9b0057a9-14a5-48eb-8640-1f4c2f89e669.png)



## Verification Environment

The process of verification is done using Python language with the help of [CoCoTb](https://www.cocotb.org/) library.
<br> <br>

#### Test 1 ####

When the instruction corresponding to NAND is given there is a mismatch between the model output and DUT output.<br>
Inputs and instruction:


```
    mav_putvalue_src1 = 0x5
    mav_putvalue_src2 = 0x6
    mav_putvalue_src3 = 0x4
    mav_putvalue_instr = 0x40847433
```

The output from the DUT is compared with the model output. This is done using an assert statement:
```
    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    assert dut_output == expected_mav_putvalue, error_message

```
When this test was done the bug got exopsed and the error message appeared:
```
 AssertionError: Value mismatch DUT = 0x9 does not match MODEL = 0x3
```



Failure of the design :
![bug_elevator](https://user-images.githubusercontent.com/84652232/182100071-03d81375-e128-41c4-8160-a0e26e314438.png)



## Test Scenario ##

- The inputs are `mav_putvalue_src1 = 0x5`,`mav_putvalue_src2 = 0x6`,`mav_putvalue_src3 = 0x4` and instruction `mav_putvalue_instr = 0x40847433`
- Expected Output was `0x3`
- Observed Output from the DUT was `0x9`

Output mismatches for the above inputs proving that there is a design bug


## Design Bug


## Design Fix


## Verification Strategy


## Is the verification complete ?
No, there are much more set of instructions that are formed by combinations of different set of values of func7, func3 and opcode.

