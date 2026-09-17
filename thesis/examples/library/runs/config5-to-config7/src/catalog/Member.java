package catalog;

import catalog.LibraryCard;
import java.lang.String;


public interface Member {
	public static final java.lang.String name = null;
	public static final boolean active = false;
	public static final java.util.ArrayList<catalog.Media>borrowed = null;
	public void register(catalog.LibraryCard card);
	public double totalWeight();
	public void Member();
}



