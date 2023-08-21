`timescale 1us/1ns

import log2_pkg::log2;

module COEF_REG_MUX #(
    parameter WIDTH = 27,
    parameter ORDER_IIR = 2
  )(
    input ic_clk,
    input ic_rst,
    input [log2(ORDER_IIR+1)-1:0] ic_coef_sel,
    input ic_sel_a_b,
    input ic_val_coef_a,
    input ic_val_coef_b,
    input signed [WIDTH-1:0] id_coef_in_a [ORDER_IIR],
    input signed [WIDTH-1:0] id_coef_in_b [ORDER_IIR + 1],
    output logic signed [WIDTH-1:0] od_coef_out
  );

  logic signed [WIDTH-1:0] coef_in_a_r[ORDER_IIR];
  logic signed [WIDTH-1:0] coef_in_b_r[ORDER_IIR + 1];

  always_ff @ (posedge ic_clk)
    if(ic_rst)
      for (int i = 0; i < ORDER_IIR; i++)
        coef_in_a_r[i] <= 0;
    else if(ic_val_coef_a)
      for (int i = 0; i < ORDER_IIR; i++)
        coef_in_a_r[i] <= id_coef_in_a[i];
  
  always_ff @ (posedge ic_clk)
    if(ic_rst)
      for (int i = 0; i < ORDER_IIR + 1; i++)
        coef_in_b_r[i] <= 0;
    else if(ic_val_coef_b)
      for (int i = 0; i < ORDER_IIR + 1; i++)
        coef_in_b_r[i] <= id_coef_in_b[i];
  
  always_ff @ (posedge ic_clk)
    if(ic_rst)
      od_coef_out <= 0;
    else
      if(ic_sel_a_b)
        od_coef_out <= coef_in_a_r[ic_coef_sel];
      else
        od_coef_out <= coef_in_b_r[ic_coef_sel];
   
endmodule
