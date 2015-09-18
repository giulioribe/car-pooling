package com.nego.carpooling;

public class Item {
    private int type;
    private Person person;
    private boolean selected = false;

    public Item(int type) {
        this.type = type;
    }
    public Item(int type, Person person) {
        this.type = type;
        this.person = person;
    }
    public int getType() { return type; }

    public Person getItem() {
        return person;
    }

    public boolean isSelected() {
        return selected;
    }
    public void toggleSelected() {
        if(selected)
            selected = false;
        else
            selected = true;
    }
}
