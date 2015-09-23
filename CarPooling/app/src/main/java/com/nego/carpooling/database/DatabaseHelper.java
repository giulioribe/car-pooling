package com.nego.carpooling.database;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "peopledb";
    public static final int DATABASE_VERSION = 2;

    private static final String DATABASE_CREATE_PEOPLE = "create table IF NOT EXISTS people (id integer primary key autoincrement, name text not null, img text default '', maxDur long default '0', address text not null, notWith text default '');";
    private static final String DATABASE_CREATE_POP = "create table IF NOT EXISTS pop (id integer primary key autoincrement, person integer not null, address text not null);";


    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase database) {
        database.execSQL(DATABASE_CREATE_PEOPLE);
        database.execSQL(DATABASE_CREATE_POP);
    }

    @Override
    public void onUpgrade( SQLiteDatabase database, int oldVersion, int newVersion ) {
        if (oldVersion == 1) {
            database.execSQL("DROP TABLE IF EXISTS people");
            onUpgrade(database, 2, newVersion);
        }
        onCreate(database);
    }
}