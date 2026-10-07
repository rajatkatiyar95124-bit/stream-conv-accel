`timescale 1ns/1ps

module counter_tb;

    logic clk;
    logic rst;
    logic en;
    logic [7:0] count;

    counter dut (
        .clk   (clk),
        .rst   (rst),
        .en    (en),
        .count (count)
    );

    // Clock: 10 ns period
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        rst = 1;
        en  = 0;

        #12;
        rst = 0;
        en  = 1;

        #50;

        if (count == 8'd5)
            $display("PASS: count = %0d", count);
        else
            $display("FAIL: count = %0d, expected 5", count);

        $finish;
    end

endmodule