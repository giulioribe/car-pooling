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
        persons.add(new Person("Matteo Matteini", 0, "", "Via Prinella 3, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Mirco Sciabola", 0, "", "Via Mortara 11, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Giovanni Plinio", 0, "", "Via Fossato di Mortara 3, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Rocco della Rocca", 0, "", "Via Modena 51, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Samantha Cristoforetti", 0, "", "Via Pomposa 18, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Biagio Biagini", 0, "", "Via Padova 15, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Filippo Rossini", 0, "", "Via Ragno 1, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Brava Giovanna", 0, "", "Via Porta Mare 16, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Michela Franchi", 0, "", "Via Wagner 15, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Paola Paolini", 0, "", "Via Garibaldi 33, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Filotte da Atene", 0, "", "Via Comacchio 88, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nicoletta del Colle", 0, "", "Via Coppare78, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Arisa Cantante", 0, "", "Via Krasnodar 54, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Lucia Linti", 0, "", "Corso Biagio Rossetti 31, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Pluto il Cane", 0, "", "Via Arrigo Boito 9, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Signor Disney", 0, "", "Via Comacchio 334, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Kylye Martini", 0, "", "Via Arginone 339, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Signor Google", 0, "", "Via Eridano 10, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Patrizia Piacentini", 0, "", "Via Bentivoglio 73, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Federica Quinta", 0, "", "Via Ladino 44, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Monica Caccia", 0, "", "Via Bologna 643, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Jacopo Ostuni", 0, "", "Via Giuseppe Fabbri 516, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Ernesto Sparalesto", 0, "", "Via della Misericordia 41, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Giovane Baldo", 0, "", "Via dell'Acero 2, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Figaro Figaro", 0, "", "Via Anna Banti 19, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Zio Paperone", 0, "", "Via Conca 26, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Albus Silente", 0, "", "Via Vallelunga 75, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Vittoria Dolce", 0, "", "Via Copparo 216, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Alberto Albertini", 0, "", "Via Pomposa 272, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Nessuno Arrivante", 0, "", "Via Comacchio 1175, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Riccardo Lupi", 0, "", "Via Provinciale 22, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Simone Simoni", 0, "", "Via Corazza 404, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Federico Lupi", 0, "", "Via Provinciale 22, 44100 Ferrara, Italia", new ArrayList<String>()));
        persons.add(new Person("Marcella Simoni", 0, "", "Via Corazza 404, 44100 Ferrara, Italia", new ArrayList<String>()));
        for (Person p : persons)
            PersonService.startAction(this, Costants.ACTION_CREATE, p);*/


    }

}
