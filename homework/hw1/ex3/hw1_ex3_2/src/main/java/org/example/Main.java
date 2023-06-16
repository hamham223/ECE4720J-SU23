package org.example;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Vehicles my_vehicle = new Vehicles();
        Vehicles my_bus = new Bus();
        Vehicles my_car = new Car();
        my_vehicle.getInfo();
        my_car.getInfo();
        my_bus.getInfo();
    }
}

class Vehicles{
    // define basic attributes
    String type;
    String brand;

    public Vehicles(){
        this.type= "Default_type";
        this.brand = "Default_brand";
    }
    public Vehicles(String type, String brand, int age){
        this.type = type;
        this.brand = brand;
    }
    public void getInfo() {
        System.out.println("I don't know the info");
    }
}

class Car extends Vehicles{
    Integer age;
    public Car(){
        type = "Car";
        brand = "Tesla";
        age = 1;
    }
    @Override
    public void getInfo() {
        System.out.println("This is a Car, my father is vehicle");
        System.out.println("type:" + type + "\nBrand:" + brand + "\nAge: " + age);
    }
}

class Bus extends Vehicles{
    public Bus(){
        type = "Bus";
        brand = "Benz";
    }
    @Override
    public void getInfo() {
        System.out.println("This is a Bus, my farther is vehicle");
        System.out.println("type:" + type + "\nBrand:" + brand );
    }
}