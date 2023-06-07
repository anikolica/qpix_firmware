`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/24/2023 10:48:21 AM
// Design Name: 
// Module Name: demux32to1
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


// https://verilogcodes.blogspot.com/2015/10/verilog-code-for-14-demux-using-case.html

module demux1to32(
    input Data_in,
    input [5:0] sel,
    output reg [31:0] Data_out
    );

    always @(sel)
    begin
        case (sel)
            5'h00 : begin
                        Data_out = 32'h00000000;
                    end
            5'h01 : begin
                        Data_out = {31'h00000000, Data_in};
                    end
            5'h02 : begin
                        Data_out = {30'h00000000, Data_in, 1'h0};
                    end
            5'h03 : begin
                        Data_out = {29'h00000000, Data_in, 2'h0};
                    end
            5'h04 : begin
                        Data_out = {28'h0000000, Data_in, 3'h0};
                    end
            5'h05 : begin
                        Data_out = {27'h0000000, Data_in, 4'h0};
                    end
            5'h06 : begin
                        Data_out = {26'h0000000, Data_in, 5'h00};
                    end
            5'h07 : begin
                        Data_out = {25'h0000000, Data_in, 6'h00};
                    end
                    
            5'h08 : begin
                        Data_out = {24'h000000, Data_in, 7'h00};
                    end
            5'h09 : begin
                        Data_out = {23'h0000000, Data_in, 8'h00};
                    end
            5'h0a : begin
                        Data_out = {22'h000000, Data_in, 9'h000};
                    end
            5'h0b : begin
                        Data_out = {21'h000000, Data_in, 10'h000};
                    end
            5'h0c : begin
                        Data_out = {20'h00000, Data_in, 11'h000};
                    end
            5'h0d : begin
                        Data_out = {19'h00000, Data_in, 12'h000};
                    end
            5'h0e : begin
                        Data_out = {18'h00000, Data_in, 13'h0000};
                    end
            5'h0f : begin
                        Data_out = {17'h00000, Data_in, 14'h0000};
                    end     
                    
            5'h10 : begin
                        Data_out = {16'h0000, Data_in, 15'h0000};
                    end
            5'h11 : begin
                        Data_out = {15'h0000, Data_in, 16'h0000};
                    end
            5'h12 : begin
                        Data_out = {14'h0000, Data_in, 17'h00000};
                    end
            5'h13 : begin
                        Data_out = {13'h0000, Data_in, 18'h00000};
                    end
            5'h14 : begin
                        Data_out = {12'h000, Data_in, 19'h00000};
                    end
            5'h15 : begin
                        Data_out = {11'h000, Data_in, 20'h00000};
                    end
            5'h16 : begin
                        Data_out = {10'h000, Data_in, 21'h000000};
                    end
            5'h17 : begin
                        Data_out = {9'h000, Data_in, 22'h000000};
                    end
                    
            5'h18 : begin
                        Data_out = {8'h00, Data_in, 23'h000000};
                    end
            5'h19 : begin
                        Data_out = {7'h00, Data_in, 24'h000000};
                    end
            5'h1a : begin
                        Data_out = {6'h00, Data_in, 25'h0000000};
                    end
            5'h1b : begin
                        Data_out = {5'h00, Data_in, 26'h0000000};
                    end
            5'h1c : begin
                        Data_out = {4'h0, Data_in, 27'h0000000};
                    end
            5'h1d : begin
                        Data_out = {3'h0, Data_in, 28'h0000000};
                    end
            5'h1e : begin
                        Data_out = {2'h0, Data_in, 29'h00000000};
                    end
            5'h1f : begin
                        Data_out = {1'h0, Data_in, 30'h00000000};
                    end                                                                                                   
        endcase
    end
    
endmodule
