----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 05/15/2017 03:25:26 PM
-- Design Name: 
-- Module Name: one-shot - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

--from http://www.microprocessor-design.com/web_notes/JustOne.htm
entity oneshot is
    port(
        Trigger : in std_logic;
        Clock : in std_logic;
        Pulse : out std_logic 
    );
end oneshot;

architecture Behavioral of oneshot is

    signal QA: std_logic := '0';
    signal QB: std_logic := '0';
    
    begin
        Pulse <= QB;
        process (Trigger, QB)
        begin
            if QB='1' then
                QA <= '0';
            elsif (Trigger'event and Trigger='1') then
                QA <= '1';
            end if;
        end process;
    
        process (Clock)
        begin
            if Clock'event and Clock ='1' then
                QB <= QA;
            end if;
        end process;

end Behavioral;
