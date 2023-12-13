package com.sanbot.capaBot;

import com.sanbot.opensdk.function.unit.interfaces.hardware.TouchSensorListener;
import static com.sanbot.capaBot.MyUtils.concludeSpeak;

import android.media.AudioAttributes;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import android.os.AsyncTask;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.TextView;

import com.sanbot.opensdk.base.TopBaseActivity;
import com.sanbot.opensdk.beans.FuncConstant;
import com.sanbot.opensdk.function.beans.headmotion.LocateAbsoluteAngleHeadMotion;
import com.sanbot.opensdk.function.beans.speech.Grammar;
import com.sanbot.opensdk.function.beans.speech.RecognizeTextBean;
import com.sanbot.opensdk.function.unit.HardWareManager;
import com.sanbot.opensdk.function.unit.HeadMotionManager;
import com.sanbot.opensdk.function.unit.ModularMotionManager;
import com.sanbot.opensdk.function.unit.SpeechManager;
import com.sanbot.opensdk.function.unit.WheelMotionManager;
import com.sanbot.opensdk.function.unit.WingMotionManager;
import com.sanbot.opensdk.function.unit.interfaces.speech.RecognizeListener;
import com.sanbot.opensdk.function.unit.interfaces.speech.WakenListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.nio.charset.StandardCharsets;
import java.util.Objects;

import butterknife.BindView;
import butterknife.ButterKnife;


/**
 * Handles the Dialog with a person
 * Gets the pronounced sentence with speech recognition and answers with Text to Speech.
 * if specific intentions are recognized starts another activity to handle them
 * if the dialog is open (no tasks asked) the Conversational Engine handles an answer.
 *
 * NOTE: "wake up" in this context (according to the SDK) means start listening, "sleep" means stop listening
 */
public class MyDialogActivity extends TopBaseActivity {

    private final static String TAG = "IGOR-DIAL";

    private final static String TAG_T = "Touch";

    //view
    @BindView(R.id.tv_speech_recognize_result)
    TextView tvSpeechRecognizeResult;
    @BindView(R.id.imageListen)
    TextView imageListen;
    @BindView(R.id.wake)
    Button wakeButton;

    @BindView(R.id.exit)
    Button exitButton;

    @BindView(R.id.webview)
    WebView web;

    /** MY VARIABLES */
    private SpeechManager speechManager;    //speech
    private HardWareManager hardWareManager;    //leds
    private HeadMotionManager headMotionManager;    //head movements
    private WheelMotionManager wheelMotionManager;    //หมุนตัว
    private WingMotionManager wingMotionManager;    //head movements
    private ModularMotionManager modularMotionManager; //follow

    LocateAbsoluteAngleHeadMotion locateAbsoluteAngleHeadMotion = new LocateAbsoluteAngleHeadMotion(
            LocateAbsoluteAngleHeadMotion.ACTION_VERTICAL_LOCK,90,30
    );

