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
async def REG_tb(dut):
  clock = Clock(dut.ic_clk, 10, units="ns") # create a clock for dut.clk pin with 10 ns period
  cocotb.start_soon(clock.start())

  DATA_WIDTH = int(dut.DATA_WIDTH)

  dut.id_data_in.value = 0
  dut.ic_rst.value = 0
  dut.ic_en.value = 0

  await reset(dut)

  await FallingEdge(dut.ic_clk)

  for i in range(100):
    d_in = random.randint(pow(-2,DATA_WIDTH-1), pow(2,DATA_WIDTH-1)-1)
    dut.ic_en.value = 1
    dut.id_data_in.value = d_in
    await FallingEdge(dut.ic_clk)
    
    dut.ic_en.value = 0
    assert dut.od_data_out.value.signed_integer == d_in, f"Failed on the {i}th cycle. Got {dut.od_data_out.value.signed_integer}, expected {d_in}"
    
    await ClockCycles(dut.ic_clk, 2, rising=False) # wait for 2 clock cycles


from cocotb_test.simulator import run
import pytest
import glob

@pytest.mark.parametrize(
  "parameters", [
    {"DATA_WIDTH": "8"},
    {"DATA_WIDTH": "16"},
    {"DATA_WIDTH": "24"},
    {"DATA_WIDTH": "32"}
  ])
def test_resgister(parameters):
  run(
    verilog_sources=glob.glob("src/REG.sv"),
    toplevel="REG",
    module="test_REG",
    simulator="icarus",
    waves="wave.vcd",
    parameters=parameters,
    extra_env=parameters,
    sim_build="sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items()))
  )

