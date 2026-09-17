package catalog;

import catalog.Identifiable;


public interface IBorrowable extends catalog.Identifiable {
	public boolean borrow(int memberId);
}



