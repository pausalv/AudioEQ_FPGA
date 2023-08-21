
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

async def check_all_0(dut, ORDER_IIR):
  dut.ic_sel_a_b.value = 0
  for i in range(ORDER_IIR + 1):
    dut.ic_coef_sel.value = i
    await FallingEdge(dut.ic_clk)
    assert dut.od_coef_out.value.signed_integer == 0, f"Failed on the {i}th cycle. Got {dut.od_coef_out.value}, expected {0}"

  dut.ic_sel_a_b.value = 1
  for i in range(ORDER_IIR):
    dut.ic_coef_sel.value = i
    await FallingEdge(dut.ic_clk)
    assert dut.od_coef_out.value.signed_integer == 0, f"Failed on the {i}th cycle. Got {dut.od_coef_out.value}, expected {0}"
    



@cocotb.test()
async def coef_reg_mux(dut):
  clock = Clock(dut.ic_clk, 10, units="ns") # create a clock for dut.clk pin with 10 ns period
  cocotb.start_soon(clock.start())

  WIDTH = int(dut.WIDTH)
  ORDER_IIR = int(dut.ORDER_IIR)

  dut.ic_rst.value = 0
  dut.ic_coef_sel.value = 0
  dut.ic_sel_a_b.value = 0
  dut.ic_val_coef_a.value = 0
  dut.ic_val_coef_b.value = 0
  dut.id_coef_in_a.value = [0 for i in range(ORDER_IIR)]
  dut.id_coef_in_b.value = [0 for i in range(ORDER_IIR+1)]

  await reset(dut)

  await FallingEdge(dut.ic_clk)

  a = [0 for i in range(ORDER_IIR)]
  b = [0 for i in range(ORDER_IIR+1)]
  
  for i in range(ORDER_IIR+1):
    if(i < ORDER_IIR):
      a[i] = random.randint(pow(-2,WIDTH-1), pow(2,WIDTH-1)-1)
    b[i] = random.randint(pow(-2,WIDTH-1), pow(2,WIDTH-1)-1)

  print(a)
  print(b)  

  await check_all_0(dut, ORDER_IIR)

  dut.id_coef_in_a.value = a[::-1]
  dut.ic_val_coef_a.value = 1

  await FallingEdge(dut.ic_clk)

  dut.ic_val_coef_a.value = 0

  dut.ic_sel_a_b.value = 0
  for i in range(ORDER_IIR + 1):
    dut.ic_coef_sel.value = i
    await FallingEdge(dut.ic_clk)
    assert dut.od_coef_out.value.signed_integer == 0, f"Failed on the {i}th cycle. Got {dut.od_coef_out.value.signed_integer}, expected {0}"

  dut.ic_sel_a_b.value = 1
  for i in range(ORDER_IIR):
    dut.ic_coef_sel.value = i
    await FallingEdge(dut.ic_clk)
    assert dut.od_coef_out.value.signed_integer == a[i], f"Failed on the {i}th cycle. Got {dut.od_coef_out.value.signed_integer}, expected {a[i]}"

  dut.id_coef_in_b.value = b[::-1]

  dut.ic_val_coef_b.value = 1

  await FallingEdge(dut.ic_clk)

  dut.ic_val_coef_b.value = 0

  dut.ic_sel_a_b.value = 0
  for i in range(ORDER_IIR + 1):
    dut.ic_coef_sel.value = i
    await FallingEdge(dut.ic_clk)
    assert dut.od_coef_out.value.signed_integer == b[i], f"Failed on the {i}th cycle. Got {dut.od_coef_out.value.signed_integer}, expected {a[i]}"
  
  dut.ic_sel_a_b.value = 1
  for i in range(ORDER_IIR):
    dut.ic_coef_sel.value = i
    await FallingEdge(dut.ic_clk)
    assert dut.od_coef_out.value.signed_integer == a[i], f"Failed on the {i}th cycle. Got {dut.od_coef_out.value.signed_integer}, expected {b[i]}"
  

from cocotb_test.simulator import run
import pytest
import glob

@pytest.mark.parametrize(
  "parameters", [
    {"WIDTH": "8", "ORDER_IIR": "2"},
    {"WIDTH": "16", "ORDER_IIR": "3"},
    {"WIDTH": "24", "ORDER_IIR": "4"},
    {"WIDTH": "32", "ORDER_IIR": "5"}
  ])
def test_coef_reg_mux(parameters):
  run(
    verilog_sources=['./src/log2_pkg.sv','./src/COEF_REG_MUX.sv'],
    toplevel="COEF_REG_MUX",    # top level HDL
    module="test_COEF_REG_MUX", # test module within HD
    simulator="icarus",
    waves="wave.vcd",
    parameters=parameters,
    extra_env=parameters,
    sim_build="sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items()))
  )