package com.ve472.l1;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.io.File;

import java.io.FileReader;
import java.io.IOException;
import java.io.BufferedReader;

public class Cinema {
    // public static void main( String[] args )
    // {
    //     Cinema myCinema = new Cinema("/home/shawn/Desktop/Lab1/my-app/config_dir");
    //     System.out.println(myCinema.halls_in_cinema.get("apple").movie_name);
    // }

    HashMap<String, Hall> halls_in_cinema = new HashMap<String, Hall>();

    // HashMap<String, List<Hall>> movies_in_cinema = new HashMap<String, List<Hall>>();
    HashMap<String, List<String>> movies_in_cinema = new HashMap<String, List<String>>();
    
    public Cinema(String dir){
        File file = new File(dir);		
		File[] fs = file.listFiles();	
		for(File f:fs){					
			if(f.isFile()){
                Hall new_hall = new Hall(f);
                try {
                    BufferedReader reader;
                    reader = new BufferedReader(new FileReader(
                            f));
                    String hall_name = reader.readLine();
                    String movie_name = reader.readLine();
                    halls_in_cinema.put(hall_name, new_hall);
                    if (movies_in_cinema.get(movie_name) == null){
                        // //create a new movie map
                        // List<Hall> thisMovieList = new ArrayList<Hall>();
                        // thisMovieList.add(new_hall);
                        // movies_in_cinema.put(movie_name, thisMovieList);

                        List<String> thisMovieList = new ArrayList<String>();
                        thisMovieList.add(new_hall.hall_name);
                        movies_in_cinema.put(movie_name, thisMovieList);
                    }else{
                        // List<Hall> thisMovieList = movies_in_cinema.get(movie_name);
                        // thisMovieList.add(new_hall);

                        List<String> thisMovieList = movies_in_cinema.get(movie_name);
                        thisMovieList.add(new_hall.hall_name);
                    }
                    reader.close();
                }catch (IOException e) {
                    e.printStackTrace();
                }
            }

				

		}
    }

}
