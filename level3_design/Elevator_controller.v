module Controller(clk,reset,requested_floor,wait_floor,door,Up,Down,y);

input clk,reset;
input [4:0] requested_floor;

output reg[1:0] door;
output reg[1:0] Up;
output reg[1:0] Down;
output reg[1:0] wait_floor;
output [4:0] y;

reg [4:0] current_floor ;

always @ (posedge clk)
    begin
        if(reset)
        begin
            current_floor=4'd0;
            wait_floor=4'd1;
            door = 1'd1;
            Up=1'd0;
            Down=1'd0;
        end
        else
        begin
            if(requested_floor < 4'd15)
            begin
                if(requested_floor < current_floor)
                begin
                    current_floor=current_floor+1;
                    door=1'd0;
                    wait_floor=4'd0;
                    Up=1'd0;
                    Down=1'd1;
                end
                else if (requested_floor > current_floor)
                begin
                    current_floor = current_floor+1;
                    door=1'd0;
                    wait_floor=4'd0;
                    Up=1'd1;
                    Down=1'd0;
                end
                else if(requested_floor == current_floor)
                begin
                    current_floor = current_floor+1;
                    door=1'd1;
                    wait_floor=4'd1;
                    Up=1'd0;
                    Down=1'd0;
                end
            end
        end
    end
    
assign y = current_floor;

endmodule
