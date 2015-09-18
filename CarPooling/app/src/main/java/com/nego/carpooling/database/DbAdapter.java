package com.nego.carpooling.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;

import com.nego.carpooling.Person;

public class DbAdapter {


    private Context context;
    private SQLiteDatabase database;
    private DatabaseHelper dbHelper;

    // Database fields
    private static final String DATABASE_TABLE = "people";

    public static final String KEY_ID = "id";
    public static final String KEY_NAME = "name";
    public static final String KEY_IMG = "img";
    public static final String KEY_HAS_CAR = "has_car";
    public static final String KEY_ADDRESS = "address";

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

    private ContentValues createContentValues(int ID, String name, String img, int has_car, String address) {
        ContentValues values = new ContentValues();
        values.put(KEY_ID, ID);
        values.put(KEY_NAME, name);
        values.put(KEY_IMG, img);
        values.put(KEY_HAS_CAR, has_car);
        values.put(KEY_ADDRESS, address);

        return values;
    }

    private ContentValues createContentValues(String name, String img, int has_car, String address) {
        ContentValues values = new ContentValues();
        values.put(KEY_NAME, name);
        values.put(KEY_IMG, img);
        values.put(KEY_HAS_CAR, has_car);
        values.put(KEY_ADDRESS, address);

        return values;
    }

    public boolean createPerson(Person p) {
        ContentValues initialValues = createContentValues(p.getName(), p.getImg(), p.getHas_car(), p.getAddress());
        return database.insertOrThrow(DATABASE_TABLE, null, initialValues) > 0;
    }

    public boolean updatePerson(Person p) {
        ContentValues updateValues = createContentValues(p.getId(), p.getName(), p.getImg(), p.getHas_car(), p.getAddress());
        return database.update(DATABASE_TABLE, updateValues, KEY_ID + "==" + p.getId(), null) > 0;
    }


    public boolean deletePerson(int ID) {
        return database.delete(DATABASE_TABLE, KEY_ID + "==" + ID, null) > 0;
    }


    public Cursor fetchAllPersons() {
        return database.query(DATABASE_TABLE, new String[]{KEY_ID, KEY_NAME, KEY_IMG, KEY_HAS_CAR, KEY_ADDRESS}, null, null, null, null, null);
    }

    public Cursor getPersonById(int id) {
        Cursor mCursor = database.query(true, DATABASE_TABLE, new String[]{
                        KEY_ID, KEY_NAME, KEY_IMG, KEY_HAS_CAR, KEY_ADDRESS},
                KEY_ID + " == '" + id + "'", null, null, null, null, null);

        return mCursor;
    }

}