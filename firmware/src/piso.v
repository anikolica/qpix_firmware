`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: University of Pennsylvania
// Engineer: A. Nikolica
// 
// Create Date: 02/21/2023 03:03:33 PM
// Design Name: 
// Module Name: piso
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


module piso (
    input load, xmit, clk, rst,
    input [31:0] data_in,
    output reg data_out,
    output reg clk_out,
    output [31:0] debug,
    output [6:0] debug2);
  
    // PISO register array to load and shift data
    reg [31:0] data_reg;
    reg [6:0] counter;
    reg clk_d;
    assign debug = data_reg;
    assign debug2 = counter;
    
    always @ (posedge clk) begin // lag the clock so data is present already on rising edge
        clk_out <= clk_d;
    end
  
    always @ (posedge clk or negedge rst) begin
        if (rst) begin
            data_reg <= 32'h00000000; // Reset PISO register array on reset
            counter <= 7'h00;
            clk_d <= 1'b0;
            data_out <= 1'b0;
        end
        else begin 
            if (load) begin // Load the data to the PISO register array and reset the serial data out register
                {data_reg, data_out} <= {data_in, 1'b0};
                //data_reg <= data_in;
                counter <= 7'h00;
            end
            else if (xmit) begin // Shift the loaded data 1 bit LEFT (MSB first) into the serial data out register
                if (counter < 7'h40) begin
                    if (counter % 2 == 0) begin // change data on rising (even) edge
                        {data_out, data_reg} <= {data_reg[31:0], 1'b0};
                        //data_out <= data_reg[31];
                        //data_reg <= {data_reg[30:0], 1'b0};
                        clk_d <= ~clk_d;
                        counter <= counter + 1;
                    end
                    else begin // always advance clock for 16 bits
                        clk_d <= ~clk_d;
                        counter <= counter + 1;
                    end
                end
                else begin // stop clock if out of bits
                    clk_d <= 1'b0;
                    data_out <= 1'b0;
                    counter <= 7'h40;
                end
            end
            else begin // line quiet otherwise
                clk_d <= 1'b0;
                data_out <= 1'b0;
            end
        end
    end 
endmodule
