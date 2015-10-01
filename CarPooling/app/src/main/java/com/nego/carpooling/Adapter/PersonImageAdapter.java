package com.nego.carpooling.Adapter;

import android.content.Context;
import android.graphics.Bitmap;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.v4.content.ContextCompat;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import com.nego.carpooling.Person;
import com.nego.carpooling.R;

import java.util.ArrayList;
import java.util.List;

public class PersonImageAdapter extends RecyclerView.Adapter<PersonImageAdapter.ViewHolder> {
    private List<Person> mDataset = new ArrayList<>();
    private Context mContext;

    public static class ViewHolder extends RecyclerView.ViewHolder {

        public View mView;
        public ImageView img;
        public ViewHolder(View v, ImageView img) {
            super(v);
            mView = v;
            this.img = img;
        }

    }

    public PersonImageAdapter(Context mContext, ArrayList<Person> persons) {
        this.mContext = mContext;
        mDataset = persons;
    }

    @Override
    public PersonImageAdapter.ViewHolder onCreateViewHolder(ViewGroup parent,
                                                   int viewType) {

        ViewHolder vh;
        View v;

        v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.grid_person_img, parent, false);
        vh = new ViewHolder(v,
                (ImageView) v.findViewById(R.id.p_img));

        return vh;
    }


    @Override
    public void onBindViewHolder(final ViewHolder holder, final int position) {
        if (mDataset.get(position).getImg().equals("")) {
            holder.img.setImageDrawable(ContextCompat.getDrawable(mContext, R.drawable.ic_person_null));
        } else {
            try {
                holder.img.setImageBitmap(Bitmap.createScaledBitmap(MediaStore.Images.Media.getBitmap(mContext.getContentResolver(), Uri.parse(mDataset.get(position).getImg())), 64, 64, false));
            } catch (Exception e) {}
        }
    }

    @Override
    public int getItemCount() {
        return mDataset.size();
    }
}
