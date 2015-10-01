package com.nego.carpooling;

import android.app.ActivityOptions;
import android.app.Dialog;
import android.app.TimePickerDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.location.Address;
import android.os.Build;
import android.os.Handler;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.internal.view.ContextThemeWrapper;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.transition.Explode;
import android.transition.Fade;
import android.util.Pair;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.view.animation.AccelerateDecelerateInterpolator;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.TimePicker;

import com.nego.carpooling.Adapter.PersonImageAdapter;

import java.util.ArrayList;
import java.util.Calendar;

public class Preferences extends AppCompatActivity {

    private Toolbar toolbar;
    private TextView button;
    private ArrayList<Person> persons;

    private Calendar calendar;
    private Context mContextPicker;
    private String location = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preferences);


        if (Utils.isBrokenSamsungDevice()) {
            mContextPicker = new ContextThemeWrapper(this, android.R.style.Theme_Holo_Light_Dialog);
        } else {
            mContextPicker = this;
        }

        try {
            persons = getIntent().getParcelableArrayListExtra(Costants.EXTRA_PEOPLE_SELECTED);
        } catch (Exception e) {
            finish();
        }

        // TOOLBAR
        toolbar = (Toolbar) findViewById(R.id.my_awesome_toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        setTitle(R.string.title_activity_preferences);

        button = (TextView) findViewById(R.id.next_button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent next = new Intent(Preferences.this, Follow.class);

                next.putParcelableArrayListExtra(Costants.EXTRA_PEOPLE_SELECTED, persons);
                next.putExtra(Costants.EXTRA_TIME, calendar.getTimeInMillis());
                next.putExtra(Costants.EXTRA_PLACE, location);

                startActivity(next);
            }
        });


        calendar = Calendar.getInstance();
        if (savedInstanceState != null) {
            // TODO ripristina altre preferenze
            calendar.set(Calendar.HOUR_OF_DAY, savedInstanceState.getInt(Costants.KEY_PREFERENCES_CALENDAR_H));
            calendar.set(Calendar.MINUTE, savedInstanceState.getInt(Costants.KEY_PREFERENCES_CALENDAR_M));
            setLocation(savedInstanceState.getString(Costants.KEY_PREFERENCES_LOCATION));
        } else {
            calendar.setTimeInMillis(Utils.getFutureTime(this));
            SharedPreferences SP = getSharedPreferences(Costants.PREFERENCES_COSTANT, Context.MODE_PRIVATE);
            setLocation(SP.getString(Costants.KEY_LAST_PLACE, ""));
        }
        ((TextView) findViewById(R.id.time_to_arrive)).setText(Utils.getTime(this, calendar.getTimeInMillis()));

        findViewById(R.id.action_eta).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                TimePickerDialog mTimePicker = new TimePickerDialog(mContextPicker, R.style.mDialog_Picker, new TimePickerDialog.OnTimeSetListener() {
                    @Override
                    public void onTimeSet(TimePicker timePicker, int selectedHour, int selectedMinute) {
                        calendar.set(Calendar.HOUR_OF_DAY, selectedHour);
                        calendar.set(Calendar.MINUTE, selectedMinute);
                        if (Utils.isOldDate(calendar.getTimeInMillis()))
                            calendar.add(Calendar.DAY_OF_MONTH, 1);
                        else
                            calendar.set(Calendar.DAY_OF_MONTH, Calendar.getInstance().get(Calendar.DAY_OF_MONTH));
                        ((TextView) findViewById(R.id.time_to_arrive)).setText(Utils.getTime(Preferences.this, calendar.getTimeInMillis()));
                        checkGo();
                    }
                }, calendar.get(Calendar.HOUR_OF_DAY), calendar.get(Calendar.MINUTE), true);
                mTimePicker.show();
            }
        });

        findViewById(R.id.action_place).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final View dialogView = LayoutInflater.from(Preferences.this).inflate(R.layout.dialog_pa, null);
                final Dialog dialog_arrivo = new Dialog(Preferences.this, R.style.mDialog);
                ((EditText) dialogView.findViewById(R.id.address)).setText(location);
                dialogView.findViewById(R.id.action_save).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        final String a = ((EditText) dialogView.findViewById(R.id.address)).getText().toString();
                        if (a.equals("")) {
                            Utils.SnackbarC(Preferences.this, "Inserisci un indirizzo", dialogView.findViewById(R.id.address));
                        } else {
                            ((TextView) dialogView.findViewById(R.id.action_save)).setText("Valutazione indirizzo...");
                            dialogView.findViewById(R.id.action_save).setEnabled(false);
                            final Handler mHandler = new Handler();

                            new Thread(new Runnable() {
                                public void run() {
                                    final Address postal_address = Utils.getLocationFromAddress(Preferences.this, a);
                                    mHandler.post(new Runnable() {
                                        public void run() {
                                            if (postal_address == null) {
                                                Utils.SnackbarC(Preferences.this, "Indirizzo non valido", dialogView.findViewById(R.id.address));
                                                ((TextView) dialogView.findViewById(R.id.action_save)).setText("save");
                                                dialogView.findViewById(R.id.action_save).setEnabled(true);
                                            } else {
                                                setLocation(postal_address.getAddressLine(0) + ", " + postal_address.getAddressLine(1) + ", " + postal_address.getAddressLine(2));
                                                dialog_arrivo.dismiss();
                                            }
                                        }
                                    });
                                }
                            }).start();
                        }
                    }
                });
                dialog_arrivo.setContentView(dialogView);
                dialog_arrivo.show();
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_preferences, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == android.R.id.home) {
            onBackPressed();
            return true;
        }

        if (id == R.id.action_settings) {
            startActivity(new Intent(this, Settings.class));
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onSaveInstanceState (Bundle outState) {
        super.onSaveInstanceState(outState);
        // TODO salva altre preferenze
        outState.putInt(Costants.KEY_PREFERENCES_CALENDAR_H, calendar.get(Calendar.HOUR_OF_DAY));
        outState.putInt(Costants.KEY_PREFERENCES_CALENDAR_M, calendar.get(Calendar.MINUTE));
        outState.putString(Costants.KEY_PREFERENCES_LOCATION, location);
    }

    public void setLocation(String l) {
        location = l;
        if (location.equals("")) {
            ((TextView) findViewById(R.id.place_to_arrive)).setText("Undefined");
        } else {
            SharedPreferences SP = getSharedPreferences(Costants.PREFERENCES_COSTANT, Context.MODE_PRIVATE);
            SP.edit().putString(Costants.KEY_LAST_PLACE, location).apply();
            ((TextView) findViewById(R.id.place_to_arrive)).setText(location);
        }
        checkGo();
    }

    public void checkGo() {
        if (!location.equals("")) {
            button.animate().scaleX(1).scaleY(1).setInterpolator(new AccelerateDecelerateInterpolator()).start();
        } else {
            button.animate().scaleX(0).scaleY(0).setInterpolator(new AccelerateDecelerateInterpolator()).start();
        }
    }
}
