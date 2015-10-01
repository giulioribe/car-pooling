package com.nego.carpooling;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.location.Address;
import android.net.Uri;
import android.os.Handler;
import android.provider.ContactsContract;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.nego.carpooling.Functions.PersonService;

import java.util.ArrayList;


public class EditPerson extends AlertDialog {

    private Context mContext;
    private String p_img = "";
    private Person person = null;

    private EditText name;
    private EditText address;
    private ImageView img;
    private ImageView edit_img;
    private ImageView delete_img;

    private Handler mHandler;

    private TextView save_button;

    public EditPerson(final Context context, Intent intent, Bundle savedInstanceState) {
        super(context, R.style.Dialog_Pop);
        mContext = context;


        final View dialogView = LayoutInflater.from(context).inflate(R.layout.dialog_person, null);

        name = (EditText) dialogView.findViewById(R.id.name);
        address = (EditText) dialogView.findViewById(R.id.address);
        img = (ImageView) dialogView.findViewById(R.id.p_image);
        edit_img = (ImageView) dialogView.findViewById(R.id.action_edit_img);
        delete_img = (ImageView) dialogView.findViewById(R.id.action_delete);
        save_button = (TextView) dialogView.findViewById(R.id.action_save);

        if (intent.getAction() != null && intent.getAction().equals(Costants.ACTION_EDIT_PERSON)) {
            Person p = intent.getParcelableExtra(Costants.EXTRA_PERSON);
            p_img = p.getImg();

            name.setText(p.getName());
            address.setText(p.getAddress());

            person = p;
        }

        // IMG
        setImg(p_img);

        edit_img.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent getIntent = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                getIntent.setType("image/*");
                Intent chooserIntent = Intent.createChooser(getIntent, mContext.getString(R.string.choose_img));

                ((ChoosePeople) mContext).startActivityForResult(chooserIntent, Costants.CODE_REQUEST_IMG);
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
            dialogView.findViewById(R.id.action_choose_contact).setVisibility(View.VISIBLE);
            dialogView.findViewById(R.id.action_choose_contact).setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent contact_intent = new Intent(Intent.ACTION_PICK, Uri.parse("content://contacts/people"));
                    contact_intent.setType(ContactsContract.Contacts.CONTENT_TYPE);
                    ((ChoosePeople) mContext).startActivityForResult(contact_intent, Costants.CODE_REQUEST_CONTACT);
                }
            });
        } else {
            dialogView.findViewById(R.id.action_choose_contact).setVisibility(View.GONE);
        }


        if (savedInstanceState != null) {
            p_img = savedInstanceState.getString(Costants.KEY_DIALOG_IMG);
            name.setText(savedInstanceState.getString(Costants.KEY_DIALOG_NAME));
            address.setText(savedInstanceState.getString(Costants.KEY_DIALOG_ADDRESS));
            if (p_img != null)
                setImg(p_img);
        }

        this.setView(dialogView);
    }

    public void savePerson() {
        final String n = name.getText().toString();
        if (n.equals("")) {
            Utils.SnackbarC(mContext, "Inserisci un nome", name);
        } else {
            final String a = address.getText().toString();

            if (a.equals("")) {
                Utils.SnackbarC(mContext, "Inserisci un indirizzo", address);
            } else {
                save_button.setText("Valutazione indirizzo...");
                save_button.setEnabled(false);
                mHandler = new Handler();

                new Thread(new Runnable() {
                    public void run() {
                        final Address postal_address = Utils.getLocationFromAddress(mContext, a);
                        mHandler.post(new Runnable() {
                            public void run() {
                                try {
                                    if (postal_address == null) {
                                        Utils.SnackbarC(mContext, "Indirizzo non valido", address);
                                        save_button.setText("save");
                                        save_button.setEnabled(true);
                                    } else {
                                        if (person == null) {
                                            ArrayList<String> arrayList = new ArrayList<String>();
                                            arrayList.add("");
                                            PersonService.startAction(mContext, Costants.ACTION_CREATE, new Person(n, 0, p_img, postal_address.getAddressLine(0) + ", " + postal_address.getAddressLine(1) + ", " + postal_address.getAddressLine(2), arrayList, arrayList));
                                        } else {
                                            person.setName(n);
                                            person.setImg(p_img);
                                            person.setAddress(postal_address.getAddressLine(0) + ", " + postal_address.getAddressLine(1) + ", " + postal_address.getAddressLine(2));
                                            PersonService.startAction(mContext, Costants.ACTION_UPDATE, person);
                                        }
                                        dismiss();
                                    }
                                } catch (Exception e) {
                                    Toast.makeText(mContext, e.toString(), Toast.LENGTH_SHORT).show();
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
            img.setImageDrawable(ContextCompat.getDrawable(mContext, R.drawable.ic_person_null));
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
                    new AlertDialog.Builder(mContext)
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

    public ArrayList<String> saveIstance() {
        ArrayList<String> arrayList = new ArrayList<>();
        arrayList.add(name.getText().toString());
        arrayList.add(p_img);
        arrayList.add(address.getText().toString());
        return arrayList;
    }
}
