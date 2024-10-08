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
    
    /* reg [5:0] test_mux_sel = 5'h00; 
    demux1to32 test_mux (
        .Data_in(clk),
        .sel(test_mux_sel),
        .Data_out()
    ); */
    
    reg clk = 1'b0;
    reg clk200 = 1'b0;
    reg TRIGGER = 1'b0;
    reg [15:0] oLVDS = 16'h0;
    reg opad_deltaT = 1'b0;
    reg [64*32-1:0] reg_rw = 2048'h0;
    
    // Include SIM=1 in the defines in Vivado
    // to get faster clock for serial interface
    top_rtl top (
        .clk(clk),
        .clk200(clk200),
        .oLVDS(oLVDS),
        .opad_deltaT(opad_deltaT),
        .reg_rw(reg_rw)
    );
    
    // *** TESTS ***
    
    always #10 clk = ~clk; // System clock 50MHz
    always #2.5 clk200 = ~clk200; // Event clock 200MHz
   
    initial begin
        // Test clock demux
        /* #100    test_mux_sel = 5'h01;
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
        #100    test_mux_sel = 5'h1f; */
        
        #0      reg_rw[ 0 * 32 + 0] = 1'b1; // master reset
        #500    reg_rw[ 0 * 32 + 0] = 1'b0;
               
        // Test FIFO
        #500    reg_rw[ 5 * 32 + 0] = 1'b1; // TRIGGER
        #0      opad_deltaT = 1'b1;
        #500    oLVDS[0] = 1'b1; // Events
        #10     oLVDS[0] = 1'b0;
        #500    oLVDS[0] = 1'b1;
        #10     oLVDS[0] = 1'b0;
        #200    oLVDS[0] = 1'b1; // More events
        #10     oLVDS[0] = 1'b0;
        #100    oLVDS[0] = 1'b1;
        #10     oLVDS[0] = 1'b0;
        
        #500    reg_rw[ 6 * 32 + 0] = 1'b1; // Read FIFO0 five times
        #100    reg_rw[ 6 * 32 + 0] = 1'b0; // 5th read should not issue
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        
        //#10     opad_deltaT = 1'b0;
        //#500    oLVDS[1] = 1'b1; // More events on second channel
        //#10     oLVDS[1] = 1'b0;
        //#500    oLVDS[1] = 1'b1;
        //#10     oLVDS[1] = 1'b0;
        
        // Test all FIFOs
        #500    oLVDS[1] = 1'b1;
        #10     oLVDS[1] = 1'b0;
        #10     oLVDS[2] = 1'b1;
        #10     oLVDS[2] = 1'b0;
        #10     oLVDS[3] = 1'b1;
        #10     oLVDS[3] = 1'b0;
        #10     oLVDS[4] = 1'b1;
        #10     oLVDS[4] = 1'b0;
        #10     oLVDS[5] = 1'b1;
        #10     oLVDS[5] = 1'b0;
        #10     oLVDS[6] = 1'b1;
        #10     oLVDS[6] = 1'b0;
        #10     oLVDS[7] = 1'b1;
        #10     oLVDS[7] = 1'b0;
        #10     oLVDS[8] = 1'b1;
        #10     oLVDS[8] = 1'b0;
        #10     oLVDS[9] = 1'b1;
        #10     oLVDS[9] = 1'b0;
        #10     oLVDS[10] = 1'b1;
        #10     oLVDS[10] = 1'b0;
        #10     oLVDS[11] = 1'b1;
        #10     oLVDS[11] = 1'b0;
        #10     oLVDS[12] = 1'b1;
        #10     oLVDS[12] = 1'b0;
        #10     oLVDS[13] = 1'b1;
        #10     oLVDS[13] = 1'b0;
        #10     oLVDS[14] = 1'b1;
        #10     oLVDS[14] = 1'b0;
        #10     oLVDS[15] = 1'b1;
        #10     oLVDS[15] = 1'b0;
        #500    reg_rw[ 6 * 32 + 1] = 1'b1;
        #100    reg_rw[ 6 * 32 + 1] = 1'b0;
        #500    reg_rw[ 6 * 32 + 2] = 1'b1;
        #100    reg_rw[ 6 * 32 + 2] = 1'b0;
        #500    reg_rw[ 6 * 32 + 3] = 1'b1;
        #100    reg_rw[ 6 * 32 + 3] = 1'b0;
        #500    reg_rw[ 6 * 32 + 4] = 1'b1;
        #100    reg_rw[ 6 * 32 + 4] = 1'b0;
        #500    reg_rw[ 6 * 32 + 5] = 1'b1;
        #100    reg_rw[ 6 * 32 + 5] = 1'b0;
        #500    reg_rw[ 6 * 32 + 6] = 1'b1;
        #100    reg_rw[ 6 * 32 + 6] = 1'b0;
        #500    reg_rw[ 6 * 32 + 7] = 1'b1;
        #100    reg_rw[ 6 * 32 + 7] = 1'b0;
        #500    reg_rw[ 6 * 32 + 8] = 1'b1;
        #100    reg_rw[ 6 * 32 + 8] = 1'b0;
        #500    reg_rw[ 6 * 32 + 9] = 1'b1;
        #100    reg_rw[ 6 * 32 + 9] = 1'b0;
        #500    reg_rw[ 6 * 32 + 10] = 1'b1;
        #100    reg_rw[ 6 * 32 + 10] = 1'b0;
        #500    reg_rw[ 6 * 32 + 11] = 1'b1;
        #100    reg_rw[ 6 * 32 + 11] = 1'b0;
        #500    reg_rw[ 6 * 32 + 12] = 1'b1;
        #100    reg_rw[ 6 * 32 + 12] = 1'b0;
        #500    reg_rw[ 6 * 32 + 13] = 1'b1;
        #100    reg_rw[ 6 * 32 + 13] = 1'b0;
        #500    reg_rw[ 6 * 32 + 14] = 1'b1;
        #100    reg_rw[ 6 * 32 + 14] = 1'b0;
        #500    reg_rw[ 6 * 32 + 15] = 1'b1;
        #100    reg_rw[ 6 * 32 + 15] = 1'b0;
        
        #500    reg_rw[ 5 * 32 + 0] = 1'b0; // TRIGGER off
        #0      opad_deltaT = 1'b0;
        
        // Test window sampling
        #0      reg_rw[ 7 * 32 + 31 :  7 * 32 +  0] = 32'h00000064; // window width, 100 counts = 2us
        #0      reg_rw[ 8 * 32 +  15 : 8 * 32 +   0] = 16'h00fa; // reset width, 250 counts, 5us
        #0      reg_rw[ 8 * 32 +  31 : 8 * 32 +  16] = 16'h0005; // reset cal gap, 5 counts, 100ns
        #0      reg_rw[ 9 * 32 + 15 :  9 * 32 +  0] = 16'h0064; // window wait, 100 counts = 2us
        #0      reg_rw[ 9 * 32 + 31] = 1'b1; // select window_sample_valid
        #500    reg_rw[ 0 * 32 + 15] = 1'b1; // trigger a reset and TRIGGER
        #7000   oLVDS[0] = 1'b1; // Events
        #10     oLVDS[0] = 1'b0;
        #500    oLVDS[0] = 1'b1;
        #10     oLVDS[0] = 1'b0;
        #500    oLVDS[0] = 1'b1;
        #10     oLVDS[0] = 1'b0;
        #500    reg_rw[ 6 * 32 + 0] = 1'b1; // Read FIFO0 four times
        #100    reg_rw[ 6 * 32 + 0] = 1'b0; // 4th read should not issue
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        #500    reg_rw[ 6 * 32 + 0] = 1'b1;
        #100    reg_rw[ 6 * 32 + 0] = 1'b0;
        #0      reg_rw[ 0 * 32 + 15] = 1'b0;
        
        // Kickstart beta-multipliers
        #200    reg_rw[ 0 * 32 + 24] = 1'b1; // opad_startup
        #200    reg_rw[ 0 * 32 + 25] = 1'b1; // opad_startup2
        
        // Test 32-bit register load
        // Reset interfaces 1 and 2
        #200    reg_rw[ 1 * 32 + 9] = 1'b1; // selDefData (not timed)
        #200    reg_rw[ 1 * 32 + 8] = 1'b1; // loadData sends 100us pulse
        #200    reg_rw[ 1 * 32 + 8] = 1'b0; // loadData de-assert
        #200    reg_rw[ 1 * 32 + 9] = 1'b0; // selDefData de-assert, make 200000 if real-time
        
        // Serial interface 1
        #200    reg_rw[ 2 * 32 + 31 : 2 * 32 +  0] = 32'h12345678; // data in our register
        
        #200    reg_rw[ 1 * 32 + 1] = 1'b1; // load data into SR
        #200    reg_rw[ 1 * 32 + 1] = 1'b0; // must load SR de-assert before xmit, make 200000 if real-time
        
        #200    reg_rw[ 1 * 32 + 2] = 1'b1; // shift out with gated clock, takes a long time!
        #600    reg_rw[ 1 * 32 + 8] = 1'b1; // QPix loadData one-shot, make 6000 if real-time
        
        #200    reg_rw[ 1 * 32 + 8] = 1'b1; // loadData de-assert
        #200    reg_rw[ 1 * 32 + 2] = 1'b0; // shift out de-assert
        
        // Serial interface 2
        #200    reg_rw[ 4 * 32 + 31 : 4 * 32 +  0] = 32'ha0a0a0af; // data in our register
        
        #200    reg_rw[ 3 * 32 + 1] = 1'b1; // load data into SR
        #200    reg_rw[ 3 * 32 + 1] = 1'b0; // must load SR de-assert before xmit, make 200000 if real-time
        
        #200    reg_rw[ 3 * 32 + 2] = 1'b1; // shift out with gated clock, takes a long time!
        #600    reg_rw[ 3 * 32 + 8] = 1'b1; // QPix loadData one-shot, make 6000 if real-time
        
        #200    reg_rw[ 3 * 32 + 8] = 1'b1; // loadData de-assert
        #200    reg_rw[ 3 * 32 + 2] = 1'b0; // shift out de-assert
        
        // External resets (pulses)
        #4000   reg_rw[ 0 * 32 + 2] = 1'b1; // RST_EXT
        #200    reg_rw[ 0 * 32 + 2] = 1'b0; // RST_EXT
        #200    reg_rw[ 0 * 32 + 3] = 1'b1; // RST_EXT2
        #200    reg_rw[ 0 * 32 + 3] = 1'b0; // RST_EXT2
        
        // External resets (manual reg write)
        #200    reg_rw[ 0 * 32 + 5] = 1'b1; // RST_EXT
        #200    reg_rw[ 0 * 32 + 5] = 1'b0; 
        #200    reg_rw[ 0 * 32 + 6] = 1'b1; // RST_EXT2
        #200    reg_rw[ 0 * 32 + 6] = 1'b0;
        
        // Calibrate
        #1000   reg_rw[ 0 * 32 + 4] = 1'b1;
        #6000   reg_rw[ 0 * 32 + 4] = 1'b0;
        
        // Reset and trigger
        #1000   reg_rw[ 0 * 32 + 7] = 1'b1;
        #6000   reg_rw[ 0 * 32 + 7] = 1'b0;
        
        // Readback routine
        #200    reg_rw[ 1 * 32 + 5] = 1'b1; // pulse CLKin2
        #200    reg_rw[ 1 * 32 + 5] = 1'b0;
        #200    reg_rw[ 1 * 32 + 4] = 1'b1; // serialOutCnt
        #600    reg_rw[ 1 * 32 + 6] = 1'b1; // 32 pulse CLKin2
        #200    reg_rw[ 1 * 32 + 6] = 1'b0;
        #4000   reg_rw[ 1 * 32 + 4] = 1'b0; 
        #200    reg_rw[ 3 * 32 + 5] = 1'b1; // pulse CLKin2
        #200    reg_rw[ 3 * 32 + 5] = 1'b0;
        #200    reg_rw[ 3 * 32 + 4] = 1'b1; // serialOutCnt2
        #600    reg_rw[ 3 * 32 + 6] = 1'b1; // 32 pulse CLKin2
        #200    reg_rw[ 3 * 32 + 6] = 1'b0;
        #4000   reg_rw[ 3 * 32 + 4] = 1'b0;
 
        // Pulse control pads
        #2000   reg_rw[ 0 * 32 + 12] = 1'b1; // pulse opad_control
        #200    reg_rw[ 0 * 32 + 12] = 1'b0; 
        #200    reg_rw[ 0 * 32 + 13] = 1'b1; // pulse opad2_control
        #200    reg_rw[ 0 * 32 + 13] = 1'b0; 
        
        // Start replenishment clocks
        #200    reg_rw[ 0 * 32 + 16] = 1'b1; // opad_CLK
        #200    reg_rw[ 0 * 32 + 17] = 1'b1; // opad2_CLK
        
    end
endmodule
