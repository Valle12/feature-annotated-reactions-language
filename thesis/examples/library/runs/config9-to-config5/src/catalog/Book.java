package catalog;

import catalog.MediaImpl;


public abstract class Book extends catalog.MediaImpl {
	public Book() {
	}
	public final void describe() {
	}
	private catalog.Isbn isbn;
	public catalog.Isbn getIsbn() {
		return this.isbn;
	}
	public void setIsbn(catalog.Isbn isbn) {
		this.isbn = isbn;
	}
	private int pageCount;
	public int getPageCount() {
		return this.pageCount;
	}
	public void setPageCount(int pageCount) {
		this.pageCount = pageCount;
	}
}



