package com.detectparkinson.john;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import static android.view.View.SCROLLBARS_INSIDE_OVERLAY;

public class test2 extends AppCompatActivity {

    WebView web2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test2);
        web2 = (WebView) findViewById(R.id.web3);
        web2.setWebViewClient(new test2.MyBrowser());
        web2.getSettings().setLoadsImagesAutomatically(true);
        web2.getSettings().setJavaScriptEnabled(true);
        web2.setScrollBarStyle(SCROLLBARS_INSIDE_OVERLAY);
        web2.loadUrl("https://www.youtube.com/");
    }

    class MyBrowser extends WebViewClient {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            view.loadUrl(url);
            return true;
        }
    }
};
