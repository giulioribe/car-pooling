package com.nego.carpooling;

import android.app.ActivityOptions;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.transition.Fade;
import android.util.Pair;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Locale;

public class CalculateDistances extends AppCompatActivity {

    private Toolbar toolbar;
    private FloatingActionButton button;
    private ArrayList<Person> persons;

    private Calendar calendar;
    private String location = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_calculate_distances);

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

        button = (FloatingActionButton) findViewById(R.id.next_button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent next = new Intent(CalculateDistances.this, Follow.class);

                next.putParcelableArrayListExtra(Costants.EXTRA_PEOPLE_SELECTED, persons);
                next.putExtra(Costants.EXTRA_TIME, calendar.getTimeInMillis());
                next.putExtra(Costants.EXTRA_PLACE, location);

                // TODO aggiungere le varie preferenze

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                    ActivityOptions options = ActivityOptions.makeSceneTransitionAnimation(CalculateDistances.this,
                            Pair.create((View) button, "floating_button"),
                            Pair.create(findViewById(R.id.line_t), "line_t"),
                            Pair.create(findViewById(R.id.action_pref), "grid_container"));

                    startActivity(next, options.toBundle());
                } else {
                    startActivity(next);
                }
            }
        });


        String uri = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=";
        String uri_dest = "&destinations=";

        String uri_o = "";
        String uri_d = "";
        int k = 0;
        for (Person p : persons) {
            String divider = "|";
            if (k == 0)
                divider = "";
            uri_o = uri_o + divider + Uri.encode(p.getAddress());
            uri_d = uri_d + divider + Uri.encode(p.getAddress());
            k++;
        }

        String uri_lan = "&language=" + Locale.getDefault().getLanguage();
        String uri_key = "&key=AIzaSyB27xz94JVRPsuX4qJMMiZpGVoQiQITFb8";
        new DownloadTask().execute(uri + uri_o + uri_dest + uri_d + uri_lan + uri_key);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_calculate_distances, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == android.R.id.home) {
            onBackPressed();
            return true;
        }

        if (id == R.id.action_help) {
            startActivity(new Intent(this, Help.class));
        }

        return super.onOptionsItemSelected(item);
    }

    /**
     * Implementation of AsyncTask, to fetch the data in the background away from
     * the UI thread.
     */
    private class DownloadTask extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... urls) {
            try {
                return loadFromNetwork(urls[0]);
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
                jsonObject = new JSONObject(result.toString());
            } catch (Exception e) {}
            // TODO usare bene il  file json
            findViewById(R.id.loader).setVisibility(View.GONE);
            ((TextView) findViewById(R.id.text_distance)).setText(result);
        }
    }

    /** Initiates the fetch operation. */
    private String loadFromNetwork(String urlString) throws IOException {
        InputStream stream = null;
        String str ="";

        try {
            stream = downloadUrl(urlString);
            str = readIt(stream);
        } finally {
            if (stream != null) {
                stream.close();
            }
        }
        return str;
    }

    /**
     * Given a string representation of a URL, sets up a connection and gets
     * an input stream.
     * @param urlString A string representation of a URL.
     * @return An InputStream retrieved from a successful HttpURLConnection.
     * @throws java.io.IOException
     */
    private InputStream downloadUrl(String urlString) throws IOException {
        // BEGIN_INCLUDE(get_inputstream)
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setReadTimeout(10000 /* milliseconds */);
        conn.setConnectTimeout(15000 /* milliseconds */);
        conn.setRequestMethod("GET");
        conn.setDoInput(true);
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
