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
    output oTP1,
    output oTP2,
    output oTP3,
    output oTP4,
    
    // register interface
    output [16*32-1:0] reg_ro,
    input  [16*32-1:0] reg_rw
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
    
    // buffer clocks
    BUFG bufg1 (.O(      ), .I(OSC_200MHz));
    OBUF obuf1 (.O(opad_CLK), .I(clk)); // 50MHz for 16 channels
    OBUF obuf2 (.O(opad2_CLK), .I(clk));
    assign fifo_rd_clock = clk;
    assign fifo_wr_clock = clk200;
    
    // *** DECLARATIONS ***
    wire    sys_rst;
    reg [63:0] counter64 = 64'h0;
    reg [63:0] trig_ts = 64'h0;
    reg [63:0] fifo_0_data_in = 64'h0;
    reg [63:0] reg_ts = 64'h0;
    wire fifo_0_read;
    wire [63:0] fifo_0_dout;
    wire fifo_0_wr_rst_busy;
    wire fifo_0_rd_rst_busy;
    wire fifo_0_full;
    wire fifo_0_almost_full;
    wire fifo_0_empty;
    wire fifo_0_almost_empty;
    wire fifo_0_wr_en;
    
    // *** REGISTER MAP ***
    // R/W registers ...
    // Reg 0 -- control register
    assign sys_rst =            reg_rw[ 0 * 32 +  0];
    assign opad_Ext_POR =       reg_rw[ 0 * 32 +  1];
    assign opad_RST_EXT =       reg_rw[ 0 * 32 +  2];
    assign opad2_RST_EXT =      reg_rw[ 0 * 32 +  3];
    assign opad_control =       reg_rw[ 0 * 32 +  8];
    assign opad2_control =      reg_rw[ 0 * 32 +  9];
    assign opad_cal_control =   reg_rw[ 0 * 32 + 16];
    assign opad2_cal_control =  reg_rw[ 0 * 32 + 17];
    assign opad_startup =       reg_rw[ 0 * 32 + 24];
    assign opad2_startup =      reg_rw[ 0 * 32 + 25];
    
    // Reg 1 - data1 control
    assign rst1         =       reg_rw[ 1 * 32 +  0];
    assign load_ser1    =       reg_rw[ 1 * 32 +  1];
    assign xmit_ser1    =       reg_rw[ 1 * 32 +  2];
    assign opad_loadData =      reg_rw[ 1 * 32 +  8]; 
    assign opad_selDefData =    reg_rw[ 1 * 32 +  9];
    
    // Reg 2 - data2
    assign data1        =       reg_rw[ 2 * 32 + 32 : 2 * 32 +  0];
     
    // Reg 3 - data2 control
    assign rst2         =       reg_rw[ 3 * 32 +  0];
    assign load_ser2    =       reg_rw[ 3 * 32 +  1];
    assign xmit_ser2    =       reg_rw[ 3 * 32 +  2];
    
    // Reg 4 - data2
    assign data2        =       reg_rw[4 * 32 + 32 : 4 * 32 +  0];
    
    // Reg 5 - trigger control
    assign TRIGGER =            reg_rw[ 5 * 32 +  0];
    assign counter_reset =      reg_rw[ 5 * 32 +  1];
    
    // Reg 6 - FIFO control
    assign fifo_0_read =        reg_rw[ 6 * 32 +  0];
    
    // R/O registers ...
    // Reg 16,17 - trigger timestamp
    assign reg_ro[ 0 * 32 + 31 :  0 * 32 +  0] = trig_ts[63:32];
    assign reg_ro[ 1 * 32 + 31 :  1 * 32 +  0] = trig_ts[31: 0];
    
    // Red 18,19 - current FIFO 0 word (timestamp)
    assign reg_ro[ 2 * 32 + 31 :  2 * 32 +  0] = fifo_0_dout[63:32];
    assign reg_ro[ 3 * 32 + 31 :  3 * 32 +  0] = fifo_0_dout[31: 0];
    
    // Reg 20 - FIFO 0 status
    //assign reg_ro[ 4 * 32 +  0] = fifo_0_wr_rst_busy;
    assign reg_ro[ 4 * 32 +  1] = fifo_0_rd_rst_busy;
    //assign reg_ro[ 4 * 32 +  2] = fifo_0_full;
    assign reg_ro[ 4 * 32 +  3] = fifo_0_empty;
    assign reg_ro[ 4 * 32 +  4] = fifo_0_almost_empty;
    
    // Reg 29/30 - counter test
    //assign reg_ro[13 * 32 + 31 : 13 * 32 +  0] = reg_ts[63:32];
    //assign reg_ro[14 * 32 + 31 : 14 * 32 +  0] = reg_ts[31: 0];
    
    // Reg 31 - test
    assign reg_ro[15 * 32 + 31 : 15 * 32 +  0] = 32'hdeadbeef;
    
    // ** MAIN CODE ***
    // NOTE: DAC programming via PS
    
    // Parallel-in-serial-out for loading input register
    // Need to add clock divider, and oneshot for exactly 32 pulses
    piso serial_gen1 (
        .load(load_ser1),
        .xmit(xmit_ser1),
        .clk(clk), // 50MHz
        .rst(rst1),
        .data_in(data1),
        .data_out(opad_DataIn),
        .clk_out(opad_CLKin)
    );
    
    piso serial_gen2 (
        .load(load_ser2),
        .xmit(xmit_ser2),
        .clk(clk), // 50MHz
        .rst(rst2),
        .data_in(data2),
        .data_out(opad2_DataIn),
        .clk_out(opad2_CLKin)
    );
    
    // Serial-in-parallel-out for reading readout register
    // Make a 32-clock one-shot, load into SIPO->register
    //opad_CLKin2
    //opad_serialOutCnt
    //opad_DataOut1
    //opad_DataOut2
    //opad2_CLKin2
    //opad2_serialOutCnt
    //opad2_DataOut1
    //opad2_DataOut2
    
    // Count replenishments during deltaT toggle
    //opad_deltaT
    //opad2_deltaT
    
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
            fifo_0_data_in = counter64; // FIFO data is always the current timestamp
        end
    end
    
    always @ (posedge TRIGGER) // Always synchrnous with 50MHz
    begin
        trig_ts <= counter64; // Store the time we sent external trigger
    end
    
    reg [15:0] oLVDS_synced;
    reg [15:0] oLVDS_synced_0;
    always @ (posedge clk200)
    begin
        oLVDS_synced_0 <= oLVDS;
        oLVDS_synced <= oLVDS_synced_0; // double FF sync into 200MHz domain
    end
    
    // Channel 0 FIFO 
    wire fifo_0_rd_en;
    reg fifo_0_event = 1'b0;
    reg fifo_0_reqread = 1'b0;
    
    always @ (posedge clk200)
    begin
        //if (oLVDS_synced[0] && !fifo_0_wr_rst_busy && !fifo_0_full) // If event ...
        if (oLVDS_synced[0] && !fifo_0_full)
           fifo_0_event <= 1; // ... trigger a one-shot to write the timestamp
        else
           fifo_0_event <= 0;
    end 
    oneshot fifo_0_write_os (
        .Clock(clk200),
        .Trigger(fifo_0_event),
        .Pulse(fifo_0_wr_en) // FIFO write timestamp
    );
    
    always @ (posedge clk)
    begin
        //if (fifo_0_read && !fifo_0_rd_rst_busy && !fifo_0_empty)
        if (fifo_0_read && !fifo_0_empty)
           fifo_0_reqread <= 1;
        else
           fifo_0_reqread <= 0;
    end 
    oneshot fifo_0_read_os (
        .Clock(clk),
        .Trigger(fifo_0_reqread),
        .Pulse(fifo_0_rd_en)
    );
    
    In_channel_FIFO_v0 fifo_0 (
      .rst(sys_rst),
      
      .wr_clk(clk200),
      .din(fifo_0_data_in),
      .wr_en(fifo_0_wr_en),
      .wr_rst_busy(fifo_0_wr_rst_busy),
      .full(fifo_0_full),
      .almost_full(fifo_0_almost_full),
      .wr_ack(),
      .overflow(),
      .wr_data_count(),
      .prog_full_thresh(32767),
      .prog_full(),
      
      .rd_clk(clk),
      .dout(fifo_0_dout),
      .rd_en(fifo_0_rd_en),
      .rd_rst_busy(fifo_0_rd_rst_busy),
      .empty(fifo_0_empty),
      .almost_empty(fifo_0_almost_empty),
      .valid(),
      .underflow(),
      .rd_data_count(),
      .prog_empty_thresh(0),
      .prog_empty()
    );

endmodule
