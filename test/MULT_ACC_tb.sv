
module MULT_ACC_tb;

  // Parameters
  localparam integer Win = 0;
  localparam integer Wc = 0;
  localparam integer Wout = 0;

  //Ports
  logic signed [Win-1:0] id_din;
  logic signed [ Wc-1:0] id_coef;
  logic  ic_clk;
  logic  ic_ce;
  logic  ic_rst;
  logic  ic_neg_acc;
  logic [Wout-1:0] od_dout;

  MULT_ACC # (
    .Win(Win),
    .Wc(Wc),
    .Wout(Wout)
  )
  MULT_ACC_inst (
    .id_din(id_din),
    .id_coef(id_coef),
    .ic_clk(ic_clk),
    .ic_ce(ic_ce),
    .ic_rst(ic_rst),
    .ic_neg_acc(ic_neg_acc),
    .od_dout(od_dout)
  );


  always #5  ic_clk = !ic_clk;

  initial begin
    ic_clk = 1'b0;
    ic_ce = 1'b0;
    ic_rst = 1'b0;
    ic_neg_acc = 1'b0;
    id_din = 0;
    id_coef = 0;

    #10 ic_rst = 1'b1;
    #20 ic_rst = 1'b0;

    #100
    @ (negedge ic_clk)
    id_din = 10;
    id_coef = 2;

    @ (negedge ic_clk)
    assert (od_dout == id_din * id_coef) $info ("Test passed");
    else   $error ("Error at %t: expected %d, got %d", $time, id_din * id_coef, od_dout);

    $finish;

  end

endmodule
