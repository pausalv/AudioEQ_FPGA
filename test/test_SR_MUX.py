import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge
import random

async def reset(dut):
  await ClockCycles(dut.ic_clk, 2, rising=False) # wait for 2 clock cycles
  dut.ic_rst.value = 1
  await ClockCycles(dut.ic_clk, 2, rising=False) # wait for 2 clock cycles
  dut.ic_rst.value = 0
  await ClockCycles(dut.ic_clk, 2) # wait for 2 clock cycles

@cocotb.test()
async def SR_MUX_tb(dut):
  clock = Clock(dut.ic_clk, 10, units="ns") # create a clock for dut.clk pin with 10 ns period
  cocotb.start_soon(clock.start()) # start clock in a seperate thread

  IN_WIDTH = int(dut.IN_WIDTH)
  NUM = int(dut.NUM)

  dut.id_data_in.value = 0
  dut.ic_rst.value = 0
  dut.ic_en.value = 0
  dut.ic_addr.value = 0

  await reset(dut)

  await FallingEdge(dut.ic_clk)

  for i in range(NUM):
    dut.ic_addr.value = i
    await FallingEdge(dut.ic_clk)
    assert dut.od_data_out.value.signed_integer == 0, f"Failed on the {i}th cycle. Got {dut.od_data_out.value}, expected {0}"

  d_in = [0 for i in range(NUM)]

  for i in range(NUM):
    d_in[i] = random.randint(pow(-2,IN_WIDTH-1), pow(2,IN_WIDTH-1)-1)

  for i in range(NUM):
    dut.ic_en.value = 1
    dut.id_data_in.value = d_in[i]
    await FallingEdge(dut.ic_clk)
    dut.ic_en.value = 0
    
    for j in range(NUM):
      dut.ic_addr.value = j
      await FallingEdge(dut.ic_clk)

      d_out = dut.od_data_out.value.signed_integer
      
      if(j <= i):
        assert d_out == d_in[i-j], f"Failed on the {i}th cycle. Got {dut.od_data_out.value}, expected {d_in[j]}"
      else:
        assert d_out == 0, f"Failed on the {i}th cycle. Got {dut.od_data_out.value}, expected {0}"
      



from cocotb_test.simulator import run
import pytest
import glob

@pytest.mark.parametrize(
  "parameters", [
    {"IN_WIDTH": "24", "NUM": "3"},
    {"IN_WIDTH": "16", "NUM": "10"}
  ])
def test_register(parameters):
  run(
    verilog_sources=glob.glob('src/SR_MUX.sv'),
    toplevel="SR_MUX",    # top level HDL
    module="test_SR_MUX", # test module within HD
    simulator="icarus",
    waves="wave.vcd",
    parameters=parameters,
    extra_env=parameters,
    sim_build="sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items()))
  )