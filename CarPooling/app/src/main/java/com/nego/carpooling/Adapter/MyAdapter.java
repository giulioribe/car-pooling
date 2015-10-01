package com.nego.carpooling.Adapter;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v4.content.ContextCompat;
import android.support.v7.widget.PopupMenu;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.nego.carpooling.ChoosePeople;
import com.nego.carpooling.Costants;
import com.nego.carpooling.Functions.PersonService;
import com.nego.carpooling.Item;
import com.nego.carpooling.Person;
import com.nego.carpooling.R;
import com.nego.carpooling.database.DbAdapter;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;


public class MyAdapter extends RecyclerView.Adapter<MyAdapter.ViewHolder> {
    private List<Item> mDataset = new ArrayList<>();
    private Context mContext;

    public static class ViewHolder extends RecyclerView.ViewHolder {

        public View mView;
        public ViewHolder(View v) {
            super(v);
            mView = v;
        }

        public TextView name;
        public TextView address;
        public ImageView img;
        public ImageView img_c;
        public ImageView menu;
        public ViewHolder(View v, TextView name, TextView address, ImageView img, ImageView img_c, ImageView menu) {
            super(v);
            mView = v;
            this.name = name;
            this.address = address;
            this.img = img;
            this.img_c = img_c;
            this.menu = menu;
        }

    }

    public MyAdapter(DbAdapter dbHelper, Context mContext) {
        this.mContext = mContext;
        generate_list(dbHelper);
    }

    @Override
    public MyAdapter.ViewHolder onCreateViewHolder(ViewGroup parent,
                                                   int viewType) {

        ViewHolder vh;
        View v;

        v = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.grid_people, parent, false);
        vh = new ViewHolder(v,
                (TextView) v.findViewById(R.id.p_name),
                (TextView) v.findViewById(R.id.p_address),
                (ImageView) v.findViewById(R.id.p_image),
                (ImageView) v.findViewById(R.id.p_image_checked),
                (ImageView) v.findViewById(R.id.action_menu));

        return vh;
    }

    @Override
    public void onBindViewHolder(final ViewHolder holder, final int position) {

        // NOME
        holder.name.setText(mDataset.get(position).getItem().getName());

        // ADDRESS
        holder.address.setText(mDataset.get(position).getItem().getAddress());

        // IMMAGINE
        if (mDataset.get(position).getItem().getImg().equals("")) {
            holder.img.setImageDrawable(ContextCompat.getDrawable(mContext, R.drawable.ic_person_null));
        } else {
            try {
                holder.img.setImageBitmap(Bitmap.createScaledBitmap(MediaStore.Images.Media.getBitmap(mContext.getContentResolver(), Uri.parse(mDataset.get(position).getItem().getImg())), 64, 64, false));
            } catch (Exception e) {}
        }

        // SELECTED
        if (mDataset.get(position).isSelected()) {
            holder.img_c.setVisibility(View.VISIBLE);
        } else {
            holder.img_c.findViewById(R.id.p_image_checked).setVisibility(View.GONE);
        }

        // CLICK LISTENER
        holder.mView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                toggleSelection(position);
            }
        });

        // MENU
        holder.menu.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(final View v) {
                PopupMenu popup = new PopupMenu(mContext, v);
                popup.inflate(R.menu.menu_popup_item);

                popup.setOnMenuItemClickListener(new PopupMenu.OnMenuItemClickListener() {
                    @Override
                    public boolean onMenuItemClick(MenuItem item) {
                        switch (item.getItemId()) {

                            case R.id.action_modify:
                                ((ChoosePeople) mContext).editPerson(mDataset.get(position).getItem());
                                return true;
                            case R.id.action_delete:
                                new AlertDialog.Builder(mContext)
                                        .setTitle("Attenzione")
                                        .setMessage("Sicuro di voler eliminare questa persona?")
                                        .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                                            public void onClick(DialogInterface dialog, int whichButton) {
                                                PersonService.startAction(mContext, Costants.ACTION_DELETE, mDataset.get(position).getItem());
                                            }
                                        })
                                        .setNegativeButton(android.R.string.no, null).show();
                                return true;
                        }
                        return false;
                    }
                });
                popup.show();
            }
        });
    }

    @Override
    public int getItemViewType(int position) {
        Item obj = mDataset.get(position);
        return obj.getType();
    }

    @Override
    public int getItemCount() {
        return mDataset.size();
    }

    // GENERATE LIST
    public void generate_list(DbAdapter dbHelper) {
        mDataset.clear();
        Cursor cursor = dbHelper.fetchAllPersons();
        while (cursor.moveToNext()) {
            Person p = new Person(cursor);
            Cursor cursor_pop = dbHelper.getPopById(p.getId());
            p.setPop(cursor_pop);
            mDataset.add(new Item(1, p));
        }
        cursor.close();
    }

    public void toggleSelection(int pos) {
        mDataset.get(pos).toggleSelected();
        notifyItemChanged(pos);
        ((ChoosePeople) mContext).countPeople();
    }

    public void clearSelections() {
        for(int k=0;k<mDataset.size();k++)
            if (mDataset.get(k).getType() == 1 && mDataset.get(k).isSelected())
                toggleSelection(k);
    }

    public int getSelectedItemCount() {
        int f = 0;
        for(int k=0;k<mDataset.size();k++)
            if (mDataset.get(k).getType() == 1 && mDataset.get(k).isSelected())
                f++;
        return f;
    }

    public void selectAll() {
        if (getSelectedItemCount() != getItemCount()) {
            for (int k = 0; k < mDataset.size(); k++)
                if (mDataset.get(k).getType() == 1 && !mDataset.get(k).isSelected())
                    toggleSelection(k);
        } else {
            clearSelections();
        }
    }

    public ArrayList<Person> getSelectedItem() {
        ArrayList<Person> selected = new ArrayList<>();
        for (int k=0;k<mDataset.size();k++)
            if(mDataset.get(k).getType() == 1 && mDataset.get(k).isSelected()) {
                selected.add(mDataset.get(k).getItem());
            }
        return selected;
    }

    public void setSelected(Bundle savedInstanceState) {
        ArrayList<Person> persons = savedInstanceState.getParcelableArrayList(Costants.KEY_PEOPLE_SELECTED);
        for (Item i : mDataset) {
            for (Person p : persons) {
                if (p.getId() == i.getItem().getId())
                    i.toggleSelected();
            }
        }
    }

}
