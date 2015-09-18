package com.nego.carpooling;

import android.content.Context;
import android.database.Cursor;
import android.os.Parcel;
import android.os.Parcelable;

import com.nego.carpooling.database.DbAdapter;

public class Person implements Parcelable {

    private int id;
    private String name;
    private String img;
    private int has_car;
    private String address;

    public Person(int id, String name, String img, int has_car, String address) {
        this.id = id;
        this.name = name;
        this.img = img;
        this.has_car = has_car;
        this.address = address;
    }

    public Person(String name, String img, int has_car, String address) {
        this.name = name;
        this.img = img;
        this.has_car = has_car;
        this.address = address;
    }

    public Person(Cursor cursor){
        this.id = cursor.getInt(cursor.getColumnIndex(DbAdapter.KEY_ID));
        this.name = cursor.getString(cursor.getColumnIndex(DbAdapter.KEY_NAME));
        this.img = cursor.getString( cursor.getColumnIndex(DbAdapter.KEY_IMG) );
        this.has_car = cursor.getInt(cursor.getColumnIndex(DbAdapter.KEY_HAS_CAR));
        this.address = cursor.getString(cursor.getColumnIndex(DbAdapter.KEY_ADDRESS));
    }

    public int getId() {
        return id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setImg(String img) {
        this.img = img;
    }

    public String getImg() {
        return img;
    }

    public void setHas_car(int has_car) {
        this.has_car = has_car;
    }

    public int getHas_car() {
        return has_car;
    }

    public boolean hasCar() {
        return has_car == 1;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getAddress() {
        return address;
    }

    public boolean create(DbAdapter dbAdapter) {
        return dbAdapter.createPerson(this);
    }

    public boolean update(DbAdapter dbAdapter) {
        return dbAdapter.updatePerson(this);
    }

    public boolean delete(DbAdapter dbAdapter) {
        return dbAdapter.deletePerson(this.getId());
    }


    // PARCELIZZAZIONE

    public static final Parcelable.Creator<Person> CREATOR = new Parcelable.Creator<Person>() {
        public Person createFromParcel(Parcel source) {
            return new Person(source.readInt(), source.readString(), source.readString(), source.readInt(), source.readString());
        }
        public Person[] newArray(int size) {
            return new Person[size];
        }
    };

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(id);
        dest.writeString(name);
        dest.writeString(img);
        dest.writeInt(has_car);
        dest.writeString(address);
    }
}
