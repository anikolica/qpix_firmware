`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/09/2021 11:58:51 AM
// Design Name: 
// Module Name: top_rtl
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


module top_rtl(

    // clock and trigger pins
    input  clk,
    input  clk200,
    input  OSC_200MHz,
    output TRIGGER,
    
    // QPix pins
    output opad_Ext_POR,
    output opad_CLKin,
    output opad_CLKin2,
    output opad_DataIn,
    output opad_control,
    output opad_loadData,
    output opad_selDefData,
    output opad_serialOutCnt,
    output opad_startup,
    output opad_cal_control,
    input  opad_DataOut1,
    input  opad_DataOut2,
    output opad2_cal_control,
    output opad2_RST_EXT,
    output opad_RST_EXT,
    input  opad_deltaT,
    input  opad2_deltaT,
    input  [15:0] oLVDS,
    output opad2_loadData,
    output opad2_selDefData,
    output opad2_serialOutCnt,
    output opad2_startup,
    output opad2_CLKin,
    output opad2_CLKin2,
    output opad2_DataIn,
    output opad2_control,
    input  opad2_DataOut1,
    input  opad2_DataOut2,
    output opad_CLK,
    output opad2_CLK,
    //output oTP1,
    //output oTP2,
    output oTP3,
    output oTP4,
    
    // register interface
    output [64*32-1:0] reg_ro,
    input  [64*32-1:0] reg_rw
    );
    
    /*
    // TEST CODE
    // At the console: poke 0x43c00000 [value]
    // where [value] forces a 1MHz clock on the output pins as follows:
    reg test_reg; 
    always @(posedge OSC_200MHz) begin
        test_reg <= opad_DataOut1;
    end
    wire [5:0] test_mux_sel;
    wire [3:0] unconnected;
    assign test_mux_sel = reg_rw[0 * 32 + 5 : 0 * 32 + 0];
    demux1to32 test_mux (
        .Data_in(clk),
        .sel(test_mux_sel),
        .Data_out( {unconnected,
                    TRIGGER,        // [value] = 28 ...
                    opad_Ext_POR,   // ... 27 ...
                    opad_CLKin,
                    opad_CLKin2,
                    opad_DataIn,
                    opad_control,
                    opad_loadData,
                    opad_selDefData,
                    opad_serialOutCnt,
                    opad_startup,
                    opad_cal_control,
                    opad2_cal_control,
                    opad2_RST_EXT,
                    opad_RST_EXT,
                    opad2_loadData,
                    opad2_selDefData,
                    opad2_serialOutCnt,
                    opad2_startup,
                    opad2_CLKin,
                    opad2_CLKin2,
                    opad2_DataIn,
                    opad2_control,
                    opad_CLK,
                    opad2_CLK,
                    oTP1,
                    oTP2,
                    oTP3,           // ... 2 ...
                    oTP4})          // ... 1 ...
                                    // ... 0 = no output
    ); */
     
    // *** DECLARATIONS ***
    wire sys_rst; // Reset all logic
    
    // 16 data input channel interface signals
    wire counter_reset;
    reg  [63:0] counter64 = 64'h0;
    reg  [63:0] trig_ts = 64'h0;
    reg  [63:0] reg_ts = 64'h0;
    reg  [63:0] fifo_data_in_0, fifo_data_in_1, fifo_data_in_2, fifo_data_in_3,
                fifo_data_in_4, fifo_data_in_5, fifo_data_in_6, fifo_data_in_7,
                fifo_data_in_8, fifo_data_in_9, fifo_data_in_10, fifo_data_in_11,
                fifo_data_in_12, fifo_data_in_13, fifo_data_in_14, fifo_data_in_15 = 64'h0;
    wire [63:0] fifo_dout_0, fifo_dout_1, fifo_dout_2, fifo_dout_3,
                fifo_dout_4, fifo_dout_5, fifo_dout_6, fifo_dout_7,
                fifo_dout_8, fifo_dout_9, fifo_dout_10, fifo_dout_11,
                fifo_dout_12, fifo_dout_13, fifo_dout_14, fifo_dout_15;
    wire [15:0] fifo_read; // register bit
    wire [15:0] fifo_rd_en;
    wire [15:0] fifo_empty;
    wire [15:0] fifo_almost_empty;
    wire [15:0] fifo_rd_rst_busy;
    wire [15:0] fifo_wr_en;
    wire [15:0] fifo_full;
    wire [15:0] fifo_almost_full;
    wire [15:0] fifo_wr_rst_busy;
    reg  [15:0] fifo_event = 16'h00;
    reg  [15:0] fifo_reqread = 16'h00;
    
    // Serial interface
    wire clk20k; // base slow clock for Qpix register interface
    wire clk_shift;
    wire clk_pulse;
    wire clk_intrst;
    wire rst1;
    wire rst2;
    wire load_ser1;
    wire load_ser2;
    wire xmit_ser1;
    wire xmit_ser2;
    wire shift_out1;
    wire shift_out2;
    wire loadData1;
    wire loadData2;
    wire [31:0] data1;
    wire [31:0] data2;
    wire pulse_opad_CLKin2;
    wire pulse_opad2_CLKin2;
    wire read_data;
    wire read_data2;
    
    // Calibration
    wire cal_control_reg, cal_control_reg2;
    
    // Window sampling
    wire [15:0] window_wait;
    wire [32:0] window_width;
    
    // Programmable reset
    wire [15:0] reset_width, rst_cal_gap;
    
    // Special pads
    wire pulse_rst_ext; // external reset
    wire pulse_rst_ext2;
    wire pulse_control;
    wire pulse2_control;
    wire clk_repl_en; // replenishment clocks
    wire clk2_repl_en;
    
    // *** CLOCK BUFFERS ***
    BUFG bufg1 (.O(      ), .I(OSC_200MHz)); // not used 6/12/23
    ODDR repl_clk (
        .Q(opad_CLK), // Replenishment clock
        .C(clk), // 50MHz
        .CE(clk_repl_en),
        .D1(1'b1),
        .D2(1'b0),
        .S(1'b0),
        .R(1'b0)
    );
    ODDR repl_clk2 (
        .Q(opad2_CLK), 
        .C(clk), 
        .CE(clk2_repl_en),
        .D1(1'b1),
        .D2(1'b0),
        .S(1'b0),
        .R(1'b0)
    );
    assign fifo_rd_clock = clk;
    assign fifo_wr_clock = clk200;
    
    // *** REGISTER MAP ***
    // ** R/W registers **
    // Reg 0 -- control register
    assign sys_rst =            reg_rw[ 0 * 32 +  0];
    assign opad_Ext_POR =       reg_rw[ 0 * 32 +  1];
    assign pulse_rst_ext =      reg_rw[ 0 * 32 +  2];
    assign pulse_rst_ext2 =     reg_rw[ 0 * 32 +  3];
    assign calibrate =          reg_rw[ 0 * 32 +  4];
    assign rst_ext_reg =        reg_rw[ 0 * 32 +  5];
    assign rst_ext2_reg =       reg_rw[ 0 * 32 +  6];
    assign rst_and_trig =       reg_rw[ 0 * 32 +  7];
    assign opad_control_reg =   reg_rw[ 0 * 32 +  8];
    assign opad2_control_reg =  reg_rw[ 0 * 32 +  9];
    assign cal_control_reg =    reg_rw[ 0 * 32 + 10];
    assign cal_control_reg2 =   reg_rw[ 0 * 32 + 11];
    assign pulse_control =      reg_rw[ 0 * 32 + 12];
    assign pulse2_control =     reg_rw[ 0 * 32 + 13];
    assign arb_trig =           reg_rw[ 0 * 32 + 14];
    assign window_trig =        reg_rw[ 0 * 32 + 15];
    assign clk_repl_en =        reg_rw[ 0 * 32 + 16];
    assign clk2_repl_en =       reg_rw[ 0 * 32 + 17];
    assign opad_startup =       reg_rw[ 0 * 32 + 24];
    assign opad2_startup =      reg_rw[ 0 * 32 + 25];
    
    // Reg 1 - data1 control
    assign rst1         =       reg_rw[ 1 * 32 +  0];
    assign load_ser1    =       reg_rw[ 1 * 32 +  1];
    assign xmit_ser1    =       reg_rw[ 1 * 32 +  2];
    assign opad_serialOutCnt =  reg_rw[ 1 * 32 +  4];
    assign pulse_opad_CLKin2 =  reg_rw[ 1 * 32 +  5];
    assign read_data =          reg_rw[ 1 * 32 +  6];
    assign loadData1    =       reg_rw[ 1 * 32 +  8]; 
    assign opad_selDefData =    reg_rw[ 1 * 32 +  9];
    
    // Reg 2 - data2
    assign data1        =       reg_rw[ 2 * 32 + 31 : 2 * 32 +  0];
     
    // Reg 3 - data2 control
    assign rst2         =       reg_rw[ 3 * 32 +  0];
    assign load_ser2    =       reg_rw[ 3 * 32 +  1];
    assign xmit_ser2    =       reg_rw[ 3 * 32 +  2];
    assign opad2_serialOutCnt = reg_rw[ 3 * 32 +  4];
    assign pulse_opad2_CLKin2 = reg_rw[ 3 * 32 +  5];
    assign read_data2 =         reg_rw[ 3 * 32 +  6];
    assign loadData2     =      reg_rw[ 3 * 32 +  8]; 
    assign opad2_selDefData =   reg_rw[ 3 * 32 +  9];
    
    // Reg 4 - data2
    assign data2        =       reg_rw[ 4 * 32 + 31 : 4 * 32 +  0];
    
    // Reg 5 - trigger control
    assign TRIGGER_pad =        reg_rw[ 5 * 32 +  0];
    assign counter_reset =      reg_rw[ 5 * 32 +  1];
    
    // Reg 6 - FIFO control
    assign fifo_read =          reg_rw[ 6 * 32 +  15 : 6 * 32 +  0];
    
    // Reg 7  - Programmable sampling control #1
    assign window_width =       reg_rw[ 7 * 32 +  31 : 7 * 32 +   0];
   
    // Reg 8 - Programmable reset control
    assign reset_width =        reg_rw[ 8 * 32 +  15 : 8 * 32 +   0];
    assign rst_cal_gap =        reg_rw[ 8 * 32 +  31 : 8 * 32 +  16];
    
    // Reg 9 - Programmable sampling control #2
    assign window_wait =        reg_rw[ 9 * 32 +  16 : 9 * 32 +   0];
    
    // Reg 10 thru 31 not connected
    
    // ** R/O registers **
    // Reg 64,65 - trigger timestamp
    assign reg_ro[ 0 * 32 + 31 :  0 * 32 +  0] = trig_ts[63:32];
    assign reg_ro[ 1 * 32 + 31 :  1 * 32 +  0] = trig_ts[31: 0];
    
    // Reg 66,67 - current FIFO 0 word (timestamp)
    assign reg_ro[ 2 * 32 + 31 :  2 * 32 +  0] = fifo_dout_0[63:32];
    assign reg_ro[ 3 * 32 + 31 :  3 * 32 +  0] = fifo_dout_0[31: 0];
    
    // Reg 68,69 - current FIFO 1 word (timestamp)
    assign reg_ro[ 4 * 32 + 31 :  4 * 32 +  0] = fifo_dout_1[63:32];
    assign reg_ro[ 5 * 32 + 31 :  5 * 32 +  0] = fifo_dout_1[31: 0];
    
    // Reg 70,71 - current FIFO 2 word (timestamp)
    assign reg_ro[ 6 * 32 + 31 :  6 * 32 +  0] = fifo_dout_2[63:32];
    assign reg_ro[ 7 * 32 + 31 :  7 * 32 +  0] = fifo_dout_2[31: 0];
    
    // Reg 72,73 - current FIFO 3 word (timestamp)
    assign reg_ro[ 8 * 32 + 31 :  8 * 32 +  0] = fifo_dout_3[63:32];
    assign reg_ro[ 9 * 32 + 31 :  9 * 32 +  0] = fifo_dout_3[31: 0];
    
    // Reg 74,75 - current FIFO 4 word (timestamp)
    assign reg_ro[10 * 32 + 31 : 10 * 32 +  0] = fifo_dout_4[63:32];
    assign reg_ro[11 * 32 + 31 : 11 * 32 +  0] = fifo_dout_4[31: 0];
    
    // Reg 76,77 - current FIFO 5 word (timestamp)
    assign reg_ro[12 * 32 + 31 : 12 * 32 +  0] = fifo_dout_5[63:32];
    assign reg_ro[13 * 32 + 31 : 13 * 32 +  0] = fifo_dout_5[31: 0];
    
    // Reg 78,79 - current FIFO 6 word (timestamp)
    assign reg_ro[14 * 32 + 31 : 14 * 32 +  0] = fifo_dout_6[63:32];
    assign reg_ro[15 * 32 + 31 : 15 * 32 +  0] = fifo_dout_6[31: 0];
    
    // Reg 80,81 - current FIFO 7 word (timestamp)
    assign reg_ro[16 * 32 + 31 : 16 * 32 +  0] = fifo_dout_7[63:32];
    assign reg_ro[17 * 32 + 31 : 17 * 32 +  0] = fifo_dout_7[31: 0];
    
    // Reg 82,84 - current FIFO 8 word (timestamp)
    assign reg_ro[18 * 32 + 31 : 18 * 32 +  0] = fifo_dout_8[63:32];
    assign reg_ro[19 * 32 + 31 : 19 * 32 +  0] = fifo_dout_8[31: 0];
    
    // Reg 84,85 - current FIFO 9 word (timestamp)
    assign reg_ro[20 * 32 + 31 : 20 * 32 +  0] = fifo_dout_9[63:32];
    assign reg_ro[21 * 32 + 31 : 21 * 32 +  0] = fifo_dout_9[31: 0];
    
    // Reg 86,87 - current FIFO 10 word (timestamp)
    assign reg_ro[22 * 32 + 31 : 22 * 32 +  0] = fifo_dout_10[63:32];
    assign reg_ro[23 * 32 + 31 : 23 * 32 +  0] = fifo_dout_10[31: 0];
    
    // Reg 88,89 - current FIFO 11 word (timestamp)
    assign reg_ro[24 * 32 + 31 : 24 * 32 +  0] = fifo_dout_11[63:32];
    assign reg_ro[25 * 32 + 31 : 25 * 32 +  0] = fifo_dout_11[31: 0];
    
    // Reg 90,91 - current FIFO 12 word (timestamp)
    assign reg_ro[26 * 32 + 31 : 26 * 32 +  0] = fifo_dout_12[63:32];
    assign reg_ro[27 * 32 + 31 : 27 * 32 +  0] = fifo_dout_12[31: 0];
    
    // Reg 92,93 - current FIFO 13 word (timestamp)
    assign reg_ro[28 * 32 + 31 : 28 * 32 +  0] = fifo_dout_13[63:32];
    assign reg_ro[29 * 32 + 31 : 29 * 32 +  0] = fifo_dout_13[31: 0];
    
    // Reg 94,95 - current FIFO 14 word (timestamp)
    assign reg_ro[30 * 32 + 31 : 30 * 32 +  0] = fifo_dout_14[63:32];
    assign reg_ro[31 * 32 + 31 : 31 * 32 +  0] = fifo_dout_14[31: 0];
    
    // Reg 96,97 - current FIFO 15 word (timestamp)
    assign reg_ro[32 * 32 + 31 : 32 * 32 +  0] = fifo_dout_15[63:32];
    assign reg_ro[33 * 32 + 31 : 33 * 32 +  0] = fifo_dout_15[31: 0];
    
    // Reg 98 - 108 not connected
    
    // Reg 109 - FIFO 0 status
    assign reg_ro[45 * 32 +  0] = fifo_empty[0];
    assign reg_ro[45 * 32 +  1] = fifo_almost_empty[0];

    assign reg_ro[45 * 32 +  2] = fifo_rd_rst_busy[0];
    //assign reg_ro[45 * 32 +  4] = fifo_full[0];
    //assign reg_ro[45 * 32 +  5] = fifo_almost_full[0];
    //assign reg_ro[45 * 32 +  6] = fifo_wr_rst_busy[0];
    
    // Reg 110 - FIFO 1 status
    assign reg_ro[46 * 32 +  0] = fifo_empty[1];
    assign reg_ro[46 * 32 +  1] = fifo_almost_empty[1];
    assign reg_ro[46 * 32 +  2] = fifo_rd_rst_busy[1];
    //assign reg_ro[46 * 32 +  4] = fifo_full[1];
    //assign reg_ro[46 * 32 +  5] = fifo_almost_full[1];
    //assign reg_ro[46 * 32 +  6] = fifo_wr_rst_busy[1];
    
    // Reg 111 - FIFO 2 status
    assign reg_ro[47 * 32 +  0] = fifo_empty[2];
    assign reg_ro[47 * 32 +  1] = fifo_almost_empty[2];
    assign reg_ro[47 * 32 +  2] = fifo_rd_rst_busy[2];
    //assign reg_ro[47 * 32 +  4] = fifo_full[2];
    //assign reg_ro[47 * 32 +  5] = fifo_almost_full[2];
    //assign reg_ro[47 * 32 +  6] = fifo_wr_rst_busy[2];
    
    // Reg 112 - FIFO 3 status
    assign reg_ro[48 * 32 +  0] = fifo_empty[3];
    assign reg_ro[48 * 32 +  1] = fifo_almost_empty[3];
    assign reg_ro[48 * 32 +  2] = fifo_rd_rst_busy[3];
    //assign reg_ro[48 * 32 +  4] = fifo_full[3];
    //assign reg_ro[48 * 32 +  5] = fifo_almost_full[3];
    //assign reg_ro[48 * 32 +  6] = fifo_wr_rst_busy[3];
    
    // Reg 113 - FIFO 4 status
    assign reg_ro[49 * 32 +  0] = fifo_empty[4];
    assign reg_ro[49 * 32 +  1] = fifo_almost_empty[4];
    assign reg_ro[49 * 32 +  2] = fifo_rd_rst_busy[4];
    //assign reg_ro[49 * 32 +  4] = fifo_full[4];
    //assign reg_ro[49 * 32 +  5] = fifo_almost_full[4];
    //assign reg_ro[49 * 32 +  6] = fifo_wr_rst_busy[4];
    
    // Reg 114 - FIFO 5 status
    assign reg_ro[50 * 32 +  0] = fifo_empty[5];
    assign reg_ro[50 * 32 +  1] = fifo_almost_empty[5];
    assign reg_ro[50 * 32 +  2] = fifo_rd_rst_busy[5];
    //assign reg_ro[50 * 32 +  4] = fifo_full[5];
    //assign reg_ro[50 * 32 +  5] = fifo_almost_full[5];
    //assign reg_ro[50 * 32 +  6] = fifo_wr_rst_busy[5];
    
    // Reg 115 - FIFO 6 status
    assign reg_ro[51 * 32 +  0] = fifo_empty[6];
    assign reg_ro[51 * 32 +  1] = fifo_almost_empty[6];
    assign reg_ro[51 * 32 +  2] = fifo_rd_rst_busy[6];
    //assign reg_ro[51 * 32 +  4] = fifo_full[6];
    //assign reg_ro[51 * 32 +  5] = fifo_almost_full[6];
    //assign reg_ro[51 * 32 +  6] = fifo_wr_rst_busy[6];
    
    // Reg 116 - FIFO 7 status
    assign reg_ro[52 * 32 +  0] = fifo_empty[7];
    assign reg_ro[52 * 32 +  1] = fifo_almost_empty[7];
    assign reg_ro[52 * 32 +  2] = fifo_rd_rst_busy[7];
    //assign reg_ro[52 * 32 +  4] = fifo_full[7];
    //assign reg_ro[52 * 32 +  5] = fifo_almost_full[7];
    //assign reg_ro[52 * 32 +  6] = fifo_wr_rst_busy[7];
    
    // Reg 117 - FIFO 8 status
    assign reg_ro[53 * 32 +  0] = fifo_empty[8];
    assign reg_ro[53 * 32 +  1] = fifo_almost_empty[8];
    assign reg_ro[53 * 32 +  2] = fifo_rd_rst_busy[8];
    //assign reg_ro[53 * 32 +  4] = fifo_full[8];
    //assign reg_ro[53 * 32 +  5] = fifo_almost_full[8];
    //assign reg_ro[53 * 32 +  6] = fifo_wr_rst_busy[8];
    
    // Reg 118 - FIFO 9 status
    assign reg_ro[54 * 32 +  0] = fifo_empty[9];
    assign reg_ro[54 * 32 +  1] = fifo_almost_empty[9];
    assign reg_ro[54 * 32 +  2] = fifo_rd_rst_busy[9];
    //assign reg_ro[54 * 32 +  4] = fifo_full[9];
    //assign reg_ro[54 * 32 +  5] = fifo_almost_full[9];
    //assign reg_ro[54 * 32 +  6] = fifo_wr_rst_busy[9];
    
    // Reg 119 - FIFO 10 status
    assign reg_ro[55 * 32 +  0] = fifo_empty[10];
    assign reg_ro[55 * 32 +  1] = fifo_almost_empty[10];
    assign reg_ro[55 * 32 +  2] = fifo_rd_rst_busy[10];
    //assign reg_ro[55 * 32 +  4] = fifo_full[10];
    //assign reg_ro[55 * 32 +  5] = fifo_almost_full[10];
    //assign reg_ro[55 * 32 +  6] = fifo_wr_rst_busy[10];
    
    // Reg 120 - FIFO 11 status
    assign reg_ro[56 * 32 +  0] = fifo_empty[11];
    assign reg_ro[56 * 32 +  1] = fifo_almost_empty[11];
    assign reg_ro[56 * 32 +  2] = fifo_rd_rst_busy[11];
    //assign reg_ro[56 * 32 +  4] = fifo_full[1];
    //assign reg_ro[56 * 32 +  5] = fifo_almost_full[11];
    //assign reg_ro[56 * 32 +  6] = fifo_wr_rst_busy[11];
    
    // Reg 121 - FIFO 12 status
    assign reg_ro[57 * 32 +  0] = fifo_empty[12];
    assign reg_ro[57 * 32 +  1] = fifo_almost_empty[12];
    assign reg_ro[57 * 32 +  2] = fifo_rd_rst_busy[12];
    //assign reg_ro[57 * 32 +  4] = fifo_full[12];
    //assign reg_ro[57 * 32 +  5] = fifo_almost_full[12];
    //assign reg_ro[57 * 32 +  6] = fifo_wr_rst_busy[12];
    
    // Reg 122 - FIFO 13 status
    assign reg_ro[58 * 32 +  0] = fifo_empty[13];
    assign reg_ro[58 * 32 +  1] = fifo_almost_empty[13];
    assign reg_ro[58 * 32 +  2] = fifo_rd_rst_busy[13];
    //assign reg_ro[58 * 32 +  4] = fifo_full[13];
    //assign reg_ro[58 * 32 +  5] = fifo_almost_full[13];
    //assign reg_ro[58 * 32 +  6] = fifo_wr_rst_busy[13];
    
    // Reg 123 - FIFO 14 status
    assign reg_ro[59 * 32 +  0] = fifo_empty[14];
    assign reg_ro[59 * 32 +  1] = fifo_almost_empty[14];
    assign reg_ro[59 * 32 +  2] = fifo_rd_rst_busy[14];
    //assign reg_ro[59 * 32 +  4] = fifo_full[14];
    //assign reg_ro[59 * 32 +  5] = fifo_almost_full[14];
    //assign reg_ro[59 * 32 +  6] = fifo_wr_rst_busy[14];
    
    // Reg 124 - FIFO 15 status
    assign reg_ro[60 * 32 +  0] = fifo_empty[15];
    assign reg_ro[60 * 32 +  1] = fifo_almost_empty[15];
    assign reg_ro[60 * 32 +  2] = fifo_rd_rst_busy[15];
    //assign reg_ro[60 * 32 +  4] = fifo_full[15];
    //assign reg_ro[60 * 32 +  5] = fifo_almost_full[15];
    //assign reg_ro[60 * 32 +  6] = fifo_wr_rst_busy[15];
    
    // Reg 125, 126 counter test
    //assign reg_ro[61 * 32 + 31 : 61 * 32 +  0] = reg_ts[63:32];
    //assign reg_ro[62 * 32 + 31 : 62 * 32 +  0] = reg_ts[31: 0];
    
    // Reg 127 - test
    assign reg_ro[63 * 32 + 31 : 63 * 32 +  0] = 32'hdeadbeef;
    
    // *** MAIN CODE ***
    // NOTE: DAC programming via PS
    
    // ** QPix register interface **
    // clock dividers
    clock_div 
        `ifdef SIM
            #(.DIVISOR(2)) // for Vivado simulation only
        `else
            #(.DIVISOR(2500)) // 50M/2500 = 20k
        `endif
            slowclk (
       .clock_in(clk), 
       .clock_out(clk20k)
    );
    clock_div 
        `ifdef SIM
            #(.DIVISOR(2*64))
        `else
            #(.DIVISOR(2500*64)) // see SR below ...
        `endif
            shiftclk (
       .clock_in(clk), 
       .clock_out(clk_shift) // 64 clocks wide at 20kHz
    );
    clock_div 
        `ifdef SIM
            #(.DIVISOR(2*2))
        `else
            #(.DIVISOR(2500*2)) // see SR below ...
        `endif
            pulseclk (
       .clock_in(clk), 
       .clock_out(clk_pulse) // 100us pulse 
    );
    clock_div 
        `ifdef SIM
            #(.DIVISOR(2))
        `else
            #(.DIVISOR(250)) // see integrator reset below ...
        `endif
            resetclk (
       .clock_in(clk), 
       .clock_out(clk_intrst) // 5us pulse
    );
    
    // Synchronize 50MHz register bits into 20kHz slow domain
    reg xmit_ser1_synced, xmit_ser1_synced_0;
    reg xmit_ser2_synced, xmit_ser2_synced_0;
    reg read_data_synced, read_data_synced_0;
    reg read_data2_synced, read_data2_synced_0;
    reg load_ser1_synced, load_ser1_synced_0;
    reg load_ser2_synced, load_ser2_synced_0;
    reg rst1_synced, rst1_synced_0;
    reg rst2_synced, rst2_synced_0;
    reg [31:0] data1_synced_0, data1_synced;
    reg [31:0] data2_synced_0, data2_synced;
    always @ (posedge clk20k)
    begin
        xmit_ser1_synced_0 <= xmit_ser1;
        xmit_ser1_synced <= xmit_ser1_synced_0;
        xmit_ser2_synced_0 <= xmit_ser2;
        xmit_ser2_synced <= xmit_ser2_synced_0;
        read_data_synced_0 <= read_data;
        read_data_synced <= read_data_synced_0;
        read_data2_synced_0 <= read_data2;
        read_data2_synced <= read_data2_synced_0;
        load_ser1_synced_0 <= load_ser1;
        load_ser1_synced <= load_ser1_synced_0;
        load_ser2_synced_0 <= load_ser2;
        load_ser2_synced <= load_ser2_synced_0;
        rst1_synced_0 <= rst1;
        rst1_synced <= rst1_synced_0;
        rst2_synced_0 <= rst2;
        rst2_synced <= rst2_synced_0;
        data1_synced_0 <= data1;
        data1_synced <= data1_synced_0;
        data2_synced_0 <= data2;
        data2_synced <= data2_synced_0;
    end
    oneshot shift1 (
       .Clock(clk_shift), // 64x 20kHz clk = 32x 10kHz clk
       .Trigger(xmit_ser1_synced),
       .Pulse(shift_out1)
    );
    oneshot shift2 (
       .Clock(clk_shift),
       .Trigger(xmit_ser2_synced),
       .Pulse(shift_out2)
    );
    oneshot load_pulse1 (
       .Clock(clk_pulse),
       .Trigger(loadData1),
       .Pulse(opad_loadData) // 1/2x 20kHz = 100us pulse
    );
    oneshot load_pulse2 (
       .Clock(clk_pulse),
       .Trigger(loadData2),
       .Pulse(opad2_loadData)
    );
    
    wire pulse_control_out, pulse2_control_out;
    oneshot ctrl_pulse (
       .Clock(clk_intrst),
       .Trigger(pulse_control),
       .Pulse(pulse_control_out) // 5us pulse out
    );
    oneshot ctrl2_pulse (
       .Clock(clk_intrst),
       .Trigger(pulse2_control),
       .Pulse(pulse2_control_out)
    );
    
    assign opad_control = opad_control_reg | pulse_control_out;
    assign opad2_control = opad2_control_reg | pulse2_control_out;
      
    // Parallel-in-serial-out for loading input register
    // SR shifts out at 1/2 input clock = 10kHz
    // That's why gating pulse is 64x 20kHz clocks = 32x 10k
    piso serial_gen1 (
        .load(load_ser1_synced),
        .xmit(shift_out1),
        .clk(clk20k),
        .rst(rst1_synced || sys_rst),
        .data_in(data1_synced),
        .data_out(opad_DataIn),
        .clk_out(opad_CLKin)
    );
    piso serial_gen2 (
        .load(load_ser2_synced),
        .xmit(shift_out2),
        .clk(clk20k),
        .rst(rst2_synced || sys_rst),
        .data_in(data2_synced),
        .data_out(opad2_DataIn),
        .clk_out(opad2_CLKin)
    );
    
    // Serial-in-parallel-out for reading readout register
    // Make a 32-clock one-shot, load into SIPO->register
    //opad_DataOut1
    //opad_DataOut2
    //opad2_DataOut1
    //opad2_DataOut2
    wire opad_CLKin2_pulse_out, opad2_CLKin2_pulse_out;
    oneshot CLKin2_pulser (
       .Clock(clk_intrst),
       .Trigger(pulse_opad_CLKin2),
       .Pulse(opad_CLKin2_pulse_out) // 5us pulse out
    );
    oneshot CLKin2_pulser2 (
       .Clock(clk_intrst),
       .Trigger(pulse_opad2_CLKin2),
       .Pulse(opad2_CLKin2_pulse_out)
    );
    wire os_to_piso_clkin2, os_to_piso2_clkin2;
    wire opad_CLKin2_pulse32_out, opad2_CLKin2_pulse32_out;
    oneshot shift1_read (
       .Clock(clk_shift), // 64x 20kHz clk = 32x 10kHz clk
       .Trigger(read_data_synced),
       .Pulse(os_to_piso_clkin2)
    );
    oneshot shift2_read (
       .Clock(clk_shift), // 64x 20kHz clk = 32x 10kHz clk
       .Trigger(read_data2_synced),
       .Pulse(os_to_piso2_clkin2)
    );
    // PISO only used here for 32-pulse train
    piso serial_gen1_read (
        .load(),
        .xmit(os_to_piso_clkin2),
        .clk(clk20k),
        .rst(rst1_synced || sys_rst),
        .data_in(),
        .data_out(),
        .clk_out(opad_CLKin2_pulse32_out)
    );
    piso serial_gen2_read (
        .load(),
        .xmit(os_to_piso2_clkin2),
        .clk(clk20k),
        .rst(rst2_synced || sys_rst),
        .data_in(),
        .data_out(),
        .clk_out(opad2_CLKin2_pulse32_out)
    );
    
    assign opad_CLKin2 = opad_CLKin2_pulse_out | opad_CLKin2_pulse32_out; 
    assign opad2_CLKin2 = opad2_CLKin2_pulse_out | opad2_CLKin2_pulse32_out;
    
    // Count replenishments during deltaT toggle
    //opad_deltaT
    //opad2_deltaT
    
    // Calibration -- stop opad_RSTx 100ns after falling edge of cal_controlx
    reg calibrate_ext_rst = 0;
    reg calibrate_cal_control = 0;
    reg[31:0] counter50M = 32'h00000000;
    always @ (posedge clk)
    begin
     if (calibrate && counter50M == 0)
     begin
         calibrate_ext_rst <= 1; // rising edge at start of reg bit transition
         calibrate_cal_control <= 1;
     end
     if (counter50M >= reset_width) // in this case, we use the same reset_width 
                                    // for both RST_EXT amd cal_control
         calibrate_cal_control <= 0; // deassert only cal_control
     if (counter50M >= reset_width + rst_cal_gap)
         calibrate_ext_rst <= 0; // falling edge of rst_ext only, after gap time
     if (!calibrate)
     begin
         calibrate_ext_rst <= 0;
         calibrate_cal_control <= 0;
         counter50M <= 0; // reset
     end
     else
        counter50M <= counter50M + 1;
    end
    
    // Reset and trigger -- opad_RSTx for 5us, then TRIGGER for longish time
    reg rst_then_trig = 1'b0;
    reg trig_after_rst = 1'b0;
    reg[31:0] counter50M_2 = 32'h00000000;
    always @ (posedge clk)
    begin
     if (rst_and_trig && counter50M_2 == 0)
         rst_then_trig <= 1;
     if (counter50M_2 >= reset_width) // nominally 250 counts, or 5us
     begin
         rst_then_trig <= 0; // deassert opad_rst
         trig_after_rst <= 1; // assert TRIGGER (external ARB)
     end
     if (!rst_and_trig)
     begin
         rst_then_trig <= 0;
         trig_after_rst <= 0; // only de-assert trigger on reg bit clear 
         counter50M_2 <= 0; // reset
     end
     else
        counter50M_2 <= counter50M_2 + 1;
    end
    
    // For triggering arbitrary function generator
    reg rst_then_trig_arb = 1'b0;
    reg trig_after_rst_arb = 1'b0;
    reg[31:0] counter50M_3 = 32'h00000000;
    always @ (posedge clk)
    begin
     if (arb_trig && counter50M_3 == 0) // hold RST_EXT1,2 when this reg bit set
         rst_then_trig_arb <= 1;
     if (counter50M_3 >= reset_width) // nominally 250 counts, or 5us
         trig_after_rst_arb <= 1; // assert TRIGGER (external ARB)
     if (counter50M_3 >= (reset_width + 32'h000001f4)) // another 500 counts, or +10us
         rst_then_trig_arb <= 0; // de-assert resets after a safe time 
     if (!arb_trig)
     begin
         rst_then_trig_arb <= 0; // reset everybody
         trig_after_rst_arb <= 0; 
         counter50M_3 <= 0; 
     end
     else
        counter50M_3 <= counter50M_3 + 1;
    end    
    
    // Window trigger -- opad_RSTx for 5us, then TRIGGER, then sample for user-defined time
    reg sample_window_valid = 1'b0;
    reg rst_for_windowsample = 1'b0;
    reg trig_for_windowsample = 1'b0;
    reg[63:0] counter50M_4 = 64'h0000000000000000; // 64 bits to account for 32-bit window_width
    always @ (posedge clk)
    begin
     if (window_trig && counter50M_4 == 0)
     begin
         sample_window_valid <= 0;
         rst_for_windowsample <= 1;
         trig_for_windowsample <= 0;
     end
     if (counter50M_4 >= reset_width) // nominally 250 counts, or 5us
     begin
         rst_for_windowsample <= 0; // deassert opad_rst
         trig_for_windowsample <= 1; // assert TRIGGER (external ARB)
     end
     if (counter50M_4 >= (reset_width + window_wait)) // user-defined time from reg 9
         sample_window_valid <= 1; // start sample window to enable FIFO writes
     if (counter50M_4 >= (reset_width + window_wait + window_width)) // user-defined time from reg 7,9
        sample_window_valid <= 0; // stop sampling
     if (!window_trig) // reset everybody
     begin
         sample_window_valid <= 0;
         rst_for_windowsample <= 0;
         trig_for_windowsample <= 0; // only de-assert trigger on reg bit clear
         counter50M_4 <= 0;
     end
     else
        counter50M_4 <= counter50M_4 + 1;
    end
    
    // Generate reset pulses
    // Previously used one-shots, but changed to programmable width
    reg opad_pulse, opad2_pulse;
    reg[31:0] counter50M_5 = 32'h00000000;
    always @ (posedge clk)
    begin
     if (pulse_rst_ext && counter50M_5 == 0)
        opad_pulse <= 1;
     if (counter50M_5 >= reset_width) // nominally 250 counts, or 5us
        opad_pulse <= 0;
     if (!pulse_rst_ext)
        counter50M_5 <= 32'h00000000;
     else
        counter50M_5 <= counter50M_5 + 1;
    end
    reg[31:0] counter50M_6 = 32'h00000000;
    always @ (posedge clk)
    begin
     if (pulse_rst_ext2 && counter50M_6 == 0)
        opad2_pulse <= 1;
     if (counter50M_6 >= reset_width) // nominally 250 counts, or 5us
        opad2_pulse <= 0;
     if (!pulse_rst_ext2)
        counter50M_6 <= 32'h00000000;
     else
        counter50M_6 <= counter50M_6 + 1;
    end
    
    // Pads an be controlled manually by register, or from the calibrate bit
    assign opad_cal_control = cal_control_reg | calibrate_cal_control;
    assign opad2_cal_control = cal_control_reg2 | calibrate_cal_control;
    // Pads an be pulsed by reg bit, or from the calibrate bit
    assign opad_RST_EXT = opad_pulse | calibrate_ext_rst | rst_then_trig | rst_then_trig_arb | rst_ext_reg | rst_for_windowsample;
    assign opad2_RST_EXT = opad2_pulse | calibrate_ext_rst | rst_then_trig | rst_then_trig_arb | rst_ext2_reg | rst_for_windowsample;
    // pad can be set to a level, or long pulsed  by the reset-and-trigger routine
    assign TRIGGER = TRIGGER_pad | trig_after_rst | trig_after_rst_arb | trig_for_windowsample; 
    
    // One-shots for test pulses
    //oTP1
    //oTP2
    //oTP3
    //oTP4
    
    //always @ (posedge clk)
    //begin
    //    reg_ts_0 <= counter64;
    //end
    
    // Trigger and readout
    always @ (posedge clk200) 
    begin
        if (counter_reset)
            counter64 <= 64'h0;
        else
        begin
            counter64 <= counter64 + 1; // always count while powered up
            fifo_data_in_0 <= counter64; // FIFO data is always the current timestamp
            fifo_data_in_1 <= counter64;
            fifo_data_in_2 <= counter64;
            fifo_data_in_3 <= counter64;
            fifo_data_in_4 <= counter64;
            fifo_data_in_5 <= counter64;
            fifo_data_in_6 <= counter64;
            fifo_data_in_7 <= counter64;
            fifo_data_in_8 <= counter64;
            fifo_data_in_9 <= counter64;
            fifo_data_in_10 <= counter64;
            fifo_data_in_11 <= counter64;
            fifo_data_in_12 <= counter64;
            fifo_data_in_13 <= counter64;
            fifo_data_in_14 <= counter64;
            fifo_data_in_15 <= counter64;
        end
    end
    
    always @ (posedge TRIGGER_pad) // Always synchronous with 50MHz
    begin
        trig_ts <= counter64; // Store the time we sent external trigger
    end
    
    reg deltaT_synced_0;
    reg deltaT_synced;
    reg [15:0] oLVDS_synced;
    reg [15:0] oLVDS_synced_0;
    always @ (posedge clk200)
    begin
        deltaT_synced_0 <= opad_deltaT;
        deltaT_synced <= deltaT_synced_0;
        oLVDS_synced_0 <= oLVDS;
        oLVDS_synced <= oLVDS_synced_0; // double FF sync into 200MHz domain
    end
    
    genvar i; 
    generate
        for (i = 0; i < 16; i = i + 1)
        begin
            always @ (posedge clk200)
            // NOTE: (deltaT_synced | sample_window_valid) only works here because they are mutually exclusive
            // i.e. using the window sampling routine, deltaT is ignored, and using the normal sampling routine
            // does not generate the sample_window_valid signal.
            begin
                if (oLVDS_synced[i] && !fifo_full[i] && (deltaT_synced | sample_window_valid))
                   fifo_event[i] <= 1; // ... trigger a one-shot to write the timestamp
                else
                   fifo_event[i] <= 0;
            end
            oneshot fifo_write_os (
               .Clock(clk200),
               .Trigger(fifo_event[i]),
               .Pulse(fifo_wr_en[i]) // FIFO write timestamp
            );
            
            always @ (posedge clk)
            begin
                if (fifo_read[i] && !fifo_empty[i])
                   fifo_reqread[i] <= 1;
                else
                   fifo_reqread[i] <= 0;
            end 
            oneshot fifo_read_os (
                .Clock(clk),
                .Trigger(fifo_reqread[i]),
                .Pulse(fifo_rd_en[i])
            );
         end
     endgenerate
    
    In_channel_FIFO_v0 fifo_0 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_0),
      .wr_en(fifo_wr_en[0]),
      .wr_rst_busy(fifo_wr_rst_busy[0]),
      .full(fifo_full[0]),
      .almost_full(fifo_almost_full[0]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_0),
      .rd_en(fifo_rd_en[0]),
      .rd_rst_busy(fifo_rd_rst_busy[0]),
      .empty(fifo_empty[0]),
      .almost_empty(fifo_almost_empty[0]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_1 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_1),
      .wr_en(fifo_wr_en[1]),
      .wr_rst_busy(fifo_wr_rst_busy[1]),
      .full(fifo_full[1]),
      .almost_full(fifo_almost_full[1]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_1),
      .rd_en(fifo_rd_en[1]),
      .rd_rst_busy(fifo_rd_rst_busy[1]),
      .empty(fifo_empty[1]),
      .almost_empty(fifo_almost_empty[1]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_2 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_2),
      .wr_en(fifo_wr_en[2]),
      .wr_rst_busy(fifo_wr_rst_busy[2]),
      .full(fifo_full[2]),
      .almost_full(fifo_almost_full[2]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_2),
      .rd_en(fifo_rd_en[2]),
      .rd_rst_busy(fifo_rd_rst_busy[2]),
      .empty(fifo_empty[2]),
      .almost_empty(fifo_almost_empty[2]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_3 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_3),
      .wr_en(fifo_wr_en[3]),
      .wr_rst_busy(fifo_wr_rst_busy[3]),
      .full(fifo_full[3]),
      .almost_full(fifo_almost_full[3]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_3),
      .rd_en(fifo_rd_en[3]),
      .rd_rst_busy(fifo_rd_rst_busy[3]),
      .empty(fifo_empty[3]),
      .almost_empty(fifo_almost_empty[3]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_4 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_4),
      .wr_en(fifo_wr_en[4]),
      .wr_rst_busy(fifo_wr_rst_busy[4]),
      .full(fifo_full[4]),
      .almost_full(fifo_almost_full[4]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_4),
      .rd_en(fifo_rd_en[4]),
      .rd_rst_busy(fifo_rd_rst_busy[4]),
      .empty(fifo_empty[4]),
      .almost_empty(fifo_almost_empty[4]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_5 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_5),
      .wr_en(fifo_wr_en[5]),
      .wr_rst_busy(fifo_wr_rst_busy[5]),
      .full(fifo_full[5]),
      .almost_full(fifo_almost_full[5]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_5),
      .rd_en(fifo_rd_en[5]),
      .rd_rst_busy(fifo_rd_rst_busy[5]),
      .empty(fifo_empty[5]),
      .almost_empty(fifo_almost_empty[5]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_6 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_6),
      .wr_en(fifo_wr_en[6]),
      .wr_rst_busy(fifo_wr_rst_busy[6]),
      .full(fifo_full[6]),
      .almost_full(fifo_almost_full[6]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_6),
      .rd_en(fifo_rd_en[6]),
      .rd_rst_busy(fifo_rd_rst_busy[6]),
      .empty(fifo_empty[6]),
      .almost_empty(fifo_almost_empty[6]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_7 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_7),
      .wr_en(fifo_wr_en[7]),
      .wr_rst_busy(fifo_wr_rst_busy[7]),
      .full(fifo_full[7]),
      .almost_full(fifo_almost_full[7]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_7),
      .rd_en(fifo_rd_en[7]),
      .rd_rst_busy(fifo_rd_rst_busy[7]),
      .empty(fifo_empty[7]),
      .almost_empty(fifo_almost_empty[7]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_8 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_8),
      .wr_en(fifo_wr_en[8]),
      .wr_rst_busy(fifo_wr_rst_busy[8]),
      .full(fifo_full[8]),
      .almost_full(fifo_almost_full[8]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_8),
      .rd_en(fifo_rd_en[8]),
      .rd_rst_busy(fifo_rd_rst_busy[8]),
      .empty(fifo_empty[8]),
      .almost_empty(fifo_almost_empty[8]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_9 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_9),
      .wr_en(fifo_wr_en[9]),
      .wr_rst_busy(fifo_wr_rst_busy[9]),
      .full(fifo_full[9]),
      .almost_full(fifo_almost_full[9]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_9),
      .rd_en(fifo_rd_en[9]),
      .rd_rst_busy(fifo_rd_rst_busy[9]),
      .empty(fifo_empty[9]),
      .almost_empty(fifo_almost_empty[9]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_10 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_10),
      .wr_en(fifo_wr_en[10]),
      .wr_rst_busy(fifo_wr_rst_busy[10]),
      .full(fifo_full[10]),
      .almost_full(fifo_almost_full[10]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_10),
      .rd_en(fifo_rd_en[10]),
      .rd_rst_busy(fifo_rd_rst_busy[10]),
      .empty(fifo_empty[10]),
      .almost_empty(fifo_almost_empty[10]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_11 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_11),
      .wr_en(fifo_wr_en[11]),
      .wr_rst_busy(fifo_wr_rst_busy[11]),
      .full(fifo_full[11]),
      .almost_full(fifo_almost_full[11]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_11),
      .rd_en(fifo_rd_en[11]),
      .rd_rst_busy(fifo_rd_rst_busy[11]),
      .empty(fifo_empty[11]),
      .almost_empty(fifo_almost_empty[11]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_12 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_12),
      .wr_en(fifo_wr_en[12]),
      .wr_rst_busy(fifo_wr_rst_busy[12]),
      .full(fifo_full[12]),
      .almost_full(fifo_almost_full[12]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_12),
      .rd_en(fifo_rd_en[12]),
      .rd_rst_busy(fifo_rd_rst_busy[12]),
      .empty(fifo_empty[12]),
      .almost_empty(fifo_almost_empty[12]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_13 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_13),
      .wr_en(fifo_wr_en[13]),
      .wr_rst_busy(fifo_wr_rst_busy[13]),
      .full(fifo_full[13]),
      .almost_full(fifo_almost_full[13]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_13),
      .rd_en(fifo_rd_en[13]),
      .rd_rst_busy(fifo_rd_rst_busy[13]),
      .empty(fifo_empty[13]),
      .almost_empty(fifo_almost_empty[13]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_14 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_14),
      .wr_en(fifo_wr_en[14]),
      .wr_rst_busy(fifo_wr_rst_busy[14]),
      .full(fifo_full[14]),
      .almost_full(fifo_almost_full[14]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_14),
      .rd_en(fifo_rd_en[14]),
      .rd_rst_busy(fifo_rd_rst_busy[14]),
      .empty(fifo_empty[14]),
      .almost_empty(fifo_almost_empty[14]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    
    In_channel_FIFO_v0 fifo_15 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_data_in_15),
      .wr_en(fifo_wr_en[15]),
      .wr_rst_busy(fifo_wr_rst_busy[15]),
      .full(fifo_full[15]),
      .almost_full(fifo_almost_full[15]),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(4094),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_dout_15),
      .rd_en(fifo_rd_en[15]),
      .rd_rst_busy(fifo_rd_rst_busy[15]),
      .empty(fifo_empty[15]),
      .almost_empty(fifo_almost_empty[15]),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );
    

endmodule