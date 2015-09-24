package com.nego.carpooling;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.drawable.Drawable;
import android.location.Address;
import android.net.Uri;
import android.os.Handler;
import android.provider.ContactsContract;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.nego.carpooling.Functions.PersonService;

import java.util.ArrayList;

public class EditP extends AppCompatActivity {

    private String p_img = "";
    private Person person = null;
    private long max_dur = 0;
    private ArrayList<String> notWith = new ArrayList<>();
    private ArrayList<String> pop = new ArrayList<>();

    private EditText name;
    private EditText address;
    private ImageView img;
    private ImageView edit_img;
    private ImageView delete_img;
    private LinearLayout action_not_with;
    private LinearLayout action_max_dur;
    private TextView subtitle_not_with;
    private TextView subtitle_max_dur;

    private Handler mHandler;

    private ImageView save_button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_editp);

        Intent intent = getIntent();

        name = (EditText) findViewById(R.id.name);
        address = (EditText) findViewById(R.id.address);
        img = (ImageView) findViewById(R.id.p_image);
        edit_img = (ImageView) findViewById(R.id.action_edit_img);
        delete_img = (ImageView) findViewById(R.id.action_delete);
        save_button = (ImageView) findViewById(R.id.action_save);
        action_max_dur = (LinearLayout) findViewById(R.id.action_max_dur);
        action_not_with = (LinearLayout) findViewById(R.id.action_not_with);
        subtitle_max_dur = (TextView) findViewById(R.id.subtitle_max_dur);
        subtitle_not_with = (TextView) findViewById(R.id.subtitle_not_with);

        findViewById(R.id.action_back_pressed).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                onBackPressed();
            }
        });

        if (intent.getAction() != null && intent.getAction().equals(Costants.ACTION_EDIT_PERSON)) {
            Person p = intent.getParcelableExtra(Costants.EXTRA_PERSON);
            p_img = p.getImg();

            name.setText(p.getName());
            address.setText(p.getAddress());
            max_dur = p.getMax_dur();
            notWith = p.getNotWith();
            pop = p.getPop();

            person = p;
        }

        // SETTER IMG, MAX DUR, NOT WITH, POP
        setImg(p_img);
        setMax_dur(max_dur);
        setNotWith(notWith);
        setPop(pop);

        edit_img.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent getIntent = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                getIntent.setType("image/*");
                Intent chooserIntent = Intent.createChooser(getIntent, getString(R.string.choose_img));

                startActivityForResult(chooserIntent, Costants.CODE_REQUEST_IMG);
            }
        });


        // BUTTONS
        save_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                savePerson();
            }
        });

        if (person == null) {
            findViewById(R.id.action_choose_contact).setVisibility(View.VISIBLE);
            findViewById(R.id.action_choose_contact).setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent contact_intent = new Intent(Intent.ACTION_PICK, Uri.parse("content://contacts/people"));
                    contact_intent.setType(ContactsContract.Contacts.CONTENT_TYPE);
                    startActivityForResult(contact_intent, Costants.CODE_REQUEST_CONTACT);
                }
            });
        } else {
            findViewById(R.id.action_choose_contact).setVisibility(View.GONE);
        }

        action_max_dur.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final View dialogView = LayoutInflater.from(EditP.this).inflate(R.layout.dialog_max_dur, null);
                final Dialog dialog_max_dur = new Dialog(EditP.this, R.style.mDialog);
                ((EditText) dialogView.findViewById(R.id.hour)).setText("" + max_dur / 60);
                ((EditText) dialogView.findViewById(R.id.minute)).setText("" + (max_dur - (max_dur / 60) * 60));
                dialogView.findViewById(R.id.action_save).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        String hour = ((EditText) dialogView.findViewById(R.id.hour)).getText().toString();
                        String minute = ((EditText) dialogView.findViewById(R.id.minute)).getText().toString();
                        if (hour.equals(""))
                            hour = "0";
                        if (minute.equals(""))
                            minute = "0";
                        setMax_dur((Long.parseLong(hour) * 60) + Long.parseLong(minute));
                        dialog_max_dur.dismiss();
                    }
                });
                dialog_max_dur.setContentView(dialogView);
                dialog_max_dur.show();
            }
        });

        action_not_with.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(EditP.this, "Da fare...", Toast.LENGTH_SHORT).show();
            }
        });


        if (savedInstanceState != null) {
            p_img = savedInstanceState.getString(Costants.KEY_DIALOG_IMG);
            name.setText(savedInstanceState.getString(Costants.KEY_DIALOG_NAME));
            address.setText(savedInstanceState.getString(Costants.KEY_DIALOG_ADDRESS));
            if (p_img != null)
                setImg(p_img);
            setNotWith(Utils.stringToArrayList(savedInstanceState.getString(Costants.KEY_DIALOG_NOT_WITH)));
            setPop(Utils.stringToArrayList(savedInstanceState.getString(Costants.KEY_DIALOG_POP)));
            setMax_dur(savedInstanceState.getLong(Costants.KEY_DIALOG_MAX_DUR));
        }
    }

    @Override
    protected void onSaveInstanceState (Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putString(Costants.KEY_DIALOG_NAME, name.toString());
        outState.putString(Costants.KEY_DIALOG_IMG, p_img);
        outState.putString(Costants.KEY_DIALOG_ADDRESS, address.toString());
        outState.putLong(Costants.KEY_DIALOG_MAX_DUR, max_dur);
        outState.putString(Costants.KEY_DIALOG_NOT_WITH, Utils.arrayListToString(notWith));
        outState.putString(Costants.KEY_DIALOG_POP, Utils.arrayListToString(pop));
    }


    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == Costants.CODE_REQUEST_IMG && resultCode == Activity.RESULT_OK) {
            if (data != null) {
                Uri selectedImageURI = data.getData();
                setImg(selectedImageURI.toString());
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

            setPerson(name, address, photo);

            cursor.close();
        }
    }

    public void savePerson() {
        final String n = name.getText().toString();
        if (n.equals("")) {
            Utils.SnackbarC(this, "Inserisci un nome", name);
        } else {
            final String a = address.getText().toString();

            if (a.equals("")) {
                Utils.SnackbarC(this, "Inserisci un indirizzo", address);
            } else {
                save_button.setEnabled(false);
                mHandler = new Handler();

                new Thread(new Runnable() {
                    public void run() {
                        final Address postal_address = Utils.getLocationFromAddress(EditP.this, a);
                        mHandler.post(new Runnable() {
                            public void run() {
                                try {
                                    if (postal_address == null) {
                                        Utils.SnackbarC(EditP.this, "Indirizzo non valido", address);
                                        save_button.setEnabled(true);
                                    } else {
                                        if (person == null) {
                                            PersonService.startAction(EditP.this, Costants.ACTION_CREATE, new Person(n, max_dur, p_img, postal_address.getAddressLine(0) + ", " + postal_address.getAddressLine(1) + ", " + postal_address.getAddressLine(2), notWith, pop));
                                        } else {
                                            person.setName(n);
                                            person.setImg(p_img);
                                            person.setMax_dur(max_dur);
                                            person.setNotWith(notWith);
                                            person.setPop(pop);
                                            person.setAddress(postal_address.getAddressLine(0) + ", " + postal_address.getAddressLine(1) + ", " + postal_address.getAddressLine(2));
                                            PersonService.startAction(EditP.this, Costants.ACTION_UPDATE, person);
                                        }
                                        finish();
                                    }
                                } catch (Exception e) {
                                    Toast.makeText(EditP.this, e.toString(), Toast.LENGTH_SHORT).show();
                                }
                            }
                        });
                    }
                }).start();
            }
        }
    }

    public void setImg(String p_uri) {
        p_img = p_uri;
        if (p_uri.equals("")) {
            delete_img.setVisibility(View.GONE);
            img.setImageDrawable(ContextCompat.getDrawable(this, R.drawable.ic_person_null));
        } else {
            img.setImageURI(Uri.parse(p_img));
            Drawable d_img = img.getDrawable();
            if (d_img == null) {
                setImg("");
            }
            delete_img.setVisibility(View.VISIBLE);
            delete_img.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    new AlertDialog.Builder(EditP.this)
                            .setTitle("Attenzione")
                            .setMessage("Sicuro di voler eliminare questa foto?")
                            .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int whichButton) {
                                    setImg("");
                                }
                            })
                            .setNegativeButton(android.R.string.no, null).show();
                }
            });
        }
    }

    public void setPerson(String name_a, String address_a, String photo) {
        if (name_a != null)
            name.setText(name_a);
        if (address_a != null)
            address.setText(address_a);
        if (photo != null)
            setImg(photo);
    }

    public void setNotWith(ArrayList<String> arrayList) {
        notWith = arrayList;
        String text = "";
        String d = "";
        boolean first = true;
        for (String s : notWith) {
            text += d + s;
            if (first) {
                first = false;
                d = ", ";
            }
        }
        subtitle_not_with.setText(text);
    }

    public void setPop(ArrayList<String> arrayList) {
        pop = arrayList;
        String text = "";
        String d = "";
        boolean first = true;
        for (String s : notWith) {
            text += d + s;
            if (first) {
                first = false;
                d = ", ";
            }
        }
    }

    public void setMax_dur(long l) {
        max_dur = l;
        subtitle_max_dur.setText(Utils.formatDur(max_dur));
    }

}
