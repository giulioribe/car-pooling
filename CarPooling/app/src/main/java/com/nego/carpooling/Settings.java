package com.nego.carpooling;

import android.app.Dialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.location.Address;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

public class Settings extends AppCompatActivity {

    private Toolbar toolbar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        // TOOLBAR
        toolbar = (Toolbar) findViewById(R.id.my_awesome_toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        final SharedPreferences SP = getSharedPreferences(Costants.PREFERENCES_COSTANT, Context.MODE_PRIVATE);

        String version = "";
        try {
            version = getString(R.string.text_version) + getPackageManager().getPackageInfo(getPackageName(), 0).versionName;
        } catch (Exception e) {

        }
        ((TextView) findViewById(R.id.text_version)).setText(version);

        ((TextView) findViewById(R.id.subtitle_server)).setText(SP.getString(Costants.PREFERENCE_LAST_SERVER, ""));
        findViewById(R.id.server_grid).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final View dialogView = LayoutInflater.from(Settings.this).inflate(R.layout.dialog_pa, null);
                final Dialog dialog_server = new Dialog(Settings.this, R.style.mDialog);
                ((EditText) dialogView.findViewById(R.id.address)).setText(SP.getString(Costants.PREFERENCE_LAST_SERVER, ""));
                dialogView.findViewById(R.id.action_save).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        final String a = ((EditText) dialogView.findViewById(R.id.address)).getText().toString();
                        if (a.equals("")) {
                            Utils.SnackbarC(Settings.this, "Inserisci un indirizzo", dialogView.findViewById(R.id.address));
                        } else {
                            SP.edit().putString(Costants.PREFERENCE_LAST_SERVER, a).apply();
                            ((TextView) findViewById(R.id.subtitle_server)).setText(a);
                            dialog_server.dismiss();
                        }
                    }
                });
                dialog_server.setContentView(dialogView);
                dialog_server.show();
            }
        });

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_settings, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.action_feedback) {
            return true;
        }

        if (id == android.R.id.home)
            onBackPressed();

        return super.onOptionsItemSelected(item);
    }
}
