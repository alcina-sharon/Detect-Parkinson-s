package com.detectparkinson.john;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import static android.view.View.SCROLLBARS_INSIDE_OVERLAY;

public class fb extends AppCompatActivity {
    WebView web1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fb);
        web1 = (WebView) findViewById(R.id.webv);
        web1.setWebViewClient(new fb.MyBrowser());
        web1.getSettings().setLoadsImagesAutomatically(true);
        web1.getSettings().setJavaScriptEnabled(true);
        web1.setScrollBarStyle(SCROLLBARS_INSIDE_OVERLAY);
        web1.loadUrl("https://www.youtube.com/watch?v=63uNdFZLuy0");
    }

    class MyBrowser extends WebViewClient {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            view.loadUrl(url);
            return true;
        }
    }
};
