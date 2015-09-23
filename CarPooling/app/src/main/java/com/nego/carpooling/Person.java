package com.nego.carpooling;

import android.content.Context;
import android.database.Cursor;
import android.os.Parcel;
import android.os.Parcelable;
import android.util.Log;

import com.nego.carpooling.database.DbAdapter;

import java.util.ArrayList;

public class Person implements Parcelable {

    private int id;
    private String name;
    private String img;
    private long max_dur;
    private String address;
    private ArrayList<String> notWith = new ArrayList<>();
    private ArrayList<String> pop = new ArrayList<>();

    public Person(int id, String name, long max_dur, String img, String address, ArrayList<String> notWith, ArrayList<String> pop) {
        this.id = id;
        this.name = name;
        this.img = img;
        this.max_dur = max_dur;
        this.address = address;
        this.notWith = notWith;
        this.pop = pop;
    }

    public Person(String name, long max_dur, String img, String address, ArrayList<String> notWith, ArrayList<String> pop) {
        this.name = name;
        this.name = name;
        this.img = img;
        this.max_dur = max_dur;
        this.address = address;
        this.notWith = notWith;
        this.pop = pop;
    }

    public Person(Cursor cursor){
        this.id = cursor.getInt(cursor.getColumnIndex(DbAdapter.KEY_ID));
        this.name = cursor.getString(cursor.getColumnIndex(DbAdapter.KEY_NAME));
        this.img = cursor.getString(cursor.getColumnIndex(DbAdapter.KEY_IMG));
        this.max_dur = cursor.getLong(cursor.getColumnIndex(DbAdapter.KEY_MAX_DUR));
        this.address = cursor.getString(cursor.getColumnIndex(DbAdapter.KEY_ADDRESS));
        this.notWith = Utils.stringToArrayList(cursor.getString(cursor.getColumnIndex(DbAdapter.KEY_NOT_WITH)));
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

    public void setMax_dur(long max_dur) {
        this.max_dur = max_dur;
    }

    public long getMax_dur() {
        return max_dur;
    }

    public void setNotWith(ArrayList<String> notWith) {
        this.notWith = notWith;
    }

    public ArrayList<String> getNotWith() {
        return notWith;
    }

    public void setPop(ArrayList<String> pop) {
        this.pop = pop;
    }
    public void setPop(Cursor cursor_pop) {
        while (cursor_pop.moveToNext()) {
            this.pop.clear();
            this.pop.add(cursor_pop.getString(cursor_pop.getColumnIndex(DbAdapter.KEY_ADDRESS)));
        }
    }

    public ArrayList<String> getPop() {
        return pop;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getAddress() {
        return address;
    }

    public boolean create(DbAdapter dbAdapter) {
        if (dbAdapter.createPerson(this)) {
            if (!pop.isEmpty()) {
                for (String p : pop) {
                    dbAdapter.createPop(p, id);
                }
            }
            return true;
        }
        return false;
    }

    public boolean update(DbAdapter dbAdapter) {
        if (dbAdapter.updatePerson(this)) {
            dbAdapter.deleteAllPop(id);
            if (!pop.isEmpty()) {
                for (String p : pop) {
                    dbAdapter.createPop(p, id);
                }
            }
            return true;
        }
        return false;
    }

    public boolean delete(DbAdapter dbAdapter) {
        if (dbAdapter.deletePerson(this.getId())) {
            dbAdapter.deleteAllPop(id);
            return true;
        }
        return false;
    }


    // PARCELIZZAZIONE

    public static final Parcelable.Creator<Person> CREATOR = new Parcelable.Creator<Person>() {
        public Person createFromParcel(Parcel source) {
            return new Person(source.readInt(), source.readString(), source.readLong(), source.readString(), source.readString(), Utils.stringToArrayList(source.readString()), Utils.stringToArrayList(source.readString()));
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
        dest.writeLong(max_dur);
        dest.writeString(img);
        dest.writeString(address);
        dest.writeString(Utils.arrayListToString(notWith));
        dest.writeString(Utils.arrayListToString(pop));
    }
}
