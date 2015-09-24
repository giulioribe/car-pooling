package com.nego.carpooling;

import android.content.Context;
import android.content.pm.LauncherApps;
import android.graphics.drawable.Drawable;
import android.location.Address;
import android.location.Geocoder;
import android.os.Build;
import android.os.Handler;
import android.support.design.widget.Snackbar;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;


public class Utils {

    public static boolean isEmpty(EditText etText) {
        return etText.getText().toString().trim().length() == 0;
    }


    public static void SnackbarC(final Context context, String title, final View view) {
        Snackbar.make(view, title, Snackbar.LENGTH_LONG).show();
    }

    public static String getDate(Context context, long date) {
        Calendar today = Calendar.getInstance();
        Calendar byR = Calendar.getInstance();
        byR.setTimeInMillis(date);
        SimpleDateFormat HM = new SimpleDateFormat("HH:mm");
        SimpleDateFormat DM = new SimpleDateFormat("MMM d, HH:mm");
        SimpleDateFormat MY = new SimpleDateFormat("MMM d y, HH:mm ");
        if (today.get(Calendar.YEAR) == byR.get(Calendar.YEAR) &&
                today.get(Calendar.MONTH) == byR.get(Calendar.MONTH) &&
                today.get(Calendar.DAY_OF_MONTH) == byR.get(Calendar.DAY_OF_MONTH)) {
            return HM.format(new Date(byR.getTimeInMillis()));
        } else if (today.get(Calendar.YEAR) == byR.get(Calendar.YEAR)) {
            return DM.format(new Date(byR.getTimeInMillis()));
        } else {
            return MY.format(new Date(byR.getTimeInMillis()));
        }
    }

    public static String getTime(Context context, long date) {
        Calendar byR = Calendar.getInstance();
        Calendar now = Calendar.getInstance();
        byR.setTimeInMillis(date);
        SimpleDateFormat HM = new SimpleDateFormat("HH:mm");
        String today = "";
        if (byR.get(Calendar.HOUR_OF_DAY) < now.get(Calendar.HOUR_OF_DAY) || (byR.get(Calendar.HOUR_OF_DAY) == now.get(Calendar.HOUR_OF_DAY) && byR.get(Calendar.MINUTE) < now.get(Calendar.MINUTE)))
            today = " di domani";
        return "Arrivo per le " + HM.format(new Date(byR.getTimeInMillis())) + today;
    }

    public static boolean isOldDate(long date) {
        Calendar today = Calendar.getInstance();
        return (today.getTimeInMillis() > date);
    }




    public static boolean isBrokenSamsungDevice() {
        return (Build.MANUFACTURER.equalsIgnoreCase("samsung")
                && isBetweenAndroidVersions(
                Build.VERSION_CODES.LOLLIPOP,
                Build.VERSION_CODES.LOLLIPOP_MR1));
    }

    public static boolean isBetweenAndroidVersions(int min, int max) {
        return Build.VERSION.SDK_INT >= min && Build.VERSION.SDK_INT <= max;
    }


    public static Address getLocationFromAddress(Context context, String strAddress) {

        Geocoder coder = new Geocoder(context);
        List<Address> address;

        int i = 0;
        while (i<100) {
            try {
                address = coder.getFromLocationName(strAddress, 5);
                Log.i("address", address.get(0).toString());
                if (address != null) {
                    return address.get(0);
                }

            } catch (Exception ex) {
            }
            i++;
        }

        return  null;

    }


    public static Address getAddressFromLocation(Context context, String lat, String lon) {

        Geocoder coder = new Geocoder(context);
        List<Address> address;
        int i = 0;
        while (i<100) {
            try {
                address = coder.getFromLocation(new Double(lat), new Double(lon), 5);
                if (address != null) {
                    return address.get(0);
                }

            } catch (Exception ex) {
            }
            i++;
        }

        return  null;

    }

    public static long getFutureTime(Context context) {
        Calendar c = Calendar.getInstance();
        int hour = c.get(Calendar.HOUR_OF_DAY);
        int minute = c.get(Calendar.MINUTE);

        if (hour < 9) {
            hour = 9;
            minute = 0;
        } else if (hour >= 9 && hour < 12) {
            hour = 12;
            minute = 0;
        } else if (hour >=  12 && hour < 19) {
            hour = 19;
            minute = 0;
        } else if (hour >= 19  && hour < 22) {
            hour = 22;
            minute = 0;
        } else if (hour >= 22) {
            hour = 9;
            minute = 0;
        }

        c.set(Calendar.HOUR_OF_DAY, hour);
        c.set(Calendar.MINUTE, minute);

        return c.getTimeInMillis();
    }

    public static String arrayListToString (ArrayList<String> arrayList) {
        String text = "";
        String divider = "";
        boolean first = true;

        if (arrayList != null && arrayList.size() > 0) {

            for (String k : arrayList) {
                text += divider + k;
                if (first) {
                    divider = "_";
                    first = false;
                }
            }
        }

        return text;
    }

    public static ArrayList<String> stringToArrayList (String s) {
        ArrayList<String> arrayList = new ArrayList<>();
        if (s != null && !s.equals("")) {
            String[] strings = s.split("_");

            for (String k : strings) {
                arrayList.add(k);
            }
        }

        return arrayList;
    }

    public static String formatDur(long l) {
        String format = "";
        if (l == 0)
            return "Nessuna Preferenza";
        long minute = l;
        long hour = minute / 60;
        format = hour + "h " + (minute - 60 * hour) + "m";
        return format;
    }

    public static void setBackground(final Context context, final View view, final int i) {
        final Handler mHandler = new Handler();

        new Thread(new Runnable() {
            public void run() {

                final Drawable drawable = ContextCompat.getDrawable(context, i);
                mHandler.post(new Runnable() {
                    public void run() {
                        view.setBackground(drawable);
                    }
                });
            }
        }).start();
    }

    public static void setSrc(final Context context, final ImageView view, final int i) {
        final Handler mHandler = new Handler();

        new Thread(new Runnable() {
            public void run() {

                final Drawable drawable = ContextCompat.getDrawable(context, i);
                mHandler.post(new Runnable() {
                    public void run() {
                        view.setImageDrawable(drawable);
                    }
                });
            }
        }).start();
    }

}
