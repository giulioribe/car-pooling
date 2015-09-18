package com.nego.carpooling;

import android.content.Intent;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import java.util.ArrayList;
import java.util.Calendar;

public class Follow extends AppCompatActivity {

    private Toolbar toolbar;
    private FloatingActionButton button;
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
}
