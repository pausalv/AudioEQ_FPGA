`timescale 1us/1ns

module REG #(
    parameter integer DATA_WIDTH = 24
  )(
    input ic_clk,
    input ic_rst,
    input ic_en,
    input signed [DATA_WIDTH-1:0] id_data_in,
    output logic signed [DATA_WIDTH-1:0] od_data_out
  );

  always_ff @ (posedge ic_clk)
    if(ic_rst)
      od_data_out <= 0;
    else if(ic_en)
      od_data_out <= id_data_in;


endmodule
