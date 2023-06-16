package com.ve472.l1;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.HelpFormatter;


import java.io.FileReader;
import java.io.IOException;
import java.util.Collections;
import java.util.List;
import java.io.BufferedReader;
/**
 * Hello world!
 *
 */
public class Main
{
    public static void main( String[] args )
    {
        CommandLine commandLine;
        Option option_help = Option.builder("h")
            .desc("print this message")
            .longOpt("help")
            .hasArg(false)
            .build();
        Option option_hall = Option.builder(null)
            .desc("path of the hall config directory")
            .hasArg(true)
            .longOpt("hall")
            .build();
        Option option_query = Option.builder(null)
            .desc("query of customer orders")
            .longOpt("query")
            .hasArg(true)
            .build();
        Options options = new Options();

        CommandLineParser parser = new DefaultParser();

        String[] Testarg = { 
        "--hall", "/home/shawn/Desktop/Lab1/my-app/config_dir", 
        "--query", "/home/shawn/Desktop/Lab1/my-app/query.txt",
        //"-h"
        };

        options.addOption(option_help);
        options.addOption(option_hall);
        options.addOption(option_query);

        HelpFormatter formatter = new HelpFormatter();

        try
        {
            commandLine = parser.parse(options, args);
            //commandLine = parser.parse(options, Testarg);
            
            if(args.length == 0){
            //if(Testarg.length == 0){
                throw new ParseException("Empty length");
            }

            if (commandLine.hasOption("h"))
            {
                formatter.printHelp("cinema", options, false);
            }

            if (commandLine.hasOption("query") && commandLine.hasOption("hall"))
            {
                Cinema myCinema = new Cinema(commandLine.getOptionValue("hall"));
                Processing_query(myCinema, commandLine.getOptionValue("query"));
            }
            return;


        }
        catch (ParseException exception)
        {
            
            formatter.printHelp("cinema", options, false);
            return;
        }
    }



    protected static void Processing_query(Cinema myCinema, String query_path){
        BufferedReader reader;
        try {
            reader = new BufferedReader(new FileReader(
                    query_path));
            String query = reader.readLine();
            while (query != null){
                String[] querySplit = query.split(",");
                String name = querySplit[0].trim();
                String movie = querySplit[1].trim();
                Integer tickInteger = Integer.parseInt(querySplit[2].trim());
                
                if(myCinema.movies_in_cinema.get(movie) != null){
                    List<String> hall_list = myCinema.movies_in_cinema.get(movie);
                    // sort in alphabetical order
                    Collections.sort(hall_list);

                    String currenthall = hall_list.get(0);


                    for (String hall : hall_list){
                        
                        Hall thisHall = myCinema.halls_in_cinema.get(hall);
                        if(thisHall == null){
                            continue;
                        }
                        thisHall.Getseat(tickInteger);
                        if(thisHall.Flag){
                            //success break iteration
                            currenthall = thisHall.hall_name;
                            break;
                        }
                    }

                    if(myCinema.halls_in_cinema.get(currenthall)==null){
                        //failed
                        String str = String.valueOf(name);

                        System.out.print(name);
                        System.out.print(",");
                        System.out.print(movie);
                        System.out.print("\n");

                    }
                    else if(myCinema.halls_in_cinema.get(currenthall).Flag){
                        //success
                        Hall thisHall = myCinema.halls_in_cinema.get(currenthall);
                        Integer tarRow = thisHall.tarRow+1;
                        String str = new StringBuilder().append(name).append(",").append(movie).append(",").append(currenthall).append(",").append(tarRow).toString();
                        System.out.print(str);
                        //System.out.print(name + "," + movie + "," + currenthall + "," + tarRow);
                        for (Integer i = thisHall.tarCol+1; i<= thisHall.tarCol+tickInteger; i++){
                            System.out.print(new StringBuilder().append(",").append(i).toString());
                        }
                        System.out.print("\n");

                    }else{
                        //failed
                        System.out.println(new StringBuilder().append(name).append(",").append(movie).toString());
                    }
                }
                else
                {
                    //failed no movie
                    System.out.println(new StringBuilder().append(name).append(",").append(movie).toString());
                }
                query = reader.readLine();
            }
            reader.close();
        }catch (IOException e) {
            e.printStackTrace();
        }
    }


}

