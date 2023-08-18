
import words_lengths_pkg::*;


module IIR_parallel#(
    parameter integer Nsig = 16,
    parameter integer Ncoef = 16,
    parameter integer Nstage = 4
)(
    input ic_clk,
    input ic_rstn,
    input signed [Nsig-1:0] id_input,
    input signed [Ncoef-1:0] id_num[Nstage],
    input signed [Ncoef-1:0] id_den[Nstage - 1],
    output logic signed [Nsig-1:0] od_output
    );


    logic signed [Nsig-1:0] input_r[Nstage];
    logic signed [Nsig-1:0] output_r[Nstage];

    logic signed [Nsig+Ncoef-1:0] input_mul[Nstage];

    always_ff @ (posedge ic_clk)
        if(!ic_rstn)
            for(integer i=0; i<Nstage; i++)
                input_r[i] <= 0;
        else begin
            input_r[0] <= id_input;
            for(integer i=1; i<Nstage; i++)
                input_r[i] <= input_r[i];
        end

    always_ff @ (posedge ic_clk)
        if(!ic_rstn)
            for(integer i=0; i<Nstage; i++)
                input_mul[i] <= 0;
        else
            for(integer i=1; i<Nstage; i++)
                input_mul[i] <= input_r[i] * id_num[i];



    always_ff @ (posedge ic_clk)
        if(!ic_rstn)
            for(integer i=0; i<Nstage; i++)
                output_r[i] <= 0;
        else begin
            output_r[0] <= input_r[0];
            for(integer i=1; i<Nstage; i++)
                output_r[i] <= output_r[i];
        end





endmodule
