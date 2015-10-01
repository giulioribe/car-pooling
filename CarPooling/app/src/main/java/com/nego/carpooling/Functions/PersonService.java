package com.nego.carpooling.Functions;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.nego.carpooling.Costants;
import com.nego.carpooling.Person;
import com.nego.carpooling.database.DbAdapter;

public class PersonService extends IntentService {

    public static void startAction(Context context, String action, Person p) {
        Intent intent = new Intent(context, PersonService.class);
        intent.setAction(action);
        intent.putExtra(Costants.EXTRA_PERSON, p);
        context.startService(intent);
    }

    private void sendResponse(String s, Person p) {
        Intent i = new Intent(Costants.ACTION_UPDATE_LIST);
        i.putExtra(Costants.EXTRA_ACTION_TYPE, s);
        i.putExtra(Costants.EXTRA_PERSON, p);
        sendBroadcast(i);
    }

    public PersonService() {
        super("PersonService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        if (intent != null) {
            final String action = intent.getAction();
            if (Costants.ACTION_CREATE.equals(action)) {
                final Person person = intent.getParcelableExtra(Costants.EXTRA_PERSON);
                createPerson(person);
            } else if (Costants.ACTION_UPDATE.equals(action)) {
                final Person person = intent.getParcelableExtra(Costants.EXTRA_PERSON);
                updatePerson(person);
            } else if (Costants.ACTION_DELETE.equals(action)) {
                final Person person = intent.getParcelableExtra(Costants.EXTRA_PERSON);
                deletePerson(person);
            }
        }
    }

    private void createPerson(Person p) {
        DbAdapter dbHelper = new DbAdapter(this);
        dbHelper.open();
        if (p.create(dbHelper)) {
            sendResponse(Costants.ACTION_CREATE, p);
        }
        dbHelper.close();
    }

    private void updatePerson(Person p) {
        DbAdapter dbHelper = new DbAdapter(this);
        dbHelper.open();
        if (p.update(dbHelper)) {
            sendResponse(Costants.ACTION_UPDATE, p);
        }
        dbHelper.close();
    }

    private void deletePerson(Person p) {
        DbAdapter dbHelper = new DbAdapter(this);
        dbHelper.open();
        if (p.delete(dbHelper)) {
            sendResponse(Costants.ACTION_DELETE, p);
        }
        dbHelper.close();
    }

}
