`timescale 1us/1ns

module SR_MUX #(
    parameter integer IN_WIDTH = 24,
    parameter integer NUM = 3
)(
    input ic_clk,
    input ic_rst,
    input ic_en,
    input [NUM-1:0] ic_addr,
    input signed [IN_WIDTH-1:0] id_data_in,
    output logic signed [IN_WIDTH-1:0] od_data_out
);

integer i;

reg signed [IN_WIDTH-1:0] SR [NUM-1:0];

// initial
//     for(i = 0; i < NUM; i=i+1)
//         SR[i] = 0;

always_ff @ (posedge ic_clk)
    if(ic_rst)
        for (i = 0; i < NUM; i=i+1)
            SR[i] <= 0;
    else if(ic_en) begin
        for (i = 1; i < NUM; i=i+1)
            SR[i] <= SR[i-1];
        SR[0] <= id_data_in;
    end

always_ff @ (posedge ic_clk)
    if(ic_rst)
        od_data_out <= 0;
    else
        if(ic_addr < NUM)
            od_data_out <= SR[ic_addr];
        else
            od_data_out <= 0;


endmodule