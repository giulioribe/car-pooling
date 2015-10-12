package com.nego.carpooling;

import android.app.ActivityOptions;
import android.content.Intent;
import android.os.Build;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.transition.Fade;
import android.transition.Slide;
import android.transition.Transition;
import android.transition.TransitionValues;
import android.util.Pair;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.view.animation.AccelerateDecelerateInterpolator;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.nego.carpooling.Functions.PersonService;
import com.nego.carpooling.database.DbAdapter;

import java.util.ArrayList;
import java.util.Calendar;

public class Main extends AppCompatActivity {

    private TextView button_new_route;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        button_new_route = (TextView) findViewById(R.id.button_new_route);
        button_new_route.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Main.this, ChoosePeople.class));
            }
        });

        ArrayList<Person> persons = new ArrayList<>();/*
        persons.add(new Person("Riccardo Frantini", 0, "", "Via Giuseppe Fabbri 11, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Mirco Contri", 0, "", "Via Saragat 1, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Federico Spinardi", 0, "", "Via Nazionale 77, 45030 Occhiobello, Italia", new ArrayList<String>()));
        persons.add(new Person("Francesca Filippini", 0, "", "Via Bologna 11, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Giulia Crismi", 0, "", "Via Palestro 22, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Cristiano Lepri", 0, "", "Via Pomposa 48, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Rita Petruccini", 0, "", "Via Porta Reno 24, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Asfolso D'Este", 0, "", "Via Corso Giovecca 1, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Matteo Matteini", 0, "", "Via Prinella 3, 44100 Ferrara, Italia", new ArrayList<String>()));*/
        /*
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nome", 0, "", "Via , 44100 Ferrara, Italia", new ArrayList<String>()));*/
        /*for (Person p : persons)
            PersonService.startAction(this, Costants.ACTION_CREATE, p);*/


    }

}
