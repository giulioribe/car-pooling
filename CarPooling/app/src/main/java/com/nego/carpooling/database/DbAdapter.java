package com.nego.carpooling.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import com.nego.carpooling.Person;
import com.nego.carpooling.Utils;

import java.util.ArrayList;

public class DbAdapter {


    private Context context;
    private SQLiteDatabase database;
    private DatabaseHelper dbHelper;

    // Database fields
    private static final String DATABASE_TABLE_PEOPLE = "people";
    private static final String DATABASE_TABLE_POP = "pop";

    public static final String KEY_ID = "id";
    public static final String KEY_NAME = "name";
    public static final String KEY_IMG = "img";
    public static final String KEY_MAX_DUR = "maxDur";
    public static final String KEY_ADDRESS = "address";
    public static final String KEY_NOT_WITH = "notWith";

    public static final String KEY_PERSON = "person";

    public DbAdapter(Context context) {
        this.context = context;
    }

    public DbAdapter open() throws SQLException {
        dbHelper = new DatabaseHelper(context);
        database = dbHelper.getWritableDatabase();
        if (database.getVersion() < DatabaseHelper.DATABASE_VERSION)
            dbHelper.onUpgrade(database, database.getVersion(), DatabaseHelper.DATABASE_VERSION);
        else
            dbHelper.onCreate(database);
        return this;
    }

    public void close() {
        dbHelper.close();
    }

    private ContentValues createContentValues(int ID, String name, long max_dur, String img, ArrayList<String> notWith, String address) {
        ContentValues values = new ContentValues();
        values.put(KEY_ID, ID);
        values.put(KEY_NAME, name);
        values.put(KEY_IMG, img);
        values.put(KEY_MAX_DUR, max_dur);
        values.put(KEY_NOT_WITH, Utils.arrayListToString(notWith));
        values.put(KEY_ADDRESS, address);

        return values;
    }

    private ContentValues createContentValues(String name, long max_dur, String img, ArrayList<String> notWith, String address) {
        ContentValues values = new ContentValues();
        values.put(KEY_NAME, name);
        values.put(KEY_IMG, img);
        values.put(KEY_MAX_DUR, max_dur);
        values.put(KEY_NOT_WITH, Utils.arrayListToString(notWith));
        values.put(KEY_ADDRESS, address);

        return values;
    }

    private ContentValues createContentValues(String address, int person) {
        ContentValues values = new ContentValues();
        values.put(KEY_ADDRESS, address);
        values.put(KEY_PERSON, person);

        return values;
    }

    public boolean createPerson(Person p) {
        ContentValues initialValues = createContentValues(p.getName(), p.getMax_dur(), p.getImg(), p.getNotWith(), p.getAddress());
        return database.insertOrThrow(DATABASE_TABLE_PEOPLE, null, initialValues) > 0;
    }

    public boolean updatePerson(Person p) {
        ContentValues updateValues = createContentValues(p.getId(), p.getName(), p.getMax_dur(), p.getImg(), p.getNotWith(), p.getAddress());
        return database.update(DATABASE_TABLE_PEOPLE, updateValues, KEY_ID + "==" + p.getId(), null) > 0;
    }


    public boolean deletePerson(int ID) {
        return database.delete(DATABASE_TABLE_PEOPLE, KEY_ID + "==" + ID, null) > 0;
    }


    public Cursor fetchAllPersons() {
        return database.query(DATABASE_TABLE_PEOPLE, new String[]{KEY_ID, KEY_NAME, KEY_MAX_DUR, KEY_IMG, KEY_NOT_WITH, KEY_ADDRESS}, null, null, null, null, null);
    }

    public Cursor getPersonById(int id) {
        Cursor mCursor = database.query(true, DATABASE_TABLE_PEOPLE, new String[]{
                        KEY_ID, KEY_NAME, KEY_MAX_DUR, KEY_IMG, KEY_NOT_WITH, KEY_ADDRESS},
                KEY_ID + " == '" + id + "'", null, null, null, null, null);

        return mCursor;
    }


    public boolean createPop(String address, int person) {
        ContentValues initialValues = createContentValues(address, person);
        return database.insertOrThrow(DATABASE_TABLE_POP, null, initialValues) > 0;
    }

    public boolean deleteAllPop(int ID) {
        return database.delete(DATABASE_TABLE_POP, KEY_PERSON + "==" + ID, null) > 0;
    }


    public Cursor getPopById(int id) {
        Cursor mCursor = database.query(true, DATABASE_TABLE_POP, new String[]{
                        KEY_ADDRESS},
                KEY_PERSON + " == '" + id + "'", null, null, null, null, null);

        return mCursor;
    }

}