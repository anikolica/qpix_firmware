`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/21/2023 03:22:56 PM
// Design Name: 
// Module Name: tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module tb(

    );

    reg clk = 0;
    reg rst = 0;
    reg load_ser1 = 0;
    reg xmit_ser1 = 0;
    reg [31:0] data1 = 32'h1db6ff8b;
    piso serial_gen1 (
        .load(load_ser1),
        .xmit(xmit_ser1),
        .clk(clk),
        .rst(rst),
        .data_in(data1),
        .data_out(),
        .clk_out()
    );
    
    reg [5:0] test_mux_sel = 5'h00; 
    demux1to32 test_mux (
        .Data_in(clk),
        .sel(test_mux_sel),
        .Data_out()
    );
    
    reg clk200 = 0;
    reg TRIGGER = 1'b0;
    reg [15:0] oLVDS = 16'h0;
    reg [16*32-1:0] reg_rw = 1024'h0;
    top_rtl top (
        .clk(clk),
        .clk200(clk200),
        .OSC_200MHz(      ),
        .oLVDS(oLVDS),
        .reg_rw(reg_rw)
    );
    
    // *** TESTS ***
    
    always #10 clk = ~clk; // System clock 50MHz
    always #2.5 clk200 = ~clk200; // Event clock 200MHz
   
    initial begin
        #20     rst = 1;
        #75     rst = 0;

        // Test 32-bit register load
        #200    load_ser1 = 1;
        #100    load_ser1 = 0;
        
        #200    xmit_ser1 = 1;
        #1600   xmit_ser1 = 0;
        
        // Test clock demux
        #100    test_mux_sel = 5'h01;
        #100    test_mux_sel = 5'h02;
        #100    test_mux_sel = 5'h03;
        #100    test_mux_sel = 5'h04;
        #100    test_mux_sel = 5'h05;
        #100    test_mux_sel = 5'h06;
        #100    test_mux_sel = 5'h07;
        #100    test_mux_sel = 5'h08;
        #100    test_mux_sel = 5'h09;
        #100    test_mux_sel = 5'h0a;
        #100    test_mux_sel = 5'h0b;
        #100    test_mux_sel = 5'h0c;
        #100    test_mux_sel = 5'h0d;
        #100    test_mux_sel = 5'h0e;
        #100    test_mux_sel = 5'h0f;
        #100    test_mux_sel = 5'h10;
        #100    test_mux_sel = 5'h11;
        #100    test_mux_sel = 5'h11;
        #100    test_mux_sel = 5'h12;
        #100    test_mux_sel = 5'h13;
        #100    test_mux_sel = 5'h14;
        #100    test_mux_sel = 5'h15;
        #100    test_mux_sel = 5'h16;
        #100    test_mux_sel = 5'h17;
        #100    test_mux_sel = 5'h18;
        #100    test_mux_sel = 5'h19;
        #100    test_mux_sel = 5'h1a;
        #100    test_mux_sel = 5'h1b;
        #100    test_mux_sel = 5'h1c;
        #100    test_mux_sel = 5'h1d;
        #100    test_mux_sel = 5'h1e;
        #100    test_mux_sel = 5'h1f;
        
        // Test FIFO
        #500    reg_rw[ 5 * 32 + 0] = 1'b1; // TRIGGER
        #500    oLVDS[0] = 1'b1;
        #10     oLVDS[0] = 1'b0;
        #500    oLVDS[0] = 1'b1;
        #10     oLVDS[0] = 1'b0;
        
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        
        #500    oLVDS[1] = 1'b1;
        #10     oLVDS[1] = 1'b0;
        #500    oLVDS[1] = 1'b1;
        #10     oLVDS[1] = 1'b0;
    end
endmodule
