`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: University of Pennsylvania 
// Engineer: A. Nikolica
// 
// Create Date: 03/24/2025 04:41:41 PM
// Design Name: 
// Module Name: tb_debug1
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: Test one channel data collection over a relatively long time
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module tb_debug1(

    );
    
    reg clk = 1'b0;
    reg clk200 = 1'b0;
    reg TRIGGER = 1'b0;
    reg [15:0] oLVDS = 16'h0;
    reg opad2_deltaT = 1'b0;
    reg [64*32-1:0] reg_rw = 2048'h0;
    
    // Include SIM=1 in the defines in Vivado
    // to get faster clock for serial interface
    top_rtl top (
        .clk(clk),
        .clk200(clk200),
        .oLVDS(oLVDS),
        .opad2_deltaT(opad2_deltaT),
        .reg_rw(reg_rw)
    );
    
    // *** TESTS ***
    
    always #10 clk = ~clk; // System clock 50MHz
    always #2.5 clk200 = ~clk200; // Event clock 200MHz
    
    always begin
        #40         oLVDS[0] = 1'b0; // repeated 40ns wide pulse
        #1000000    oLVDS[0] = 1'b1;
    end
    
    task read;
        begin
            #500    reg_rw[ 6 * 32 + 0] = 1'b1; // Read FIFO0
            #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        end
    endtask
   
    initial begin
        #0      reg_rw[ 0 * 32 + 0] = 1'b1; // master reset
        #500    reg_rw[ 0 * 32 + 0] = 1'b0;
        
        // For 111 ms, Nandor's settings
        #100    reg_rw[ 2 * 32 + 31 :  2 * 32 +  0] = 32'h55b6ffc4; // data to QPix, irrelevant
        #0      reg_rw[ 4 * 32 + 31 :  4 * 32 +  0] = 32'h55b6ffc4; // data to QPix, irrelevant
        //#0      reg_rw[ 7 * 32 + 31 :  7 * 32 +  0] = 32'h0054afb0; // window width = 111ms
        #0      reg_rw[ 7 * 32 + 31 :  7 * 32 +  0] = 32'h00557300; // window width = 112ms
        #0      reg_rw[ 8 * 32 + 31 :  8 * 32 +  0] = 32'h000500fa; // reset width = 5us, reset_cal_gap = 200us (irrelevant)
        #0      reg_rw[ 9 * 32 + 31 :  9 * 32 +  0] = 32'h80000064; // sample on window, window wait = 2us
        #0      reg_rw[10 * 32 + 31 : 10 * 32 +  0] = 32'h00000001; // deltaT2, irrelevant

        //#1000   opad2_deltaT = 1'b1;
        //#4000   opad2_deltaT = 1'b0;
        
        #1000       reg_rw[ 0 * 32 + 15] = 1'b1; // window trig
        #113000000  reg_rw[ 5 * 32 + 0] = 1'b1; // This is a NO-OP
                
        repeat(150)
            #500 read();
        
        // run for 115ms    
        //#100    reg_rw[ 0 * 32 + 15] = 1'b0;

    end
endmodule
