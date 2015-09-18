package com.nego.carpooling.database;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "peopledb";
    public static final int DATABASE_VERSION = 1;

    private static final String DATABASE_CREATE = "create table IF NOT EXISTS people (id integer primary key autoincrement, name text not null, img text default '', has_car integer default '0', address text not null);";

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase database) {
        database.execSQL(DATABASE_CREATE);
    }

    @Override
    public void onUpgrade( SQLiteDatabase database, int oldVersion, int newVersion ) {
        onCreate(database);
    }
}