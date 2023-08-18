import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles

import random
# import numpy as np

async def reset(dut):
  await ClockCycles(dut.ic_clk, 2) # wait for 2 clock cycles
  dut.ic_rst.value = 1
  await ClockCycles(dut.ic_clk, 2) # wait for 2 clock cycles
  dut.ic_rst.value = 0
  await ClockCycles(dut.ic_clk, 2) # wait for 2 clock cycles

'''
1. Testbench
'''
@cocotb.test()
async def mult_acc_tb1(dut):

  ''' Clock Generation '''
  clock = Clock(dut.ic_clk, 10, units="ns") # create a clock for dut.clk pin with 10 ns period
  cocotb.start_soon(clock.start()) # start clock in a seperate thread

  dut.id_din.value = 0
  dut.id_coef.value = 0
  dut.ic_ce.value = 0
  dut.ic_rst.value = 0
  dut.ic_neg_acc.value = 0

  await reset(dut)

  acc = 0
  await FallingEdge(dut.ic_clk)

  ''' Assign random values to input, wait for a clock and verify output '''
  for i in range(100): # 100 experiments
        
    din = random.randint(pow(-2,int(dut.Win)-1), pow(2,int(dut.Win)-1)-1) # generate a random number between -2^Win and 2^(Win-1)-1
    coef = random.randint(pow(-2,int(dut.Win)-1), pow(2,int(dut.Win)-1)-1) # generate a random number between -2^Wc and 2^(Wc-1)-1

    exact = acc + din * coef # compute the exact value
    acc = exact # update the accumulator


    # drive the input pins
    dut.id_din.value = din
    dut.id_coef.value = coef
    dut.ic_ce.value = 1
        
    await FallingEdge(dut.ic_clk)
        
    computed = dut.od_dout.value.signed_integer # Read pins as signed integer.
        
    assert exact == computed, f"Failed on the {i}th cycle. Got {computed}, expected {exact}" # If any assertion fails, the test fails, and the string would be printed in console
    print(f"Driven value: {exact} \t received value: {computed}") 


@cocotb.test()
async def mult_acc_tb2(dut):

  ''' Clock Generation '''
  clock = Clock(dut.ic_clk, 10, units="ns") # create a clock for dut.clk pin with 10 ns period
  cocotb.start_soon(clock.start()) # start clock in a seperate thread

  dut.id_din.value = 0
  dut.id_coef.value = 0
  dut.ic_ce.value = 0
  dut.ic_rst.value = 0
  dut.ic_neg_acc.value = 1

  await reset(dut)

  acc = 0
  await FallingEdge(dut.ic_clk)

  ''' Assign random values to input, wait for a clock and verify output '''
  for i in range(100):

    din = random.randint(pow(-2,int(dut.Win)-1), pow(2,int(dut.Win)-1)-1) # generate a random number between -2^Win and 2^(Win-1)-1
    coef = random.randint(pow(-2,int(dut.Win)-1), pow(2,int(dut.Win)-1)-1) # generate a random number between -2^Wc and 2^(Wc-1)-1

    exact = acc - din * coef # compute the exact value
    acc = exact # update the accumulator


    # drive the input pins
    dut.id_din.value = din
    dut.id_coef.value = coef
    dut.ic_ce.value = 1

    await FallingEdge(dut.ic_clk)
        
    computed = dut.od_dout.value.signed_integer # Read pins as signed integer.
        
    assert exact == computed, f"Failed on the {i}th cycle. Got {computed}, expected {exact}" # If any assertion fails, the test fails, and the string would be printed in console
    print(f"Driven value: {exact} \t received value: {computed}") 



'''
2. Pytest Setup
'''

from cocotb_test.simulator import run
import pytest
import glob

@pytest.mark.parametrize(
  # Two sets of parameters to test across
  "parameters", [
    {"Win": "8", "Wc": "8", "Wout": "20"},
  ])
def test_register(parameters):

  run(
    verilog_sources=glob.glob('src/MULT_ACC.sv'),
    toplevel="MULT_ACC",    # top level HDL
        
    module="test_MULT_ACC", # name of the file that contains @cocotb.test() -- this file
    simulator="icarus",
    waves=True,

    parameters=parameters,
    extra_env=parameters,
    sim_build="sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
  )