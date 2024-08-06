//Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
//--------------------------------------------------------------------------------
//Tool Version: Vivado v.2020.1 (lin64) Build 2902540 Wed May 27 19:54:35 MDT 2020
//Date        : Mon Jun  5 13:23:31 2023
//Host        : lxeng99 running 64-bit Ubuntu 16.04.6 LTS
//Command     : generate_target design_1_wrapper.bd
//Design      : design_1_wrapper
//Purpose     : IP block netlist
//--------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

module design_1_wrapper
   (DDR_addr,
    DDR_ba,
    DDR_cas_n,
    DDR_ck_n,
    DDR_ck_p,
    DDR_cke,
    DDR_cs_n,
    DDR_dm,
    DDR_dq,
    DDR_dqs_n,
    DDR_dqs_p,
    DDR_odt,
    DDR_ras_n,
    DDR_reset_n,
    DDR_we_n,
    FIXED_IO_ddr_vrn,
    FIXED_IO_ddr_vrp,
    FIXED_IO_mio,
    FIXED_IO_ps_clk,
    FIXED_IO_ps_porb,
    FIXED_IO_ps_srstb,
    FPGA_I2C_scl_io,
    FPGA_I2C_sda_io,
    OSC_200MHz,
    TRIGGER,
    oLVDS,
    //oTP1,
    //oTP2,
    i2c0_sda_io,
    i2c0_scl_io,
    oTP3,
    oTP4,
    opad2_CLK,
    opad2_CLKin,
    opad2_CLKin2,
    opad2_DataIn,
    opad2_DataOut1,
    opad2_DataOut2,
    opad2_RST_EXT,
    opad2_cal_control,
    opad2_control,
    opad2_deltaT,
    opad2_loadData,
    opad2_selDefData,
    opad2_serialOutCnt,
    opad2_startup,
    opad_CLK,
    opad_CLKin,
    opad_CLKin2,
    opad_DataIn,
    opad_DataOut1,
    opad_DataOut2,
    opad_Ext_POR,
    opad_RST_EXT,
    opad_cal_control,
    opad_control,
    opad_deltaT,
    opad_loadData,
    opad_selDefData,
    opad_serialOutCnt,
    opad_startup);
  inout [14:0]DDR_addr;
  inout [2:0]DDR_ba;
  inout DDR_cas_n;
  inout DDR_ck_n;
  inout DDR_ck_p;
  inout DDR_cke;
  inout DDR_cs_n;
  inout [3:0]DDR_dm;
  inout [31:0]DDR_dq;
  inout [3:0]DDR_dqs_n;
  inout [3:0]DDR_dqs_p;
  inout DDR_odt;
  inout DDR_ras_n;
  inout DDR_reset_n;
  inout DDR_we_n;
  inout FIXED_IO_ddr_vrn;
  inout FIXED_IO_ddr_vrp;
  inout [53:0]FIXED_IO_mio;
  inout FIXED_IO_ps_clk;
  inout FIXED_IO_ps_porb;
  inout FIXED_IO_ps_srstb;
  inout FPGA_I2C_scl_io;
  inout FPGA_I2C_sda_io;
  input OSC_200MHz;
  output TRIGGER;
  input [15:0]oLVDS;
  //output oTP1;
  //output oTP2;
  inout i2c0_sda_io;
  inout i2c0_scl_io;
  output oTP3;
  output oTP4;
  output opad2_CLK;
  output opad2_CLKin;
  output opad2_CLKin2;
  output opad2_DataIn;
  input opad2_DataOut1;
  input opad2_DataOut2;
  output opad2_RST_EXT;
  output opad2_cal_control;
  output opad2_control;
  input opad2_deltaT;
  output opad2_loadData;
  output opad2_selDefData;
  output opad2_serialOutCnt;
  output opad2_startup;
  output opad_CLK;
  output opad_CLKin;
  output opad_CLKin2;
  output opad_DataIn;
  input opad_DataOut1;
  input opad_DataOut2;
  output opad_Ext_POR;
  output opad_RST_EXT;
  output opad_cal_control;
  output opad_control;
  input opad_deltaT;
  output opad_loadData;
  output opad_selDefData;
  output opad_serialOutCnt;
  output opad_startup;

  wire [14:0]DDR_addr;
  wire [2:0]DDR_ba;
  wire DDR_cas_n;
  wire DDR_ck_n;
  wire DDR_ck_p;
  wire DDR_cke;
  wire DDR_cs_n;
  wire [3:0]DDR_dm;
  wire [31:0]DDR_dq;
  wire [3:0]DDR_dqs_n;
  wire [3:0]DDR_dqs_p;
  wire DDR_odt;
  wire DDR_ras_n;
  wire DDR_reset_n;
  wire DDR_we_n;
  wire FIXED_IO_ddr_vrn;
  wire FIXED_IO_ddr_vrp;
  wire [53:0]FIXED_IO_mio;
  wire FIXED_IO_ps_clk;
  wire FIXED_IO_ps_porb;
  wire FIXED_IO_ps_srstb;
  wire FPGA_I2C_scl_i;
  wire FPGA_I2C_scl_io;
  wire FPGA_I2C_scl_o;
  wire FPGA_I2C_scl_t;
  wire FPGA_I2C_sda_i;
  wire FPGA_I2C_sda_io;
  wire FPGA_I2C_sda_o;
  wire FPGA_I2C_sda_t;
  wire i2c0_scl_i;
  wire i2c0_scl_io;
  wire i2c0_scl_o;
  wire i2c0_scl_t;
  wire i2c0_sda_i;
  wire i2c0_sda_io;
  wire i2c0_sda_o;
  wire i2c0_sda_t;
  wire OSC_200MHz;
  wire TRIGGER;
  wire [15:0]oLVDS;
  wire oTP1;
  wire oTP2;
  wire oTP3;
  wire oTP4;
  wire opad2_CLK;
  wire opad2_CLKin;
  wire opad2_CLKin2;
  wire opad2_DataIn;
  wire opad2_DataOut1;
  wire opad2_DataOut2;
  wire opad2_RST_EXT;
  wire opad2_cal_control;
  wire opad2_control;
  wire opad2_deltaT;
  wire opad2_loadData;
  wire opad2_selDefData;
  wire opad2_serialOutCnt;
  wire opad2_startup;
  wire opad_CLK;
  wire opad_CLKin;
  wire opad_CLKin2;
  wire opad_DataIn;
  wire opad_DataOut1;
  wire opad_DataOut2;
  wire opad_Ext_POR;
  wire opad_RST_EXT;
  wire opad_cal_control;
  wire opad_control;
  wire opad_deltaT;
  wire opad_loadData;
  wire opad_selDefData;
  wire opad_serialOutCnt;
  wire opad_startup;

  IOBUF FPGA_I2C_scl_iobuf
       (.I(FPGA_I2C_scl_o),
        .IO(FPGA_I2C_scl_io),
        .O(FPGA_I2C_scl_i),
        .T(FPGA_I2C_scl_t));
  IOBUF FPGA_I2C_sda_iobuf
       (.I(FPGA_I2C_sda_o),
        .IO(FPGA_I2C_sda_io),
        .O(FPGA_I2C_sda_i),
        .T(FPGA_I2C_sda_t));
  IOBUF i2c0_scl_iobuf
       (.I(i2c0_scl_o),
        .IO(i2c0_scl_io),
        .O(i2c0_scl_i),
        .T(i2c0_scl_t));
  IOBUF i2c0_sda_iobuf
       (.I(i2c0_sda_o),
        .IO(i2c0_sda_io),
        .O(i2c0_sda_i),
        .T(i2c0_sda_t));      
  design_1 design_1_i
       (.DDR_addr(DDR_addr),
        .DDR_ba(DDR_ba),
        .DDR_cas_n(DDR_cas_n),
        .DDR_ck_n(DDR_ck_n),
        .DDR_ck_p(DDR_ck_p),
        .DDR_cke(DDR_cke),
        .DDR_cs_n(DDR_cs_n),
        .DDR_dm(DDR_dm),
        .DDR_dq(DDR_dq),
        .DDR_dqs_n(DDR_dqs_n),
        .DDR_dqs_p(DDR_dqs_p),
        .DDR_odt(DDR_odt),
        .DDR_ras_n(DDR_ras_n),
        .DDR_reset_n(DDR_reset_n),
        .DDR_we_n(DDR_we_n),
        .FIXED_IO_ddr_vrn(FIXED_IO_ddr_vrn),
        .FIXED_IO_ddr_vrp(FIXED_IO_ddr_vrp),
        .FIXED_IO_mio(FIXED_IO_mio),
        .FIXED_IO_ps_clk(FIXED_IO_ps_clk),
        .FIXED_IO_ps_porb(FIXED_IO_ps_porb),
        .FIXED_IO_ps_srstb(FIXED_IO_ps_srstb),
        .FPGA_I2C_scl_i(FPGA_I2C_scl_i),
        .FPGA_I2C_scl_o(FPGA_I2C_scl_o),
        .FPGA_I2C_scl_t(FPGA_I2C_scl_t),
        .FPGA_I2C_sda_i(FPGA_I2C_sda_i),
        .FPGA_I2C_sda_o(FPGA_I2C_sda_o),
        .FPGA_I2C_sda_t(FPGA_I2C_sda_t),
        .OSC_200MHz(OSC_200MHz),
        .TRIGGER(TRIGGER),
        .oLVDS(oLVDS),
        //.oTP1(oTP1),
        //.oTP2(oTP2),
        .i2c0_scl_i(i2c0_scl_i),
        .i2c0_scl_o(i2c0_scl_o),
        .i2c0_scl_t(i2c0_scl_t),
        .i2c0_sda_i(i2c0_sda_i),
        .i2c0_sda_o(i2c0_sda_o),
        .i2c0_sda_t(i2c0_sda_t),
        .oTP3(oTP3),
        .oTP4(oTP4),
        .opad2_CLK(opad2_CLK),
        .opad2_CLKin(opad2_CLKin),
        .opad2_CLKin2(opad2_CLKin2),
        .opad2_DataIn(opad2_DataIn),
        .opad2_DataOut1(opad2_DataOut1),
        .opad2_DataOut2(opad2_DataOut2),
        .opad2_RST_EXT(opad2_RST_EXT),
        .opad2_cal_control(opad2_cal_control),
        .opad2_control(opad2_control),
        .opad2_deltaT(opad2_deltaT),
        .opad2_loadData(opad2_loadData),
        .opad2_selDefData(opad2_selDefData),
        .opad2_serialOutCnt(opad2_serialOutCnt),
        .opad2_startup(opad2_startup),
        .opad_CLK(opad_CLK),
        .opad_CLKin(opad_CLKin),
        .opad_CLKin2(opad_CLKin2),
        .opad_DataIn(opad_DataIn),
        .opad_DataOut1(opad_DataOut1),
        .opad_DataOut2(opad_DataOut2),
        .opad_Ext_POR(opad_Ext_POR),
        .opad_RST_EXT(opad_RST_EXT),
        .opad_cal_control(opad_cal_control),
        .opad_control(opad_control),
        .opad_deltaT(opad_deltaT),
        .opad_loadData(opad_loadData),
        .opad_selDefData(opad_selDefData),
        .opad_serialOutCnt(opad_serialOutCnt),
        .opad_startup(opad_startup));
endmodule
