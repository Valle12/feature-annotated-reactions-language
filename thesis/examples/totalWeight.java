public double totalWeight() {
  double total = 0.0;
  for (catalog.Media media : this.borrowed) {
    total += media.getWeight();
  }
  return total;
}
