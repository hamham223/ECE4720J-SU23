package com.ve472.l1;
import java.io.BufferedReader;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.io.FileReader;
import java.io.IOException;

public class Hall {
    String hall_name;
    String movie_name;
    List<List<Boolean>> seat_info = new ArrayList<>();
    Integer line_num;
    Double centrl_line;
    Boolean Flag;
    Integer tarRow;
    Integer tarCol;


    public Hall(){};
    public Hall(File configFile){
        BufferedReader reader;
        try {
            Flag = false;
            reader = new BufferedReader(new FileReader(
                    configFile));
            this.hall_name = reader.readLine();
            this.movie_name = reader.readLine();

            String line = reader.readLine();
            line_num = 0;
            while (line != null) {
                line_num = line_num + 1;
                // System.out.println(line);
                String[] lineSplit = line.split(" ");
                ArrayList<Boolean> lineList = new ArrayList<Boolean>();

                for (String seat:lineSplit) {
                    lineList.add(seat.equals("1"));
                }
                this.seat_info.add(lineList);
                
                line = reader.readLine();
                centrl_line = Double.valueOf(lineList.size()-1) /2;
            }
            reader.close();

            

        } catch (IOException e) {
            e.printStackTrace();
        }
    };



    protected void Getseat(Integer num){
        // num is the seat you need
        Flag = false;
        Double oldDis = Double.MAX_VALUE;
        Double newDis = Double.MAX_VALUE;
        Double centralOffset = Double.valueOf((num-1))/2;

    
        try{
            if(seat_info.size() <= 0){
                return;
            }
            if(seat_info.get(0).size()<num){
                return;
            }
        }catch(NullPointerException e){
            return;
        }
        
        
        for (Integer row = seat_info.size()-1; row >=0; row--){
            for (Integer col = 0; col <= seat_info.get(0).size()-num; col++){
                for(Integer i = 0; i < num; i++){
                    if (!seat_info.get(row).get(col+i)){
                        break;
                    }else{
                        if(i == num-1 && seat_info.get(row).get(col+i)){ //get the position
                            Flag = true;
                            newDis = Math.pow((seat_info.size()-1 - row), 2) + Math.pow(centrl_line - (Double.valueOf(col) + centralOffset),2);
                            if (newDis < oldDis - 0.1){

                                oldDis = newDis;
                                tarRow = row;
                                tarCol = col;
                            }
                        }
                    }
                }
            }
        }

        // //update if success
        if (Flag == true){
            //update the config
            for (Integer col = tarCol; col < tarCol + num; col++){
                List<Boolean> row = seat_info.get(tarRow);
                if(row.get(col) == false){
                    System.out.println("Error, reuse occupied seat");
                }
                row.set(col, false);
                seat_info.set(tarRow, row);
            }
        }
    }
}
