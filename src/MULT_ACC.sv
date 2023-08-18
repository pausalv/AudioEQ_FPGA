module MULT_ACC #(
    parameter integer Win = 24,  //! Input signal width
    parameter integer Wc  = 27,   //! Coefficient width
    parameter integer Wout = 64  //! Output signal width
) (
    input signed [Win-1:0] id_din,  //! Input data
    input signed [ Wc-1:0] id_coef, //! Coefficient

    input ic_clk,  //! Clock
    input ic_ce,  //! Accumulation enable
    input ic_rst,  //! Reset
    input ic_neg_acc,  //! Negate accumulation

    output logic signed [Wout-1:0] od_dout  //! Output data
);

  //! Multiplication result
  logic signed [Wout-1:0] mult;

  //! Accumulator
  logic signed [Wout-1:0] acc;

  logic ce_r;  //! Registered accumulation enable
  logic rst_r;  //! Registered reset
  logic neg_acc_r;  //! Registered negate accumulation

  assign mult = id_din * id_coef;

  assign od_dout = acc;

  always_ff @(posedge ic_clk) begin : accumulator
    if (rst_r) acc <= 0;
    else if (ce_r) acc <= neg_acc_r ? acc + mult : acc - mult;
    else acc <= acc;
  end

  always_ff @(posedge ic_clk) begin : register_control_signals
    rst_r <= ic_rst;
    ce_r <= ic_ce;
    neg_acc_r <= ic_neg_acc;
  end

endmodule
