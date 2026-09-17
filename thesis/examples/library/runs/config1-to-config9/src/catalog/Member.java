package catalog;

import catalog.LibraryCard;
import java.lang.String;


public class Member {
	public Member() {
	}
	private java.lang.String name;
	public java.lang.String getName() {
		return this.name;
	}
	public void setName(java.lang.String name) {
		this.name = name;
	}
	private boolean active;
	public boolean getActive() {
		return this.active;
	}
	public void setActive(boolean active) {
		this.active = active;
	}
	private java.util.ArrayList<catalog.MediaImpl>borrowed;
	public java.util.ArrayList<catalog.MediaImpl>getBorrowed() {
		return this.borrowed;
	}
	public void setBorrowed(java.util.ArrayList<catalog.MediaImpl>borrowed) {
		this.borrowed = borrowed;
	}
	public static final void register(catalog.LibraryCard card) {
	}
	public double totalWeight() {
	}
}