    String lastRecognizedSentence = " ";
    String messageApi = " ";
    String ApiUrl = "... /receive-data"; // run on ngrok
    Handler noResponseAction = new Handler();
    Handler speechResponseHandler = new Handler();

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    public void onCreate(Bundle savedInstanceState) {
        register(MyDialogActivity.class);
        //The screen is always on
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        super.onCreate(savedInstanceState);
        //layout
        setContentView(R.layout.activity_dialog);
        ButterKnife.bind(this);

        web = findViewById(R.id.webview);
        web.getSettings().setMediaPlaybackRequiresUserGesture(false);

        web.getSettings().setJavaScriptEnabled(true);
        web.getSettings().setDomStorageEnabled(true);

        web.setWebChromeClient(new WebChromeClient());
        web.setWebViewClient(new WebViewClient());

        web.loadUrl("... /index.html");

        //Initialize managers
        speechManager = (SpeechManager) getUnitManager(FuncConstant.SPEECH_MANAGER);
        // systemManager = (SystemManager) getUnitManager(FuncConstant.SYSTEM_MANAGER);
        hardWareManager = (HardWareManager) getUnitManager(FuncConstant.HARDWARE_MANAGER);
        headMotionManager = (HeadMotionManager) getUnitManager(FuncConstant.HEADMOTION_MANAGER);
        wheelMotionManager = (WheelMotionManager)getUnitManager(FuncConstant.WHEELMOTION_MANAGER);
        wingMotionManager = (WingMotionManager)getUnitManager(FuncConstant.WINGMOTION_MANAGER);
        modularMotionManager = (ModularMotionManager) getUnitManager(FuncConstant.MODULARMOTION_MANAGER);

        //listeners
        initListener();

        //initialize listeners of hardware
        initHardwareListeners();

        //wake button, useful for people that have to wait so much to speak that the robot goes to sleep
        wakeButton.setVisibility(View.GONE);
        wakeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                wakeUpListening();
            }
        });

        //exit button
        exitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //force stop listening
                speechManager.doSleep();
                //starts base activity
                Intent myIntent = new Intent(MyDialogActivity.this, MyBaseActivity.class);
                MyDialogActivity.this.startActivity(myIntent);
                //terminates
                finish();
            }
        });

        //Robot head up, ask what to do, and wake up listening
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                //head up
                headMotionManager.doAbsoluteLocateMotion(locateAbsoluteAngleHeadMotion);
                //wake up
                wakeUpListening();
            }
        }, 200);

    }

    /**
     * Initialize the listener
     */
    private void initListener() {
        Log.i(TAG, "work in");

        //Set wakeup, sleep callback
        speechManager.setOnSpeechListener(new WakenListener() {
            @Override
            public void onWakeUpStatus(boolean b) {

            }

            @Override
            public void onWakeUp() {
                Log.i(TAG, "WAKE UP callback");
            }

            @Override
            public void onSleep() {
                Log.i(TAG, "SLEEP callback");
                //infiniteWakeup is a custom variable to control the duration
                //stop infinite listening
                speechManager.doSleep();
            }
        });
        //Speech recognition callback
        speechManager.setOnSpeechListener(new RecognizeListener() {
            @Override
            public void onRecognizeText(@NonNull RecognizeTextBean recognizeTextBean) {

            }

            @Override
            public boolean onRecognizeResult(@NonNull Grammar grammar) {

                //start timer
                //long startTime = System.nanoTime();
                //cast object received to text string lastRecognizedSentence
                try {
                    lastRecognizedSentence = Objects.requireNonNull(grammar.getText()).toLowerCase();
                } catch (NullPointerException e) {
                    lastRecognizedSentence = "null";
                }
                //recognized part
                //notify update to UI with a separate thread not to freeze the interface
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        //update ui with text recognized
                        tvSpeechRecognizeResult.setText(lastRecognizedSentence);
                    }
                });

                //here can start the computation on the text recognized

                //IGOR: must not exceed 200ms (or less?) don't trust the documentation(500ms), I had to create an handler
                //separate handler so the function could return quickly true, otherwise the robot answers random things over your answers.

                speechResponseHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        Log.i(TAG, ">>>>Recognized voice: "+ lastRecognizedSentence);

                        //deletes "no response action"
                        noResponseAction.removeCallbacksAndMessages(null);

                        if (!lastRecognizedSentence.isEmpty()) {
                            if ("gpt_call".equals(messageApi)){
                                Log.i(TAG, "gpt call");
                                sendToAPI("gpt_call", lastRecognizedSentence);
                            }
                            else{
                                Log.i(TAG, "e call");
                                sendToAPI("e", lastRecognizedSentence);
                            }
                        }

                    }
                });

                //Log.i(TAG, "DURATION millisec: " + (System.nanoTime() - startTime)/1000000);
                return true;
            }

            @Override
            public void onRecognizeVolume(int i) {
            }

            @Override
            public void onStartRecognize() {

            }

            @Override
            public void onStopRecognize() {

            }

            @Override
            public void onError(int i, int i1) {

            }
        });

    }

    private void initHardwareListeners() {
        //hardware touch
        hardWareManager.setOnHareWareListener(
                new TouchSensorListener() {
                    @Override
                    public void onTouch(int i, boolean b) {

                    }

                    @Override
                    public void onTouch(int part) {
                        switch (part) {
                            case 9: case 10:
                                //hand right
                                Log.i(TAG_T, "touching hand right" );
                                sendToAPI("t", "touching_hand");
                                break;
                            case 12 : case 13:
                                //left/right head
                                Log.i(TAG_T, "left/right head" );
                                speechManager.doWakeUp();
                        }
                    }
                }
        );
    }

    private void sendToAPI(final String someValue, final String sentence) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    // Create URL object
                    URL url = new URL(ApiUrl);

                    // Open a connection to the URL
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();

                    // Set the request method to POST
                    connection.setRequestMethod("POST");
                    connection.setRequestProperty("Content-Type", "application/json");
                    connection.setDoOutput(true);

                    // Create JSON payload
                    JSONObject jsonInput = new JSONObject();
                    jsonInput.put("somevalue", someValue);
                    jsonInput.put("sentence", sentence);

                    // Write data to the connection output stream
                    try (OutputStream os = connection.getOutputStream()) {
                        byte[] input = jsonInput.toString().getBytes(StandardCharsets.UTF_8);
                        os.write(input, 0, input.length);
                    }

                    // Get the response from the API
                    try (BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                        StringBuilder response = new StringBuilder();
                        String responseLine;
                        while ((responseLine = br.readLine()) != null) {
                            response.append(responseLine.trim());
                        }

                        String response_toString = response.toString();
                        Log.i(TAG, "API Response: " + response_toString);

                        try {
                            JSONObject jsonResponse = new JSONObject(response_toString);
                            String message = jsonResponse.getString("message");
                            messageApi = message;
                            Log.i(TAG, "Message: " + message);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    } catch (IOException e) {
                        e.printStackTrace();
                    } catch (Exception e) {
                        Log.e(TAG, "Error logging API response: " + e.getMessage());
                    }

                    // Close the connection
                    connection.disconnect();
                } catch (IOException | JSONException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    @Override
    protected void onMainServiceConnected() {

    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        if (web != null) {
            web.destroy();
        }

        //stop infinite listening
        speechManager.doSleep();
        //if person pushes "back" before the normal termination
        MyBaseActivity.busy = false;
        //deletes "no response action" and all the handlers
        noResponseAction.removeCallbacksAndMessages(null);
        Log.i(TAG, "destroy, noResponseHandler deleted");
    }

    private void wakeUpListening() {
        speechManager.doWakeUp();
        imageListen.setVisibility(View.VISIBLE);
        wakeButton.setVisibility(View.GONE);

        //head up
        headMotionManager.doAbsoluteLocateMotion(locateAbsoluteAngleHeadMotion);
        Log.i(TAG, "wakeup answer-active, noResponseHandler activated");

    }

    //END
}

