package com.nego.carpooling;

import android.app.ActivityOptions;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.database.Cursor;
import android.location.Address;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.util.Pair;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.nego.carpooling.database.DbAdapter;

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
        setTitle(R.string.title_activity_follow);

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
                json_p.put(Costants.JSON_USER_ID, "" + p.getId());
                json_p.put(Costants.JSON_USER_ADDRESS, p.getAddress());
                json_p.put(Costants.JSON_USER_MAX_DUR, p.getMax_dur() * 60 * 1000);
                json_p.put(Costants.JSON_USER_NOT_WITH, Utils.arrayListToString(p.getNotWith()));
                json_p.put(Costants.JSON_USER_POP, Utils.arrayListToString(p.getPop()));
                users.put(json_p);
            }

            toSend.put(Costants.JSON_USERS, users);
            new DownloadTask().execute(toSend);

        } catch (Exception e) {
            Log.i("creazione json", e.toString());
        }
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


        return super.onOptionsItemSelected(item);
    }

    private class DownloadTask extends AsyncTask<JSONObject, Void, String> {

        @Override
        protected String doInBackground(JSONObject... params) {
            try {
                return loadFromNetwork(params[0].toString());
            } catch (IOException e) {
                return "Connection Error: " + e.toString();
            }
        }

        @Override
        protected void onPostExecute(String result) {
            JSONObject jsonObject;
            try {
                Log.i("result", result);
                jsonObject = new JSONObject(result);
                setResult(jsonObject);
            } catch (Exception e) {
                Log.i("error_json", e.toString());
                Toast.makeText(Follow.this, result, Toast.LENGTH_SHORT).show();
            }
        }
    }

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

        URL url = new URL(SP.getString(Costants.PREFERENCE_LAST_SERVER, ""));
        //URL url = new URL("http://tommasoberlose.altervista.org/old/carpooling.php");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setReadTimeout(60000);
        conn.setConnectTimeout(60000);
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

    private String destinations = "";
    private String toSend = "";
    private String getData = "";

    public void setResult(JSONObject jsonObj) {
        try {
            findViewById(R.id.loader).setVisibility(View.GONE);
            LinearLayout container = (LinearLayout) findViewById(R.id.container_result);
            container.removeAllViews();

            // Prendo tutte le euristiche
            JSONObject jsonArrayEuristiche = jsonObj.getJSONObject(Costants.JSON_RESPONSE_EURISTICHE);
            String jsonArrayName = jsonArrayEuristiche.getString(Costants.JSON_RESPONSE_NAME);
            JSONObject jsonArrayResults = jsonArrayEuristiche.getJSONObject(Costants.JSON_RESPONSE_RESULTS);

            String[] names = jsonArrayName.split(",");

            for (int e = 0; e < jsonArrayResults.length(); e++) {
                boolean first = true;

                toSend = "";
                if (e != 0)
                    toSend += "\n";
                View card_layout = LayoutInflater.from(this).inflate(R.layout.card_layout, null);
                JSONObject js = jsonArrayResults.getJSONObject(names[e]);
                destinations = "";

                JSONArray cars = js.getJSONArray(Costants.JSON_RESPONSE_CARS);
                String cost = js.getString(Costants.JSON_RESPONSE_COSTO);
                for (int k = 0; k < cars.length(); k++) {
                    getData = "";

                    String car_id = (cars.getJSONObject(k)).getString(Costants.JSON_RESPONSE_ID);
                    String car_partenze = (cars.getJSONObject(k)).getString(Costants.JSON_RESPONSE_PARTENZE);

                    String[] ids = car_id.split(",");
                    String[] partenze_s = car_partenze.split(",");
                    for (int i = 0; i < ids.length; i++) {
                        String id = ids[i];
                        String orario = partenze_s[i];
                        String name = "";
                        String address = "";
                        for (Person p : persons) {
                            if (id.equals("" + p.getId())) {
                                name = p.getName();
                                address = p.getAddress();
                                break;
                            }
                        }

                        View layout = LayoutInflater.from(this).inflate(R.layout.layout_euristiche, null);
                        ((TextView) layout.findViewById(R.id.name)).setText(name);
                        ((TextView) layout.findViewById(R.id.partenza)).setText(Utils.getHour(this, Long.parseLong(orario)));

                        getData = id + "_" + Uri.encode(name) + "_" + Uri.encode(address);

                        toSend += name;

                        if (i != 0) {
                            layout.findViewById(R.id.auto).setVisibility(View.INVISIBLE);
                        } else {
                            layout.findViewById(R.id.auto).setVisibility(View.VISIBLE);
                        }
                        if (i != (ids.length - 1)) {
                            layout.findViewById(R.id.show_route_container).setVisibility(View.GONE);
                            layout.findViewById(R.id.action_view_route).setOnClickListener(null);
                        } else {
                            layout.findViewById(R.id.show_route_container).setVisibility(View.VISIBLE);
                            ((TextView)layout.findViewById(R.id.action_view_route)).setText("http://giulioribe.github.io/car-pooling/directions.html?dataM=" + getData + "&dataD=" + Uri.encode(location));
                            layout.findViewById(R.id.action_view_route).setOnClickListener(new View.OnClickListener() {
                                @Override
                                public void onClick(View v) {
                                    Intent i = new Intent(Follow.this, Maps.class);
                                    i.putExtra(Costants.EXTRA_MAP_DATA, "http://giulioribe.github.io/car-pooling/directions.html?dataM=" + getData + "&dataD=" + Uri.encode(location));

                                    startActivity(i);
                                }
                            });
                        }
                        toSend += "\n" + Utils.getHour(this, Long.parseLong(orario));
                        ((LinearLayout) card_layout.findViewById(R.id.card_container)).addView(layout);
                    }
                }
                ((TextView) card_layout.findViewById(R.id.title_e)).setText("Euristica " + names[e]);
                ((TextView) card_layout.findViewById(R.id.costo_e)).setText("Costo: " + cost + "m");
                card_layout.findViewById(R.id.action_share).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        Intent sendIntent = new Intent();
                        sendIntent.setAction(Intent.ACTION_SEND);
                        sendIntent.putExtra(Intent.EXTRA_TEXT, toSend);
                        sendIntent.setType("text/plain");
                        try {
                            startActivity(sendIntent);
                        } catch (Exception ex) {
                        }
                    }
                });
                container.addView(card_layout);

            }
        } catch (Exception e) {
            Log.i("error", e.toString());
        }
    }
}
