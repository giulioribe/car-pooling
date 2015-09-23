package com.nego.carpooling;

import android.app.ActivityOptions;
import android.content.Intent;
import android.os.Build;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.transition.Transition;
import android.transition.TransitionValues;
import android.util.Pair;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.view.animation.AccelerateDecelerateInterpolator;
import android.widget.TextView;
import android.widget.Toast;

import com.nego.carpooling.database.DbAdapter;

import java.util.ArrayList;

public class Main extends AppCompatActivity {

    private TextView button_new_route;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        DbAdapter dbHelper = new DbAdapter(this);
        dbHelper.open();
        Person p = new Person("Tommaso Berlose", 0, "", new ArrayList(), "Via Otello Putinati 122, Ferrara", new ArrayList());
        p.create(dbHelper);
        dbHelper.close();

        button_new_route = (TextView) findViewById(R.id.button_new_route);
        button_new_route.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                    ActivityOptions options = ActivityOptions.makeSceneTransitionAnimation(Main.this,
                            Pair.create(findViewById(R.id.container), "toolbar"));

                    startActivity(new Intent(Main.this, ChoosePeople.class), options.toBundle());
                } else {
                    startActivity(new Intent(Main.this, ChoosePeople.class));
                }
            }
        });

    }

}
