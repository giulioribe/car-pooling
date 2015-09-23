package com.nego.carpooling;

import android.app.Activity;
import android.app.ActivityOptions;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.provider.ContactsContract;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.transition.Explode;
import android.transition.Fade;
import android.util.Pair;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.view.animation.AccelerateDecelerateInterpolator;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.nego.carpooling.Adapter.MyAdapter;
import com.nego.carpooling.database.DbAdapter;

import java.util.ArrayList;

public class ChoosePeople extends AppCompatActivity {

    private Toolbar toolbar;
    private RecyclerView grid_people;
    private EditPerson dialogPerson;
    private TextView button;

    private BroadcastReceiver mReceiver;
    private MyAdapter mAdapter;
    private DbAdapter dbHelper;
    private Bundle savedInstanceState;

    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choosepeople);
        this.savedInstanceState = savedInstanceState;

        // TOOLBAR
        toolbar = (Toolbar) findViewById(R.id.my_awesome_toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        setTitle("");

        button = (TextView) findViewById(R.id.next_button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent next = new Intent(ChoosePeople.this, Preferences.class);
                next.putParcelableArrayListExtra(Costants.EXTRA_PEOPLE_SELECTED, mAdapter.getSelectedItem());

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                    ActivityOptions options = ActivityOptions.makeSceneTransitionAnimation(ChoosePeople.this,
                            Pair.create(findViewById(R.id.line_t), "line_t"),
                            Pair.create((View) button, "floating_button"),
                            Pair.create(findViewById(R.id.card_grid), "grid_container"));

                    startActivity(next, options.toBundle());
                } else {
                    startActivity(next);
                }
            }
        });

        grid_people = (RecyclerView) findViewById(R.id.grid_people);
        grid_people.setHasFixedSize(true);
        LinearLayoutManager llm = new LinearLayoutManager(this);
        llm.setOrientation(LinearLayoutManager.VERTICAL);
        grid_people.setLayoutManager(llm);
        doList();

        if (savedInstanceState != null) {
            if (savedInstanceState.getBoolean(Costants.KEY_DIALOG_OPEN)) {
                dialogPerson = new EditPerson(ChoosePeople.this, new Intent(), savedInstanceState);
                dialogPerson.show();
                savedInstanceState.remove(Costants.KEY_DIALOG_OPEN);
            }
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_choose_people, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == android.R.id.home) {
            onBackPressed();
            return true;
        }

        if (id == R.id.new_person) {
            dialogPerson = new EditPerson(ChoosePeople.this, new Intent(), savedInstanceState);
            dialogPerson.show();
        }

        return super.onOptionsItemSelected(item);
    }

    public void doList() {
        findViewById(R.id.loader).animate().alpha(1).start();
        grid_people.animate().alpha(0).start();
        final Handler mHandler = new Handler();

        new Thread(new Runnable() {
            public void run() {
                dbHelper = new DbAdapter(ChoosePeople.this);
                dbHelper.open();
                final int count = dbHelper.fetchAllPersons().getCount();
                mAdapter = new MyAdapter(dbHelper, ChoosePeople.this);
                dbHelper.close();

                mHandler.post(new Runnable() {
                    public void run() {
                        grid_people.setAdapter(mAdapter);
                        if (count != 0) {
                            findViewById(R.id.no_persons).setVisibility(View.GONE);
                        } else {
                            findViewById(R.id.no_persons).setVisibility(View.VISIBLE);
                        }
                        if (savedInstanceState != null && savedInstanceState.getParcelableArrayList(Costants.KEY_PEOPLE_SELECTED) != null) {
                            mAdapter.setSelected(savedInstanceState);
                            savedInstanceState.remove(Costants.KEY_PEOPLE_SELECTED);
                        }
                        findViewById(R.id.loader).animate().alpha(0).start();
                        countPeople();
                        grid_people.animate().alpha(1).start();
                    }
                });
            }
        }).start();
    }

    @Override
    public void onBackPressed() {
        if (mAdapter != null && mAdapter.getSelectedItemCount() > 0) {
            mAdapter.clearSelections();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        IntentFilter intentFilter = new IntentFilter(Costants.ACTION_UPDATE_LIST);

        mReceiver = new BroadcastReceiver() {

            @Override
            public void onReceive(Context context, Intent intent) {
                doList();
            }
        };
        registerReceiver(mReceiver, intentFilter);
    }

    @Override
    public void onPause() {
        unregisterReceiver(mReceiver);
        super.onPause();
    }

    @Override
    protected void onSaveInstanceState (Bundle outState) {
        super.onSaveInstanceState(outState);
        if (dialogPerson != null && dialogPerson.isShowing()) {
            outState.putBoolean(Costants.KEY_DIALOG_OPEN, true);
            ArrayList<String> all = dialogPerson.saveIstance();
            outState.putString(Costants.KEY_DIALOG_NAME, all.get(0));
            outState.putString(Costants.KEY_DIALOG_IMG, all.get(1));
            outState.putString(Costants.KEY_DIALOG_ADDRESS, all.get(2));
        } else {
            outState.putBoolean(Costants.KEY_DIALOG_OPEN, false);
        }

        if (mAdapter != null && mAdapter.getSelectedItemCount() > 0)
            outState.putParcelableArrayList(Costants.KEY_PEOPLE_SELECTED, mAdapter.getSelectedItem());
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == Costants.CODE_REQUEST_IMG && resultCode == Activity.RESULT_OK) {
            if (data != null) {
                Uri selectedImageURI = data.getData();
                dialogPerson.setImg(selectedImageURI.toString());
            }
        } else if (requestCode == Costants.CODE_REQUEST_CONTACT && resultCode == Activity.RESULT_OK) {
            Uri contactData = data.getData();

            String name = "";
            String address = "";
            String photo = "";
            long id = 0;

            Cursor cursor = getContentResolver().query(contactData, null, null, null, null);
            if (cursor.moveToFirst()) {
                name = cursor.getString(cursor.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME));
                photo = cursor.getString(cursor.getColumnIndex(ContactsContract.Contacts.PHOTO_URI));
                id = cursor.getLong(cursor.getColumnIndex(ContactsContract.Contacts._ID));

            }
            cursor.close();

            cursor = getContentResolver().query(ContactsContract.Data.CONTENT_URI,
                    new String[]{ ContactsContract.CommonDataKinds.StructuredPostal.FORMATTED_ADDRESS,
                            ContactsContract.CommonDataKinds.StructuredPostal.CITY},
                    ContactsContract.Data.CONTACT_ID + "=? AND " +
                            ContactsContract.CommonDataKinds.StructuredPostal.MIMETYPE + "=?",
                    new String[]{String.valueOf(id), ContactsContract.CommonDataKinds.StructuredPostal.CONTENT_ITEM_TYPE},
                    null);
            if (cursor.moveToFirst()) {
                address = cursor.getString(cursor.getColumnIndex(ContactsContract.CommonDataKinds.StructuredPostal.FORMATTED_ADDRESS));
            }

            dialogPerson.setPerson(name, address, photo);

            cursor.close();
        }
    }

    public void editPerson(Person person) {
        Intent i = new Intent(Costants.ACTION_EDIT_PERSON);
        i.putExtra(Costants.EXTRA_PERSON, person);
        dialogPerson = new EditPerson(this, i, savedInstanceState);
        dialogPerson.show();
    }

    public void countPeople() {
        if (mAdapter.getSelectedItemCount() > 0) {
            findViewById(R.id.button_layout).setVisibility(View.VISIBLE);
        } else {
            findViewById(R.id.button_layout).setVisibility(View.GONE);
        }
    }

}
