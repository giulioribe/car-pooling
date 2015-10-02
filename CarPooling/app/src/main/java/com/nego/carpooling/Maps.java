package com.nego.carpooling;

import android.location.Address;
import android.net.Uri;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.RelativeLayout;
import android.widget.Toast;

public class Maps extends AppCompatActivity {

    private Toolbar toolbar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        // TOOLBAR
        toolbar = (Toolbar) findViewById(R.id.my_awesome_toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        setTitle(R.string.title_activity_maps);

        if (getIntent().getStringExtra(Costants.EXTRA_MAP_DATA) != null)
            uploadMap(getIntent().getStringExtra(Costants.EXTRA_MAP_DATA));
        else
            finish();

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == android.R.id.home) {
            onBackPressed();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    public void uploadMap(String url) {
        WebView webview = (WebView) findViewById(R.id.map);
        webview.setWebViewClient(new WebViewClient());
        WebSettings webSettings = webview.getSettings();
        webSettings.setJavaScriptEnabled(true);

        try {
            webview.loadUrl(url);
            findViewById(R.id.loader).setVisibility(View.GONE);
            findViewById(R.id.map).setVisibility(View.VISIBLE);
        } catch (Exception e) {
            Toast.makeText(Maps.this, "Errore", Toast.LENGTH_SHORT).show();
            Log.i("errore_map_get_address", e.toString());
        }
    }

}
