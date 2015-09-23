package com.nego.carpooling;

import android.app.ActivityOptions;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Pair;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.Reader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Locale;

public class Follow extends AppCompatActivity {

    private Toolbar toolbar;
    private TextView button;
    private ArrayList<Person> persons;

    private Calendar calendar;
    private String location = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_follow);

        // TOOLBAR
        toolbar = (Toolbar) findViewById(R.id.my_awesome_toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        setTitle("");

        try {
            Calendar c = Calendar.getInstance();
            c.set(Calendar.HOUR_OF_DAY, 9);
            c.set(Calendar.MINUTE, 0);
            persons = getIntent().getParcelableArrayListExtra(Costants.EXTRA_PEOPLE_SELECTED);
            calendar = Calendar.getInstance();
            calendar.setTimeInMillis(getIntent().getLongExtra(Costants.EXTRA_TIME, c.getTimeInMillis()));
            location = getIntent().getStringExtra(Costants.EXTRA_PLACE);
        } catch (Exception e) {
            finish();
        }

        try {
            JSONObject toSend = new JSONObject();
            toSend.put(Costants.JSON_TIME_TO_ARRIVE, calendar.getTimeInMillis());
            toSend.put(Costants.JSON_PLACE_TO_ARRIVE, location);

            JSONArray users = new JSONArray();

            for (Person p : persons) {
                JSONObject json_p = new JSONObject();
                json_p.put(Costants.JSON_USER_ID, p.getId());
                json_p.put(Costants.JSON_USER_ADDRESS, p.getAddress());
                json_p.put(Costants.JSON_USER_MAX_DUR, p.getMax_dur());
                json_p.put(Costants.JSON_USER_NOT_WITH, Utils.arrayListToString(p.getNotWith()));
                json_p.put(Costants.JSON_USER_POP, Utils.arrayListToString(p.getPop()));
                users.put(json_p);
            }

            toSend.put(Costants.JSON_USERS, users);

        } catch (Exception e) {

        }

/*

        String uri = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=";
        String uri_dest = "&destinations=";

        String uri_o = "";
        int k = 0;
        for (Person p : persons) {
            String divider = "|";
            if (k == 0)
                divider = "";
            uri_o = uri_o + divider + Uri.encode(p.getAddress());
            k++;
        }

        String uri_lan = "&language=" + Locale.getDefault().getLanguage();
        String uri_key = "&key=AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8";
        new DownloadTask().execute(uri + uri_o + uri_dest + uri_o + uri_lan + uri_key);

        */

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_follow, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == android.R.id.home) {
            onBackPressed();
            return true;
        }

        if (id == R.id.action_share) {
            // TODO share content
        }


        return super.onOptionsItemSelected(item);
    }

    private class DownloadTask extends AsyncTask<JSONObject, Void, String> {

        @Override
        protected String doInBackground(JSONObject... params) {
            try {
                return loadFromNetwork(params[0].toString());
            } catch (IOException e) {
                return "Connection Error";
            }
        }

        /**
         * Uses the logging framework to display the output of the fetch
         * operation in the log fragment.
         */
        @Override
        protected void onPostExecute(String result) {
            JSONObject jsonObject = null;
            try {
                jsonObject = new JSONObject(result);
            } catch (Exception e) {}
            // TODO usare bene il  file json
            findViewById(R.id.loader).setVisibility(View.GONE);
            ((TextView) findViewById(R.id.text_distance)).setText(result);
        }
    }

    /** Initiates the fetch operation. */
    private String loadFromNetwork(String jsonString) throws IOException {
        InputStream stream = null;
        String str ="";

        try {
            stream = download(jsonString);
            str = readIt(stream);
        } finally {
            if (stream != null) {
                stream.close();
            }
        }
        return str;
    }


    private InputStream download(String jsonString) throws IOException {
        // BEGIN_INCLUDE(get_inputstream)

        final SharedPreferences SP = getSharedPreferences(Costants.PREFERENCES_COSTANT, Context.MODE_PRIVATE);

        //URL url = new URL(SP.getString(Costants.PREFERENCE_LAST_SERVER, ""));
        URL url = new URL("http://tommasoberlose.altervista.org/old/carpooling.php");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setReadTimeout(10000);
        conn.setConnectTimeout(15000);
        conn.setRequestMethod("POST");
        conn.setDoInput(true);
        conn.setDoOutput(true);
        conn.setRequestProperty("Accept", "application/json");
        conn.setRequestProperty("Content-type", "application/json");

        OutputStream os = conn.getOutputStream();
        BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(os, "UTF-8"));
        writer.write(jsonString, 0, jsonString.length());
        writer.flush();
        writer.close();
        os.close();

        // Start the query
        conn.connect();
        InputStream stream = conn.getInputStream();
        return stream;
        // END_INCLUDE(get_inputstream)
    }

    /** Reads an InputStream and converts it to a String.
     * @param stream InputStream containing HTML from targeted site.
     * @return String concatenated according to len parameter.
     * @throws java.io.IOException
     */
    private String readIt(InputStream stream) throws IOException {
        Reader reader = null;
        BufferedReader streamReader = new BufferedReader(new InputStreamReader(stream, "UTF-8"));
        StringBuilder responseStrBuilder = new StringBuilder();

        String inputStr;
        while ((inputStr = streamReader.readLine()) != null)
            responseStrBuilder.append(inputStr);
        return responseStrBuilder.toString();
    }
}
